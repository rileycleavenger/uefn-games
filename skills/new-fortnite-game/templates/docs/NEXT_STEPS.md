# Next steps

**Phase:** 0 – setup. **Next single task:** …

## Human-only steps (start early: some take days)
- [ ] Fortnite Developer Program enrolment: 18+, a real-money Epic purchase in the last 365 days, tax interview, Hyperwallet (up to 5 business days)
- [ ] Claude Code tools (the skill's Setup step 0): `/plugin install unreal-engine-skills-for-claude-code@claude-plugins-official`, the `verse` skill, Git + LFS, Python 3; Blender, Pillow and UE 5.6+ only for the art pass
- [ ] UEFN installed (Epic Games Launcher), project created in `Documents/Fortnite Projects/<Project>` (not in OneDrive)
- [ ] Project Settings: **Python Editor Scripting** and **UEFN MCP Toolsets** ticked; editor restarted
- [ ] `.mcp.json` in the project root; Claude Code started there; `/mcp` shows `unreal-mcp`
- [ ] Version control chosen: Lore (team) or Git + LFS with Lore off (solo). See the skill's publishing.md §6.
- [ ] A second Fortnite account or a friend for 2-client tests; playtest group set up later

## Phases (each ends with a human playtest gate)
1. Setup and read-only MCP check (list toolsets, Verse files, devices in the level)
2. Greybox: spawn, teams, round start and end, using devices only
3. Core rules in Verse (`rules.verse`, `tuning.verse`) + self-test
4. One interaction end to end with 2 real clients
5. Win/lose, round flow, join in progress, leave mid-round
6. Persistence (`player_save`), tested with Simulate New User and Import From Live
7. UI pass (Verse UI or HUD devices), readable on phone
8. Art pass in small batches (Blender / Fab / MetaHumans), memory checked after each batch
9. Analytics devices, Accolades, other platforms
10. Private version → playtest group → release (Unlisted first) → iterate on analytics

## Memory log
| Date | Change | Memory (of budget) |
|---|---|---|
| | | |

## Experiments (one at a time)
| Date shipped | Hypothesis | Metric | Result | Kept? |
|---|---|---|---|---|
| | | | | |
