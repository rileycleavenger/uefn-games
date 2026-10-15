# Creative devices: the most useful ones, and how Verse uses them

Devices are Fortnite's built-in gameplay pieces. Place them in the level, set them up in the Details panel, and either wire them to each other (event bindings) or drive them from a Verse device through `@editable` references.

**Rule: use a device when one exists for the job, and use Verse for the rules that connect them.** Devices are tested, replicated, cheap to build and familiar to moderators. Verse holds the logic you need to read, diff and review: scoring, economy, round flow, odds.

Sources:
- Device classes in Verse: https://dev.epicgames.com/documentation/en-us/uefn/verse-api/fortnitedotcom/devices
- Coding device interactions: https://dev.epicgames.com/documentation/en-us/fortnite/coding-device-interactions-in-verse

Member names marked ✔ were checked on Epic's API pages on 2026-10-14. Everything else is **from memory or the community: grep `Fortnite.digest.verse` before using it.**

## Wiring patterns
```verse
@editable StartButton:button_device = button_device{}     # 1. Expose it, then pick the placed device in the Details panel
StartButton.InteractedWithEvent.Subscribe(OnStart)        # 2. React to every event (handler takes agent) ✔
Agent := StartButton.InteractedWithEvent.Await()          # 3. Or wait for one event (inside <suspends>)
RoundTimer.Start()                                        # 4. Call methods to drive a device
```
- An array of devices works too: `@editable Spawners:[]player_spawner_device = array{}`.
- Subscribing returns a `cancelable`. Cancel it when the feature ends.
- In-editor event bindings (Device A's "On Triggered" → Device B's "Enable") need no Verse. They're fine for simple wiring, but they're invisible to a `git diff`. **Record every binding in `docs/DEVICES.md`** (device name → event → target → function) so the reviewer can check it.

## The core set (most islands need these)
| Device | Verse class | Typical use | Key members |
|---|---|---|---|
| Island Settings | (actor `IslandSettings_0`, not a device class) | Max players, teams, rounds, respawn, persistence test mode, test players | Set with MCP `ObjectTools`; see uefn-mcp.md |
| Player Spawner | `player_spawner_device` | Where players appear, by team | `SpawnedEvent` |
| Team Settings & Inventory | `team_settings_and_inventory_device` | Team names, starting items, respawn hooks | `TeamMemberSpawnedEvent` [3P] |
| Class Designer / Class Selector | `class_designer_device`, `class_and_team_selector_device` | Loadouts, health, movement per class | |
| Round Settings | `round_settings_device` | Per-round rules, round-end conditions | |
| End Game | `end_game_device` | End the match for a winner | `Activate(Agent)` |
| Timer | `timer_device` | Round clocks and countdowns | ✔ `SuccessEvent`, `FailureEvent`, `StartUrgencyModeEvent`, `Start`/`Pause`/`Resume`/`Reset`/`Complete` (per agent and `ForAll` versions), `SetActiveDuration`, `SetMaxDuration` |
| Score Manager | `score_manager_device` | Award score | `Activate(Agent)`, `SetScoreAward` |
| Elimination Manager | `elimination_manager_device` | React to eliminations | `EliminatedEvent`, `EliminationEvent` [community: the second gives `?agent` for the eliminator] |
| Tracker | `tracker_device` | Count-to-N objectives, quests | `Increment`, `CompleteEvent` |
| HUD Message | `hud_message_device` | On-screen text | ✔ `Show()`, `Show(Agent)`, `Hide`, `SetText` (clamped to 150 characters), `SetDisplayTime`, `ClearAllMessages` |
| Billboard | `billboard_device` | World-space text signs | `SetText` |
| Popup Dialog | `popup_dialog_device` | Yes/No and choice prompts | `Show(Agent)`, `RespondingButtonEvent` (agent, button index) |
| Button / Conditional Button | `button_device`, `conditional_button_device` | Interact to do something; key-item doors | ✔ `InteractedWithEvent` |
| Trigger | `trigger_device` | Fire logic when stepped on or signalled | `TriggeredEvent`, `Trigger` |
| Input Trigger | `input_trigger_device` | Custom key presses | `PressedEvent`, `ReleasedEvent`. ✔ Latency is a full client→server round trip |
| Item Granter | `item_granter_device` | Give weapons, items, currency | `GrantItem(Agent)` |
| Item Spawner / Remover | `item_spawner_device`, `item_remover_device` | Floor loot; clear inventories | |
| Vending Machine | `vending_machine_device` | Buy items with in-game currency | |
| Barrier | `barrier_device` | Walls that open per phase or team | `Enable`, `Disable` |
| Mutator Zone | `mutator_zone_device` | Area rules: no build, speed, team-only | `AgentEntersEvent`, `AgentExitsEvent` |
| Damage Volume | `damage_volume_device` | Hazards, storm-like areas | |
| Capture Area | `capture_area_device` | King of the hill, control points | |
| Teleporter | `teleporter_device` | Lobby → arena, respawn rooms | `Teleport(Agent)` |
| Prop Mover | `prop_mover_device` | Smooth moving platforms and doors (replicated motion) | |
| Player Reference | `player_reference_device` | Show a player's stats on a podium | |
| Cinematic Sequence | `cinematic_sequence_device` | Intros, cutscenes, animated props | `Play`, `Stop` |
| Accolades | `accolades_device` | XP awards (counts towards Engagement Payouts) | ✔ `Award(Agent)`, `TestAwardEvent` (fires only in unpublished islands) |
| Analytics | `analytics_device` | Count player-driven events for the Creator Portal | `Submit(Agent)`; see publishing.md |
| NPC Spawner / Guard Spawner / Creature Spawner | `npc_spawner_device`, `guard_spawner_device`, `creature_spawner_device` | AI enemies and NPC characters (incl. MetaHumans) | |
| Map Indicator | `map_indicator_device` | Map and compass markers | |
| HUD Controller | `hud_controller_device` | Hide or show Fortnite HUD parts | |
| Random Number Generator | `rng_device` | Device-only randomness (prefer `GetRandomInt` in Verse) | |

