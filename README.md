# One Life — Chernarus (DayZ Server Config)

Server-side mission configuration for the **One Life** DayZ community server on **Xbox One**,
running the **Chernarus** map. This repository holds the economy, spawn, event, weather, and
map-object configuration that defines how the server plays.

## What's in here

| Path | Purpose |
|------|---------|
| `cfg*.xml` / `cfg*.json` | Core server config: economy core, spawnable types, limits, event spawns/groups, weather, gameplay, player spawn points, random presets. |
| `db/` | Central economy database — `types.xml` (loot), `events.xml`, `economy.xml`, `globals.xml`, `messages.xml`. |
| `env/` | Animal and infected territory definitions, one file per species. |
| `mapgroup*.xml`, `mapclusterproto.xml`, `areaflags.map` | Map object group clusters, positions, and prototypes (largely map-editor generated — edit with care). |
| `init.c` | Mission init script (Enforce Script). |

## Contributing

Changes follow a Claude-Code-enforced workflow: **fork → `feature/*` branch → PR into
`develop` → review → squash-merge → `develop`→`main` release**. Every PR updates
`CHANGELOG.md`, and `CLAUDE.md` is the last file touched before opening a PR.

See `CONTRIBUTING.md` for the contributor steps and `CLAUDE.md` for the full workflow and its
guardrails. Releases are tracked in `CHANGELOG.md` and on the
[Releases](https://github.com/dayz-one-life/chernarus/releases) page.
