from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ButtonStyle


# ========== BATTING BUTTONS (Group mein Batter ke liye) ==========

def get_batting_buttons(batter_name: str, over_balls: int):
    """Batting inline buttons - Batter group mein dekhega"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("0️⃣ 0", callback_data="bat_0", style=ButtonStyle.DEFAULT),
            InlineKeyboardButton("1️⃣ 1", callback_data="bat_1", style=ButtonStyle.DEFAULT),
            InlineKeyboardButton("2️⃣ 2", callback_data="bat_2", style=ButtonStyle.DEFAULT)
        ],
        [
            InlineKeyboardButton("3️⃣ 3", callback_data="bat_3", style=ButtonStyle.DEFAULT),
            InlineKeyboardButton("4️⃣ 4", callback_data="bat_4", style=ButtonStyle.DEFAULT),
            InlineKeyboardButton("6️⃣ 6", callback_data="bat_6", style=ButtonStyle.DANGER)
        ],
        [
            InlineKeyboardButton("🏏 OUT", callback_data="bat_out", style=ButtonStyle.DANGER)
        ]
    ])


# ========== BOWLING BUTTONS (DM mein Bowler ke liye) ==========

def get_bowling_buttons(batsman_name: str, bowler_name: str, score: str, overs: str):
    """Bowling inline buttons - Bowler DM mein dekhega"""
    caption = f"""🏏 **CRICKET GAME - BOWLING**

**Batsman:** {batsman_name}
**Bowler:** {bowler_name}

📊 **Score:** {score}
🎯 **Overs:** {overs}

━━━━━━━━━━━━━━━━━━
**Send your bowling number:**
"""
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("1️⃣ 1", callback_data="bowl_1", style=ButtonStyle.DEFAULT),
            InlineKeyboardButton("2️⃣ 2", callback_data="bowl_2", style=ButtonStyle.DEFAULT),
            InlineKeyboardButton("3️⃣ 3", callback_data="bowl_3", style=ButtonStyle.DEFAULT)
        ],
        [
            InlineKeyboardButton("4️⃣ 4", callback_data="bowl_4", style=ButtonStyle.DEFAULT),
            InlineKeyboardButton("5️⃣ 5", callback_data="bowl_5", style=ButtonStyle.DEFAULT),
            InlineKeyboardButton("6️⃣ 6", callback_data="bowl_6", style=ButtonStyle.DANGER)
        ],
        [
            InlineKeyboardButton("🔙 Back to Group", callback_data="back_to_group", style=ButtonStyle.SECONDARY)
        ]
    ])
    return caption, buttons


# ========== BATTING PROMPT (Group mein Batter ke liye) ==========

def get_batting_prompt(batter_name: str, over_balls: int, score: str, bowler_name: str):
    """Batting prompt message - Batter group mein dekhega"""
    prompt = f"""🏏 **Now Batter:** {batter_name}

📊 **Current Score:** {score}
🎯 **Bowler:** {bowler_name}
⚡ **Over Balls:** {over_balls}/6

━━━━━━━━━━━━━━━━━━
**Choose your batting number:**
"""
    return prompt


# ========== LIVE SCORE BUTTON (Scorecard ke neeche) ==========

def get_live_score_button():
    """Live score button - Channel link open karega"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Live Cricket Score", callback_data="live_score", style=ButtonStyle.PRIMARY)]
    ])


# ========== NEXT BOWLER SELECTION BUTTON (Over complete hone ke baad) ==========

def get_next_bowler_prompt(host_name: str):
    """Next bowler selection prompt - Host ke liye"""
    return f"Over! Hey {host_name}, Please choose the next bowler by command /bowling."


# ========== NEXT BATSMAN PROMPT (Wicket ke baad) ==========

def get_next_batsman_prompt():
    """Next batsman selection prompt - Captain ke liye"""
    return "Out! Please choose the next batsman by command /batting."


# ========== OUT ANIMATION MESSAGE ==========

def get_out_message(batter_name: str):
    """Out ho jane ke baad ka message"""
    return f"🎯 Number matches, {batter_name} is out!\n\n{batter_name} is walking back to the pavilion 🏃‍♂️👋\n\nOut! Please choose the next batsman by command /batting."


