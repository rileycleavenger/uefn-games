# UEFN MCP: setup, tools and verified usage

Researched 2026-10-14. Labels:
- **[Epic]** stated on an Epic page (URL given).
- **[3P]** reported by a third-party source, not by Epic. Treat it as a strong hint and confirm it with `describe_toolset` before relying on it.
- **[?]** uncertain.

Main sources:
- [Epic] UEFN MCP: https://dev.epicgames.com/documentation/fortnite/uefn-mcp
- [Epic] Unreal MCP in UE 5.8 (the same plugin; UEFN points to it as its "related document"): https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor
- [Epic] 42.00 release notes (Aug 20, 2026; first release with the MCP): https://dev.epicgames.com/documentation/fortnite/42-00-fortnite-ecosystem-updates-and-release-notes
- [Epic] 42.10 release notes (adds the Programmatic toolset): https://dev.epicgames.com/documentation/fortnite/42-10-fortnite-ecosystem-updates-and-release-notes
- [Epic] 42.30 release notes (UMG Verse-field binding; fix for dialogs that stalled MCP): https://dev.epicgames.com/documentation/fortnite/42-30-fortnite-ecosystem-updates-and-release-notes
- [Epic] Forum announcement: https://forums.unrealengine.com/t/unreal-mcp-is-now-available-in-uefn/2745278
- [3P] Verse skill by Magnus Enebakk, whose handle suggests Epic staff (unconfirmed); written for UEFN 42.30. See `reference/uefn/editor-mcp.md`: https://github.com/magnusenebakk-epic/verse-skill
- [3P] Pinned tool allowlist for v42 (29 toolsets, 384 tools): https://github.com/Valid/uefn-python-bridge (`bridge/uefn_tool_policy.py`)

## 1. What it is
- [Epic] "UEFN MCP embeds an MCP server inside the Unreal Editor for Fortnite process". Any MCP client, such as Claude Code, Cursor or the MCP Inspector, can drive the editor over a local HTTP connection.
- [Epic] It is in **beta**: "expect some rough edges". Not every UE 5.8 toolset works in UEFN yet. It shipped in UEFN 42.00.
- [Epic] There is **no authentication** and it is loopback only. The UE page says it "is not safe to expose beyond the local machine". Never forward port 8000.
- [Epic] Tool calls run **serially on the game thread**: don't send overlapping calls.
- [Epic] Known issues:
  - "MCP tool calls can cause the editor to hitch and hang."
  - The Python toolsets use XYZ, not UEFN's Left-Up-Forward (LUF) coordinates, so you may have to convert between them yourself.

## 2. Setup (once per project)
1. [Epic] In UEFN, open **Project Settings** and tick **Python Editor Scripting** and **UEFN MCP Toolsets**. "Both of these must be enabled for UEFN MCP to function."
   - [?] Fortnite's blog and some forum posts call these **beta access** toggles. Some accounts report the menu is missing (forum, Sep–Oct 2026, no Epic reply yet): https://forums.unrealengine.com/t/project-settings-menu-missing-in-uefn-cannot-enable-uefn-mcp-toolsets/2758333. If the user can't see them, stop and tell them. Don't look for a workaround.
2. [Epic] The server starts with the editor. "To start and stop the server, you must close and re-open the editor."
   - The default port is **8000**. To change it, set Editor Preferences > **Server Port Number**.
   - [?] The UE page also documents Auto Start Server and console commands such as `ModelContextProtocol.GenerateClientConfig ClaudeCode`. The UEFN page only hints at config generation, so don't rely on them.
3. [Epic] Put a `.mcp.json` file in the **UEFN project root**:
   ```json
   { "mcpServers": { "unreal-mcp": { "type": "http", "url": "http://127.0.0.1:8000/mcp" } } }
   ```
   [3P] Or register it once for all projects:
   `claude mcp add --transport http --scope user unreal-mcp http://127.0.0.1:8000/mcp`
4. [Epic] Start Claude Code from the project root, where `.mcp.json` lives. Then run `/mcp` and check that `unreal-mcp` is connected.
5. Run a read-only check first. For example: "List the toolsets. Read only, change nothing. Then list the Verse files and the devices in the level."

[3P] Things that break the connection:
- Only one editor serves port 8000, normally the first one opened.
- After the editor restarts, the old MCP session silently stops working. Reconnect with `/mcp`, which starts a new `initialize`.
- Without Python enabled, the Object, Actor and Scene toolsets are missing. Preflight with `ValkyrieToolset.ValkyriePythonToolset` → `IsPythonEnabledInUEFN`.

## 3. Discover → describe → call (always)
[Epic] Tool Search is on by default. `tools/list` returns only three meta-tools:
- `list_toolsets`: the toolset names and descriptions
- `describe_toolset`: the schemas for one toolset
- `call_tool`: runs a tool. Pass `toolset_name`, `tool_name` and `arguments`.

