# Verse cheat sheet

Checked 2026-10-14 against:
- Epic's Verse docs: https://dev.epicgames.com/documentation/en-us/fortnite/verse-language-reference
- The Book of Verse: https://verselang.github.io/book/
- The verse-skill (UEFN 42.30): https://github.com/magnusenebakk-epic/verse-skill

**The project's `*.digest.verse` files are the ground truth.** Grep them before using any API name. If this sheet and the digest disagree, the digest wins. Write the difference into `docs/LESSONS.md`.

## 0. The rules that matter most
1. **Never invent an API.** Grep `Fortnite.digest.verse`, `UnrealEngine.digest.verse` and `Verse.digest.verse` first. Through MCP: `VerseToolset.Grep`, or `ListFiles("")` to find them. On disk: glob for `*.digest.verse` under `%LOCALAPPDATA%\UnrealEditorFortnite\Saved\VerseProject\` [?]. Models often invent handlers such as `OnPlayerEliminated`, and they don't exist.
2. **Build after every change** (`BuildAll`, or Verse → Build Verse Code). Quote the diagnostics. Clean means compiles, not works.
3. **All Verse runs on the server.** See section 9.
4. Verse is not Python or C++. Everything is an expression, failure is control flow, and values are immutable unless declared `var`.

## 1. Files, modules, imports
- Each `.verse` file lives in the project's Verse folder. **A folder is a module.** Make a folder module `<public>` if other modules use its types.
- Imports go at the top:
  ```verse
  using { /Fortnite.com/Devices }                  # creative_device, button_device, …
  using { /Fortnite.com/Characters }               # fort_character, GetFortCharacter
  using { /Fortnite.com/Playspaces }               # fort_playspace
  using { /Fortnite.com/UI }                       # text_block, button_regular, …
  using { /Verse.org/Simulation }                  # Sleep, agent, player, …
  using { /Verse.org/Random }                      # GetRandomInt, GetRandomFloat
  using { /UnrealEngine.com/Temporary/UI }         # player_ui, canvas, GetPlayerUI
  using { /UnrealEngine.com/Temporary/Diagnostics } # log, log_channel
  using { /UnrealEngine.com/Temporary/SpatialMath } # vector3 (XYZ), used by fort_character
  ```
- There are two `vector3` types:
  - `/Verse.org/SpatialMath`: Left-Up-Forward, used by Scene Graph.
  - `/UnrealEngine.com/Temporary/SpatialMath`: XYZ, used by characters and devices.
  - Don't mix them.
- **No shadowing at all.** A name can't repeat a built-in, a member, an outer name or a module name. Don't call things `Max`, `Floor`, `Print` and so on.

## 2. Naming and style
- Types and classes: `snake_case` (`round_manager_device`). Functions, variables and fields: `PascalCase` (`StartRound`, `PlayerScores`).
- Player-facing text goes in `<localizes>` messages, not string literals:
  ```verse
  RoundStartText<localizes>:message = "Round starting!"
  ScoreText<localizes>(Score:int):message = "Score: {Score}"
  ```
- Prefix every log line with a plain-text tag (`MYGAME:`) so it's easy to grep in `LogVerse`.

## 3. Variables, types, containers
```verse
Limit:int = 10                   # constant
var Score:int = 0                # mutable; the type is required
set Score += 5
var Names:[]string = array{}     # array
set Names += array{"Ana"}
var Points:[player]int = map{}   # map (key must be comparable)
Half:float = 0.5
Flag:logic = true
MaybeTarget:?agent = false       # option: false means "none"
```
- **int and float never mix implicitly.**
  - `1.0 * I` turns an int into a float.
  - `Floor[F]`, `Ceil[F]`, `Round[F]` and `Int[F]` turn a float into an int. They can fail (`<decides>`), so call them with `[]`.
- **`int / int` gives a `rational` and can fail** (division by zero): `if (Q := Floor(A / B))`. `Mod[A, B]` and `Quotient[A, B]` are failable too.
- `Round` uses banker's rounding: `Round[2.5] = 2`.
- Don't compare floats with `=`. Use a tolerance.
- **Maps:**
  - A missing key fails the read.
  - `set Map[K] = V` needs a failure context.
  - There is no delete. Rebuild the map with `for` to drop a key.
- **Arrays:** `Arr[I]` can fail. Tuples use `T(0)` and never fail.

## 4. Failure (the core idea)
- An expression either **succeeds with a value or fails**. Comparisons don't return a bool: they succeed or fail.
- **Failable expressions:**
  - comparisons, `not`, `and`, `or`
  - indexing (`Arr[0]`, `Map[K]`)
  - `X?` on an option
  - casts (`player[Agent]`, `my_class[Obj]`)
  - `<decides>` calls (`F[]`)
  - `set Map[K] = …`
- **Failure contexts:** `if (…)`, `for (…)` filters, `<decides>` bodies, `option{…}`, `logic{…}`.
- When an `if` condition fails, **every effect inside it rolls back.**
- Use `()` for calls that can't fail and `[]` for calls that can. Mixing them up is a compile error.
```verse
if (Player := player[Agent], Character := Agent.GetFortCharacter[]):
    Character.SetVulnerability(false)      # check the exact member in the digest
