# Road to Badlands Merge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adopt Bohemia's Road to Badlands mission config as the new base for the One Life Chernarus server, then re-apply our customizations (loot nerf, zed buff, preserved gameplay/globals/messages/loadout).

**Architecture:** Three logical commits — (1) copy the vanilla upstream files over the repo while keeping three of our files untouched, (2) apply a deterministic loot-nerf transform to `db/types.xml`, (3) apply a +1 zed-buff transform to `env/zombie_territories.xml`. Transforms are Python scripts stored under `docs/tools/` (excluded from FTP deploy) so they're reproducible next update. A final commit updates `CHANGELOG.md`.

**Tech Stack:** DayZ mission config (XML/JSON), Python 3 (stdlib `re`, `math`), `xmllint` (ships with macOS), bash, git.

## Global Constraints

- Working branch: `feature/road-to-badlands-merge` (already created off `origin/develop`). Do NOT commit on `main`/`develop`.
- Upstream source dir: `../road-to-badlands-mission-files/dayzOffline.chernarusplus/` (relative to repo root `/Users/steveharmeyer/Development/dayz-one-life/chernarus`).
- Preserve every repo file's **current filename casing** — only file contents change. The one casing mismatch is repo `cfgIgnoreList.xml` ← upstream `cfgignorelist.xml`.
- **Loot nerf rule:** `nominal → ceil(nominal/2)`, `min → ceil(min/2)`, applied to every `<type>` in `types.xml` EXCEPT those with `deloot="1"` (in `<flags>`) or a `<usage name="ContaminatedArea"/>` child. `ceil` keeps `1→1` and `0→0`.
- **Zed buff rule:** every `<zone>` in `zombie_territories.xml` with `dmax > 0` gets `dmin+1` and `dmax+1`; zones with `dmax=0` are skipped.
- Transforms must rewrite ONLY the target values (nominal/min inner text; dmin/dmax attribute values), leaving all other bytes identical, for a clean diff.
- `co-authored-by` trailer on every commit: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.

---

### Task 1: Adopt the Road to Badlands vanilla base

**Files:**
- Overwrite from upstream (10 files): `cfgeventgroups.xml`, `cfgIgnoreList.xml` (←`cfgignorelist.xml`), `cfgrandompresets.xml`, `cfgspawnabletypes.xml`, `mapgrouppos.xml`, `mapgroupproto.xml`, `db/events.xml`, `db/types.xml`, `env/fox_territories.xml`, `env/zombie_territories.xml`
- Keep OURS (do NOT touch): `cfggameplay.json`, `db/globals.xml`, `db/messages.xml`, `custom/loadout.json`
- No-op (already identical to upstream): all other mission files

**Interfaces:**
- Produces: a working tree where `db/types.xml` and `env/zombie_territories.xml` are pristine upstream (to be transformed in Tasks 2–3), and all other upstream changes are adopted.

- [ ] **Step 1: Confirm our three preserved files match `origin/develop` (safety check)**

```bash
cd /Users/steveharmeyer/Development/dayz-one-life/chernarus
git diff --quiet origin/develop -- cfggameplay.json db/globals.xml db/messages.xml custom/loadout.json && echo "PRESERVED FILES CLEAN" || echo "WARNING: preserved files differ from origin/develop"
```
Expected: `PRESERVED FILES CLEAN`

- [ ] **Step 2: Copy the 10 upstream files over the repo (preserving repo casing)**

```bash
cd /Users/steveharmeyer/Development/dayz-one-life/chernarus
NEW=../road-to-badlands-mission-files/dayzOffline.chernarusplus
cp "$NEW/cfgeventgroups.xml"        cfgeventgroups.xml
cp "$NEW/cfgignorelist.xml"         cfgIgnoreList.xml   # casing preserved
cp "$NEW/cfgrandompresets.xml"      cfgrandompresets.xml
cp "$NEW/cfgspawnabletypes.xml"     cfgspawnabletypes.xml
cp "$NEW/mapgrouppos.xml"           mapgrouppos.xml
cp "$NEW/mapgroupproto.xml"         mapgroupproto.xml
cp "$NEW/db/events.xml"             db/events.xml
cp "$NEW/db/types.xml"              db/types.xml
cp "$NEW/env/fox_territories.xml"   env/fox_territories.xml
cp "$NEW/env/zombie_territories.xml" env/zombie_territories.xml
echo "copied"
```
Expected: `copied`

- [ ] **Step 3: Verify the working tree changed exactly the intended files**

```bash
git status --short
```
Expected: modified `M` on exactly the 10 files above (`cfggameplay.json`, `db/globals.xml`, `db/messages.xml` must NOT appear).