The rules:
1. At the start of each session, call `list_toolsets`. **Don't trust a tool name from memory or from this file** until `describe_toolset` has confirmed it in this editor build.
2. Read every result. Many tools report failure as a value, not an error. Anything that isn't an explicit success is a stop.
3. One call at a time. Wait for slow calls such as builds, session start and push.
4. Never call while the editor shows a modal dialog. Ask the human to close it.

## 4. The toolsets
[Epic] The UEFN page lists the feature areas:
- Toolset Registry
- **Verse**: "reads, edits, and compiles project Verse source"
- **Verse Scene Graph** entities
- **Creative Devices**: "browses the catalog, places devices, and edits any @editable properties"
- **Sessions**: "UEFN plays using Play-in-Client (PIC) and not Play-in-Editor (PIE)"
- **Verse File Sandboxing**: "Confines Verse file operations to the creator's project"

The 42.00 notes also mention building UI with UMG. 42.10 added the Programmatic toolset, which batches several tool calls in one script.

[3P] Exact names, from the v42 allowlist and the verse-skill (42.30). Confirm each one with `describe_toolset`.

| Toolset | Tools |
|---|---|
| `ValkyrieToolset.VerseToolset` | `ListFiles`, `ReadFile`, `WriteFile(path, content, bCreateIfMissing)`, `Replace(path, oldString, newString)`, `Grep`, `CreateDirectory`, `Copy`, `Move`, `Delete(path, bRecursive)`, `BuildAll` |
| `ValkyrieToolset.SessionToolset` | `StartSession(location?, rotation?)`, `StopSession`, `StartGame`, `StopGame`, `PushChanges{bVerseOnly}`, `GetSessionStatus`, `GetGameState`, `GetClientLogEntries` |
| `ValkyrieToolset.DeviceToolset` | `ListDeviceAssets(nameFilter)`, `PlaceDevice(assetPath, transform)`, `ListDeviceProperties`, `GetDeviceProperties`, `SetDeviceProperty`, `AddEventBinding`, `RemoveEventBinding`, `ListEventBindings`, `GetBindingOptions` |
| `ValkyrieToolset.EntityToolset` | `CreateEntity(entityClass, transform, name, parentEntity?)`, `DeleteEntity`, `FindEntities`, `AddComponent(entity, componentClass)`, `RemoveComponent`, `GetComponents`, `List/Get/SetComponentProperty`, `ListComponentClasses`, `ListEntityClasses`, `Get/SetEntityTransform` |
| `ValkyrieToolset.ValkyriePythonToolset` | `IsPythonEnabledInUEFN`, `EnablePythonInUEFN` |
| `EditorToolset.EditorAppToolset` | `CaptureViewport`, `Get/SetCameraTransform`, `SelectActors`, `OpenEditorForAsset`, … |
| `EditorToolset.LogsToolset` | `GetLogEntries(category, pattern, maxEntries)`, `GetLogCategories`, `Get/SetVerbosity` |
| `editor_toolset.toolsets.*` | `ActorTools`, `AssetTools` (including `save_assets`), `ObjectTools` (`get/set/list_properties`), `SceneTools` (`find_actors`, `trace_world`), `MaterialTools`, `MaterialInstanceTools`, `StaticMeshTools`, `SkeletalMeshTools`, `TextureTools`, `DataTableTools`, `CurveTableTools`, `PrimitiveTools` |
| Others | `UMGToolSet`, `MVVMToolset`, `VerseFieldsToolset`, `WidgetAnimationToolset`, `GameplayTagsToolset`, Niagara toolsets, `PhysicsAssetToolset`, `ProgrammaticToolset.execute_tool_script` |

[3P] Argument formats:
- Object arguments: `{"refPath": "..."}`.
- Transforms: `{"location":{x,y,z},"rotation":{pitch,yaw,roll},"scale":{x,y,z}}`.
- Always pass all three parts. A rotation-only transform moved an actor to the origin.
- `ObjectTools.set_properties` wants `values` as a JSON **string**. If you pass an object, it returns `false`.
- Many device settings come in `X` / `X_Override` pairs. Set both.

## 5. The Verse loop through MCP
1. Read first: `ListFiles("")` shows the project package and the read-only digests, e.g. `/Verse.org (Verse)/Verse.digest.verse`. [3P] The project root path is `/<project-guid>`, and each folder is a module.
2. Write with `WriteFile` or `Replace`.
3. Build with `BuildAll`. [3P] It takes about 3 s and returns a diagnostics array. `[]` means it compiled. Each entry has severity, code, message, file and span. **Quote the diagnostics.** A clean build proves the code compiles, not that it works.
4. [3P] Don't build in the middle of a session. Stop the session first, or use `PushChanges`.
5. [3P] Never delete or move `.verse` files on disk while the editor is open: every later build then fails with "Error getting text contents of snippet". Delete through `VerseToolset.Delete` or the Verse Explorer.

