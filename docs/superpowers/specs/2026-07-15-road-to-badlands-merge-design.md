# Road to Badlands merge — One Life Chernarus

**Date:** 2026-07-15
**Status:** Approved design, pre-implementation

## Goal

Incorporate Bohemia's *Road to Badlands* update into the One Life Chernarus server
mission config, while preserving our custom gameplay tweaks. Upstream ships **vanilla**
default values, so a straight file copy would silently revert every customization we have.
The strategy is therefore: **adopt the new upstream files as the base, then re-apply our
customizations on top.**

Source of the new files:
`../road-to-badlands-mission-files/dayzOffline.chernarusplus/`

## Strategy

1. Overwrite the repo with the new Road to Badlands files as the base.
2. Re-apply our customizations file-by-file per the table below.
3. Preserve each repo file's **current filename casing** — the FTP deploy and
   `cfgeconomycore.xml` references depend on exact names (e.g. `cfgIgnoreList.xml`,
   `cfgEffectArea.json`). Only file *contents* change, never repo filenames.

## Per-file actions

| File | Action |
|------|--------|
| `db/types.xml` | Take new upstream file → apply **Transform 1 (loot nerf)** |
| `env/zombie_territories.xml` | Take new upstream file → apply **Transform 2 (zed buff)** |
| `custom/loadout.json` | Add our file as-is (not present in upstream) |
| `db/messages.xml` | Overwrite with our file as-is (One Life onboarding rotation) |
| `cfggameplay.json` | Overwrite with our file as-is (verified: upstream added no new keys) |
| `db/globals.xml` | Overwrite with our file as-is (verified: upstream added no new keys) |
| `cfgIgnoreList.xml` | **Vanilla** — take new upstream, drop our prior additions |
| `cfgeventgroups.xml`, `cfgrandompresets.xml`, `cfgspawnabletypes.xml`, `mapgrouppos.xml`, `mapgroupproto.xml`, `db/events.xml`, `env/fox_territories.xml` | Take new upstream wholesale (no customization of ours here) |
| All other files (already identical) | No-op |

### Customizations intentionally NOT preserved
- `cfgIgnoreList.xml` additions (flares, `PunchedCard`, colored `ShippingContainerKeys`)
  from v1.4.0 — reverting to vanilla ignore list per decision.

## Transform 1 — Loot nerf (`db/types.xml`)

Applied to the **new upstream** `types.xml` (1970 `<type>` blocks). For each `<type>` block:

**Skip (leave upstream values untouched) if either:**
- its `<flags .../>` element has `deloot="1"` (~47 types), **or**
- it contains a `<usage name="ContaminatedArea"/>` child (~15 types).

**Otherwise, nerf:**
- `<nominal>N</nominal>` → `ceil(N / 2)`
- `<min>M</min>` → `ceil(M / 2)`

`ceil` division guarantees `1 → 1` (never drops to 0) and `0 → 0`.

**Implementation note:** the script must rewrite **only** the inner values of `<nominal>`
and `<min>` on qualifying blocks, leaving every other byte identical, so the diff is clean
and reviewable. (Block-scoped text rewrite, not a full XML re-serialization, to avoid
whitespace/attribute-quoting churn.)

## Transform 2 — Zed buff (`env/zombie_territories.xml`)

Applied to the **new upstream** `zombie_territories.xml`. The original v1.2.0 buff was a
uniform **+2** on `dmin`/`dmax`; this update uses **+1** instead.

For each `<zone .../>` element:
- **Skip** if `dmax == 0` (intentionally-empty zone — leave it empty).
- Otherwise: `dmin → dmin + 1`, `dmax → dmax + 1`.

## Verification

- `xmllint --noout` on every touched XML file (well-formedness).
- `types.xml`: block count still 1970; spot-check (a) a normal item is halved (ceil),
  (b) a `deloot="1"` item is unchanged, (c) a `ContaminatedArea` item is unchanged.
- `zombie_territories.xml`: spot-check a non-zero zone shows +1 and a `dmax="0"` zone is
  unchanged.
- Review the full git diff to confirm only intended lines changed.

## Release notes / workflow

Versioned change. `CHANGELOG.md` gains an `[Unreleased]` entry documenting:
- **Changed:** adopted Road to Badlands upstream base for all mission config.
- **Changed:** loot nerf re-derived as a deterministic rule — halve `nominal`/`min`
  (round up) on all `types.xml` entries except `deloot="1"` and `ContaminatedArea` items.
- **Changed:** zed buff reduced from +2 to +1 on `zombie_territories.xml` zone
  `dmin`/`dmax` (zero zones skipped).
- **Removed:** `cfgIgnoreList.xml` custom additions (reverted to vanilla).
- Preserved as-is: `custom/loadout.json`, `db/messages.xml`, `cfggameplay.json`,
  `db/globals.xml`.

Delivered via a `feature/*` branch → PR into `develop` (solo-maintainer flow), then a
`develop` → `main` release cut.
