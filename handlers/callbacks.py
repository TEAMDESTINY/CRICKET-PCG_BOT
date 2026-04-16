from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from database.mongodb import db
from team.game_engine import game_engine
from team.buttons import get_batting_buttons, get_bowling_buttons, get_live_score_button
from team.scorecard import scorecard_gen
from team.timers import game_timer
from config import (
    LIVE_SCORE_LINK, UPDATES_LINK, SUPPORT_LINK, 
    OWNER_LINK, BOT_USERNAME, WICKET_VIDEO_URL, OUT_VIDEO_URL,
    IMAGE_URL, GAME_INSTRUCTIONS_IMAGE_URL,
    TEAM_START_VIDEO_URL, TEAM_BOWLING_VIDEO_URL, TEAM_BATTING_VIDEO_URL,
    TEAM_ADD_VIDEO_URL, TEAM_REMOVE_VIDEO_URL, TEAM_STARTGAME_VIDEO_URL
)
import asyncio


# ========== DEFINE WELCOME_CAPTION HERE ==========
WELCOME_CAPTION = """
🏏 **Welcome to Cricket Bot!**

🔴 **Live Cricket Scores:** Get real-time updates on live matches. Use /matches to see live scores.

🎮 **Manage Your Team:** Strategize, set your lineup, and play the game just like a pro captain.

🗽 **1 VS 1:** Find one vs one match /1v1

Use /help to learn more about the game.
"""


# ========== MAIN CALLBACK HANDLER ==========

@Client.on_callback_query()
async def handle_callbacks(client: Client, callback_query: CallbackQuery):
    """Handle all callback queries"""
    data = callback_query.data
    user_id = callback_query.from_user.id
    message = callback_query.message
    
    # ========== BATTING CALLBACKS ==========
    if data.startswith("bat_"):
        await handle_batting_callback(client, callback_query, data)
    
    # ========== BOWLING CALLBACKS ==========
    elif data.startswith("bowl_"):
        await handle_bowling_callback(client, callback_query, data)
    
    # ========== LIVE SCORE CALLBACK ==========
    elif data == "live_score":
        await callback_query.answer("📊 Opening Live Score Channel...")
    
    # ========== BACK TO GROUP CALLBACK ==========
    elif data == "back_to_group":
        await callback_query.answer("🔙 Returning to group...")
    
    # ========== START/HELP CALLBACKS ==========
    elif data == "game_instructions":
        await handle_game_instructions(client, callback_query)
    
    elif data == "solo_play":
        await handle_solo_play(client, callback_query)
    
    elif data == "team_play":
        await handle_team_play(client, callback_query)
    
    elif data == "auction":
        await handle_auction(client, callback_query)
    
    elif data == "home":
        await handle_home(client, callback_query)
    
    elif data == "back_to_game_instructions":
        await back_to_game_instructions(client, callback_query)
    
    elif data == "add_to_group":
        await callback_query.answer("➕ Use the button below to add me to your group!")
    
    # ========== TEAM MODE VIDEO CALLBACKS (Video open honge) ==========
    elif data == "team_start":
        await callback_query.answer("🎬 Opening START guide...")
        await callback_query.message.reply_video(
            video=TEAM_START_VIDEO_URL,
            caption="📌 START - Use /create_team in your group to begin the match!"
        )
    
    elif data == "team_add":
        await callback_query.answer("📋 Opening ADD guide...")
        await callback_query.message.reply_video(
            video=TEAM_ADD_VIDEO_URL,
            caption="📌 ADD - Use /add_A and /add_B commands to add players!"
        )
    
    elif data == "team_remove":
        await callback_query.answer("🗑️ Opening REMOVE guide...")
        await callback_query.message.reply_video(
            video=TEAM_REMOVE_VIDEO_URL,
            caption="📌 REMOVE - Use /remove_A and /remove_B commands to remove players!"
        )
    
    elif data == "team_startgame":
        await callback_query.answer("🚀 Opening START GAME guide...")
        await callback_query.message.reply_video(
            video=TEAM_STARTGAME_VIDEO_URL,
            caption="📌 START GAME - Use /startgame command when both teams are ready!"
        )
    
    elif data == "team_bowling":
        await callback_query.answer("🎯 Opening BOWLING guide...")
        await callback_query.message.reply_video(
            video=TEAM_BOWLING_VIDEO_URL,
            caption="📌 BOWLING - Use /bowling command to select the bowler!"
        )
    
    elif data == "team_batting":
        await callback_query.answer("🏏 Opening BATTING guide...")
        await callback_query.message.reply_video(
            video=TEAM_BATTING_VIDEO_URL,
            caption="📌 BATTING - Use /batting command to select the batsman!"
        )
    
    else:
        await callback_query.answer("⚙️ Feature coming soon!")


# ========== BATTING CALLBACK HANDLER ==========