else:
    Print("MYGAME: not a player")

# Several conditions, one per line:
if:
    Player := player[Agent]
    Stats := StatsMap[Player]
    Stats.Score > 10
then:
    Print("MYGAME: high score")

IsHigh:logic = logic{Score > 100}          # turn failure into a logic value
FirstName:string = Names[0] or "nobody"    # fall back when the expression fails
```

## 5. Effect specifiers
| Specifier | Meaning |
|---|---|
| `<suspends>` | Async: it can wait (`Sleep`, `Await`, `race`). Callers must be `<suspends>`, or use `spawn`. **Can't be combined with `<decides>`.** |
| `<decides>` | The function can fail. Call it with `F[]` inside a failure context. **It must also have `<transacts>`, `<reads>` or `<computes>`.** |
| `<transacts>` | Reads, writes and allocates, and can be rolled back. Use it for helpers called inside `if` or `<decides>` code. |
| `<computes>` | Pure: no reading or writing of mutable state. |
| `<reads>` / `<writes>` / `<allocates>` | Finer-grained heap effects. |
| `<converges>` | Guaranteed to end. Native or signature only, so you won't write it. |
| `<no_rollback>` | Effects can't be undone, so the function can't be called in a failure context. Its deprecation is planned [?]. |

Facts:
- **The default effect is uncertain**, and the sources disagree on it. In practice, a plain function can't be called from an `if` condition, a `for` filter or a `<decides>` body. **Annotate helpers explicitly** (`<transacts>` or `<computes>`).
- Event `Signal`, `spawn` and `branch` bodies are no-rollback. Compute values into a variable first, then use them in the `if`.
- A function may do less than it declares, never more.
- At most one exclusive effect (`<computes>`, `<transacts>`, `<converges>`) per function.

```verse
# A failable helper:
IsAlive(Agent:agent)<transacts><decides>:void =
    Character := Agent.GetFortCharacter[]
    Character.IsActive[]               # check in the digest

# A pure helper (not called Clamp: that would shadow the built-in):
ClampScore(V:int, Lo:int, Hi:int)<computes>:int =
    if (V < Lo) then Lo else if (V > Hi) then Hi else V
```

## 6. Concurrency
| Expression | What it does |
|---|---|
| `sync:` | Runs every arm, waits for all of them and returns a tuple. Needs at least two async arms. |
| `race:` | Returns the first arm to finish and **cancels the rest**. Every arm must suspend. |
| `rush:` | Returns the first arm to finish. The others keep running. |
| `branch:` | Runs in the background and is cancelled when the enclosing function ends. |
| `spawn{F()}` | Starts an unstructured task that outlives its scope. It works from non-async code. `F` must be `<suspends>`. |
| `Sleep(S)` | `Sleep(0.0)` waits one tick. `Sleep(Inf)` waits until cancelled. |
| `X.Await()` | Waits for one event: a device event or `event(t)`. |

- `rush` and `branch` can't sit directly inside `loop` or `for`.
- Cancellation happens only at suspension points. `defer:` runs cleanup when a task is cancelled.
- Prefer events and `Await` over polling. Never write a `loop` without a suspension point in it: the server stops a task that runs too long [3P: roughly >9 s per resume].

```verse
# Wait for a button press, or give up after 10 s.
WaitForPress()<suspends>:?agent =
    race:
        block:
            A := StartButton.InteractedWithEvent.Await()
            option{A}
        block:
            Sleep(10.0)
            false

# A round timer that ends early if everyone leaves.
RunRound()<suspends>:void =
    race:
        Sleep(RoundSeconds)
        AwaitEveryoneLeft()   # your own <suspends> function

# Per-player work started from an event handler (not <suspends>):
OnPlayerAdded(Player:player):void =
    spawn{ WatchPlayer(Player) }
```

## 7. Classes, devices, events
```verse
using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/Diagnostics }

round_log := class(log_channel){}

