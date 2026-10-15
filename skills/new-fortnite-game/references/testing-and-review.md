# Testing and review for UEFN

UEFN has no Play-in-Editor, no headless runner and no unit-test framework for Verse (none that I found [?]). The MCP **can't press buttons or walk**. So testing has six layers, and the human does the input layer.

```
1. Build (BuildAll: diagnostics [])
2. Verse self-test at session start (event- or timer-driven, reads LogVerse)
3. Session with test players (Island Settings → Debug → Test Players on Start)
4. Evidence: editor viewport + Fortnite client screenshots + LogVerse excerpt
5. playtest-reviewer agent (read-only) → APPROVE / REJECT
6. Human plays with 2+ real clients and a break-it checklist → commit
```

## 1. Build
- Run `ValkyrieToolset.VerseToolset.BuildAll` through MCP, or Verse → Build Verse Code.
- Quote the diagnostics. Any error is a stop. Read the warnings in the files you touched.

## 2. Verse self-test (the replacement for unit tests)
- Keep rules in **pure functions** (`<computes>` or `<transacts>`, no devices) in a `Rules` module: scoring, economy maths, odds, round-state transitions. Rules that don't touch devices can be checked with known inputs.
- Add a `selftest_device` (template: `templates/verse/selftest_device.verse`). Its `@editable RunSelfTest:logic = false`. When true, at `OnBegin` it:
  - calls each rule with known inputs and prints `MYGAME SELFTEST PASS <name>` or `FAIL <name> expected=… got=…`
  - ends with `MYGAME SELFTEST DONE passed=N failed=M`
- Read it with `LogsToolset.GetLogEntries(category="LogVerse", pattern="MYGAME SELFTEST")`.
  - **Count the steps, not just "failed=0"**: a run that stopped early looks green.
  - Read only lines from this run. Print a run id (a new tag) in `OnBegin` and match it.
- Device behaviour can be smoke-tested by calling device methods (`Timer.Start()`, `Trigger.Trigger()`). Label those results **"device path, not input path"**.
- **Lesson from Casino Royale:** a test command that bypassed the real input hid a broken minigun for weeks. The self-test proves rules. Only a human pressing the real button proves the input path.
- **Turn `RunSelfTest` off before any private version or publish.** The reviewer checks this.

## 3. Sessions and multiple clients
- **Launch Session** opens a Fortnite client connected to UEFN.
  - The first cook can take several minutes.
  - Push Changes updates a running session; Verse-only pushes are fast.
  - With **Auto Push Verse Changes**, every successful compile pushes automatically.
  - Source: https://dev.epicgames.com/documentation/fortnite/live-edit-and-iteration-improvements-in-fortnite
- **Test players:** Island Settings → Debug → **Test Players on Start** = Fill or Custom spawns up to 98 idle test players (capped by Max Players).
  - They take damage, join teams, use spawners and can instigate devices.
  - **In Verse, test players are agents but not `player`s.** `GetPlayspace().GetParticipants()` includes them; `GetPlayers()` doesn't.
  - They are not real network clients, so they don't test latency, UI per client, or join-in-progress.
  - Source: https://dev.epicgames.com/documentation/en-us/fortnite/multiplayer-previewing-in-unreal-editor-for-fortnite
- **Real second client:**
  - A friend or teammate joins the live edit session through the Fortnite party panel. Set their permission (Play / Edit) under My Island → Permissions.
  - Editing a project you don't own requires being on its team (Creator Portal → Share with Team).
  - No collaborators under 18.
  - Source: https://dev.epicgames.com/documentation/fortnite/collaborating-in-unreal-editor-for-fortnite
- **Private version playtest:**
  1. Publish Project gives a private version.
  2. Creator Portal → Playtests → Create Playtest gives a code.
  3. Add up to **50 playtesters** (adults, age-verified) to the Playtest Group.
  4. Update Playtest points the group at a newer version.
  - Source: https://dev.epicgames.com/documentation/en-us/fortnite-creative/adding-playtesters-in-fortnite-creative