## 6. The session loop through MCP
1. Remove scratch actors (prefix them `zz_`). [3P] `StartSession` validates the island and **saves the level**.
2. `StartSession`. [3P] The first cook can take more than 2 minutes. Poll `GetSessionStatus` until it says Connected, then `GetGameState` until it says CanStart or Running.
3. `StartGame` if the match hasn't started by itself.
4. Read Verse output with `LogsToolset.GetLogEntries(category="LogVerse", pattern="<your tag>")`.
   - [3P] Verse `Print` goes to the **editor** log, not the client log, so `GetClientLogEntries` won't show it.
   - Use plain-text tags such as `MYGAME:`. A pattern starting with `[` returned nothing.
   - The editor log file is `%LOCALAPPDATA%\UnrealEditorFortnite\Saved\Logs\UnrealEditorFortnite.log`.
5. Iterate:
   - `PushChanges {"bVerseOnly":true}` takes about 10 s.
   - `{"bVerseOnly":false}` takes 50–80 s and restarts the round.
   - After a push, confirm that a **new startup Print tag** appeared before trusting the test.
6. `StopSession` when done. It leaves the Fortnite client open.

[3P] Known blockers:
- If validation fails, UEFN opens a modal "Unable to Play" dialog, and every MCP call hangs until a human closes it. The reasons (e.g. "Disallowed reference to …") are in the editor log **file**. Read the file, then ask the human to close the dialog.
- If a Verse-only push says "The Refresh command is not currently available", run `StopGame`, then push with `bVerseOnly:false`.
- Saving a big level can block every call for about 2 minutes.
- A deliberate runtime `Err` once left the editor unresponsive. Don't trigger runtime errors when no one is watching.
- **The MCP can't simulate player input.** The human does the input tests. See testing-and-review.md.
- **Never start, stop or push into a session the human is playing in.** Check `GetSessionStatus` first and ask.

## 7. Devices, entities, island settings
- **Place a device:** [3P] `ListDeviceAssets("Timer")` → `PlaceDevice(assetPath, transform)` → name it with `ActorTools.set_label`.
- **Bind a Verse device's `@editable` to a placed device:** [3P]
  1. `GetDeviceProperties(holder, [Field])` gives the field's sub-object path.
  2. `ObjectTools.set_properties(that path, '{"savedActor":{"refPath":"<device actor path>"}}')`.
  3. `SetDeviceProperty` rejected this case.
  - Or ask the human to set it in the Details panel. That is often faster.
- **Entities:** [3P] `CreateEntity` with `/EntityFramework/_Verse/VNI/Entity.entity`. Your own Verse classes are named like `/<project-guid>/_Verse.<folder>-<class>`, and they show up only after a successful build.
- **Island settings:** [3P] use `ObjectTools.get/set_properties` on `IslandSettings_0` (find it with `SceneTools.find_actors {"name":"Island"}`). For example, `totalRounds`, `respawnTime`, and `roundTimeLimit` with `roundTimeLimit_Override`.
- **Screenshots:** [3P] `EditorAppToolset.CaptureViewport` returns a PNG of the **editor** viewport, which also shows hidden objects. Gameplay screenshots come from the Fortnite client. See testing-and-review.md.

## 8. What the MCP does not do
- **Publishing.** [Epic] No page mentions it. [3P] There is no publish tool. Save with `AssetTools.save_assets`, then the human clicks **Upload to Private Version** in UEFN and finishes in the Creator Portal.
- **Private-version playtests.** No Epic page mentions them.
- **Player input.** The MCP can't press buttons or walk.
- **Starting or stopping the server.** Only an editor restart does that.
- **Custom toolsets.** [?] One community README says UEFN ignores custom Python toolsets, so the `create-toolset` skill probably doesn't apply. Unverified.

## 9. Rules for this skill
- Commit before every batch of editor changes: MCP edits aren't always undoable.
- Ask for a plan on multi-step requests. Keep each batch small and name things explicitly ("the Timer device named `RoundTimer`").
- Prefix scratch objects `zz_` and remove them before a session.
- Read the full text of any Python script before approving it (`execute_tool_script`, Python toolsets).
- Never run Claude Code with `--dangerously-skip-permissions` while the MCP is connected.
- Only one agent drives the editor at a time. Don't start a second editor while one is serving port 8000.
- If `/mcp` shows it disconnected, don't edit files on disk as a workaround for editor-only changes. Say so and wait.

## 10. Community MCP servers (optional)
Epic's MCP is the base. Community servers are add-ons; see resources.md. Don't install any server that injects DLLs, uses private servers or automates the mouse and keyboard.
