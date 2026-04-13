from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.mongodb import db
from utils.decorators import game_active, captain_only
from utils.validators import is_valid_player_number
from team.game_engine import game_engine
from team.buttons import (
    get_batting_buttons, get_bowling_buttons, get_batting_prompt,
    get_out_message, get_ball_result_message
)
from team.messages import (
    BOWLER_SELECTED, BATSMAN_SELECTED, SECOND_BATSMAN_SELECTED,
    INVALID_BATSMAN, INVALID_BOWLER, SAME_BATSMAN_ERROR,
    NO_ACTIVE_GAME, SWAP_SUCCESS, SWAP_NOT_ALLOWED
)
from team.timers import game_timer, send_bowler_timeout, send_batter_timeout
from config import TEAM_BOWLING_VIDEO_URL, TEAM_BATTING_VIDEO_URL, BOWLING_TIMER_SECONDS
import asyncio
import random


# ========== BOWLING COMMAND ==========

@Client.on_message(filters.command("bowling") & filters.group)
@game_active
@captain_only
async def select_bowler(client: Client, message: Message):
    """
    /bowling 3 - Select bowler by player number
    """
    group_id = message.chat.id
    user_id = message.from_user.id
    args = message.text.split()
    
    if len(args) != 2:
        await message.reply("❌ Usage: /bowling <player_number>\nExample: /bowling 3")
        return
    
    # Validate player number
    valid, player_num = is_valid_player_number(args[1], max_players=11)
    if not valid:
        await message.reply("❌ Invalid player number! Please use number between 1 and 11.")
        return
    
    # Get match data
    match = await db.get_match(group_id)
    if not match:
        await message.reply(NO_ACTIVE_GAME)
        return
    
    # Determine which team is bowling
    bowling_team_key = f"team_{match.get('bowling_team', 'A').lower()}"
    bowling_team = match.get(bowling_team_key, {})
    
    # Find player
    selected_player = None
    for player in bowling_team.get("players", []):
        if player.get("number") == player_num:
            selected_player = player
            break
    
    if not selected_player:
        await message.reply(INVALID_BOWLER.format(player_num=player_num))
        return
    
    # Check if player is already bowling this over
    current_bowler = match.get("current_bowler", {})
    if current_bowler and current_bowler.get("number") == player_num:
        await message.reply("❌ This player is already bowling the current over!")
        return
    
    # Check if player is out (can't bowl if out? Actually out players can bowl)
    if selected_player.get("is_out", False):
        await message.reply(f"⚠️ {selected_player.get('username')} is out! Choose another bowler.")
        return
    
    # Set current bowler
    match["current_bowler"] = selected_player
    if "balls_bowled" not in selected_player:
        selected_player["balls_bowled"] = []
    if "runs_conceded" not in selected_player:
        selected_player["runs_conceded"] = 0
    if "wickets" not in selected_player:
        selected_player["wickets"] = 0
    
    await db.save_match(group_id, match)
    
    # Send confirmation
    await message.reply(
        BOWLER_SELECTED.format(
            bowler_name=selected_player.get("username"),
            team_name=match.get("bowling_team", "A")
        )
    )


# ========== BATTING COMMAND ==========

