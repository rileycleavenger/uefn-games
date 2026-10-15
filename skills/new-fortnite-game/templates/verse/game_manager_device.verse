# One Verse device owns the round flow; Fortnite devices do the gameplay pieces.
# Place it in the level, then set EVERY @editable in the Details panel (or bind them through the MCP).
# Template from the new-fortnite-game skill: not compiled by the skill author. Build it (BuildAll), read the
# diagnostics, and check every device member against your project's Fortnite.digest.verse.

using { /Fortnite.com/Devices }
using { /Fortnite.com/UI }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/UI }
using { /UnrealEngine.com/Temporary/Diagnostics }

game_log := class(log_channel){}

ScoreText<localizes>(Score:int):message = "Score: {Score}"

game_manager_device := class(creative_device):
    Logger:log = log{Channel := game_log}

    @editable StartButton:button_device = button_device{}     # starts a round
    @editable ActionButton:button_device = button_device{}    # the scoring action (stand-in for your real mechanic)
    @editable RoundTimer:timer_device = timer_device{}
    @editable EndGame:end_game_device = end_game_device{}

    var RoundActive:logic = false
    var Scores:[player]int = map{}
    var Streaks:[player]int = map{}
    var ScoreWidgets:[player]text_block = map{}

    OnBegin<override>()<suspends>:void =
        # Bump the build number after every push and check this line in LogVerse before trusting a test.
        Logger.Print("MYGAME: game_manager build 1 started")
        GetPlayspace().PlayerRemovedEvent().Subscribe(OnPlayerRemoved)
        ActionButton.InteractedWithEvent.Subscribe(OnAction)
        loop:
            StartButton.InteractedWithEvent.Await()
            RunRound()

    RunRound()<suspends>:void =
        set Scores = map{}
        set Streaks = map{}
        set RoundActive = true
        Logger.Print("MYGAME: round start")
        RoundTimer.SetActiveDuration(RoundSeconds)
        RoundTimer.Start()
        race:
            RoundTimer.SuccessEvent.Await()
            RoundTimer.FailureEvent.Await()
            Sleep(RoundSeconds + 10.0)   # safety net if the timer is misconfigured
        set RoundActive = false
        for (Player -> Score : Scores):
            RecordRound(Player, Score)
        Logger.Print("MYGAME: round end")

    # Runs on the server for whoever pressed. Validate here: the device can't tell who "should" press it.
    OnAction(Agent:agent):void =
        if (RoundActive?, Player := player[Agent]):
            Streak := Streaks[Player] or 0
            NewScore := (Scores[Player] or 0) + PointsForAction(Streak)
            if (set Scores[Player] = NewScore, set Streaks[Player] = Streak + 1) {}
            ShowScore(Player, NewScore)
            Logger.Print("MYGAME: action score={NewScore}")
            if (IsWinningScore[NewScore]):
                EndGame.Activate(Agent)

    # Per-player UI: each player sees only their own widget.
    ShowScore(Player:player, Score:int):void =
        if (Existing := ScoreWidgets[Player]):
            Existing.SetText(ScoreText(Score))
        else if (PlayerUI := GetPlayerUI[Player]):
            NewWidget := text_block{DefaultText := ScoreText(Score)}
            PlayerUI.AddWidget(NewWidget)
            if (set ScoreWidgets[Player] = NewWidget) {}

    # Players can leave at any time: drop their round state (maps have no delete, so rebuild them).
    OnPlayerRemoved(Leaver:player):void =
        var KeptScores:[player]int = map{}
        for (Player -> Score : Scores, Player <> Leaver):
            if (set KeptScores[Player] = Score) {}
        set Scores = KeptScores
        var KeptWidgets:[player]text_block = map{}
        for (Player -> Widget : ScoreWidgets, Player <> Leaver):
            if (set KeptWidgets[Player] = Widget) {}
        set ScoreWidgets = KeptWidgets
