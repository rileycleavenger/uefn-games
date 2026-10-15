---
name: new-fortnite-game
description: Make a new Fortnite island (game) in UEFN (Unreal Editor for Fortnite) with Claude Code. Takes it from pitch and GDD through Verse code, Creative devices, assets (Blender, Fab, MetaHumans), testing in sessions with multiple clients, the memory budget, and publishing through the Creator Portal, then iteration on analytics. Uses Epic's UEFN MCP server (the editor's built-in "unreal-mcp"). Use when the user wants to build, plan, test or publish a Fortnite / UEFN / Verse island or map, or says "Fortnite game", "UEFN", "Verse", "Creative device", "island code", "Creator Portal", "Engagement Payouts". Not for standalone Unreal Engine games (use vibe-steam-game-unreal) or Roblox.
argument-hint: "<your game idea, e.g. 'zombie farm defense for 4 players'>"
---

# New Fortnite game (UEFN + Verse + UEFN MCP)

The human is the director and the only real playtester. Your job is to turn small, clear instructions into working, server-side Verse plus device setups. Each step is verified, reviewed and committed. Stop and say so when an instruction is vague, a tool fails, or a result can't be verified.

## Start here: the game idea
The idea passed in: **$ARGUMENTS**
- **No idea given** (the line above is empty): ask the human for one or two sentences about the game, and wait.
- **The idea is the pitch.** Fill gaps with sensible defaults and ask only what blocks the GDD (at most 3 questions, e.g. player count, solo vs teams, round length).
- Run step 0 (the rules check) on it first. If it breaks a rule, say so and offer the closest publishable version before any design work.
- Draft `docs/GDD.md` from it and get the human's OK. Then go through the Workflow phases **one at a time**, each ending with a human playtest. Never try to build the whole island in one pass.
- If the current folder isn't a UEFN project yet (no `.uefnproject`), start with Setup.
- Pick a short uppercase log tag from the island name (e.g. `ZOMBIEFARM`) and use it in place of `MYGAME` everywhere: templates, log patterns, the self-test.

## Background and references
**UEFN is not full Unreal.** There is no C++, no Blueprint gameplay, no Play-in-Editor, no dedicated servers to run, and no store page to build. You get Verse, Creative devices, Fortnite's characters and items, Epic's servers, a memory budget, content rules and the Creator Portal.

Load the `references/` files when you reach that phase. Facts were researched on 2026-10-14 (UEFN about v42.30). Anything marked [?] is uncertain: check it before relying on it.

| Reference | Load when |
|---|---|
| `references/uefn-mcp.md` | Setting up or using the editor MCP (tools, sessions, logs, limits) |
| `references/verse-cheatsheet.md` | Writing any Verse |
| `references/devices.md` | Choosing or wiring devices; Scene Graph or devices |
| `references/asset-pipeline.md` | Blender, Fab, MetaHumans, imports, memory |
| `references/testing-and-review.md` | Self-test, sessions, screenshots, the reviewer, human playtests |
| `references/publishing.md` | Content rules, release, money, analytics, version control |
| `references/resources.md` | Docs, community libraries, what to avoid |
| `templates/` | Bootstrapping a new project (CLAUDE.md, docs, Verse skeletons, tools, reviewer agent) |

**Companion skill:** for deep Verse language and API detail, install Magnus Enebakk's `verse` skill: `git clone https://github.com/magnusenebakk-epic/verse-skill ~/.claude/skills/verse`. It targets UEFN 42.30, and the author appears to be Epic staff (unconfirmed). This skill covers the workflow; that one covers the language.

## Step 0: the rules check (before any design work)
Fortnite moderates every island. Check the pitch against the Developer Rules first (publishing.md section 1):
- **No gambling or casino-style games, even with fake money.** Rules 1.11 and 1.15.5, as quoted in the press; the official page needs an Epic login. That rules out slots, roulette, card betting, raffles and chip imagery. A casino game like Casino Royale is very likely not publishable as an island. Say so plainly and offer a different theme or mechanic.
- **Parody names and original designs only.** No real brands, logos, places or people. No recreated Fortnite skins, characters or music.
- Rating ceiling: ESRB Teen / PEGI 16.
- **No Experimental features in the core loop.** Islands that use them can't be released. Conversations (AI NPCs) is Experimental. Scene Graph is Beta, which is publishable.
- The publisher must be 18+ and enrolled in the Fortnite Developer Program (Epic purchase, tax interview, Hyperwallet). **Ask the human to start enrolment in week 1.**