@Client.on_message(filters.command("batting") & filters.group)
@game_active
@captain_only
async def select_batsman(client: Client, message: Message):
    """
    /batting 3 - Select batsman by player number
    """
    group_id = message.chat.id
    args = message.text.split()
    
    if len(args) != 2:
        await message.reply("❌ Usage: /batting <player_number>\nExample: /batting 3")
        return
    
    # Validate player number
    valid, player_num = is_valid_player_number(args[1], max_players=11)
    if not valid:
        await message.reply("❌ Invalid player number! Please use number between 1 and 11.")
        return
    
    # Get match data
    match = await db.get_match(group_id)
    if not match:
        await message.reply(NO_ACTIVE_GAME)
        return
    
    # Determine which team is batting
    batting_team_key = f"team_{match.get('batting_team', 'A').lower()}"
    batting_team = match.get(batting_team_key, {})
    
    # Find player
    selected_player = None
    for player in batting_team.get("players", []):
        if player.get("number") == player_num:
            selected_player = player
            break
    
    if not selected_player:
        await message.reply(INVALID_BATSMAN.format(player_num=player_num))
        return
    
    # Check if player is already batting
    current_batsmen = match.get("current_batsmen", [])
    for batsman in current_batsmen:
        if batsman.get("number") == player_num:
            await message.reply(SAME_BATSMAN_ERROR.format(player_name=selected_player.get("username")))
            return
    
    # Check if player is out
    if selected_player.get("is_out", False):
        await message.reply(f"❌ {selected_player.get('username')} is already out! Choose another batsman.")
        return
    
    # Add to current batsmen list
    if not current_batsmen:
        # First batsman (striker)
        match["current_batsmen"] = [selected_player]
        await message.reply(
            BATSMAN_SELECTED.format(
                batsman_name=selected_player.get("username"),
                team_name=match.get("batting_team", "A")
            )
        )
    elif len(current_batsmen) == 1:
        # Second batsman (non-striker)
        match["current_batsmen"].append(selected_player)
        await message.reply(
            SECOND_BATSMAN_SELECTED.format(batsman_name=selected_player.get("username"))
        )
        
        # Both batsmen selected, start game in 10 seconds
        await asyncio.sleep(10)
        await start_ball(client, group_id, match)
    else:
        await message.reply("❌ Both batsmen are already selected! Wait for wicket to select next batsman.")
        return
    
    await db.save_match(group_id, match)


# ========== START BALL ==========

async def start_ball(client: Client, group_id: int, match: dict):
    """Start a new ball"""
    
    # Get current batsman (striker)
    current_batsmen = match.get("current_batsmen", [])
    if not current_batsmen:
        return
    
    striker = current_batsmen[0]
    bowler = match.get("current_bowler")
    
    if not bowler:
        await client.send_message(group_id, "❌ No bowler selected! Use /bowling first.")
        return
    
    # Get current over info
    ball_count = match.get("ball_count", 0)
    over_count = match.get("over_count", 0)
    score = match.get(f"team_{match.get('batting_team', 'A').lower()}", {}).get("score", 0)
    wickets = match.get(f"team_{match.get('batting_team', 'A').lower()}", {}).get("wickets", 0)
    
    # Send batting prompt to group with video
    batting_prompt = get_batting_prompt(
        striker.get("username"),
        ball_count + 1,
        f"{score}/{wickets}",
        bowler.get("username")
    )
    
    # Send video with batting buttons
    await client.send_video(
        chat_id=group_id,
        video=TEAM_BATTING_VIDEO_URL,
        caption=batting_prompt,
        reply_markup=get_batting_buttons(striker.get("username"), ball_count + 1)
    )
    
    # Send bowling DM to bowler with video
    bowling_caption, bowling_buttons = get_bowling_buttons(
        striker.get("username"),
        bowler.get("username"),
        f"{score}/{wickets}",
        f"{over_count}.{ball_count}"
    )
    
    await client.send_video(
        chat_id=bowler.get("user_id"),
        video=TEAM_BOWLING_VIDEO_URL,
        caption=bowling_caption,
        reply_markup=bowling_buttons
    )
    
    # Store ball state
    match["current_ball"] = {
        "striker": striker,
        "bowler": bowler,
        "status": "waiting",
        "batter_number": None,
        "bowler_number": None,
        "start_time": asyncio.get_event_loop().time()
    }
    await db.save_match(group_id, match)
    
    # Start timer for bowler
    async def on_bowler_timeout(bowler_name):
        # Handle timeout
        await send_bowler_timeout(bowler_name, client, bowler.get("user_id"), group_id)
        # Auto generate random number
        await process_ball_response(group_id, "bowler", str(random.randint(1, 6)), is_timeout=True)
    
    async def on_bowler_warning_30(bowler_name):
        await client.send_message(bowler.get("user_id"), f"⚠️ {bowler_name}, you have 30 seconds left!")
    
    async def on_bowler_warning_10(bowler_name):
        await client.send_message(bowler.get("user_id"), f"⚠️ {bowler_name}, you have 10 seconds left!")
    
    await game_timer.start_bowler_timer(
        bowler.get("user_id"),
        bowler.get("username"),
        on_bowler_timeout,
        on_bowler_warning_30,
        on_bowler_warning_10
    )


