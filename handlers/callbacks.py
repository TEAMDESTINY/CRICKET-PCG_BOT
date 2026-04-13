from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.mongodb import db
from team.game_engine import game_engine
from team.buttons import get_batting_buttons, get_bowling_buttons, get_live_score_button
from team.scorecard import scorecard_gen
from team.timers import game_timer
from config import (
    LIVE_SCORE_CHANNEL_LINK, UPDATES_LINK, SUPPORT_LINK, 
    OWNER_LINK, BOT_USERNAME, WICKET_VIDEO_URL, OUT_VIDEO_URL
)
import asyncio


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
        # Just open channel link - no action needed, button handles URL
    
    # ========== BACK TO GROUP CALLBACK ==========
    elif data == "back_to_group":
        await callback_query.answer("🔙 Returning to group...")
        # Button with URL handles this
    
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
    
    # ========== TEAM MODE CALLBACKS (from team menu) ==========
    elif data == "team_start":
        await callback_query.answer("⚙️ Use /create_team in your group to start a match!", show_alert=True)
    
    elif data == "team_add":
        await callback_query.answer("⚙️ Use /add_A and /add_B commands in your group!", show_alert=True)
    
    elif data == "team_remove":
        await callback_query.answer("⚙️ Use /remove_A and /remove_B commands in your group!", show_alert=True)
    
    elif data == "team_startgame":
        await callback_query.answer("⚙️ Use /startgame command in your group after teams are ready!", show_alert=True)
    
    elif data == "team_bowling":
        await callback_query.answer("⚙️ Use /bowling command in your group!", show_alert=True)
    
    elif data == "team_batting":
        await callback_query.answer("⚙️ Use /batting command in your group!", show_alert=True)
    
    else:
        await callback_query.answer("⚙️ Feature coming soon!")


# ========== BATTING CALLBACK HANDLER ==========

async def handle_batting_callback(client: Client, callback_query: CallbackQuery, data: str):
    """Handle batting number selection"""
    user_id = callback_query.from_user.id
    message = callback_query.message
    group_id = message.chat.id
    
    # Get current match
    match = await db.get_match(group_id)
    if not match:
        await callback_query.answer("❌ No active game found!", show_alert=True)
        await message.delete()
        return
    
    # Check if it's the batter's turn
    current_ball = match.get("current_ball", {})
    if not current_ball:
        await callback_query.answer("⏳ No active ball! Please wait.", show_alert=True)
        return
    
    striker = current_ball.get("striker", {})
    if striker.get("user_id") != user_id:
        await callback_query.answer("❌ You are not the current batter!", show_alert=True)
        return
    
    # Extract batting number
    if data == "bat_out":
        batter_number = "OUT"
        await callback_query.answer("🏏 OUT selected!")
    else:
        batter_number = int(data.split("_")[1])
        await callback_query.answer(f"🏏 Batting number: {batter_number}")
    
    # Cancel batter timer
    await game_timer.cancel_batter_timer(user_id)
    
    # Process response
    from team.commands import process_ball_response
    await process_ball_response(group_id, "batter", batter_number)
    
    # Delete the batting message
    await message.delete()


# ========== BOWLING CALLBACK HANDLER ==========

async def handle_bowling_callback(client: Client, callback_query: CallbackQuery, data: str):
    """Handle bowling number selection (from DM)"""
    user_id = callback_query.from_user.id
    message = callback_query.message
    
    # Get group_id from match data (need to find which group this bowler is in)
    # For now, we need to store bowler's group association
    # This is a simplified version - in production, store user's active match
    
    # Extract bowling number
    if data.startswith("bowl_"):
        bowling_number = int(data.split("_")[1])
        await callback_query.answer(f"🎯 Bowling number: {bowling_number}")
        
        # Cancel bowler timer
        await game_timer.cancel_bowler_timer(user_id)
        
        # Find which group this bowler belongs to
        # For now, we'll need to implement a user_match mapping
        # Simplified: search through active matches
        group_id = await find_bowler_group(user_id)
        
        if group_id:
            from team.commands import process_ball_response
            await process_ball_response(group_id, "bowler", bowling_number)
        
        # Delete the bowling message
        await message.delete()


