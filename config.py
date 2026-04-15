import os
from dotenv import load_dotenv

load_dotenv()

# ========== MONGODB ==========
MONGO_URI = "mongodb+srv://sparshshivare2606:sparshs2607@cluster0.cvditmt.mongodb.net/?appName=Cluster0"
DB_NAME = "cricket_bot"
BOT_USERNAME = "testingpcgbot"

# ========== OWNER / DEVELOPER LINK ==========
OWNER_LINK = "https://t.me/oye_sparsh"

# ========== BOT TOKEN ==========
BOT_TOKEN = "8628663860:AAEAND6Ng7jZhoLd0nQLsukVqWVbpZ4UuRM"

# ========== OWNER ID - ADD THIS LINE ==========
OWNER_ID = 6572893382

# ========== OWNER / DEVELOPER LINK ==========
OWNER_LINK = "https://t.me/oye_sparsh"

# ========== GAME INSTRUCTIONS IMAGE ==========
GAME_INSTRUCTIONS_IMAGE_URL = "https://files.catbox.moe/iq4758.jpg"

# ========== ADMIN IDs ==========
ADMIN_IDS = [6572893382]

# ========== TEAM MODE VIDEOS ==========
TEAM_START_VIDEO_URL = "https://files.catbox.moe/yld4p8.mp4"
TEAM_ADD_VIDEO_URL = "https://graph.org/file/871e94f8f49ae663b1d23-529b03dd09d1b4c4b7.mp4"
TEAM_REMOVE_VIDEO_URL = "https://graph.org/file/1bbab31bb595c4c074420-19e090953fc5fa9c6c.mp4"
TEAM_STARTGAME_VIDEO_URL = "https://graph.org/file/f5a26d8b50d39c393e7d1-8d0bf1bc4ed772cb2a.mp4"
TEAM_BOWLING_VIDEO_URL = "https://graph.org/file/3680f9d14543771855ee0-1ff9d9b2aeabefedb2.mp4"
TEAM_BATTING_VIDEO_URL = "https://graph.org/file/088a969e3ba0815255edc-d60caf55c97b8b1615.mp4"
MEMBERS_LIST_IMAGE_URL = "https://files.catbox.moe/zovpa4.jpg"
SOLO_GAME_START_IMAGE = "https://files.catbox.moe/zovpa4.jpg"
BOWLING_DM_IMAGE_URL = "https://graph.org/file/3680f9d14543771855ee0-1ff9d9b2aeabefedb2.mp4"

# ========== RESULT IMAGE ==========
RESULT_IMAGE_URL = "https://graph.org/file/17971526dfefa9e20863b-44207fd3a022c59c53.jpg"

# ========== LINKS ==========
UPDATES_LINK = "https://t.me/your_updates_channel"
SUPPORT_LINK = "https://t.me/your_support_group"
PLAYZONE_LINK = "https://t.me/your_playzone_group"
LIVE_SCORE_LINK = "https://t.me/your_live_score_channel"

# ========== IMAGES/VIDEOS ==========
IMAGE_URL = "https://files.catbox.moe/0odkk1.jpg"
HOST_IMAGE_URL = "https://files.catbox.moe/0odkk1.jpg"
BOWLING_VIDEO_URL = "https://files.catbox.moe/r75e19.mp4"
BATTING_VIDEO_URL = "https://files.catbox.moe/26qdaw.mp4"
SIX_VIDEO_URL = ""
FOUR_VIDEO_URL = ""
WICKET_VIDEO_URL = "https://files.catbox.moe/7ixfhp.mp4"
OUT_VIDEO_URL = "https://files.catbox.moe/7ixfhp.mp4"

# ========== GAME SETTINGS ==========
DEFAULT_OVERS = 10
MAX_OVERS = 20
MIN_OVERS = 1
BOWLING_TIMER_SECONDS = 60
JOINING_TIMER_SECONDS = 120
MAX_PLAYERS_PER_TEAM = 11
MIN_PLAYERS_PER_TEAM = 2

# ========== BOWLING SPEED OPTIONS ==========
BOWLING_SPEEDS = ["FANCODE", "TANCODE", "ATHANSTAN", "FAST", "PHYSICAL", "63"]
BOWLING_SPEEDS_BUTTONS = ["FANCODE", "TANCODE", "ATHANSTAN", "FAST", "PHYSICAL", "63"]

# ========== BATTING RATINGS ==========
BATTING_RATINGS = {
    "ND BAT": 66,
    "MENTAL": 66,
    "PACE": 63,
    "PHYSICAL": 66
}

# ========== SOLO MODE BOWLERS ==========
SOLO_BOWLERS = [
    {"name": "Fast Bowler", "icon": "⚡", "speed": "FAST"},
    {"name": "Spin Bowler", "icon": "🔄", "speed": "SPIN"},
    {"name": "Pace Bowler", "icon": "💨", "speed": "PACE"}
]

# ========== SOLO PLAYER ICONS ==========
SOLO_ICONS = ["🟢", "⚽", "🔥", "🌞", "💬", "🎮", "🏀", "🐍", "🕊️", "⭐", "⚡", "💎"]