- **Other platforms:** Session Options → **Connect To Platform** to test on console or mobile. Do this before the first release: mobile and Switch get the lowest LODs and the tightest memory.
- **Never start, stop, restart or push into a session the human is playing in.**
  - Before any session call, check `GetSessionStatus` and ask: "Is anyone playing? May I push / restart?"
  - A push with `bVerseOnly:false` restarts the round for everyone in it.

## 4. Evidence: screenshots and logs
- **Editor viewport:** `EditorToolset.EditorAppToolset.CaptureViewport` returns a PNG. Use a saved camera transform so before/after shots match. It shows hidden objects too, so it's good for layout and scale, not for what a player sees.
- **Fortnite client window:** `templates/tools/window_shot.ps1 -Title "Fortnite"` captures the client window as shown, HUD included. It uses Windows `PrintWindow`, reads pixels only and sends no input.
  - [?] It works for the Unreal editor's client windows. It is untested on the Fortnite client, which runs Easy Anti-Cheat.
  - If it returns black, ask the human for a screenshot (Win+Shift+S) and a short description.
  - **Never inject into, hook, or send keyboard/mouse input to the Fortnite client.**
- **Logs:**
  - Verse `Print` and `log` output goes to the editor log, category `LogVerse`.
  - The file is `%LOCALAPPDATA%\UnrealEditorFortnite\Saved\Logs\UnrealEditorFortnite.log`.
  - Fortnite client logs are in `%LOCALAPPDATA%\FortniteGame\Saved\Logs\` and contain no Verse prints.
  - Collapse repeated lines and quote the relevant ones.
- **Save evidence to `shots/<date>-<task>/`.** Name files by what they show (`01-lobby-hud.png`). Keep a `log.txt` excerpt beside them. Don't commit large images unless the project wants them, and if so use LFS.
- **Images for the human:** after each batch, show the human the key screenshot or contact sheet. For a report (balance, retention, a pre-publish checklist), publish an Artifact page and give them the link.

## 5. The playtest-reviewer agent
Template: `templates/agents/playtest-reviewer.md` → copy it to `.claude/agents/` in the project.
- **The agent that builds never approves.** After each feature, give the reviewer:
  - the **Done means / Must not change / I'll verify by** lines
  - the screenshot paths
  - the LogVerse excerpt and the self-test summary
  - the diff range (git or Lore)
  - `docs/DEVICES.md` changes
- It reads only. It returns APPROVE or REJECT with concrete problems.
- On REJECT: fix, gather fresh evidence, review again. Don't argue with the reviewer, and don't "approve" for it.

## 6. The human playtest (each gate)
Give the human a checklist of no more than 5 steps, including break attempts:
- **Two players** do the same thing in the same moment (both press the button, both buy the last item).
- A player **leaves mid-interaction**, and a new player **joins in progress**.
- A player is **eliminated mid-interaction** (respawn while holding state).
- **Round restart:** does state reset or carry over as the GDD says? (`OnBegin` reruns each round.)
- **Spam the input.** Use the real button, not a debug path.
- Persistence: **Simulate New User** and **Import From Live** (Island Settings → Persistence Behavior).
- At least once per gate: a real second client (friend, team member or playtest group), not only test players.

Also list what you couldn't verify: feel, fun, readability on a phone screen, audio, fairness under lag.

## 7. Performance and memory (each art batch, and before every release)
- Launch Memory Calculation after End Game. Record the number. Treat 80% of the budget as the warning line. See asset-pipeline.md.
- Turn on "Monitor Performance" and use the Spatial Profiler in the busiest spot with test players filled.
- Look for server hitches from Verse loops: replace polling with events, and add `Sleep` in loops.

## 8. When something breaks
- Bug report format (`docs/BUGS.md`): **Steps / Expected / Actual / Evidence / Cause / Fix**. Find the cause before changing anything.
- **Two failed fixes → roll back** to the last good commit (or Lore snapshot) and shrink the problem.
- No silent workarounds. If a tool, device or API can't do what's asked, stop and say so in one sentence.
- Write the lesson in `docs/LESSONS.md`, one line.
