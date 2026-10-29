# Creative Workshop — independent edition

Last updated: 2026-10-28.

This repository contains an independent modified edition of wordcraft, originally developed by the ArtCraft Team and contributors. Creative Workshop is not affiliated with, endorsed by, or supported by the ArtCraft Team.

- Original project: https://github.com/storytold/wordcraft
- This edition: https://github.com/dfoliveira2143/wordcraft
- Support: https://github.com/dfoliveira2143/wordcraft/issues
- Original code licenses and copyright notices remain in [LICENSE-MIT](../LICENSE-MIT), [LICENSE-APACHE](../LICENSE-APACHE) and [NOTICE](../NOTICE).
- The original restricted ArtCraft logo/mark files are excluded. Their [terms](brand/LICENSE-brand.txt) remain as a legal reference, not permission to restore them.
- Existing openly licensed application icons retain their authorship and licenses. Internal command IDs and compatibility identifiers are not claims of affiliation.
- Do not restore ArtCraft branding when merging upstream changes. Review About screens, help links, translations, package metadata, screenshots, and embedded graphics.
- Historical documents may refer to the original project. Such references are attribution, not branding for this edition.

## Release status

Lightweight validation completed: Rust formatting and syntax parsing of changed JSON/TOML/XML files. The shared automation passed 20 offline safety tests. Application compilation, full tests, asset gates and visual review remain pending. Existing executables, installers, portable folders and published releases were not rebuilt or replaced by editing these sources. Do not distribute old branded builds as Creative Workshop. Before release, rebuild, inspect the UI and packages, and replace screenshots containing the old marks. No push is authorized by this migration.

## Update protection

The trusted `.github/artcraft-sync.py` checks candidate Git objects before dispatching validation and before integration. It blocks known restricted logo filenames, new public ArtCraft claims/support URLs, and missing Creative Workshop policy. It never executes candidate code with publication permissions. Credits are allowed. This is a conservative text/path check, not image recognition or a legal audit. Renamed/redrawn marks and screenshots still require visual review. The controller and this policy are protected from upstream changes.

This controller is prepared locally, not deployed. The remote automation follows `main`; local work is on `development`. Publish and integrate the branding and controller together through an explicitly authorized operation. Do not regenerate staging from an old controller.
