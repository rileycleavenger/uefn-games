# <Island name> — one-page GDD

> This page is the single source of truth. If the island disagrees with it, ask which one is right, then update this page.

## Rules check (fill this in before anything else)
- [ ] No gambling, casino-style games, raffles or prize wheels tied to purchases (Developer Rules 1.11, 1.15.5)
- [ ] No real brands, logos, places, people, or recreated Fortnite or other IP. Names are parody or original.
- [ ] Fits Fortnite's rating ceiling (ESRB Teen / PEGI 16). No gore.
- [ ] Doesn't rely on Experimental features, which can't be published (check each feature's status)

## Hook
One sentence a player reads on the Discover tile. It must match real gameplay.

## Core loop
"You ___, to ___, so that ___." Name the thing the player does every ~10 seconds, and say what they do in the **first 30 seconds** after spawning.

## Players and session
- Players: min __ / max __ (Island Settings). Teams: __. Join in progress: yes/no.
- Round length: __ min. Rounds per match: __. Requeue: __.
- What carries between rounds (in memory) and between sessions (`weak_map` persistence): …

## Systems (build in this order, one at a time)
| # | System | Devices | Verse owns |
|---|---|---|---|
| 1 | Spawn, teams, round start/end | Player Spawner, Island Settings, Timer, End Game | Round flow |
| 2 | Core mechanic | … | The rule and its numbers |
| 3 | Scoring / win / lose + HUD | Score Manager or Verse UI | Score rules |
| 4 | Progression / persistence | — | `player_save` |
| 5 | … | | |

## Win / lose
- Win: …
- Lose: …
- Restart / requeue: works from both, at any moment.

## Numbers
Every tunable number lives in `data/tuning.csv`, generated into `tuning.verse`. If balance matters, the numbers come from a simulator (`tools/sim.py`) that writes the CSV.

## Content
- Map size and areas: … (plan streaming cells; the memory budget is per area)
- NPCs: … (MetaHumans: at most __, about 60 MB each)
- Custom props: … (Blender scripts) / Fab assets: …
- Target session: __ min. Target D1 retention: __% (compare with the Creator Portal benchmark for the genre).

## Art and audio direction
- Style: …
- Reference images: `docs/refs/*.png`
- Mood: …

## Platforms
- PC, console, mobile? Check UI readability on a phone. Mobile and Switch get Min LOD 2 and the tightest memory.

## Scope cut list (NOT in v1)
- In-island transactions (after D1 retention is healthy)
- AI-voiced NPCs (Conversations is Experimental)
- …

## Publishing
- Island code: … Visibility: Unlisted → Listed
- Tags: … Thumbnail idea (real gameplay only): …
- Analytics events (Analytics device names, numbered): `01_…`, `02_…`
