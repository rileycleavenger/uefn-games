# Publishing, rules, money and analytics

Researched 2026-10-14. The current UEFN is about v42.30 (Oct 1, 2026).

The official Developer Rules page (https://legal.epicgames.com/fortnite/developer-rules, updated Apr 29, 2026) sits behind an Epic login. **Rule wording below comes from secondary quotes. Have the human read the current rules before the first release.**

## 1. Content rules to check at the pitch, not at the end
- **No gambling or casino-style games, even with fake money.**
  - As quoted by Insider Gaming (Nov 11, 2025: https://insider-gaming.com/fortnite-gambling-evidence/), rule **1.11** says developers may not "implement gambling content, raffles, or casino-style games", which are "prohibited whether or not they involve real money or virtual currency".
  - Rule **1.15.5** bans content that would "teach or prominently feature images or activities that are typically associated with real-world gambling".
  - In practice: no slot machines, roulette, blackjack, poker-for-chips, betting, raffles or chip imagery.
  - Prize wheels can't be tied to paid items (4.4.15). Paid random items need displayed odds.
  - **A casino game such as Casino Royale is very likely not publishable as a Fortnite island.** Check this before writing a GDD.
- **IP (1.7 / 1.7.1):**
  - You must own or license everything, in the island and in its metadata.
  - Use Epic assets only as UEFN provides them. No recreated Fortnite skins, characters or music.
  - Third-party brands that appear in Fortnite still need your own licence.
  - **Use parody names and original designs only.** No real brands, logos, venues or people.
- **Age rating ceiling:** ESRB Teen, PEGI 16, USK 16, IARC 16+. Anything above Fortnite's maximum rating isn't allowed. No gore.
- **Thumbnails and metadata:**
  - They must show real gameplay from the island.
  - No "AFK / XP / coin farm" claims, no V-Bucks or real-currency imagery, and no real people or Epic logos.
  - No guns pointed at the viewer.
  - General-audience rules also ban references to gambling.
  - No impersonating other creators or brands. No advertising Support-a-Creator codes.
  - Minimum 1920×1080, 16:9, at most 5 MB.
  - Source: https://dev.epicgames.com/documentation/fortnite/thumbnail-image-policies
- **AI NPC personas (Conversations, rule 1.22):**
  - No medical or mental-health personas, no romantic or companion personas.
  - Don't claim the voices are recorded.
  - The feature is Experimental, so it can't be published until it reaches Beta.
- **Consequences:** a failed release, a locked project (the whole team loses access), a disabled island (analytics and payouts lost), or action against the account.

## 2. Who can publish
Source: https://dev.epicgames.com/documentation/fortnite/fortnite-developer-program
- You must be **18 or older**, and enrolled in the **Fortnite Developer Program**:
  - A real-money Epic purchase in the last 365 days (gift cards don't count), or at least $20 spent in Fortnite.
  - A tax interview (W-9 or W-8).
  - An activated **Hyperwallet** account. Verification can take up to 5 business days.
- **Start enrolment in week 1.** It is the slowest manual step and only the human can do it.

## 3. Release steps
In UEFN:
1. Save everything. Commit. Run the pre-publish checklist (section 7).
2. Launch Session, then End Game, so assets are cooked.
3. Run Project → **Launch Memory Calculation**. It must be under budget.
4. Project → **Publish Project** creates a **private version**. The MCP has no publish tool: the human clicks this.
   - Source: https://dev.epicgames.com/documentation/en-us/fortnite/publishing-projects-in-unreal-editor-for-fortnite

In the Creator Portal (https://create.fortnite.com), as the human:
1. Optional: run a playtest with the private version (Playtests → Create Playtest, up to 50 adult playtesters).
2. Projects → island → Private Versions → **Create release**. Validation runs.
3. Fill in, in order:
   1. **Game Details**: title, description, tags, player counts.
   2. **Rating**: the IARC questionnaire. Retake it whenever content changes the answers, and declare digital purchases if you sell anything.
   3. **In-Island Transactions**.
   4. **Promotional Media**: landscape and portrait thumbnails plus a logo. Trailer, gameplay video, screenshots and lobby background are optional.
   5. **Attribution**: every third-party asset, matching `docs/CREDITS.md`.
   6. **Visibility**: Listed, Unlisted (code only) or scheduled.
4. **Submit for review.**
   - Moderation has two stages: a metadata and asset pre-check, then an in-island review.
   - Epic publishes no review time. Plan for days, not hours [?].
   - A failed release leaves the live version untouched.
   - Islands that use **Experimental** features can't be released.
   - Sources:
     - https://dev.epicgames.com/documentation/en-us/fortnite/publishing-from-the-creator-portal-in-fortnite-creative
     - https://dev.epicgames.com/documentation/en-us/fortnite/island-moderation-tips-and-faqs-in-fortnite-creative

Island settings that matter for matchmaking:
- Max Players: 1–100, default 16.
- Matchmaking Max Players Per Session: default 32.
- Minimum Players: default 8.
- Join in progress.
- Source: https://dev.epicgames.com/documentation/en-us/fortnite/island-settings-in-unreal-editor-for-fortnite

Through MCP, island settings are properties on `IslandSettings_0` (see uefn-mcp.md section 7). Change them in small steps and capture before/after values.

## 4. Money
**Engagement Payouts.** Source: https://dev.epicgames.com/documentation/en-us/fortnite/engagement-payout-in-fortnite-creative
- 40% of eligible net Fortnite real-money revenue goes into a pool.
- The pool is shared by engagement: active playtime, retention, playtime near V-Bucks spending, and bringing in new or lapsed players. Payment comes about 30 days after month end.
- Accolades (XP) devices help players progress. Use them honestly: "XP farm" islands break the metadata rules.

**In-island transactions** (live since Jan 9, 2026). Source: https://dev.epicgames.com/documentation/en-us/fortnite/in-island-transactions-overview-in-fortnite
- Entitlements are Durable, Consumable or Paid Area, priced 50–5,000 V-Bucks in steps of 50.
- Revenue share: 100% of the V-Bucks value (about 74% of spend) until Jan 31, 2027, then 50%.
- Purchases are final and bound to the island. Stop selling at least 20 days before you unpublish.
- The Verse API moved to `/UnrealEngine.com/Marketplace` in v42.20; the old paths are aliases.
- Paid random items:
  - Need displayed odds and are restricted in several countries.
  - Use `RestrictPaidRandomItems`, `RestrictDirectPromptsToPurchase` and `GetMinPurchaseAge`.
  - No paid prize-wheel spins or luck boosts (4.4.15).
  - Source: https://dev.epicgames.com/documentation/en-us/fortnite/guidelines-for-in-island-monetization-in-fortnite
- **Ship the free game first.** Add transactions only after D1 retention is healthy, and redo the IARC rating when you do.

## 5. Analytics and iteration
- **Creator Portal → Project Analytics** (https://dev.epicgames.com/documentation/fortnite/project-analytics-for-fortnite-games):
  - The impressions → clicks → plays funnel (CTR)
  - Session length, bounce at 2, 5 and 10 minutes, queue time
  - Active players, new vs returning
  - **D1/D7 retention**
  - Post-game surveys
  - **Benchmarks** (v42.30): percentiles against top islands in your genre
- **Analytics device** (https://dev.epicgames.com/documentation/fortnite/using-analytics-devices-in-fortnite-creative):
  - Counts player-driven events and uploads daily to the Analytics Device Dashboard.
  - Give each event a numbered name (`03_Stage3_Reached`).
  - The limit is 50 per island on one page and 100 on another [?]. Each one costs memory.
- **Fortnite Data API** (https://dev.epicgames.com/documentation/en-us/fortnite/using-fortnite-data-api-in-fortnite): public metrics for listed islands (plays, peak CCU, D1/D7) in 10-minute, hourly or daily buckets, going back 7 days. Use it to compare with similar islands.
- **What to change:**

  | Symptom | Change |
  |---|---|
  | Low CTR | A/B test thumbnails (the Creator Portal supports it) |
  | High bounce at 2–5 minutes | Fix the first minute: spawn → first fun action in under 30 s, clear goal on screen |
  | D1/D7 below benchmark | Add a reason to come back: progression (`weak_map` persistence), daily goals, unlocks |
  | Short sessions | Shorter rounds, faster requeue, a visible next goal |

- **Iteration loop:**
  1. Write the hypothesis in `docs/NEXT_STEPS.md`.
  2. Make one change.
  3. Ship a new version.
  4. Wait at least 3–7 days.
  5. Compare with the benchmark.
  6. Keep the change or roll it back.
  - Only one experiment at a time, the same rule as "one system per task".
- **Persistence and versions:** activating an older version in the Creator Portal can wipe persistent data. Never roll back an island with saved data without the human's explicit OK.

## 6. Version control (Lore, formerly Unreal Revision Control)
- UEFN's built-in version control was renamed **Lore** in v42.00. It is on by default for new projects and hosted by Epic.
  - Check out (lock), Sync Latest, Check-in Changes, per-asset history. A VS Code extension shows Verse snapshot history.
  - Sources:
    - https://dev.epicgames.com/documentation/fortnite/lore-version-control-in-unreal-editor-for-fortnite
    - https://dev.epicgames.com/documentation/fortnite/lore-version-control-best-practices-in-unreal-editor-for-fortnite
- Epic: "Do not enable multiple version control methods outside of Lore." Lore doesn't track source files such as `.blend` or `.psd`.
- Lore was open-sourced under MIT (https://github.com/EpicGames/lore, pre-1.0). The UEFN build still uses a proprietary format, so open-source tools can't read it yet.
- Recommended setup:
  - **Team project: keep Lore on** for the UEFN project. Keep a **Git repo outside the UEFN project folder** for `docs/`, `tools/`, Blender scripts, the sim and art sources. The reviewer reads Verse from the project folder and diffs it against Lore history or a copied snapshot.
  - **Solo project, the Casino Royale style** [inference, not documented by Epic]:
    - Turn Lore off for the project (allowed for personal projects).
    - Put the whole project folder in **Git + LFS with file locking**: `*.uasset`, `*.umap`, `*.glb`, `*.fbx`, `*.png`, `*.wav` and similar are lockable LFS files.
    - Ignore `Saved/`, `Intermediate/`, `DerivedDataCache/` and `.urc/`.
    - **Never run both.**
    - Lock a binary file (`git lfs lock`) before editing it in UEFN: an editor save on a read-only file can fail silently.
  - Either way: keep the project out of OneDrive or other cloud-synced folders (forum reports of broken projects). Commit before every batch of MCP edits.

## 7. Pre-publish checklist (the reviewer runs this too)
1. Build clean. Self-test passes with the full step count. `RunSelfTest = false`.
2. No `zz_` scratch objects, debug prints or test-only devices. Island Settings → Test Players on Start = None.
3. Memory calculation is under budget. Record the number.
4. `docs/CREDITS.md` is complete and matches the Creator Portal Attribution step.
5. Content rules (section 1) are re-read against the current island: no gambling, no real brands, no recreated Fortnite IP, thumbnails show real gameplay.
6. Persistence: tested with **Simulate New User** and **Import From Live**. No breaking change to a published `<persistable>` type.
7. A 2+ real-client playtest of the full loop: join, play, leave, rejoin, round restart, end.
8. Other platforms checked (Connect To Platform), or listed as not checked.
9. The IARC questionnaire answers are still true.
10. The human has read the current Developer Rules and approves the release.
