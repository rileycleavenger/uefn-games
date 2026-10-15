# Lessons

One line per lesson: what went wrong → the rule we follow now. Read this at the start of every session. Copy the general ones into the next project's file.

Starter lessons carried over from the Casino Royale (Unreal) project:
- A test shortcut that skipped the real input hid a broken weapon → test every feature through the real player input path (walk up, press the real button), not a debug trigger.
- A scripted test ran inside the director's own play session → never start, end or drive a session the human is in. Ask first.
- A tool call reported success while the result was wrong → read every tool result, the Verse build output and the log; look at a screenshot before saying "done".
- An editor save failed silently on a locked file → lock binary files (`git lfs lock`) before editing them, and check that the save really happened.
- A hand-written numbers table drifted from the game → generate balance numbers from the simulator into data, never hand-tune them in code.
- Two blind fixes in a row made it worse → after two failed fixes, roll back and shrink the problem.
- Blocky scripted characters looked "like Roblox characters" → use real characters (MetaHumans or quality Fab characters) for anything the player looks at up close.

Project lessons:
- (example) `Button.InteractedWithEvent` never fired → the `@editable` reference was empty in the Details panel; check every `@editable` is set after placing a device.