# ========== PROCESS BALL RESPONSE ==========

async def process_ball_response(group_id: int, response_type: str, number: any, is_timeout: bool = False):
    """Process bowler or batter response"""
    
    match = await db.get_match(group_id)
    if not match:
        return
    
    current_ball = match.get("current_ball", {})
    if not current_ball:
        return
    
    # Update response
    if response_type == "bowler":
        current_ball["bowler_number"] = number
        # Cancel timer
        await game_timer.cancel_bowler_timer(current_ball["bowler"].get("user_id"))
    else:
        current_ball["batter_number"] = number
    
    # Check if both responses received
    if current_ball.get("bowler_number") is not None and current_ball.get("batter_number") is not None:
        await resolve_ball(client, group_id, match, current_ball)
    
    await db.save_match(group_id, match)


# ========== RESOLVE BALL ==========

async def resolve_ball(client: Client, group_id: int, match: dict, current_ball: dict):
    """Resolve ball after both responses received"""
    
    batter_num = current_ball.get("batter_number")
    bowler_num = current_ball.get("bowler_number")
    striker = current_ball.get("striker")
    bowler = current_ball.get("bowler")
    
    # Compare
    result_type, value = game_engine.compare_ball(batter_num, bowler_num)
    
    # Get current stats
    batting_team_key = f"team_{match.get('batting_team', 'A').lower()}"
    batting_team = match.get(batting_team_key, {})
    
    # Update based on result
    if result_type == "wicket":
        # Wicket
        batting_team["wickets"] = game_engine.update_score_on_wicket(batting_team.get("wickets", 0))
        
        # Update batsman stats
        striker["is_out"] = True
        striker["ball_by_ball"].append("W")
        striker["balls"] += 1
        
        # Update bowler stats
        bowler["wickets"] = bowler.get("wickets", 0) + 1
        bowler["balls_bowled"].append("W")
        
        # Send out message
        await client.send_video(
            chat_id=group_id,
            video=WICKET_VIDEO_URL,
            caption=get_out_message(striker.get("username"))
        )
        
        # Remove striker from current batsmen
        current_batsmen = match.get("current_batsmen", [])
        current_batsmen.pop(0)
        match["current_batsmen"] = current_batsmen
        
        # Check if innings complete
        if batting_team["wickets"] >= len(batting_team.get("players", [])):
            await end_innings(client, group_id, match)
            return
        
        # Ask for next batsman
        await client.send_message(group_id, "Out! Please choose the next batsman by command /batting.")
        
    else:
        # Runs scored
        runs = value
        batting_team["score"] = game_engine.update_score_on_run(batting_team.get("score", 0), runs)
        
        # Update batsman stats
        striker["runs"] += runs
        striker["balls"] += 1
        striker["ball_by_ball"].append(str(runs))
        
        # Update bowler stats
        bowler["runs_conceded"] = bowler.get("runs_conceded", 0) + runs
        bowler["balls_bowled"].append(str(runs))
        
        # Send result message
        await client.send_message(
            group_id,
            get_ball_result_message(runs, bowler_num, batter_num, 0)
        )
        
        # Swap strike on odd runs
        if runs % 2 == 1:
            current_batsmen = match.get("current_batsmen", [])
            if len(current_batsmen) > 1:
                current_batsmen[0], current_batsmen[1] = current_batsmen[1], current_batsmen[0]
                match["current_batsmen"] = current_batsmen
    
    # Update ball count
    ball_count = match.get("ball_count", 0) + 1
    over_count = match.get("over_count", 0)
    
    if ball_count >= 6:
        # Over complete
        ball_count = 0
        over_count += 1
        
        # Send scorecard
        from team.scorecard import scorecard_gen
        await scorecard_gen.send_scorecard(client, group_id, match, is_live=True)
        
        # Ask for next bowler
        host_name = match.get("host", {}).get("username")
        await client.send_message(group_id, f"Over! Hey {host_name}, Please choose the next bowler by command /bowling.")
        
        # Clear current bowler
        match["current_bowler"] = None
        
        # Check if innings complete
        if over_count >= match.get("total_overs", 10):
            await end_innings(client, group_id, match)
            return
    
    match["ball_count"] = ball_count
    match["over_count"] = over_count
    match["current_ball"] = None
    
    # Update overs display
    overs_display = f"{over_count}.{ball_count}"
    batting_team["overs"] = overs_display
    
    await db.save_match(group_id, match)
    
    # Start next ball if innings not complete
    if match.get("status") not in ["completed", "innings_break"]:
        await start_ball(client, group_id, match)


