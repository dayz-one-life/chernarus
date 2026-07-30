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

## [2.2.2] - 2026-07-30

### Changed
- Reset the entire mission to vanilla Road to Badlands values: revert the loot nerf (`db/types.xml`), the vehicle event tuning (`db/events.xml`), and the preset-chance cut (`cfgrandompresets.xml`). Every mission file is now byte-identical to Bohemia's upstream **except** `db/globals.xml` and `db/messages.xml`, which come from the maintained custom copies in the parent folder (shorter flag refresh, idle-mode tweaks, `LootDamageMin` 0.25, no time-hopping/login penalties; app-promo broadcast).

## [2.2.1] - 2026-07-28

### Changed
- `db/events.xml`: set `nominal` and `min` to 1 on all seven vehicle events (VehicleBoat, VehicleCivilianSedan, VehicleHatchback02, VehicleOffroad02, VehicleOffroadHatchback, VehicleSedan02, VehicleTruck01) — the economy now targets ~1 of each vehicle type on the map; `max` and child entries unchanged.

## [2.2.0] - 2026-07-28

### Added
- `docs/tools/halve_preset_chances.py`: deterministic transform that halves preset-level chances (re-runnable on a fresh upstream drop; XML-parse-based count check).

### Changed
- `db/types.xml`: the loot nerf now applies with **no exclusions** — the 47 `deloot="1"` (heli-crash/convoy) and `ContaminatedArea` (gas-zone) types have their `nominal`/`min` halved too; `nerf_loot.py` updated to match.
- `cfggameplay.json`: drop the unconscious-respawn block (`disableRespawnInUnconsciousness` back to vanilla `false`) and re-enable the personal light (`disablePersonalLight` back to vanilla `false`); the empty `spawnGearPresetFiles` key is removed entirely.
- `db/globals.xml`: raise `LootDamageMin` from `0.2` to `0.25` — freshly spawned loot now tops out at 75% quality.
- `db/messages.xml`: replace the two-message onboarding rotation with a single repeating app-promo broadcast ("One Life is better with the app. https://dayzonelife.com").
- `env/zombie_territories.xml`: revert the zed buff — restore vanilla zone `dmin`/`dmax` (file is now byte-identical to Bohemia's upstream), removing the +1 density applied since 1.2.0.
- `cfggameplay.json`: revert the climate tweak — restore vanilla seasonal `environmentMinTemps`/`environmentMaxTemps` (−3…26°C across the year), replacing the flat 0…3°C range.
- `cfgrandompresets.xml`: cut the preset-level `chance` on all 75 active `<cargo>`/`<attachments>` presets by 50% (3 already-disabled presets untouched; per-item chances unchanged).

### Removed
- `docs/tools/road-to-badlands/buff_zeds.py`: retired — the zed buff it re-derived no longer exists, and keeping it risked silently re-applying the buff on the next upstream merge.

## [2.1.0] - 2026-07-27

### Changed
- `cfggameplay.json`: disable free-form "build anywhere" base building — all 14 `disable*` booleans in `HologramData` (11) and `ConstructionData` (3) flipped back to `false`, restoring vanilla placement/construction checks.

### Removed
- Custom minimal fresh-spawn loadout: deleted `custom/loadout.json` and emptied `spawnGearPresetFiles` in `cfggameplay.json` — players spawn with vanilla default gear again.

## [2.0.3] - 2026-07-27

### Changed
- `cfggameplay.json`: warm the ambient environment temperature range from −6…0°C to **0…3°C** (all twelve monthly `environmentMinTemps`/`environmentMaxTemps` values).

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