## The stack (don't substitute without asking)
| Job | Tool |
|---|---|
| Editor | UEFN (Epic Games Launcher), Windows |
| Editor control | **UEFN MCP**: the built-in `unreal-mcp` server at `http://127.0.0.1:8000/mcp`. Beta since v42.00. |
| Gameplay rules | **Verse** (text, diffable, built with `BuildAll`) |
| Fortnite gameplay | **Creative devices**, driven from Verse through `@editable` references |
| Own props, components | Scene Graph entities and components (Beta) where they fit |
| Tuning numbers | `data/tuning.csv` → `tools/gen_tuning.py` → `tuning.verse` (Verse can't read files at runtime) |
| Models | **Blender as headless Python scripts** → `.glb` + previews; Blender MCP for look-dev |
| Free assets | Fab inside UEFN (free only, licence recorded); Sketchfab CC0/CC BY; Mixamo |
| Characters | **MetaHumans** for NPCs. Players wear their own Fortnite outfits. |
| UI | Verse UI (`player_ui`, `canvas`, `text_block`) or HUD devices |
| Version control | Lore (Epic's, formerly URC) for teams; or Git + LFS with locking and Lore off for solo projects. Never both. |
| Docs | `docs/` GDD, NEXT_STEPS, DEVICES, BUGS, LESSONS, CREDITS |

## Non-negotiable rules
1. **Commit before every session and every batch of MCP edits.** MCP edits aren't always undoable.
2. **One system per request.** Restate **Done means / Must not change / I'll verify by** before starting. Never change terrain, lighting and gameplay in one request.
3. **Discover → describe → call.** Call `list_toolsets`, then `describe_toolset`, then `call_tool`. Never use a tool name you haven't confirmed in this editor build. Never invent a Verse API: **grep the project's `*.digest.verse` first.**
4. **Read every result.** Quote `BuildAll` diagnostics, tool results and `LogVerse` lines before saying "done". A tool call that succeeds doesn't mean the island is right.
5. **The server decides, and in Verse everything already runs on the server.** Keep money, score, odds and RNG in Verse rules. Never put hidden values in UI text or visible device settings. Validate who triggered a device; anyone in range can press it.
6. **Numbers come from data, never hand-tuned in code.** If balance matters, a simulator writes the CSV. Re-run it after any rule change, and keep its model checked against `rules.verse` through the self-test.
7. **The builder never approves.** After each feature, run the `playtest-reviewer` agent with screenshots, the LogVerse excerpt, the self-test summary, the diff and the Done line. Then the human plays with **2+ real clients**.
8. **Test through real input.** The MCP can't press buttons. A debug shortcut that skipped the real input once hid a broken weapon. Device-path and self-test results are labelled as such; input paths are proven by the human.
9. **Never hijack a play session.** Don't start, stop, restart or push into a session the human is in. Check `GetSessionStatus` and ask.
10. **No silent workarounds.** If a tool, device or API can't do what's asked, stop and say so in one sentence. **Two failed fixes → roll back** and shrink the problem.
11. **Write lessons down**: one line each in `docs/LESSONS.md`.
12. **Editor safety:**
    - Close modal dialogs before calling, or ask the human to: they block every MCP call.
    - Don't build Verse mid-session; use Push Changes.
    - Never delete `.verse` files on disk while UEFN is open.
    - Prefix scratch objects `zz_` and remove them before a session (StartSession saves the level).
    - Read every Python script before approving it.
    - Never use `--dangerously-skip-permissions` with the MCP connected.
    - Keep port 8000 local.
13. **Show progress as images.** After each batch, show the human the key screenshot or contact sheet. Publish reports (pre-publish check, analytics review, balance) as an Artifact.

## Setup (once per machine and project)
1. The human installs UEFN and creates the project from a template in `Documents/Fortnite Projects/<Name>`, not in OneDrive. The Feature Examples are worth opening: Verse Device, Gunfight, and Speedway Race with Verse Persistence.
2. Project Settings → tick **Python Editor Scripting** and **UEFN MCP Toolsets**, then restart UEFN. The server starts with the editor; only an editor restart stops it. [?] Some accounts report these settings missing (beta access). If so, stop and tell the human.
3. Put `.mcp.json` in the project root:
   ```json
   { "mcpServers": { "unreal-mcp": { "type": "http", "url": "http://127.0.0.1:8000/mcp" } } }
   ```
   Or: `claude mcp add --transport http --scope user unreal-mcp http://127.0.0.1:8000/mcp`. Add the `blender` MCP too if you'll model interactively.
4. Start Claude Code **in the project root**. `/mcp` should show `unreal-mcp` connected. After any editor restart, reconnect: the old session silently dies.
5. Choose version control (publishing.md section 6). Copy `templates/gitignore.template` and `templates/gitattributes.template` for Git, then run `git lfs install`.
6. Copy the templates in:
   - `CLAUDE.md`
   - `docs/*`
   - `data/tuning.csv`
   - `tools/` (`gen_tuning.py`, `window_shot.ps1`, `blender/`)
   - `agents/playtest-reviewer.md` → `.claude/agents/`
   - the Verse files in `verse/` → the project's Verse folder, through `VerseToolset.WriteFile` or by hand
   Then commit.
7. Read-only check: "List the toolsets. Read only, change nothing. List the Verse files and the read-only digests, the devices in the level, and Island Settings' max players."

## Verse project layout
- **Folder = module.** Keep a small game in one folder; split into folders (modules) only when it grows.
- Find the Verse root with `VerseToolset.ListFiles("")`. [3P] It is `/<project-guid>`.
- Starting files (templates):
  | File | Holds |
  |---|---|
  | `game_manager_device.verse` | One `creative_device` that owns round flow and wires devices through `@editable` |
  | `rules.verse` | **Pure** rules (`<computes>` / `<transacts>`, no devices): scoring, economy, odds |
  | `tuning.verse` | Generated constants. Never edit it by hand. |
  | `player_save.verse` | One versioned `class<final><persistable>` + a module-scope `weak_map(player, …)` |
  | `selftest_device.verse` | Checks the rules with known inputs, prints `MYGAME SELFTEST …` |
- Templates are syntax-checked against Epic's docs and the Book of Verse, **not compiled by the skill author**. Build them first, and fix against the project's digests.

## Workflow: idea → published island
Each phase is a gate: verify, review, the human plays, commit.
1. **Pitch + rules check (step 0)**
   - One page in `docs/GDD.md`: hook, core loop, the first 30 seconds, players and teams, round flow, what persists, systems in build order, scope cuts.
   - Pick a genre with an audience: check the Fortnite Data API and Discover.
2. **Setup and read-only check** (above).
3. **Greybox with devices only:** spawns, teams, round start and end, a timer, end game. Use Fortnite's building pieces or simple meshes. Record every device and binding in `docs/DEVICES.md`.
4. **Core rules in Verse:** `rules.verse` + `tuning.verse` + the self-test. Build, then check the self-test in a session.
5. **One interaction end to end with 2 real clients:** the core mechanic, from button or trigger to rule to UI.
6. **Mode rules:**
   - win and lose
   - round restart (`OnBegin` reruns, so fields reset)
   - join in progress, leaving mid-round
   - elimination mid-interaction
7. **Persistence:** `player_save`, written at checkpoints. Test with Simulate New User and Import From Live. Freeze the schema mindset now: after publish you can only add fields with defaults.
8. **UI:** Verse widgets per player, or HUD/Billboard/Popup devices. Readable on a phone screen.
9. **Art pass in small batches** (asset-pipeline.md):
   - Blender scripts → previews → contact sheet → the human approves → import.
   - Free Fab assets with licences recorded.
   - MetaHuman NPCs, a few only (about 60 MB each).
   - Run the memory calculation after every batch.
10. **Game feel:** audio, VFX, camera, Accolades (XP), and the Analytics devices (numbered event names).
11. **Performance and platforms:** memory under budget (80% warning line), the busiest spot profiled with test players, Connect To Platform for console and mobile.
12. **Publish (the human clicks):**
    1. Pre-publish checklist (publishing.md section 7).
    2. Publish Project creates a private version.
    3. Playtest group.
    4. Creator Portal release: details, IARC rating, transactions, media, attribution, visibility.
    5. Submit for review. Start **Unlisted**, then Listed.
13. **Iterate on analytics:**
    - Look at CTR, 2–5 minute bounce, session length and D1/D7 against the Creator Portal benchmarks.
    - One experiment per version. Log it in NEXT_STEPS.
    - Add in-island transactions only after retention is healthy, and redo the IARC rating when you do.

## Build loop (every feature)
```
read LESSONS → restate Done / Don't change / Verify → grep digests for every API you'll use
→ edit Verse (WriteFile/Replace) → BuildAll: diagnostics [] → MCP device/entity wiring (or ask the human)
→ StartSession / PushChanges (ask first if anyone is playing) → check the new build tag in LogVerse
→ self-test DONE line (step count) → screenshots (viewport + client) → playtest-reviewer
→ human playtest, 2+ real clients, break-it checklist → commit (+ DEVICES.md) → LESSONS.md
```
- Verse-only change: `PushChanges {"bVerseOnly":true}` takes about 10 s. Level or property changes: `bVerseOnly:false` takes about a minute and **restarts the round**.
- Read `LogVerse` through `LogsToolset.GetLogEntries(category="LogVerse", pattern="MYGAME")`. Verse prints are not in the client log.
- Do the five-minute jobs by hand: nudging a prop, one Details-panel value, binding one `@editable`. Tell the human when the editor is faster.

## Verse in one screen (details: verse-cheatsheet.md)
- **Failure is control flow.** Failable expressions only run in failure contexts, and an `if` that fails rolls back its effects:
  - failable: `X[I]`, `Map[K]`, `player[Agent]`, `F[]` for `<decides>` functions, comparisons, `Opt?`
  - failure contexts: `if (…)`, `for (…)` filters, `<decides>` bodies, `logic{}`, `option{}`, `X or Default`
- **Effects:**
  - `<suspends>`: async. Not combinable with `<decides>`.
  - `<decides>`: can fail. Pair it with `<transacts>`, `<reads>` or `<computes>`.
  - `<transacts>`: can be rolled back. Annotate helpers you call from `if` conditions with it.
  - `<computes>`: pure.
- **Concurrency:**
  - `race` (first wins, others cancelled), `sync` (wait for all), `rush`, `branch`, `spawn{}` (from non-async code)
  - `Sleep(0.0)` waits one tick
  - Prefer `Event.Await()` and `Subscribe` over polling loops
- **Devices:** `@editable Button:button_device = button_device{}`, then `Button.InteractedWithEvent.Subscribe(OnPressed)` in `OnBegin<override>()<suspends>:void`.
  - **Set every `@editable` in the Details panel.** An unset one fails silently.
- **Players:**
  - `agent` vs `player` (`player[Agent]`) vs `fort_character` (`Agent.GetFortCharacter[]`)
  - `GetPlayspace().GetPlayers()` returns humans only; `GetParticipants()` includes test players and AI
  - Handle `PlayerRemovedEvent()`
- **Persistence:**
  - Module-scope `var Saves:weak_map(player, player_save) = map{}`, where `player_save` is a `class<final><persistable>` with no `var` fields
  - 256 KB per player, at most 4 player-keyed maps
  - After publish, only add fields with defaults
- **Pitfalls:**
  - `()` vs `[]`
  - unannotated helpers inside `if`
  - int/float mixing, `int / int` is a failable rational
  - shadowed names (don't define `Clamp`, `Max`, `Print`)
  - busy loops
  - subscriptions that pile up across rounds
  - a running session keeps old code until you push

## Assets, UI, memory (summaries)
- **Blender → UEFN:**
  - `templates/tools/blender/`: 1 unit = 1 m, Z-up, pivot at the base, grid 5.12 m, player 1.92 m (a pillar in each preview).
  - Budget checks: tris per class, textures ≤ 2048 px and power of two.
  - Export `.glb`, which UEFN imports through Interchange.
  - Textured surfaces, not flat colours.
  - Import by drag and drop unless `describe_toolset` shows an import tool.
- **Fab:**
  - Window → Fab, filter UEFN.
  - Referenced content isn't Scene Graph compatible.
  - With computer use (the human allows it), browse free items only and **never click Buy**. Record the licence URL in CREDITS and in the Creator Portal Attribution step.
- **Characters:**
  - MetaHumans through MetaHuman Creator (UE) → UEFN Export → MetaHuman Importer → NPC Character Definition (Custom Character) → NPC Spawner.
  - Don't build humans from blocky primitives: the director rejected that look as "like Roblox characters".
- **UI:** per-player Verse widgets tracked in a `[player]widget` map, with `ui_input_mode.All` for clickable UI. Or HUD Message, Billboard and Popup devices for simple text.
- **Memory:**
  - 100,000 units per streaming area, shown as 300 MB from v42.20. You can't publish over it.
  - Measure with Launch Memory Calculation after End Game.
  - Reuse assets and device types. Log the number in NEXT_STEPS after every art batch.

## Prompt shape (use it)
```
<one system>. Don't change <list>.
<numbered requirements>
Verse decides: <what>. Devices only <display / do>.
Done means: <observable result with 2 real clients>.
Grep the digests for every API you use. Build and quote the diagnostics.
Report every Verse file, device, binding (DEVICES.md), asset and CSV row you created or changed.
If a step fails or a tool is missing, stop and tell me. Don't work around it silently.
```

## Cost and pacing
- Use medium effort by default. Raise it for the GDD, the architecture, or one stubborn bug, then lower it again.
- Batch MCP work: the first session cook takes minutes, and big level saves block calls for about 2 minutes. Queue a batch, then let the human do something else.
- Time-box experiments and roll back when the box runs out.

## Session start checklist
1. `git status` is clean (or Lore is synced), and nobody else holds locks on files you need.
2. Read CLAUDE.md, GDD, NEXT_STEPS, LESSONS, DEVICES and the open BUGS.
3. `/mcp` shows `unreal-mcp`. `list_toolsets` works. `BuildAll` returns `[]`.
4. Ask whether anyone is in a session before touching sessions.
5. State the phase and the single next task.
