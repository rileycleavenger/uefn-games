# Pure game rules. No devices, players, Sleep or Print here, so selftest_device can check every function
# with known inputs. Numbers come from tuning.verse (generated), never literals in this file.
# Template from the new-fortnite-game skill: not compiled by the skill author. Build it (BuildAll) and fix
# anything the diagnostics flag against your project's digests.

# Points for one scoring action, given how many the player already scored this round.
PointsForAction(Streak:int)<computes>:int =
    Capped := if (Streak > MaxStreakBonus) then MaxStreakBonus else Streak
    BasePoints + Capped * StreakBonus

# Succeeds when Score has reached the win line. Call it with brackets: IsWinningScore[Score]
IsWinningScore(Score:int)<computes><decides>:void =
    Score >= ScoreToWin
