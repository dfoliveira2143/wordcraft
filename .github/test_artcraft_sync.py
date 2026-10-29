import importlib.util
from pathlib import Path
import unittest
import subprocess
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('sync', Path(__file__).with_name('artcraft-sync.py'))
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)

class Notifications(unittest.TestCase):
    def test_non_conflict_does_not_call_github(self):
        with patch.object(sync, 'api') as api:
            sync.pull_request('sync/test', 'Checks failed', 'https://example.invalid/run')
            sync.notify_error('API unavailable', 'https://example.invalid/run')
            api.assert_not_called()

    def test_new_conflict_opens_one_pr(self):
        with patch.object(sync, 'api', side_effect=[[], {'number': 3}]) as api:
            self.assertEqual(sync.pull_request('sync/test', 'Conflict', 'url', conflict=True), 3)
            self.assertEqual(api.call_count, 2)
            args = api.call_args.args
            self.assertEqual(args[1], 'POST')
            self.assertEqual(args[2]['base'], 'main')

    def test_existing_conflict_is_not_notified_again(self):
        with patch.object(sync, 'api', return_value=[{'number': 3}]) as api:
            self.assertEqual(sync.pull_request('sync/test', 'Conflict', 'url', conflict=True), 3)
            self.assertEqual(api.call_count, 1)

    def prepare_candidate(self, conflict=False, protected=False):
        def git(*args, **kwargs):
            if args[0] == 'rev-parse':
                if args[1] == 'HEAD':
                    return 'c' * 40
                git.fetches += 1
                return ('a' if git.fetches == 1 else 'b') * 40
            if args[0] == 'merge-base':
                return 'd' * 40
            if args[0] == 'diff':
                if '--diff-filter=U' in args:
                    return 'file.txt' if conflict else ''
                return '.github/artcraft-sync.py' if protected else ''
            if args[0] == '-c':
                return subprocess.CompletedProcess(args, 1 if conflict else 0, '', '')
            return ''
        git.fetches = 0
        def api(route, method='GET', body=None):
            if route == 'repos/storytold/test':
                return {'default_branch':'main'}
            if '/pulls?' in route:
                return []
            if method == 'POST' and route.endswith('/pulls'):
                return {'number':1}
        with patch.object(sync, 'NAME', 'test'), patch.object(sync, 'REPO', 'owner/test'), \
             patch.object(sync, 'ancestor', return_value=False), patch.object(sync, 'git', side_effect=git) as calls, \
             patch.object(sync, 'api', side_effect=api) as requests:
            sync.prepare('url')
            return calls.call_args_list, requests.call_args_list

    def test_merge_conflict_opens_intervention_pr_without_dispatch(self):
        calls, requests = self.prepare_candidate(conflict=True)
        self.assertTrue(any(c.args[0].endswith('/pulls') and c.args[1] == 'POST' for c in requests))
        self.assertFalse(any(c.args[0].endswith('/dispatches') for c in requests))
        self.assertFalse(any(c.args[0] == 'push' and c.args[-1].endswith(':refs/heads/main') for c in calls))

    def test_candidate_requires_checks_and_never_pushes_main(self):
        calls, requests = self.prepare_candidate()
        self.assertTrue(any(c.args[0].endswith('/dispatches') for c in requests))
        self.assertFalse(any('/pulls' in c.args[0] for c in requests))
        self.assertFalse(any(c.args[0] == 'push' and c.args[-1].endswith(':refs/heads/main') for c in calls))

    def test_controller_change_is_blocked_before_push(self):
        calls, requests = self.prepare_candidate(protected=True)
        self.assertFalse(any(c.args[0] == 'push' for c in calls))
        self.assertFalse(any(len(c.args)>1 and c.args[1] == 'POST' for c in requests))

if __name__ == '__main__':
    unittest.main()
