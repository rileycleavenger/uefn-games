# Self-test for the pure rules (rules.verse + tuning.verse). Place one in the level, set RunSelfTest = true
# for test sessions, and read LogVerse for "MYGAME SELFTEST". MUST be false before any private version/publish.
# This proves rules, not input: a human still presses the real buttons.
# Template from the new-fortnite-game skill: not compiled by the skill author. Build it and fix what BuildAll reports.

using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /Verse.org/Random }
using { /UnrealEngine.com/Temporary/Diagnostics }

selftest_log := class(log_channel){}

selftest_device := class(creative_device):
    Logger:log = log{Channel := selftest_log}

    @editable RunSelfTest:logic = false

    # Update when you add or remove checks: the reviewer compares it with passed + failed.
    ExpectedSteps:int = 4

    var Passed:int = 0
    var Failed:int = 0

    OnBegin<override>()<suspends>:void =
        if (RunSelfTest?):
            RunId := GetRandomInt(1000, 9999)
            Logger.Print("MYGAME SELFTEST START run={RunId}")
            ExpectInt("points_no_streak", PointsForAction(0), BasePoints)
            ExpectInt("points_streak_capped", PointsForAction(MaxStreakBonus + 5), BasePoints + MaxStreakBonus * StreakBonus)
            ExpectTrue("win_at_line", logic{IsWinningScore[ScoreToWin]})
            ExpectTrue("no_win_below_line", logic{not IsWinningScore[ScoreToWin - 1]})
            Logger.Print("MYGAME SELFTEST DONE run={RunId} passed={Passed} failed={Failed} expected={ExpectedSteps}")

    ExpectInt(Name:string, Got:int, Want:int):void =
        if (Got = Want):
            set Passed += 1
            Logger.Print("MYGAME SELFTEST PASS {Name}")
        else:
            set Failed += 1
            Logger.Print("MYGAME SELFTEST FAIL {Name} expected={Want} got={Got}")

    ExpectTrue(Name:string, Value:logic):void =
        if (Value?):
            set Passed += 1
            Logger.Print("MYGAME SELFTEST PASS {Name}")
        else:
            set Failed += 1
            Logger.Print("MYGAME SELFTEST FAIL {Name}")