# ========== BALL RESULT MESSAGES ==========

def get_ball_result_message(runs: int, bowler_num: int, batter_num, response_time: int = 0):
    """Ball result based on comparison"""
    if runs == "OUT":
        return f"""🎯 **WICKET!** 🎯

⏱️ {response_time}ms"""
    elif runs == 6:
        return f"""🎯 **SIX!** 🚀

🏏 Batter: {batter_num} | 🎯 Bowler: {bowler_num}
⏱️ {response_time}ms"""
    elif runs == 4:
        return f"""🎯 **FOUR!** 💥

🏏 Batter: {batter_num} | 🎯 Bowler: {bowler_num}
⏱️ {response_time}ms"""
    else:
        return f"""🏏 **{runs} RUN{'S' if runs > 1 else ''}!**

🏏 Batter: {batter_num} | 🎯 Bowler: {bowler_num}
⏱️ {response_time}ms"""


# ========== SCORECARD HEADER ==========

def get_scorecard_header(total_overs: int, host_name: str):
    """Scorecard ka header"""
    return f"""╾ ⏳ 𝗧𝗼𝘁𝗮𝗹 𝗢𝘃𝗲𝗿𝘀: {total_overs}
╾ 📯 𝗛𝗼𝘀𝘁: {host_name}
────┈┄┄╌╌╌╌┄┄┈────"""


# ========== BATTING TEAM DISPLAY ==========

def get_batting_team_display(team_name: str, batsmen: list):
    """Batting team ke batsmen display"""
    display = f"𝗕𝗮𝘁𝘁𝗶𝗻𝗴 𝗧𝗲𝗮𝗺 - {team_name}\n\n"
    for batsman in batsmen:
        display += f"🏏 {batsman['name']} = {batsman['runs']}({batsman['balls']})\n"
        display += f"╰⊚(𝗖𝗦𝗥: {batsman['csr']})\n"
    return display


# ========== BOWLING TEAM DISPLAY ==========

def get_bowling_team_display(team_name: str, bowler_name: str, balls_bowled: list):
    """Bowling team ke bowler display"""
    display = f"𝗕𝗼𝘄𝗹𝗶𝗻𝗴 𝗧𝗲𝗮𝗺 - {team_name}\n\n"
    display += f"⚾ {bowler_name}\n"
    display += f"╰⊚ ({', '.join(balls_bowled)})\n"
    return display


# ========== TEAM SCORE DISPLAY ==========

def get_team_score_display(team_a_score: int, team_a_wickets: int, team_a_overs: float, team_a_crr: float,
                           team_b_score: int, team_b_wickets: int, team_b_overs: float, team_b_crr: float):
    """Dono teams ka score display"""
    return f"""👥 𝗧𝗲𝗮𝗺 - A: {team_a_score}/{team_a_wickets} | {team_a_overs} ov
╰⊚ 𝗖𝗥𝗥: {team_a_crr}
⊱⋅ ──────────── ⋅⊰
👥 𝗧𝗲𝗮𝗺 - B: {team_b_score}/{team_b_wickets} | {team_b_overs} ov
╰⊚ 𝗖𝗥𝗥: {team_b_crr}
────┈┄┄╌╌╌╌┄┄┈────"""


# ========== TIMER MESSAGES ==========

def get_timer_warning_30(player_name: str, role: str):
    """30 seconds warning"""
    return f"⚠️ **Warning:** {player_name}, you have 30 seconds left to send {role} number!"

def get_timer_warning_10(player_name: str, role: str):
    """10 seconds warning"""
    return f"⚠️ **Warning:** {player_name}, you have 10 seconds left to send {role} number!"

def get_timer_timeout(player_name: str, role: str):
    """Timeout message"""
    if role == "bowling":
        return f"⏰ No message received from bowler {player_name}, deducting 6 runs.\n❌ Seems Bowling player is not responding, User Eliminated from the game !!"
    else:
        return f"⏰ No message received from batter {player_name}!"
