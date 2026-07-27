# CLAUDE.md

This project was created from the Claude Code workflow template. The workflow below is
enforced by committed hooks in `.claude/` and streamlined by repo-level skills.

## On session start

A SessionStart hook injects a role-aware orientation. **Present that orientation to the
user at the start of a fresh session.**

## The workflow

1. All feature work happens on a **fork**, on a `feature/*` branch.
2. Updating this file (`CLAUDE.md`) is the **last step** before opening a PR.
3. `CHANGELOG.md` is updated on **every** PR.
4. PRs go into the canonical repo's **`develop`** branch.
5. Reviews are done in Claude Code and posted back to the contributor.
6. Approved PRs are **squash-merged** into `develop`.
7. Production releases go out via a **`develop` → `main`** PR.
8. Merging that PR **cuts a release** with notes.

## Skills

- Contributor: `starting-work`, `finishing-a-feature`.
- Maintainer: `reviewing-a-contribution`, `merging-a-contribution`, `drafting-a-release`, `cutting-a-release`.
- Setup: `workflow-setup` (run once).

## Guardrails (enforced by `.claude/hooks/guard.py`)

- No commits, pushes, or merges on `main`/`develop` (tag pushes and the one-time `workflow.json` setup commit are exempt).
- On a fork: PRs must target `develop` and require CHANGELOG.md + CLAUDE.md updates.
- On the canonical repo: feature work is blocked (fork instead). Fork contributions into `develop` must be squash-merged and approved; the maintainer's own same-repo release/back-merge PRs are exempt from that gate.
- Once the project is initialized (`workflow-setup` run), write/git actions are blocked unless the Superpowers plugin is installed.
- **Solo maintainer mode:** setting `soloMaintainer: true` in `.claude/workflow.json` activates a `solo` role that holds the union of contributor + maintainer permissions from a single clone (no remote swapping). Protected branches stay PR-only; contribution merges into `develop` still require `--squash` + a posted review (a `COMMENTED` review counts, since self-approval is impossible); release (`develop`→`main`) and back-merge (`main`→`develop`) PRs are exempt from the changelog/review gates. Off by default.

## Honest limitations

- Hooks only bind inside Claude Code; plain `git`/`gh` in a shell bypasses them.
- Superpowers/role detection are filesystem/remote heuristics; they fail with clear messages.
- Approved-review detection needs the canonical repo to be a real GitHub remote.

## Repository layout

See `README.md` for a project overview. This repo holds the DayZ **Chernarus** server mission configuration:

- `cfg*.xml` / `cfg*.json` — server config: economy core, spawnable types, limits, event spawns/groups, weather, gameplay, player spawn points, random presets. `cfggameplay.json` includes the ambient environment temperature range (`environmentMinTemps`/`environmentMaxTemps`, twelve monthly values each; currently a flat 0…3°C year-round).
- `cfgIgnoreList.xml` — item types the central economy ignores (never tracked, spawned, or cleaned up).
- `db/` — central economy database: `types.xml`, `events.xml`, `economy.xml`, `globals.xml`, `messages.xml`. `globals.xml` holds economy tuning vars, including the loot damage bounds (`LootDamageMin`/`LootDamageMax`) that set the quality range of freshly spawned loot. `messages.xml` holds only new-player onboarding broadcasts; reboot/restart notifications are handled by the Discord bot, not the in-game mission. The community broadcast points at `dayzonelife.com` — the website is the canonical place to earn and spend unban tokens, so link it there rather than the Discord invite.
- `env/` — animal/infected territory definitions per species.
- `mapgroup*.xml`, `mapclusterproto.xml`, `areaflags.map` — map object group clusters, positions, and prototypes (largely map-editor generated; edit with care).
- The former `custom/` directory (server-specific overrides) was removed along with its `loadout.json` fresh-spawn preset — `spawnGearPresetFiles` in `cfggameplay.json` is `[]`, so spawns use vanilla gear plus `StartingEquipSetup` in `init.c`.
- `init.c` — mission init script (Enforce Script).
- `docs/tools/` — reusable maintenance scripts, kept out of the FTP deploy. `road-to-badlands/nerf_loot.py` and `buff_zeds.py` re-derive the loot nerf (halve `nominal`/`min`, round up, excluding `deloot="1"` and `ContaminatedArea` types) and the zed buff (+1 to each zone's `dmin`/`dmax`, skipping `dmax=0`) on top of a fresh upstream mission drop. Both preserve the source file's line endings (`newline=""` — `env/zombie_territories.xml` is CRLF) and abort loudly if the element count changes.

## Deployment

`.github/workflows/deploy.yml` deploys the config to the server via FTP when a **GitHub release is published** (the last step of `cutting-a-release`). It uploads only changed files and excludes dev tooling (`.claude`, `.superpowers`, `docs`, `*.md`). Requires the `FTP_SERVER`/`FTP_USERNAME`/`FTP_PASSWORD`/`FTP_DIRECTORY` repo secrets.

## Configuration

`.claude/workflow.json` holds `canonicalRepo`, branch names, the `soloMaintainer` flag (currently `true`), and optional `commands.test`/`commands.lint`.