- [ ] **Step 4: Verify `cfgIgnoreList.xml` reverted to vanilla (our additions gone)**

```bash
grep -c 'PunchedCard\|ShippingContainerKeys\|Flaregun' cfgIgnoreList.xml
```
Expected: `0`

- [ ] **Step 5: Verify each touched XML is well-formed**

```bash
for f in cfgeventgroups.xml cfgIgnoreList.xml cfgrandompresets.xml cfgspawnabletypes.xml mapgrouppos.xml mapgroupproto.xml db/events.xml db/types.xml env/fox_territories.xml env/zombie_territories.xml; do xmllint --noout "$f" && echo "OK $f" || echo "BAD $f"; done
```
Expected: `OK` for all 10.

- [ ] **Step 6: Commit**

```bash
git add cfgeventgroups.xml cfgIgnoreList.xml cfgrandompresets.xml cfgspawnabletypes.xml mapgrouppos.xml mapgroupproto.xml db/events.xml db/types.xml env/fox_territories.xml env/zombie_territories.xml
git commit -m "chore: adopt Road to Badlands upstream mission config base

Overwrite changed mission files with the Road to Badlands vanilla base.
cfgIgnoreList.xml reverts to vanilla (custom ignores no longer needed).
cfggameplay.json, db/globals.xml, db/messages.xml, custom/loadout.json
kept as-is. types.xml and zombie_territories.xml are pristine here and get
our nerf/buff transforms in the following commits.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: Apply the loot nerf to `db/types.xml`

**Files:**
- Create: `docs/tools/road-to-badlands/nerf_loot.py`
- Modify: `db/types.xml`

**Interfaces:**
- Consumes: pristine upstream `db/types.xml` from Task 1.
- Produces: `db/types.xml` with `nominal`/`min` halved (ceil) on all non-excluded `<type>` blocks.

- [ ] **Step 1: Write the transform script**

Create `docs/tools/road-to-badlands/nerf_loot.py`:

```python
#!/usr/bin/env python3
"""Halve nominal/min (round up) on every <type> in db/types.xml except
types flagged deloot="1" or carrying a <usage name="ContaminatedArea"/>."""
import re
import sys