# ========== WELCOME CAPTION ==========
WELCOME_CAPTION = """
🏏 **𝐖ᴇʟᴄᴏᴍᴇ 𝐭ᴏ 𝐂ʀɪᴄᴋᴇᴛ 𝐁ᴏᴛ!**

🔴 **𝐋ɪᴠᴇ 𝐂ʀɪᴄᴋᴇᴛ 𝐒ᴄᴏʀᴇs:** Get real-time updates on live matches. Use /matches to see live scores.

🎮 **𝐌ᴀɴᴀɢᴇ 𝐘ᴏᴜʀ 𝐓ᴇᴀᴍ:** Strategize, set your lineup, and play the game just like a pro captain.

🗽 **1_VS_1:** Find one vs one match /1v1

Use /help to learn more about the game.
"""

# ========== MESSAGES ==========
WELCOME_MESSAGE = """
🏏 **CRICKET CHAMPIONSHIP** 🏏

**WELCOME TO CRICKET BOT!**

• **LIVE CRICKET SCORES:** Get real-time updates on live matches.
  Use /matches to see live scores.

• **MANAGE YOUR TEAM:** Strategize, set your lineup, and play the game just like a pro captain.

• **1_VS_1:** Find one vs one match /1v1

Use /help to learn more about the game.
"""

HELP_MESSAGE = """
Hello! 🤗 Need some help with Cricket Master Bot? Here are some tips to get you started:

🔹 **Join a Match:** Ready to play? Start a new match or join an existing one with your friends. Just type /start in groups.

🔹 **Manage Your Team:** Set up your lineup, choose your captain, and get ready to play. Use /startgame to get started.

🔹 **Game Instructions:** New to the game? Type help to learn how to play and master the game.

🔹 **Feedback:** We value your input! Share your /feedback with us in the support group.

🔹 **Help and Support:** If you need assistance, visit our support group or type /help.

👉 For a list of all available commands, click the "🎯 𝐆𝐚𝐦𝐞 𝐈𝐧𝐬𝐭𝐫𝐮𝐜𝐭𝐢𝐨𝐧𝐬" button below.

Enjoy your time with Cricket Master Bot! 🏏🚀
"""

GAME_INSTRUCTIONS_MESSAGE = """
🎮 **GAME INSTRUCTIONS**

Choose your mode:
"""

SOLO_MODE_MESSAGE = """
🎯 **SOLO MODE**

• /solo_start: Begin a solo match
• /solo_stats: View your stats
• /solo_leaderboard: Top players
• /end_match: End the current game
"""

TEAM_MODE_MESSAGE = """
🌟 **𝐌ᴇᴍʙᴇʀs 𝐀ᴅᴅɪɴɢ:**

/add_A - add members to team A  
/add_B - add members to team B  

Eg: /add_A 1  or /add_A @username  
(Use the player number of your team)

🌟 **𝐌ᴇᴍʙᴇʀs 𝐑ᴇᴍᴏᴠɪɴɢ:**

/remove_A - remove members from team A  
/remove_B - remove members from team B  

Eg: /remove_A 2  
(Use the player number of your team)

🌟 **𝐆ᴀᴍᴇ 𝐏ʟᴀʏ 𝐂ᴏᴍᴍᴀɴᴅs:**

/startgame - to start the game  

/bowling - choose the bowling person of team A or B  
Eg: /bowling 3  
(Use the team A or B player number for bowling)

/batting - choose the batting person of team A or B  
Eg: /batting 4  
(Use the team A or B player number for batting)

/swap - to change the playing position of the current team  

/end_match - to end the current game  

/Feedback - give your feedback about the game
"""

AUCTION_MESSAGE = """
💰 **AUCTION COMMANDS**

/add_cap - add auction captain ➕
/rm_cap - remove auction captain ➖
/cap_change_auction - change the auction captain
/auction_id - send auction player id 🆔
/start_auction - start auction 🏁
/pause_auction - pause the auction ⏸️
/resume_auction - resume the auction ▶️
/auction_host_change - change the auction host 👑
/xp - auction player put value 💰
/unsold - auction player unsold list 📋
/rm_auction_id - remove auction sold player ❌
"""

HOST_MESSAGE = """
🎮 **New Game Alert!**

Who will be the game host for this match?
"""

TEAM_CREATION_MESSAGE = """
🏏 **Team Creation**

Team creation is underway!
Join Team A by sending /join_teamA
Join Team B by sending /join_teamB

Check members: /members_list
"""

OVERS_MESSAGE = """
🏏 **Cricket Game**

How many overs do you want for this game?
"""

MATCH_START_MESSAGE = """
🎉 OHOO! Let's play a {overs} overs Match!!

{bowling_team} will bowl first!

Now, choose your player!
"""

# ========== BOWLING MESSAGES ==========
BOWLING_START_MESSAGE = """
🎯 **Hey {bowler}, now you're bowling!**

Choose your bowling speed:
"""

