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

## Requirements
- Windows, UEFN (Epic Games Launcher), Python Editor Scripting + UEFN MCP Toolsets enabled in Project Settings (beta).
- `.mcp.json` pointing at the editor's built-in server, `http://127.0.0.1:8000/mcp` (the skill walks you through it).
- To publish: 18+ and enrolled in the Fortnite Developer Program.
- Optional: Blender (headless model scripts), Git + LFS or Lore for version control, and the companion [`verse` skill](https://github.com/magnusenebakk-epic/verse-skill) for Verse language detail.

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

## Install
```
/plugin marketplace add rileycleavenger/uefn-games
/plugin install uefn-games@uefn-games
```
Or copy `skills/new-fortnite-game` into `~/.claude/skills/`. For local development: `claude --plugin-dir /path/to/uefn-games`.

## What's been verified
Facts were researched on 2026-10-14 against UEFN about v42.30; items marked `[?]` in the references are uncertain. The Verse templates were checked against Epic's docs and the Book of Verse but **not compiled**. Build them on your first project and record any fixes in that project's `docs/LESSONS.md`.