async def find_bowler_group(bowler_id: int):
    """Find which group the bowler is currently playing in"""
    # Get all active matches
    # This is a simplified version
    # In production, maintain a mapping of user_id -> group_id
    from database.mongodb import db
    # For now, return None - will be implemented properly
    return None


# ========== START/HELP CALLBACK HANDLERS ==========

async def handle_game_instructions(client: Client, callback_query: CallbackQuery):
    """Show game instructions menu"""
    from handlers.start_help import game_instructions_keyboard, WELCOME_CAPTION
    from config import GAME_INSTRUCTIONS_IMAGE_URL
    
    await callback_query.message.delete()
    await callback_query.message.reply_photo(
        photo=GAME_INSTRUCTIONS_IMAGE_URL,
        caption=WELCOME_CAPTION,
        reply_markup=game_instructions_keyboard()
    )
    await callback_query.answer()


async def handle_solo_play(client: Client, callback_query: CallbackQuery):
    """Show solo mode menu"""
    from handlers.start_help import back_keyboard, SOLO_MODE_MESSAGE
    
    await callback_query.message.edit_text(
        SOLO_MODE_MESSAGE,
        reply_markup=back_keyboard()
    )
    await callback_query.answer()


async def handle_team_play(client: Client, callback_query: CallbackQuery):
    """Show team mode menu"""
    from handlers.start_help import team_mode_keyboard, TEAM_MODE_MESSAGE
    
    await callback_query.message.edit_text(
        TEAM_MODE_MESSAGE,
        reply_markup=team_mode_keyboard()
    )
    await callback_query.answer()


async def handle_auction(client: Client, callback_query: CallbackQuery):
    """Show auction menu"""
    from handlers.start_help import back_keyboard, AUCTION_MESSAGE
    
    await callback_query.message.edit_text(
        AUCTION_MESSAGE,
        reply_markup=back_keyboard()
    )
    await callback_query.answer()


async def handle_home(client: Client, callback_query: CallbackQuery):
    """Return to home/start menu"""
    from handlers.start_help import start_keyboard, WELCOME_CAPTION
    from config import IMAGE_URL
    
    await callback_query.message.delete()
    await callback_query.message.reply_photo(
        photo=IMAGE_URL,
        caption=WELCOME_CAPTION,
        reply_markup=start_keyboard()
    )
    await callback_query.answer()


async def back_to_game_instructions(client: Client, callback_query: CallbackQuery):
    """Back to game instructions menu"""
    from handlers.start_help import game_instructions_keyboard, WELCOME_CAPTION
    from config import GAME_INSTRUCTIONS_IMAGE_URL
    from pyrogram.types import InputMediaPhoto
    
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=GAME_INSTRUCTIONS_IMAGE_URL,
            caption=WELCOME_CAPTION
        ),
        reply_markup=game_instructions_keyboard()
    )
    await callback_query.answer()


# ========== FEEDBACK CALLBACK ==========

@Client.on_message(filters.command("feedback"))
async def feedback_command(client: Client, message):
    """Handle feedback command"""
    feedback_text = message.text.replace("/feedback", "").strip()
    
    if not feedback_text:
        await message.reply(
            "📝 Please provide your feedback after the command.\n"
            "Example: /feedback Great game! Love playing it."
        )
        return
    
    # Forward to owner
    from config import OWNER_ID, OWNER_LINK
    
    try:
        await client.send_message(
            chat_id=OWNER_ID,
            text=f"📝 **New Feedback from** {message.from_user.first_name}\n"
                 f"👤 User: {message.from_user.id}\n"
                 f"💬 Feedback: {feedback_text}"
        )
        await message.reply("✅ Thank you for your feedback! We appreciate it.")
    except Exception as e:
        await message.reply("❌ Could not send feedback. Please try again later.")
