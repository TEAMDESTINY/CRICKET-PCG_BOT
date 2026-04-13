# ========== TEAM MODE MESSAGES ==========

# Host & Team Creation Messages
CREATE_TEAM_SUCCESS = """
🎮 **{host_name} is now the game host!**

Game host can create teams now by using /add_A and /add_B.
Let's get the match started! 😍❤️
"""

ALREADY_HOST_EXISTS = """
❌ A game is already active in this chat!
Host: {host_name}
Use /end_match to end the current game first.
"""

NO_ACTIVE_GAME = """
❌ No active game found in this chat!
Use /create_team to start a new game.
"""

HOST_ONLY_COMMAND = """
❌ Only the game host can use this command!
Host: {host_name}
"""

# Team Addition Messages
TEAM_ADD_SUCCESS = """
✅ Added {player_name} to Team {team}

━━━━━━━━━━━━━━━━━━
🏏 TEAM {team} ({current_count}/{max_players} players)
{player_list}
━━━━━━━━━━━━━━━━━━

Use /add_{team} to add more players
Use /startgame when teams are ready
"""

TEAM_ADD_REPORT = """
📋 Team {team} Addition Report
📅 {date}

✅ Success: {success_count}
⚠️ Issues: {issue_count}

📊 Detailed Results:
{results}
"""

TEAM_FULL = """
❌ Team {team} is full! ({max_players}/{max_players} players)
Use /remove_{team} to remove players if needed.
"""

PLAYER_ALREADY_IN_TEAM = """
⚠️ {player_name} is already in Team {team}!
"""

PLAYER_ALREADY_IN_OTHER_TEAM = """
⚠️ {player_name} is already in Team {other_team}!
Remove from there first or use different player.
"""

PLAYER_NOT_FOUND = """
❌ User {player_name} not found on Telegram!
Make sure the username is correct.
"""

# Team Removal Messages
TEAM_REMOVE_SUCCESS = """
✅ Removed {player_name} from Team {team}

━━━━━━━━━━━━━━━━━━
🏏 TEAM {team} ({current_count}/{max_players} players)
{player_list}
━━━━━━━━━━━━━━━━━━
"""

TEAM_REMOVE_REPORT = """
📋 Team {team} Removal Report
📅 {date}

✅ Success: {success_count}
⚠️ Issues: {issue_count}

📊 Detailed Results:
{results}
"""

PLAYER_NOT_IN_TEAM = """
❌ Player number {player_num} not found in Team {team}!
"""

INVALID_PLAYER_NUMBER = """
❌ Invalid player number! Please use number between 1 and {max_players}.
"""

# Team Display Messages
TEAM_DISPLAY = """
👽 Game Host: {host_name}

🏏 Batting: Team {batting_team} (Innings {innings})
🎯 Bowling: Team {bowling_team}

🎩 Team A: {team_a_name}
👒 Team B: {team_b_name}

🔵 Team A
{team_a_players}

🔴 Team B
{team_b_players}
"""

TEAM_NOT_READY = """
❌ Teams are not ready to start!

Team A: {team_a_count}/{required_players} players
Team B: {team_b_count}/{required_players} players

Both teams need {required_players} players to start the match.
"""

# Toss Messages
TOSS_ANNOUNCEMENT = """
🎲 **TOSS TIME!**

{host_name} is tossing the coin...

🏏 **{toss_winner_name} won the toss!**

Choose to bat or bowl first:
"""

TOSS_DECISION_MADE = """
🏏 {winner_name} from Team {winner_team} chose to {decision} first.

Team {bowling_team} will {bowl_first} first.

🏏 Batting: Team {batting_team}
🧤 Bowling: Team {bowling_team}
"""

TOSS_AUTO = """
🎲 **AUTO TOSS**

🏏 **Team {winner_team} won the toss!**

Team {bowling_team} will bowl first! 🎉

🏏 Batting: Team {batting_team}
🧤 Bowling: Team {bowling_team}
"""

# Match Start Messages
MATCH_START_ANNOUNCEMENT = """
OHOO!🎉 Let's play a {overs} overs Match !!

Team {bowling_team} will bowl first! 🎉

Now, type /bowling to choose the bowling member! 📝
"""

GAME_ALREADY_STARTED = """
❌ Game has already started!
Current status: {status}
"""

# Player Selection Messages
BOWLER_SELECTED = """
✅ Bowler: {bowler_name} from Team {team_name} will bowl now!

Now, type /batting to choose the batting member! 🏏
"""

BATSMAN_SELECTED = """
✅ Batsman: {batsman_name} from Team {team_name} is ready to bat!

Now choose the second /batting player!
"""

SECOND_BATSMAN_SELECTED = """
✅ {batsman_name}, now you're 2nd batter!

Get ready, the game is starting in 10 seconds! ⏰
"""

INVALID_BATSMAN = """
❌ Invalid batsman selection!
Player number {player_num} is either out or not available.
Choose a player who is not out yet.
"""

INVALID_BOWLER = """
❌ Invalid bowler selection!
Player number {player_num} is not available or already bowled this over.
Choose a different bowler.
"""

SAME_BATSMAN_ERROR = """
❌ Cannot select the same batsman again!
{player_name} is already batting.
"""

# Game Play Messages
BATTING_PROMPT = """
🏏 **Now Batter:** {batter_name} can send number (0-6)!!

📊 **Ratings:** ND BAT | MENTAL 66 | PACE 63 | PHYSICAL 66
⚡ **Over Balls:** {ball_number}/6
📈 **Score:** {score}/{wickets} ({overs} ov)
"""

