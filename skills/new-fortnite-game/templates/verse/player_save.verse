# Persistent player data (module scope). Read the persistence rules in the skill's verse-cheatsheet.md section 11
# BEFORE the first publish: after that you may only ADD fields with defaults to player_save. Never rename,
# retype or remove a field, and never change this into a struct.
# Limits: 256 KB per player per weak_map; at most 4 player-keyed weak_maps per island.
# Template from the new-fortnite-game skill: not compiled by the skill author. Build it and fix what BuildAll reports.

using { /Verse.org/Simulation }

player_save := class<final><persistable>:
    Version:int = 1
    BestScore:int = 0
    RoundsPlayed:int = 0

# Copies every field; list new fields here when you add them.
MakePlayerSave<constructor>(Old:player_save)<transacts> := player_save:
    Version := Old.Version
    BestScore := Old.BestScore
    RoundsPlayed := Old.RoundsPlayed

var PlayerSaves:weak_map(player, player_save) = map{}

GetPlayerSave(Player:player):player_save =
    if (Save := PlayerSaves[Player]) then Save else player_save{}

# Write at checkpoints (round end), not every tick: each write serialises the whole record.
RecordRound(Player:player, Score:int):void =
    Old := GetPlayerSave(Player)
    NewBest := if (Score > Old.BestScore) then Score else Old.BestScore
    Updated := player_save:
        MakePlayerSave<constructor>(Old)
        BestScore := NewBest
        RoundsPlayed := Old.RoundsPlayed + 1
    if (set PlayerSaves[Player] = Updated) {}