Also on the device index: `audio_player_device`, `vfx_spawner_device`, `customizable_light_device`, `collectible_object_device`, `objective_device`, `matchmaking_portal_device`, `stat_creator_device`, `gameplay_camera_*`, `gameplay_controls_*`, `conversation_device`, `switch_device`, `lock_device`, `teleporter_device`, `player_counter_device`, `player_checkpoint_device`, `perception_trigger_device`, `pulse_trigger_device`, `prop_manipulator_device`, `item_shop_device`.

## Starter kits by game type
| Game type | Devices | Verse owns |
|---|---|---|
| Arena / team deathmatch | Island Settings (teams, respawn), Player Spawners per team, Class Designer, Elimination Manager, Score Manager, Timer, End Game, HUD Message | Score to win, streaks, round flow, the per-player HUD |
| Deathrun / parkour | Player Checkpoints, Teleporters, Timer, Trigger per stage, Tracker, Accolades, Analytics (one per stage) | Stage timing, best times (persistence), leaderboard UI |
| Tycoon / simulator | Buttons, Vending Machines, Item Granters, Prop Movers, Billboards, Analytics, Accolades | The economy (sim-generated constants), upgrades, offline progress, saves (`weak_map`) |
| Prop hunt / hide-and-seek | Class Designer (two classes), Mutator Zones, Timer, Barrier (seeker release), HUD Message | Role assignment, the reveal schedule, scoring |
| Zone wars / BR-lite | Storm controllers, Item Spawners, Player Spawners, Elimination Manager, Round Settings | Loadouts per round, round scoring, map rotation |
| Co-op PvE | NPC / Guard / Creature Spawners, Damage Volumes, Tracker, Popup Dialog, Cinematic Sequence | Waves, difficulty scaling, objectives |

## Scene Graph or devices?
- **Scene Graph** (entities + components + prefabs, `/Verse.org/SceneGraph`) is **Beta**. It has been publishable since June 2025 (v36.00), and Epic still calls it Beta in v42: "use caution when shipping with it". Source: https://dev.epicgames.com/documentation/en-us/fortnite/scene-graph-in-unreal-editor-for-fortnite
- Epic's direction (State of Unreal, June 2026) is that UE6 merges UE5 and UEFN, with Verse as the main gameplay language and Scene Graph replacing actors and components. Early access is planned for end of 2027. Code written Scene Graph-first will age better. [Press report: https://www.strafe.com/news/read/state-of-unreal-2026-all-the-key-takeaways-from-the-epic-keynote/]
- Practical default for a first island:
  - **Use devices for Fortnite gameplay** (spawning, items, teams, eliminations, HUD). Many of these APIs are only reachable through devices today.
  - **Use Verse for the rules**, either as one `creative_device` "game manager" or as Scene Graph components.
  - Try Scene Graph components for your own interactive props (moving, spawning, per-entity logic). Load the `verse` skill's `scene-graph.md` before writing them.
  - Fab "Referenced" content is not compatible with Scene Graph (see asset-pipeline.md).
- The MCP can create entities and add components (`EntityToolset`). See uefn-mcp.md.

## Device hygiene
- Name every device in the Outliner (`RoundTimer`, `Spawn_Team1_A`). The MCP and the human both work better with explicit names.
- Each device type costs memory in every streaming cell, but more copies of the same type are cheap. Reuse types. See publishing.md, memory.
- Many device settings come in `X` / `X_Override` pairs. Set both, through MCP or in the Details panel.
- After placing a Verse device, check that **every** `@editable` is set. Then build and push.