round_manager_device := class(creative_device):
    Logger:log = log{Channel := round_log}

    @editable StartButton:button_device = button_device{}
    @editable RoundTimer:timer_device = timer_device{}
    @editable RoundSeconds:float = 60.0

    var Presses:int = 0

    OnBegin<override>()<suspends>:void =
        Logger.Print("MYGAME: round_manager started")
        StartButton.InteractedWithEvent.Subscribe(OnStartPressed)
        GetPlayspace().PlayerAddedEvent().Subscribe(OnPlayerAdded)

    OnStartPressed(Agent:agent):void =
        set Presses += 1
        RoundTimer.Start()

    OnPlayerAdded(Player:player):void =
        Logger.Print("MYGAME: player joined")
```
- A `creative_device` subclass appears in the Content Browser (under CreativeDevices) after a successful build. Drag it into the level, then **set every `@editable` in the Details panel**. An unset device reference does nothing, and nothing warns you.
- `Subscribe` returns a `cancelable`. Store it (`var Sub:?cancelable = false`) and call `Cancel()` when the work is done, so handlers don't pile up.
- `OnBegin` runs again each round, and device fields reset. Keep cross-round state in a `weak_map`.
- Class specifiers go after `class`: `foo := class<concrete>:`.
  - `<concrete>`: every field has a default. Needed for structs you edit in the Details panel.
  - `<unique>`: compared by identity, so it can be a map key.
  - `<final>`, `<abstract>`, `<persistable>`, `<castable>` (frozen after publish).
- Access specifiers: `<public>`, `<internal>` (the default), `<private>`, `<protected>`.
- Override a method with `Name<override>()`. Call the parent with `(super:)Name()`.

## 8. Agents, players, characters, teams
- `agent`: any player or AI. `player`: a human (`player[Agent]` casts and can fail). `fort_character`: the body in the world (`Agent.GetFortCharacter[]`).
- `GetPlayspace()`, called on a device, returns the `fort_playspace`:
  - `GetPlayers()`, `GetParticipants()`
  - `PlayerAddedEvent()`, `PlayerRemovedEvent()`: these are **function calls**, so subscribe with `PlayerAddedEvent().Subscribe(F)`
  - `GetTeamCollection()`
- Players can leave at any moment. A `player` reference can become invalid, so check it every time you use it. Handle `PlayerRemovedEvent()` and also cover join-in-progress (see the Gunfight feature example).

## 9. Server authority in Verse
- **All Verse runs on the server.** There is no client Verse: the Book lists `<predicts>` as unreleased. Clients see results through devices, replicated characters and per-player UI.
- What that gives you for free:
  - Money, scores, odds and RNG (`GetRandomInt`) can't be changed by a client.
  - Keep hidden values, such as odds tilts, in Verse fields. Don't put them into UI text or device settings that display them.
- What it costs:
  - Every input round-trips to the server. `input_trigger_device` latency can approach about 1 s on a bad connection.
  - Smooth motion should come from `prop_mover_device`, animations, or Scene Graph movement components, not from `TeleportTo` or `MoveTo` in a tight loop [3P].
  - Heavy loops cause server hitches for everyone. Use events and `Sleep`. Measure in a 2+ player session.
- Validate player "intent" anyway. If a button can only be used by the seated player or the right team, check it in the handler (`Agent` == expected). Devices can be triggered by anyone in range.
- [?] Seeded RNG: I found no public API for seeding Verse's random functions. If replays need determinism, write a small PRNG in Verse and log the seed.

## 10. UI (Verse widgets)
```verse
using { /UnrealEngine.com/Temporary/UI }
using { /Fortnite.com/UI }

    HelloText<localizes>:message = "Hello!"
    var Shown:[player]widget = map{}

    ShowHello(Agent:agent):void =
        if (Player := player[Agent], PlayerUI := GetPlayerUI[Player]):
            W:text_block = text_block{DefaultText := HelloText}
            PlayerUI.AddWidget(W)
            if (set Shown[Player] = W) {}

    HideHello(Player:player):void =
        if (PlayerUI := GetPlayerUI[Player], W := Shown[Player]):
            PlayerUI.RemoveWidget(W)