async def handle_batting_callback(client: Client, callback_query: CallbackQuery, data: str):
    """Handle batting number selection"""
    user_id = callback_query.from_user.id
    message = callback_query.message
    group_id = message.chat.id
    
    match = await db.get_match(group_id)
    if not match:
        await callback_query.answer("❌ No active game found!", show_alert=True)
        await message.delete()
        return
    
    current_ball = match.get("current_ball", {})
    if not current_ball:
        await callback_query.answer("⏳ No active ball! Please wait.", show_alert=True)
        return
    
    striker = current_ball.get("striker", {})
    if striker.get("user_id") != user_id:
        await callback_query.answer("❌ You are not the current batter!", show_alert=True)
        return
    
    if data == "bat_out":
        batter_number = "OUT"
        await callback_query.answer("🏏 OUT selected!")
    else:
        batter_number = int(data.split("_")[1])
        await callback_query.answer(f"🏏 Batting number: {batter_number}")
    
    await game_timer.cancel_batter_timer(user_id)
    
    from team.commands import process_ball_response
    await process_ball_response(group_id, "batter", batter_number)
    
    await message.delete()


# ========== BOWLING CALLBACK HANDLER ==========

async def handle_bowling_callback(client: Client, callback_query: CallbackQuery, data: str):
    """Handle bowling number selection (from DM)"""
    user_id = callback_query.from_user.id
    message = callback_query.message
    
    if data.startswith("bowl_"):
        bowling_number = int(data.split("_")[1])
        await callback_query.answer(f"🎯 Bowling number: {bowling_number}")
        await game_timer.cancel_bowler_timer(user_id)
        
        group_id = await find_bowler_group(user_id)
        if group_id:
            from team.commands import process_ball_response
            await process_ball_response(group_id, "bowler", bowling_number)
        
        await message.delete()


async def find_bowler_group(bowler_id: int):
    """Find which group the bowler is currently playing in"""
    matches = await db.db.active_matches.find({}).to_list(None)
    for match in matches:
        if match.get("current_bowler", {}).get("user_id") == bowler_id:
            return match.get("group_id")
    return None


# ========== START/HELP CALLBACK HANDLERS ==========

async def handle_game_instructions(client: Client, callback_query: CallbackQuery):
    from handlers.start_help import game_instructions_keyboard
    await callback_query.message.delete()
    await callback_query.message.reply_photo(
        photo=GAME_INSTRUCTIONS_IMAGE_URL,
        caption=WELCOME_CAPTION,
        reply_markup=game_instructions_keyboard()
    )
    await callback_query.answer()


async def handle_solo_play(client: Client, callback_query: CallbackQuery):
    from handlers.start_help import back_keyboard
    SOLO_MODE_MESSAGE = """
🏏 **Solo Mode:**

• /solo_start: Begin a solo match
• /joingame: Join an ongoing solo match
• /end_match: End the current game
"""
    await callback_query.message.edit_text(
        SOLO_MODE_MESSAGE,
        reply_markup=back_keyboard()
    )
    await callback_query.answer()


async def handle_team_play(client: Client, callback_query: CallbackQuery):
    from handlers.start_help import team_mode_keyboard
    TEAM_MODE_MESSAGE = """
🌟 𝐌ᴇᴍʙᴇʀs 𝐀ᴅᴅɪɴɢ:

/add_A - add members to team A  
/add_B - add members to team B  

Eg: /add_A 1  or /add_A @username  
(Use the player number of your team)

🌟 𝐌ᴇᴍʙᴇʀs 𝐑ᴇᴍᴏᴠɪɴɢ:

/remove_A - remove members from team A  
/remove_B - remove members from team B  

Eg: /remove_A 2  
(Use the player number of your team)

🌟 𝐆ᴀᴍᴇ 𝐏ʟᴀʏ 𝐂ᴏᴍᴍᴀɴᴅs:

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
    await callback_query.message.edit_text(
        TEAM_MODE_MESSAGE,
        reply_markup=team_mode_keyboard()
    )
    await callback_query.answer()


async def handle_auction(client: Client, callback_query: CallbackQuery):
    from handlers.start_help import back_keyboard
    AUCTION_MESSAGE = "💰 Auction Mode Commands:\n/add_cap - add auction captain\n/start_auction - start auction"
    await callback_query.message.edit_text(
        AUCTION_MESSAGE,
        reply_markup=back_keyboard()
    )
    await callback_query.answer()


async def handle_home(client: Client, callback_query: CallbackQuery):
    from handlers.start_help import start_keyboard
    await callback_query.message.delete()
    await callback_query.message.reply_photo(
        photo=IMAGE_URL,
        caption=WELCOME_CAPTION,
        reply_markup=start_keyboard()
    )
    await callback_query.answer()


async def back_to_game_instructions(client: Client, callback_query: CallbackQuery):
    from handlers.start_help import game_instructions_keyboard
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=GAME_INSTRUCTIONS_IMAGE_URL,
            caption=WELCOME_CAPTION
        ),
        reply_markup=game_instructions_keyboard()
    )
    await callback_query.answer()