# ========== END INNINGS ==========

async def end_innings(client: Client, group_id: int, match: dict):
    """End current innings"""
    
    innings = match.get("current_innings", 1)
    total_overs = match.get("total_overs", 10)
    
    if innings == 1:
        # First innings complete
        match["current_innings"] = 2
        
        # Swap batting and bowling teams
        old_batting = match.get("batting_team")
        old_bowling = match.get("bowling_team")
        match["batting_team"] = old_bowling
        match["bowling_team"] = old_batting
        
        # Calculate target
        first_innings_team = match.get(f"team_{old_batting.lower()}", {})
        target = first_innings_team.get("score", 0) + 1
        match["target"] = target
        
        # Reset ball count for new innings
        match["ball_count"] = 0
        match["over_count"] = 0
        match["current_batsmen"] = []
        match["current_bowler"] = None
        
        # Reset team scores for second innings? No, keep first innings score
        # But create new score for second innings team
        second_innings_team_key = f"team_{match.get('batting_team', 'A').lower()}"
        match[second_innings_team_key]["score"] = 0
        match[second_innings_team_key]["wickets"] = 0
        match[second_innings_team_key]["overs"] = "0.0"
        
        await db.save_match(group_id, match)
        
        # Announce innings break
        await client.send_message(
            group_id,
            f"🏏 **END OF INNING 1** 🏏\n\n"
            f"Team {old_batting} scored {first_innings_team.get('score')}/{first_innings_team.get('wickets')}\n\n"
            f"🎯 Target: {target} runs for Team {match.get('batting_team')}\n\n"
            f"Team {match.get('bowling_team')} will bowl first in second innings!\n\n"
            f"Now, type /bowling to choose the bowling member! 📝"
        )
        
    else:
        # Second innings complete - match over
        match["status"] = "completed"
        await db.save_match(group_id, match)
        
        # Determine winner
        team_a = match.get("team_a", {})
        team_b = match.get("team_b", {})
        
        if team_a.get("score") > team_b.get("score"):
            winner = "Team A"
        elif team_b.get("score") > team_a.get("score"):
            winner = "Team B"
        else:
            winner = "Tie"
        
        await client.send_message(
            group_id,
            f"🏆 **MATCH ENDED** 🏆\n\n"
            f"Winner: {winner}\n\n"
            f"Team A: {team_a.get('score')}/{team_a.get('wickets')}\n"
            f"Team B: {team_b.get('score')}/{team_b.get('wickets')}\n\n"
            f"Use /create_team to start a new match!"
        )


# ========== SWAP COMMAND ==========

@Client.on_message(filters.command("swap") & filters.group)
@game_active
@captain_only
async def swap_teams(client: Client, message: Message):
    """Swap batting and bowling teams"""
    
    group_id = message.chat.id
    match = await db.get_match(group_id)
    
    if not match:
        await message.reply(NO_ACTIVE_GAME)
        return
    
    # Check if game is in active play
    if match.get("status") not in ["batting", "bowling"]:
        await message.reply(SWAP_NOT_ALLOWED.format(status=match.get("status", "unknown")))
        return
    
    # Swap
    old_batting = match.get("batting_team")
    old_bowling = match.get("bowling_team")
    match["batting_team"] = old_bowling
    match["bowling_team"] = old_batting
    
    await db.save_match(group_id, match)
    
    await message.reply(
        SWAP_SUCCESS.format(
            batting_team=match.get("batting_team"),
            bowling_team=match.get("bowling_team")
        )
    )
