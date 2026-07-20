# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [2.0.2] - 2026-07-20

### Changed
- `db/messages.xml`: the "Join the pack" onboarding broadcast now points players at `dayzonelife.com` instead of the Discord invite — the website is where unban tokens are earned and spent.

## [2.0.1] - 2026-07-15

### Changed
- `db/globals.xml`: raise `LootDamageMin` from `0.0` to `0.2` so spawned loot is always at least 20% damaged (max quality capped at 80%; `LootDamageMax` stays `0.82`).

## [2.0.0] - 2026-07-15

### Added
- `docs/tools/road-to-badlands/`: reusable transform scripts (`nerf_loot.py`, `buff_zeds.py`) that re-derive our loot nerf and zed buff on top of upstream files (excluded from server deploy).

### Changed
- Adopted Bohemia's **Road to Badlands** mission config as the new base for all upstream-owned files (`cfgspawnabletypes.xml`, `cfgeventgroups.xml`, `cfgrandompresets.xml`, `mapgrouppos.xml`, `mapgroupproto.xml`, `db/events.xml`, `db/types.xml`, `env/fox_territories.xml`, `env/zombie_territories.xml`).
- **Loot nerf** re-derived as a deterministic rule: halve `nominal`/`min` (round up, so `1` stays `1`) on every `db/types.xml` type except `deloot="1"` and `ContaminatedArea` items. Now also covers new Road to Badlands loot.
- **Zed buff** reduced from +2 to **+1** on `env/zombie_territories.xml` zone `dmin`/`dmax` (zones with `dmax=0` skipped).

### Removed
- `cfgIgnoreList.xml` custom additions (flares, `PunchedCard`, colored `ShippingContainerKeys`) — reverted to vanilla; the old keys/cards they suppressed have since despawned.

## [1.5.0] - 2026-07-14

### Changed
- `.claude/workflow.json`: enable solo maintainer mode (`soloMaintainer: true`) so contributor + maintainer permissions are available from the single canonical clone.

### Removed
- `db/messages.xml`: remove the in-game server-restart countdown message (`shutdown`/`deadline` block). Reboot notifications are now handled by the Discord bot.

## [1.4.1] - 2026-07-14

### Changed
- `cfggameplay.json`: raise `environmentMaxTemps` from `-2` to `0` across all twelve months (min stays `-6`, so the ambient range is now `-6`–`0`).

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