def ceil_half(n: int) -> int:
    return -(-n // 2)  # integer ceil: 1->1, 2->1, 3->2, 0->0

def nerf_block(m: re.Match) -> str:
    block = m.group(0)
    if 'deloot="1"' in block or 'name="ContaminatedArea"' in block:
        return block
    block = re.sub(r'(<nominal>)(\d+)(</nominal>)',
                   lambda x: f'{x.group(1)}{ceil_half(int(x.group(2)))}{x.group(3)}', block)
    block = re.sub(r'(<min>)(\d+)(</min>)',
                   lambda x: f'{x.group(1)}{ceil_half(int(x.group(2)))}{x.group(3)}', block)
    return block

def transform(text: str) -> str:
    return re.sub(r'<type name=.*?</type>', nerf_block, text, flags=re.DOTALL)

if __name__ == "__main__":
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        original = f.read()
    with open(path, "w", encoding="utf-8") as f:
        f.write(transform(original))
    print(f"nerf applied to {path}")
```

- [ ] **Step 2: Prove the core logic on inline fixtures (test before touching the real file)**

Run:
```bash
cd /Users/steveharmeyer/Development/dayz-one-life/chernarus
python3 -c '
import importlib.util, sys
spec = importlib.util.spec_from_file_location("nl", "docs/tools/road-to-badlands/nerf_loot.py")
nl = importlib.util.module_from_spec(spec); spec.loader.exec_module(nl)
assert nl.ceil_half(1)==1 and nl.ceil_half(2)==1 and nl.ceil_half(3)==2 and nl.ceil_half(0)==0 and nl.ceil_half(5)==3
normal = "<type name=\"X\"><nominal>4</nominal><min>2</min><flags deloot=\"0\"/></type>"
deloot = "<type name=\"Y\"><nominal>4</nominal><min>2</min><flags deloot=\"1\"/></type>"
contam = "<type name=\"Z\"><nominal>4</nominal><min>2</min><usage name=\"ContaminatedArea\"/></type>"
assert nl.transform(normal)=="<type name=\"X\"><nominal>2</nominal><min>1</min><flags deloot=\"0\"/></type>", nl.transform(normal)
assert nl.transform(deloot)==deloot
assert nl.transform(contam)==contam
print("FIXTURE TESTS PASS")
'
```
Expected: `FIXTURE TESTS PASS`

- [ ] **Step 3: Capture pre-transform reference values**

```bash
grep -c '<type name=' db/types.xml   # expect 1970
```
Expected: `1970`

- [ ] **Step 4: Apply the transform to the real file**

```bash
python3 docs/tools/road-to-badlands/nerf_loot.py db/types.xml
```
Expected: `nerf applied to db/types.xml`

- [ ] **Step 5: Verify — well-formed, count preserved, spot-checks**

```bash
xmllint --noout db/types.xml && echo "WELLFORMED"
grep -c '<type name=' db/types.xml   # still 1970
# normal item AK101: nominal 4->2, min 2->1
awk '/<type name="AK101">/{f=1} f{print} /<\/type>/{if(f)exit}' db/types.xml | grep -E '<nominal>|<min>'
# deloot item AK74: must stay 4 / 2
awk '/<type name="AK74">/{f=1} f{print} /<\/type>/{if(f)exit}' db/types.xml | grep -E '<nominal>|<min>|deloot'
# ContaminatedArea item StarlightOptic: must be unchanged vs base commit
git diff HEAD -- db/types.xml | grep -A2 -B2 'StarlightOptic' || echo "StarlightOptic UNCHANGED"
```
Expected: `WELLFORMED`; count `1970`; AK101 shows `<nominal>2</nominal>` and `<min>1</min>`; AK74 shows `<nominal>4</nominal>`, `<min>2</min>`, `deloot="1"`; `StarlightOptic UNCHANGED`.

- [ ] **Step 6: Confirm the diff only touches nominal/min lines**

```bash
git diff HEAD -- db/types.xml | grep '^[+-]' | grep -vE '^[+-]{3}|<nominal>|<min>' | head
```
Expected: no output (every changed line is a `<nominal>` or `<min>`).

- [ ] **Step 7: Commit**

```bash
git add docs/tools/road-to-badlands/nerf_loot.py db/types.xml
git commit -m "feat: re-apply loot nerf to Road to Badlands types.xml

Halve nominal/min (round up, 1 stays 1) on every type except deloot=\"1\"
and ContaminatedArea items. Deterministic rule via docs/tools script;
covers the new Road to Badlands items automatically.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 3: Apply the +1 zed buff to `env/zombie_territories.xml`

**Files:**
- Create: `docs/tools/road-to-badlands/buff_zeds.py`
- Modify: `env/zombie_territories.xml`

**Interfaces:**
- Consumes: pristine upstream `env/zombie_territories.xml` from Task 1.
- Produces: `zombie_territories.xml` with `dmin`/`dmax` +1 on every zone where `dmax > 0`.

- [ ] **Step 1: Write the transform script**

Create `docs/tools/road-to-badlands/buff_zeds.py`:

```python
#!/usr/bin/env python3
"""Increase every zombie zone's dmin/dmax by 1, skipping zones with dmax=0."""
import re
import sys

def buff(m: re.Match) -> str:
    dmin, dmax = int(m.group(1)), int(m.group(2))
    if dmax == 0:
        return m.group(0)
    return f'dmin="{dmin + 1}" dmax="{dmax + 1}"'

def transform(text: str) -> str:
    return re.sub(r'dmin="(\d+)" dmax="(\d+)"', buff, text)

if __name__ == "__main__":
    path = sys.argv[1]
    # newline="" disables newline translation on read AND write, so the file's
    # original line endings (this file is CRLF) are preserved byte-for-byte.
    with open(path, encoding="utf-8", newline="") as f:
        original = f.read()
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(transform(original))
    print(f"buff applied to {path}")
```

**Line endings:** `env/zombie_territories.xml` uses CRLF. The `newline=""` argument
on both `open` calls is mandatory — without it Python's text mode rewrites every
`\r\n` to `\n`, changing all 807 lines and violating "all other bytes identical."

- [ ] **Step 2: Prove the core logic on inline fixtures**

Run:
```bash
cd /Users/steveharmeyer/Development/dayz-one-life/chernarus
python3 -c '
import importlib.util
spec = importlib.util.spec_from_file_location("bz", "docs/tools/road-to-badlands/buff_zeds.py")
bz = importlib.util.module_from_spec(spec); spec.loader.exec_module(bz)
assert bz.transform("dmin=\"8\" dmax=\"12\"")=="dmin=\"9\" dmax=\"13\""
assert bz.transform("dmin=\"0\" dmax=\"5\"")=="dmin=\"1\" dmax=\"6\""
assert bz.transform("dmin=\"0\" dmax=\"0\"")=="dmin=\"0\" dmax=\"0\""   # zero zone skipped
print("FIXTURE TESTS PASS")
'
```
Expected: `FIXTURE TESTS PASS`

- [ ] **Step 3: Count zones with dmax>0 before applying (reference)**

```bash
grep -oE 'dmax="[0-9]+"' env/zombie_territories.xml | grep -vc 'dmax="0"'
```
Note the number `N` (all zones, since this file has no dmax="0").

- [ ] **Step 4: Apply the transform**

```bash
python3 docs/tools/road-to-badlands/buff_zeds.py env/zombie_territories.xml
```
Expected: `buff applied to env/zombie_territories.xml`

- [ ] **Step 5: Verify — well-formed, first zone +1, changed-line count matches N**

```bash
xmllint --noout env/zombie_territories.xml && echo "WELLFORMED"
# CRLF must be preserved (this file is CRLF); still present after transform:
grep -lq $'\r' env/zombie_territories.xml && echo "CRLF PRESERVED" || echo "CRLF LOST!"
# first zone was dmin=8 dmax=12 -> expect 9/13
grep -m1 'dmin=' env/zombie_territories.xml
# numstat must be EXACTLY N added / N deleted (only the buffed zone lines);
# if line endings flipped, this shows ~807/807 instead of N/N.
git diff --numstat HEAD -- env/zombie_territories.xml
```
Expected: `WELLFORMED`; `CRLF PRESERVED`; first zone shows `dmin="9" dmax="13"`; numstat shows exactly `N	N	env/zombie_territories.xml` (added == deleted == N from Step 3).

- [ ] **Step 6: Commit**

```bash
git add docs/tools/road-to-badlands/buff_zeds.py env/zombie_territories.xml
git commit -m "feat: re-apply zed buff (+1) to Road to Badlands zombie_territories.xml

Increase dmin/dmax by 1 on every spawning zone (down from the prior +2),
skipping dmax=0 zones. Deterministic rule via docs/tools script.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 4: Update CHANGELOG and final verification

**Files:**
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: the three commits from Tasks 1–3.
- Produces: an `[Unreleased]` CHANGELOG entry; a clean, fully well-formed working tree ready for a PR.

- [ ] **Step 1: Fill in the `[Unreleased]` section of `CHANGELOG.md`**

Replace the empty `## [Unreleased]` block with:

```markdown
## [Unreleased]

### Added
- `docs/tools/road-to-badlands/`: reusable transform scripts (`nerf_loot.py`, `buff_zeds.py`) that re-derive our loot nerf and zed buff on top of upstream files (excluded from server deploy).

### Changed
- Adopted Bohemia's **Road to Badlands** mission config as the new base for all upstream-owned files (`cfgspawnabletypes.xml`, `cfgeventgroups.xml`, `cfgrandompresets.xml`, `mapgrouppos.xml`, `mapgroupproto.xml`, `db/events.xml`, `db/types.xml`, `env/fox_territories.xml`, `env/zombie_territories.xml`).
- **Loot nerf** re-derived as a deterministic rule: halve `nominal`/`min` (round up, so `1` stays `1`) on every `db/types.xml` type except `deloot="1"` and `ContaminatedArea` items. Now also covers new Road to Badlands loot.
- **Zed buff** reduced from +2 to **+1** on `env/zombie_territories.xml` zone `dmin`/`dmax` (zones with `dmax=0` skipped).

### Removed
- `cfgIgnoreList.xml` custom additions (flares, `PunchedCard`, colored `ShippingContainerKeys`) — reverted to vanilla; the old keys/cards they suppressed have since despawned.
```

(Preserved as-is and therefore not listed as changes: `custom/loadout.json`, `db/messages.xml`, `cfggameplay.json`, `db/globals.xml`.)

- [ ] **Step 2: Final well-formedness sweep across every touched XML**

```bash
cd /Users/steveharmeyer/Development/dayz-one-life/chernarus
for f in cfgeventgroups.xml cfgIgnoreList.xml cfgrandompresets.xml cfgspawnabletypes.xml mapgrouppos.xml mapgroupproto.xml db/events.xml db/types.xml env/fox_territories.xml env/zombie_territories.xml; do xmllint --noout "$f" || echo "BAD $f"; done; echo "SWEEP DONE"
```
Expected: `SWEEP DONE` with no `BAD` lines.

- [ ] **Step 3: Confirm branch history is the intended four commits**

```bash
git log --oneline origin/develop..HEAD
```
Expected: spec-doc commit, base-adoption commit, loot-nerf commit, zed-buff commit (CHANGELOG staged next).

- [ ] **Step 4: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: changelog for Road to Badlands merge

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Post-plan: opening the PR

After Task 4, the feature is code-complete. Hand off to the **finishing-a-feature** skill to run the pre-PR checklist (CHANGELOG already done; CLAUDE.md needs no change since project instructions are unchanged) and open the PR into `develop`. Release (`develop`→`main`) is a later, separate step via **drafting-a-release** / **cutting-a-release**.
