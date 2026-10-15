# uefn-games

A Claude Code plugin for **making Fortnite islands in UEFN** (Unreal Editor for Fortnite) from a one-line game idea.

## Use
Start Claude Code in your UEFN project folder and pass your idea to the skill:
```
/new-fortnite-game a 4-player co-op zombie farm defense where you plant crops by day and defend them at night
```
The skill then:
1. **Checks the idea against Fortnite's Developer Rules** (no gambling or casino-style games, no real brands, Teen rating, no Experimental features). If the idea breaks a rule, it suggests the closest version that can be published.
2. Writes a one-page **GDD** with you, asking at most a few questions that block it.
3. **Sets up the project** from the templates: CLAUDE.md, docs, Verse skeletons, the tuning pipeline, Blender scripts and a read-only playtest reviewer agent.
4. Builds **one system at a time**: greybox with devices → core rules in Verse → one interaction end to end → mode rules → persistence → UI → art → game feel → performance → publish → iterate on analytics.

Each step is built, checked with the self-test and screenshots, reviewed by the reviewer agent, then **played by you with 2+ real clients** before it's committed. You're the director and the only real playtester. The skill won't build the whole island unattended.

## Setup
The skill checks these on its first run and tells you the exact command for anything that's missing. Doing them ahead of time saves a round trip.

**1. Claude Code plugins and skills** (type these in Claude Code):
```
/plugin marketplace add rileycleavenger/uefn-games
/plugin install uefn-games@uefn-games
/plugin install unreal-engine-skills-for-claude-code@claude-plugins-official
```
Then install the companion `verse` skill for Verse language and API detail:
```
git clone https://github.com/magnusenebakk-epic/verse-skill ~/.claude/skills/verse
```
Restart Claude Code. Epic's plugin adds the `unreal-mcp` skill, which teaches safe use of the editor MCP.

**2. Programs (Windows)**
| Program | Needed for | Install |
|---|---|---|
| Epic Games Launcher + **Unreal Editor for Fortnite** | Everything | https://store.epicgames.com/download → Library → UEFN |
| Git + Git LFS | Version control | https://git-scm.com (includes LFS), then `git lfs install` |
| Python 3 | Tuning generator, contact sheets | `winget install Python.Python.3.13`, then `py -m pip install --user pillow` |
| Blender 4.x *(art pass)* | Headless model scripts | `winget install BlenderFoundation.Blender` (put `blender` on PATH) |
| Blender MCP *(optional)* | Interactive modelling | `winget install astral-sh.uv`, add the addon from [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp), then `claude mcp add blender -- uvx blender-mcp` |
| Unreal Engine 5.6+ *(optional)* | MetaHuman NPCs | Epic Games Launcher → Unreal Engine |

**3. UEFN project**
1. In UEFN, create a project in `Documents/Fortnite Projects/<Name>` (not in OneDrive).
2. Project Settings → tick **Python Editor Scripting** and **UEFN MCP Toolsets** (beta), then restart UEFN.
3. Connect Claude Code to the editor's built-in MCP server:
   ```
   claude mcp add --transport http --scope user unreal-mcp http://127.0.0.1:8000/mcp
   ```
4. Start Claude Code in the project folder. `/mcp` should show `unreal-mcp` connected.

**4. People and accounts**
- A second Fortnite account, or a friend, for the 2-client playtests.
- To publish: be 18+ and enrolled in the Fortnite Developer Program. Start early, because the tax and payout steps can take days.

## What's inside
```
.claude-plugin/              plugin + marketplace manifests
skills/new-fortnite-game/
  SKILL.md                   the workflow: rules check, stack, rules, phases, build loop
  references/                uefn-mcp, verse-cheatsheet, devices, asset-pipeline,
                             testing-and-review, publishing, resources
  templates/                 CLAUDE.md, docs/ (GDD, NEXT_STEPS, DEVICES, BUGS, LESSONS, CREDITS),
                             verse/ skeletons, data/tuning.csv, tools/ (gen_tuning, window_shot,
                             blender/), agents/playtest-reviewer.md, gitignore/gitattributes
```

## Other ways to install
Copy `skills/new-fortnite-game` into `~/.claude/skills/`. For local development: `claude --plugin-dir /path/to/uefn-games`.

## What's been verified
Facts were researched on 2026-10-14 against UEFN about v42.30; items marked `[?]` in the references are uncertain. The Verse templates were checked against Epic's docs and the Book of Verse but **not compiled**. Build them on your first project and record any fixes in that project's `docs/LESSONS.md`.
