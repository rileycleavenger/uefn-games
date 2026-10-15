# Devices and bindings

In-editor device settings and event bindings never show up in a Verse diff, so they are recorded here. Update this file in the same commit as the change. The reviewer checks it.

## Placed devices
| Outliner name | Device | Key settings (non-default) | Used by (Verse field or binding) |
|---|---|---|---|
| `GameManager` | game_manager_device (Verse) | — | — |
| `StartButton` | Button | Interact text "Start round" | `GameManager.StartButton` |
| `RoundTimer` | Timer | Duration set from Verse | `GameManager.RoundTimer` |

## Event bindings made in the editor (no Verse)
| From device → event | To device → function | Why |
|---|---|---|
| | | |

## Island Settings (non-default)
| Setting | Value | Why |
|---|---|---|
| Max Players | | |
| Test Players on Start | None (Fill only while testing) | |
| Persistence Behavior: Edit / Playtest Session | | |