BOWLING_DM_PROMPT = """
🏏 **CRICKET GAME - BOWLING**

**Match:** {team_a} vs {team_b}
**Batsman:** {batsman_name} ({batsman_team})
**Bowler:** {bowler_name} ({bowler_team})

📊 **Score:** {score}/{wickets} ({overs}.{balls} overs)
{f"🎯 **Target:** {target} runs" if target else ""}

━━━━━━━━━━━━━━━━━━
**Send your bowling number (1-6):**

⏰ You have {timer} seconds
"""

# Ball Result Messages
BALL_RESULT_RUN = """
🏏 **{runs} RUN{'S' if runs > 1 else ''}!**

🏏 Batter: {batter_num} | 🎯 Bowler: {bowler_num}
📈 **Score:** {score}/{wickets} ({overs}.{balls} ov)
⚡ **Strike Rate:** {csr}
⏱️ {response_time}ms
"""

BALL_RESULT_SIX = """
🎯 **SIX!** 🚀

🏏 Batter: {batter_num} | 🎯 Bowler: {bowler_num}
📈 **Score:** {score}/{wickets} ({overs}.{balls} ov)
⚡ **Strike Rate:** {csr}
⏱️ {response_time}ms
"""

BALL_RESULT_FOUR = """
🎯 **FOUR!** 💥

🏏 Batter: {batter_num} | 🎯 Bowler: {bowler_num}
📈 **Score:** {score}/{wickets} ({overs}.{balls} ov)
⚡ **Strike Rate:** {csr}
⏱️ {response_time}ms
"""

BALL_RESULT_WICKET = """
🎯 **WICKET!** 🎯

🏏 Batter: {batter_num} | 🎯 Bowler: {bowler_num}
📈 **Score:** {score}/{wickets} ({overs}.{balls} ov)
⏱️ {response_time}ms
"""

# OUT Messages
OUT_ANNOUNCEMENT = """
🎯 Number matches, {batter_name} is out! 🎯
"""

WALKING_BACK = """
{batter_name} is walking back to the pavilion 🏃‍♂️👋
"""

OUT_COMPLETE = """
Out! Please choose the next batsman by command /batting.
"""

NEW_BATSMAN_ANNOUNCEMENT = """
🔄 **New Batsman Coming!**

👋 Hey {new_batsman}, now you're batter!
🆕 **New batsman:** {new_batsman}

🏀 Get ready for the next ball!
"""

# Over Complete Messages
OVER_COMPLETE = """
Over! Hey {host_name}, Please choose the next bowler by command /bowling.
"""

NEW_BOWLER_ANNOUNCEMENT = """
🔄 **New Bowler!**

👋 Hey {new_bowler}, now you're bowling!

Choose your bowling speed and send number in DM.
"""

# Innings Break Messages
INNINGS_BREAK = """
━━━━━━━━━━━━━━━━━━
🏏 **END OF INNING {innings}** 🏏

{batting_team} scored {score}/{wickets} in {overs} overs
(CRR: {crr})

{target_message}
━━━━━━━━━━━━━━━━━━

Team {bowling_team} needs {runs_needed} runs in {overs_left} overs to win.

Get ready for the second innings!
"""

INNINGS_BREAK_TARGET = """
🎯 **Target:** {target} runs for Team {batting_team} to win.
"""

# Match End Messages
MATCH_END = """
━━━━━━━━━━━━━━━━━━
🏆 **MATCH ENDED** 🏆

{winner_team} won the match by {margin}!

📊 **Final Score:**
Team A: {team_a_score}/{team_a_wickets} ({team_a_overs} ov)
Team B: {team_b_score}/{team_b_wickets} ({team_b_overs} ov)

🏏 **Man of the Match:** {mom_name} ({mom_runs}({mom_balls}) • {mom_wickets} wickets)

👑 Host: {host_name}
━━━━━━━━━━━━━━━━━━

Use /create_team to start a new match!
"""

MATCH_END_TIE = """
━━━━━━━━━━━━━━━━━━
🤝 **MATCH TIED!** 🤝

Both teams scored {score} runs!

👑 Host: {host_name}
━━━━━━━━━━━━━━━━━━

Use /create_team to start a new match!
"""

# Swap Messages
SWAP_SUCCESS = """
🔄 **POSITIONS SWAPPED!**

Now batting: Team {batting_team}
Now bowling: Team {bowling_team}

Continue the game!
"""

SWAP_NOT_ALLOWED = """
❌ Cannot swap teams now!
Game is in {status} phase.
Use /swap only during active gameplay.
"""

# End Match Messages
END_MATCH_CONFIRM = """
⚠️ **Are you sure you want to end the current match?**

Type /end_match_confirm to end the game.
Type /cancel to cancel.
"""

END_MATCH_SUCCESS = """
✅ Match ended by host!

Use /create_team to start a new match.
"""

END_MATCH_CANCELLED = """
✅ Match end cancelled. Continue playing!
"""

# Error Messages
GAME_NOT_FOUND = """
❌ No game is going on in this chat! 😂😂

Use /create_team to start a new game.
"""

COMMAND_NOT_AVAILABLE = """
❌ This command is not available right now.

Current game status: {status}
"""

WAIT_FOR_TURN = """
⏳ Please wait! {player_name} is already playing this ball.
"""

INVALID_NUMBER = """
❌ Invalid number! Please send a number between 1 and 6.
"""

TIMEOUT_BOWLER = """
⏰ **No message received from bowler {bowler_name}, deducting 6 runs!**

❌ Seems Bowling player is not responding, User Eliminated from the game!!
"""

TIMEOUT_BATTER = """
⏰ **No message received from batter {batter_name}!**

❌ Batter is OUT by default!
"""

# Feedback Messages
FEEDBACK_RECEIVED = """
✅ Thank you for your feedback!

Your message has been sent to the developers.
"""

FEEDBACK_FORWARD = """
📝 **New Feedback from @{username}**

{feedback}
"""