BOWLING_NUMBER_MESSAGE = """
✅ **Speed {speed} selected!**

Now send number on bot PM (1-6 or W for wicket)
⏰ You have {seconds} seconds!
"""

BOWLING_WARNING_30 = """
⚠️ **Warning: {bowler}, you have 30 seconds left to send a number!**
"""

BOWLING_WARNING_10 = """
⚠️ **Warning: {bowler}, you have 10 seconds left to send a number!**
"""

BOWLING_TIMEOUT = """
⏰ **No message received from bowler, deducting 6 runs of bowler.**
❌ **Seems Bowling player is not responding, User Eliminated from the game !!**
"""

# ========== BATTING MESSAGES ==========
BATTING_START_MESSAGE = """
🏏 **Now Batter: {batter} can send number (0-6)!!**

📊 **Ratings:** ND BAT | MENTAL 66 | PACE 63 | PHYSICAL 66
"""

BATTING_WARNING_30 = """
⚠️ **Warning: {batter}, you have 30 seconds left to send a number!**
"""

BATTING_WARNING_10 = """
⚠️ **Warning: {batter}, you have 10 seconds left to send a number!**
"""

BATTING_TIMEOUT = """
⏰ **No message received from batter!**
"""

# ========== BALL RESULT MESSAGES ==========
BALL_RESULT_RUN = """
🏏 **{runs} RUN{'S' if runs > 1 else ''}!**

{run_type}
⏱️ {response_time}ms
"""

BALL_RESULT_SIX = """
🎯 **SIX!** 🚀

{run_type}
⏱️ {response_time}ms
"""

BALL_RESULT_FOUR = """
🎯 **FOUR!** 💥

{run_type}
⏱️ {response_time}ms
"""

BALL_RESULT_WICKET = """
🎯 **WICKET!** 🎯

{wicket_type}
⏱️ {response_time}ms
"""

# ========== PLAYER ROTATION ==========
NEW_BATSMAN_MESSAGE = """
🔄 **Number matches, {old_batter}**

👋 **Hey {new_batter}, now you're batter!**
🆕 **New batsman: {new_batter}**

🏀 **Get ready for the next ball!**
"""

NEW_BOWLER_MESSAGE = """
🔄 **Hey {new_bowler}, now you're bowling!**
"""

# ========== SCORECARD MESSAGES ==========
SCORECARD_HEADER = """
╭━─━─━─━─≪✠≫─━─━─━─━╮
"""

SCORECARD_TEAM_A_HEADER = """
───────⊱ Tᴇᴀᴍ - A ⊰──────
"""

SCORECARD_TEAM_B_HEADER = """
───────⊱ Tᴇᴀᴍ - B ⊰──────
"""

SCORECARD_SEPARATOR = """
× •-•-•-•-•-••-•-•⟮ 🏏 ⟯•-•-•-•-•-•-•-•-• ×
"""

SCORECARD_FOOTER = """
༺═────────────────═༻
"""

# ========== LIVE SCORECARD MESSAGES ==========
LIVE_SCORECARD_HEADER = """
╾ ⏳ 𝗧𝗼𝘁𝗮𝗹 𝗢𝘃𝗲𝗿𝘀: {total_overs}
╾ 📯 𝗛𝗼𝘀𝘁: {host}
────┈┄┄╌╌╌╌┄┄┈────
"""

LIVE_SCORECARD_BATTING = """
𝗕𝗮𝘁𝘁𝗶𝗻𝗴 𝗧𝗲𝗮𝗺 - {team}
"""

LIVE_SCORECARD_BOWLING = """
𝗕𝗼𝘄𝗹𝗶𝗻𝗴 𝗧𝗲𝗮𝗺 - {team}
"""

LIVE_SCORECARD_TEAM_SCORE = """
👥 𝗧𝗲𝗮𝗺 - A: {score_a}/{wickets_a} | {overs_a} ov
╰⊚ 𝗖𝗥𝗥: {crr_a}
⊱⋅ ──────────── ⋅⊰
👥 𝗧𝗲𝗮𝗺 - B: {score_b}/{wickets_b} | {overs_b} ov
╰⊚ 𝗖𝗥𝗥: {crr_b}
────┈┄┄╌╌╌╌┄┄┈────
"""

# ========== BATSMAN DISPLAY ==========
BATSMAN_DISPLAY = """
✴️ {name} = {runs}({balls})
  ╰⊚ ID : {user_id}
    ╰⊚ ({ball_by_ball})
"""

BATSMAN_DISPLAY_NO_BALLS = """
✴️ {name} = {runs}({balls})
  ╰⊚ ID : {user_id}
"""

BOWLER_DISPLAY = """
⚾ {name}
╰⊚ ({balls_bowled})
"""

# ========== TIMER MESSAGES ==========
def get_timer_warning_30(player_name: str, role: str):
    return f"⚠️ **Warning:** {player_name}, you have 30 seconds left to send {role} number!"

def get_timer_warning_10(player_name: str, role: str):
    return f"⚠️ **Warning:** {player_name}, you have 10 seconds left to send {role} number!"
