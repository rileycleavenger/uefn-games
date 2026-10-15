# <Island name> — rules for Claude

A **Fortnite island built in UEFN with Verse**, published through the Creator Portal. Follow the `new-fortnite-game` skill. For Verse language detail, load the `verse` skill if it's installed.

## Before anything
1. `git status` is clean (or Lore: Sync Latest, nothing checked out by others on files you need). Commit or ask first.
2. Read `docs/GDD.md` (the source of truth), `docs/NEXT_STEPS.md`, `docs/LESSONS.md`, `docs/DEVICES.md` and the open items in `docs/BUGS.md`.
3. If editor work is planned, check that `/mcp` shows `unreal-mcp` connected, then call `list_toolsets`. Don't use a tool name you haven't confirmed with `describe_toolset` in this editor build.
4. Build Verse (`BuildAll`) and confirm the diagnostics are `[]` before you start.
5. Say which phase the project is in and the single next task.

## Island-specific rules
- **Money, score and odds are decided in Verse only.** Use the functions in `rules.verse`, with numbers from `tuning.verse`. All Verse runs on the server. Keep hidden values out of UI text and device settings.
- **Tuning numbers come from `data/tuning.csv` → `tools/gen_tuning.py` → `tuning.verse`.** Never hand-edit `tuning.verse`. If a simulator writes the CSV, re-run it before changing a number.
- **No gambling or casino-style content** (Developer Rules 1.11, 1.15.5): no slots, roulette, card betting, raffles or chip imagery, even with fake money.
- **Parody names and original designs only.** No real brands, logos, venues or people, and no recreated Fortnite skins, characters or music.
- Free assets only. Every third-party or AI-made asset gets a row in `docs/CREDITS.md` before it ships.
- <add game-specific rules here>

## How we work
- One system per task. Before starting, restate **Done means / Must not change / I'll verify by**.
- Devices do Fortnite gameplay. Verse holds the rules. Record every in-editor device binding in `docs/DEVICES.md`.
- After each change:
  1. Build Verse and quote the diagnostics.
  2. Run the self-test (`selftest_device`, `RunSelfTest = true`) in a session, and read `LogVerse` for this run's tag and the step count.
  3. Take screenshots: the editor viewport through MCP, and the Fortnite client with `tools/window_shot.ps1` or from the human.
  4. Hand off to the `playtest-reviewer` agent.
  5. The human plays with 2+ real clients and a break-it checklist.
  6. Commit.
- **The MCP can't press buttons.** Input paths are tested by the human, never only by a debug shortcut.
- **Never start, stop, restart or push into a session the human is playing in.** Ask first.
- No silent workarounds. Two failed fixes → roll back. Write each lesson in `docs/LESSONS.md`.
- Commit before every batch of MCP edits. Prefix scratch objects `zz_` and remove them before a session.
- Read every Python script before approving it. Never use `--dangerously-skip-permissions` with the MCP connected.
- Show the human a screenshot after each batch. Publish reports (balance, analytics, pre-publish check) as an Artifact.

## Commands
```
py tools/gen_tuning.py data/tuning.csv "<Verse folder>/tuning.verse"       # numbers → Verse
blender --background --factory-startup --python tools/blender/build_models.py -- <module>   # models → build/models
py tools/blender/contact_sheet.py SM_ build/models/sheet.png               # previews → one image
powershell -ExecutionPolicy Bypass -File tools\window_shot.ps1 -Title "Fortnite"   # client screenshot
```
MCP (confirm the names with `describe_toolset` first):
- `VerseToolset.BuildAll`
- `SessionToolset.StartSession` / `PushChanges {"bVerseOnly":true}` / `StopSession`
- `LogsToolset.GetLogEntries {"category":"LogVerse","pattern":"MYGAME"}`
- `EditorAppToolset.CaptureViewport`

## Project map
| Path | What |
|---|---|
| `<Project>.uefnproject` | The UEFN project |
| `<Verse folder>` (find it with `VerseToolset.ListFiles("")`) | `game_manager_device.verse`, `rules.verse`, `tuning.verse` (generated), `player_save.verse`, `selftest_device.verse` |
| `data/tuning.csv` | Tuning numbers (source of truth for `tuning.verse`) |
| `tools/` | `gen_tuning.py`, `window_shot.ps1`, `blender/` model scripts, any balance simulator |
| `build/models/` | Generated `.glb` files and previews (not committed, or LFS) |
| `shots/` | Screenshots and log excerpts for reviews |
| `docs/` | GDD, NEXT_STEPS, DEVICES, BUGS, LESSONS, CREDITS |