```
- UI is **per player**. Track each player's widgets in a map.
- Use `canvas` with `canvas_slot` for layout, and `stack_box` and `overlay` for groups.
- Clickable UI:
  - Show it with `PlayerUI.AddWidget(Canvas, player_ui_slot{InputMode := ui_input_mode.All})`. Remove it to give back control.
  - Handle clicks with `Button.OnClick().Subscribe(Handler)`, where the handler has the form `Handler(Message:widget_message):void` and reads `Message.Player`.
- Other options:
  - Simple text: HUD Message, Billboard and Popup Dialog devices.
  - Designed UI: UMG widgets with Verse fields (asset reflection; the MCP can bind them, see uefn-mcp.md section 4).
- Sources:
  - https://dev.epicgames.com/documentation/en-us/fortnite/creating-and-removing-widgets-in-unreal-editor-for-fortnite
  - https://dev.epicgames.com/documentation/en-us/fortnite/making-widgets-interactable-in-unreal-editor-for-fortnite

## 11. Persistence (`weak_map`)
Sources:
- https://dev.epicgames.com/documentation/en-us/fortnite/using-persistable-data-in-verse
- https://dev.epicgames.com/documentation/en-us/fortnite/persistent-player-statistics-in-unreal-editor-for-fortnite
- https://dev.epicgames.com/documentation/fortnite/verse-persistence-best-practices

```verse
# Module scope: outside any class.
player_save := class<final><persistable>:
    Version:int = 1
    Coins:int = 0
    BestTime:float = 0.0

MakePlayerSave<constructor>(Old:player_save)<transacts> := player_save:
    Version := Old.Version
    Coins := Old.Coins
    BestTime := Old.BestTime

var Saves:weak_map(player, player_save) = map{}

# Inside your device:
    EnsureSave(Player:player):void =
        if (not Saves[Player]):
            if (set Saves[Player] = player_save{}) {}

    AddCoins(Agent:agent, Amount:int):void =
        if:
            Player := player[Agent]
            Old := Saves[Player]
            set Saves[Player] = player_save:
                MakePlayerSave<constructor>(Old)
                Coins := Old.Coins + Amount
```
Limits [Epic, persistence page]:
- **256 KB per player per weak_map record.** Check growing data with `FitsInPlayerMap`.
- **At most 4 player-keyed `weak_map`s per island.** At least one must hold a class.
- An older page says 128 KB and 2 maps. Trust the persistence page.

Persistable types:
- `int`, `float`, `logic`, `string`, `char`, `color`, the vectors
- arrays, maps, options and tuples of those
- `<persistable>` enums and structs
- `class<final><persistable>`: no superclass, not `<unique>`, **no `var` fields**

**After the first publish:**
- Structs and simple types can't change.
- A class may only gain new fields that have defaults.
- A player whose data fails to load can't join.
- Rolling back to an older version in the Creator Portal can wipe saved data.

So use one versioned class from day one. Add fields; never rename or retype them. Write at checkpoints, not every tick.

Testing: Island Settings → Persistence Behavior (Edit Session / Playtest Session):
- **Simulate New User** tests the first-time experience.
- **Import From Live** tests returning players.
- Edit-session data resets when you relaunch.
- Playtest data resets only with a new playtest link code.

## 12. Logging and debugging
```verse
my_log := class(log_channel){}
# in a class:  Logger:log = log{Channel := my_log}
#              Logger.Print("MYGAME: state={State}")
Print("MYGAME: shows on screen and in the log")
```
- Output goes to the **editor** log under `LogVerse`. Read it with `LogsToolset.GetLogEntries(category="LogVerse", pattern="MYGAME")`. The file is `%LOCALAPPDATA%\UnrealEditorFortnite\Saved\Logs\UnrealEditorFortnite.log`.
- A running session keeps old code until you push (`PushChanges` / Push Verse Changes). Print a version tag in `OnBegin` and check it after every push.
- Effects in a failed `if` roll back, so a `Print` inside one may never show.

## 13. Common pitfalls (check before you build)
1. A failable call without a failure context, or `()` and `[]` mixed up.
2. An unannotated helper called inside `if`, `for` or a `<decides>` body (error 3512). Annotate it `<transacts>` or `<computes>`, or hoist the call.
3. `<suspends>` missing on a function that calls `Sleep` or `Await`, or `<suspends>` combined with `<decides>`.
4. A `race` or `sync` arm that doesn't suspend.
5. A busy `loop` without `Sleep` or `Await`.
6. Subscriptions never cancelled, or made twice after a round restart.
7. An `@editable` left unset in the Details panel.
8. Forgetting to build, or testing a session that still runs old code.
9. Stale digests or language-server errors: rebuild, restart UEFN, and if needed clear `Saved/VerseProject`.
10. int/float mixing, integer division, exact float comparison.
11. Shadowed names.
12. Breaking a published persistable type.
13. Deleting `.verse` files on disk while UEFN is open. Use the Verse Explorer or `VerseToolset.Delete`.
14. Using an API from a newer UEFN version than the user's. Check the digest header, or `vz-creates/uefn` for version diffs.
