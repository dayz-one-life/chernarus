# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
### Changed
- `cfggameplay.json`: raise `environmentMaxTemps` from `-2` to `0` across all twelve months (min stays `-6`, so the ambient range is now `-6`–`0`).
### Deprecated
### Removed
### Fixed
### Security

## [1.4.0] - 2026-07-11

### Added
- `cfgIgnoreList.xml`: ignore `PunchedCard` and the colored shipping-container keys (`ShippingContainerKeys_Red`, `_Orange`, `_Yellow`, `_Blue`) so the economy no longer tracks/reports them.

## [1.3.1] - 2026-07-10

### Fixed
- Solo maintainer mode: back-merge PRs (`main`→`develop`) are no longer blocked by the contribution CHANGELOG/CLAUDE.md gate. The solo `gh-pr-create` check now parses `--head` and exempts `head == productionBranch`, mirroring the merge handler.

## [1.3.0] - 2026-07-10

### Added
- GitHub Actions FTP deploy workflow (`.github/workflows/deploy.yml`) that publishes changed config to the server when a release is published (previously deployed on pushes to `develop`). Dev tooling (`.claude`, `.superpowers`, `docs`) is excluded from the upload.

## [1.2.0] - 2026-07-10

### Added
- Custom minimal spawn loadout (`custom/loadout.json`, wired via `spawnGearPresetFiles`): worn t-shirt/canvas pants/athletic shoes plus a bandage and a steak knife.
- One Life new-player onboarding message rotation and Discord invite in `db/messages.xml`.

### Changed
- **Permadeath ruleset:** enforce no respawn while unconscious (`disableRespawnInUnconsciousness`).
- **Loot economy ~50% scarcer:** reduced `nominal` on 1040 item types in `db/types.xml` (none increased); `min` lowered on ~950.
- **Climate:** constant year-round cold (−6…−2°C) in `cfggameplay.json`.
- **Infected:** raised zombie zone density (~+37%) in `env/zombie_territories.xml`.
- **Base building:** free-form placement (placement/collision checks disabled).
- **Timers:** removed server-hop/relog penalties (`TimeHopping`/`TimePenalty` = 0), shortened login time, idle mode effectively off (`db/globals.xml`).

## [1.1.0] - 2026-07-10

### Added
- `soloMaintainer` mode: an opt-in config flag that enables a `solo` guard role, letting one person run the full workflow (feature work, contribution merge, release, back-merge) from a single clone without swapping git remotes, while preserving protected-branch and squash+review protections.

## [1.0.1] - 2026-07-10

### Changed
- Rewrote `README.md` to describe the Xbox One Life Chernarus server configuration and repository layout (replacing the inherited workflow-template README).

## [1.0.0] - 2026-07-10

### Added
- Base Chernarus server configuration imported under version control: economy core, spawnable types, event spawns/groups, weather, environment territories, player spawn points, map group clusters/positions, and `init.c`.
- Workflow initialization: stamped `canonicalRepo` (`dayz-one-life/chernarus`) in `.claude/workflow.json` so the workflow guards activate on `develop`.
