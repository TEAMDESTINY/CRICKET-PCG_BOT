import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, CallbackQuery
from pyrogram.enums import ButtonStyle
from config import (
    IMAGE_URL, GAME_INSTRUCTIONS_IMAGE_URL,
    UPDATES_LINK, SUPPORT_LINK, PLAYZONE_LINK, LIVE_SCORE_LINK,
    OWNER_LINK, BOT_USERNAME, WELCOME_MESSAGE, HELP_MESSAGE
)

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========== MESSAGES ==========

WELCOME_CAPTION = """
🏏 𝐖ᴇʟᴄᴏᴍᴇ 𝐭ᴏ 𝐂ʀɪᴄᴋᴇᴛ 𝐁ᴏᴛ!


🔴 𝐋ɪᴠᴇ 𝐂ʀɪᴄᴋᴇᴛ 𝐒ᴄᴏʀᴇs: Get real-time updates on live matches. Use /matches to see live scores.

🎮 𝐌ᴀɴᴀɢᴇ 𝐘ᴏᴜʀ 𝐓ᴇᴀᴍ: Strategize, set your lineup, and play the game just like a pro captain.

🗽 1_VS_1 : Find one vs one match /1v1

Use /help to learn more about the game.
"""

SOLO_MODE_MESSAGE = """
🏏 **Solo Mode:**

• /solo_start: Begin a solo match. Use the Solo button.
  - Next: Select your bowling mode by clicking Choose Random or Group Volunteer.

• /joingame: Join an ongoing solo match.

• /end_match: End the current game.

• /feedback: Share your feedback about the game and help us improve!

Ready to play? Let's see your skills on the field! 🌟
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
💰 **Auction Mode:**

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


# ========== KEYBOARDS ==========

def start_keyboard():
    """Start command ke neeche buttons (DM mein)"""
    logger.debug("Creating start_keyboard")
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📢 Updates", url=UPDATES_LINK),
            InlineKeyboardButton("🔗 Support", url=SUPPORT_LINK),
            InlineKeyboardButton("🏏 Play Zone", url=PLAYZONE_LINK),
            InlineKeyboardButton("📊 Live Score", url=LIVE_SCORE_LINK)
        ],
        [
            InlineKeyboardButton("➕ Add me to group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ]
    ])


def game_instructions_keyboard():
    """Game instructions ke neeche buttons (Solo, Team, Auction, Home)"""
    logger.debug("Creating game_instructions_keyboard")
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎯 Solo Play", callback_data="solo_play", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton("👥 Team Play", callback_data="team_play", style=ButtonStyle.PRIMARY)
        ],
        [
            InlineKeyboardButton("💰 Auction", callback_data="auction", style=ButtonStyle.DANGER),
            InlineKeyboardButton("🏠 Home", callback_data="home", style=ButtonStyle.DEFAULT)
        ]
    ])


def help_keyboard():
    """Help command ke neeche buttons"""
    logger.debug("Creating help_keyboard")
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ ADD ME TO GROUP", callback_data="add_to_group", style=ButtonStyle.SUCCESS),
            InlineKeyboardButton("🎯 Game Instructions", callback_data="game_instructions", style=ButtonStyle.PRIMARY)
        ],
        [
            InlineKeyboardButton("📢 UPDATES", url=UPDATES_LINK, style=ButtonStyle.DEFAULT),
            InlineKeyboardButton("🔗 SUPPORT", url=SUPPORT_LINK, style=ButtonStyle.DEFAULT)
        ],
        [
            InlineKeyboardButton("👨‍💻 DEVELOPER", url=OWNER_LINK, style=ButtonStyle.DEFAULT)
        ]
    ])


def back_keyboard():
    """Back button for returning to game instructions"""
    logger.debug("Creating back_keyboard")
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("◀️ BACK", callback_data="back_to_game_instructions", style=ButtonStyle.DEFAULT)]
    ])


def team_mode_keyboard():
    """Team mode menu buttons"""
    logger.debug("Creating team_mode_keyboard")
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("START", callback_data="team_start", style=ButtonStyle.SUCCESS),
            InlineKeyboardButton("ADD", callback_data="team_add", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton("REMOVE", callback_data="team_remove", style=ButtonStyle.DANGER)
        ],
        [
            InlineKeyboardButton("START GAME", callback_data="team_startgame", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton("BOWLING", callback_data="team_bowling", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton("BATTING", callback_data="team_batting", style=ButtonStyle.PRIMARY)
        ],
        [
            InlineKeyboardButton("◀️ BACK", callback_data="back_to_game_instructions", style=ButtonStyle.DEFAULT)
        ]
    ])


# ========== HANDLERS WITH DEBUG ==========

@Client.on_message(filters.command("start") & filters.private)
async def start_private(client: Client, message: Message):
    """/start command in private chat (DM)"""
    try:
        logger.info(f"===== /start COMMAND RECEIVED =====")
        logger.info(f"User: {message.from_user.id} - {message.from_user.first_name}")
        logger.info(f"Chat ID: {message.chat.id}")
        logger.info(f"Message text: {message.text}")
        
        logger.debug(f"Sending photo to user: {message.chat.id}")
        logger.debug(f"Photo URL: {IMAGE_URL}")
        
        await client.send_photo(
            chat_id=message.chat.id,
            photo=IMAGE_URL,
            caption=WELCOME_CAPTION,
            reply_markup=start_keyboard()
        )
        
        logger.info(f"===== /start COMMAND SUCCESS =====")
    except Exception as e:
        logger.error(f"===== /start COMMAND FAILED =====")
        logger.error(f"Error: {e}")
        logger.exception("Full traceback:")
        await message.reply(f"❌ Error: {str(e)}")


@Client.on_message(filters.command("start") & filters.group)
async def start_group(client: Client, message: Message):
    """/start command in group chat"""
    try:
        logger.info(f"===== /start COMMAND IN GROUP =====")
        logger.info(f"Group ID: {message.chat.id}")
        logger.info(f"User: {message.from_user.id}")
        
        await message.reply(
            "🏏 **Cricket Bot Active!**\n\n"
            "Use /create_team to start a match!\n"
            "Use /help for all commands."
        )
        
        logger.info(f"===== /start GROUP COMMAND SUCCESS =====")
    except Exception as e:
        logger.error(f"===== /start GROUP COMMAND FAILED =====")
        logger.error(f"Error: {e}")
        await message.reply(f"❌ Error: {str(e)}")


@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """/help command - shows help message with buttons"""
    try:
        logger.info(f"===== /help COMMAND RECEIVED =====")
        logger.info(f"User: {message.from_user.id}")
        logger.info(f"Chat ID: {message.chat.id}")
        
        await message.reply_text(HELP_MESSAGE, reply_markup=help_keyboard())
        
        logger.info(f"===== /help COMMAND SUCCESS =====")
    except Exception as e:
        logger.error(f"===== /help COMMAND FAILED =====")
        logger.error(f"Error: {e}")
        await message.reply(f"❌ Error: {str(e)}")


# ========== CALLBACKS WITH DEBUG ==========

@Client.on_callback_query()
async def start_help_callbacks(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    logger.info(f"===== CALLBACK RECEIVED =====")
    logger.info(f"Callback data: {data}")
    logger.info(f"User: {callback_query.from_user.id}")
    
    try:
        # Game Instructions - Show main menu with Solo/Team/Auction
        if data == "game_instructions":
            logger.debug("Processing game_instructions callback")
            await callback_query.message.delete()
            await callback_query.message.reply_photo(
                photo=GAME_INSTRUCTIONS_IMAGE_URL,
                caption=WELCOME_CAPTION,
                reply_markup=game_instructions_keyboard()
            )
            await callback_query.answer()
            logger.debug("game_instructions callback completed")
        
        # Solo Play Menu
        elif data == "solo_play":
            logger.debug("Processing solo_play callback")
            await callback_query.message.edit_text(
                SOLO_MODE_MESSAGE,
                reply_markup=back_keyboard()
            )
            await callback_query.answer()
            logger.debug("solo_play callback completed")
        
        # Team Play Menu
        elif data == "team_play":
            logger.debug("Processing team_play callback")
            await callback_query.message.edit_text(
                TEAM_MODE_MESSAGE,
                reply_markup=team_mode_keyboard()
            )
            await callback_query.answer()
            logger.debug("team_play callback completed")
        
        # Auction Menu
        elif data == "auction":
            logger.debug("Processing auction callback")
            await callback_query.message.edit_text(
                AUCTION_MESSAGE,
                reply_markup=back_keyboard()
            )
            await callback_query.answer()
            logger.debug("auction callback completed")
        
        # Home - Back to main start menu
        elif data == "home":
            logger.debug("Processing home callback")
            await callback_query.message.delete()
            await callback_query.message.reply_photo(
                photo=IMAGE_URL,
                caption=WELCOME_CAPTION,
                reply_markup=start_keyboard()
            )
            await callback_query.answer()
            logger.debug("home callback completed")
        
        # Back to Game Instructions
        elif data == "back_to_game_instructions":
            logger.debug("Processing back_to_game_instructions callback")
            await callback_query.message.edit_media(
                media=InputMediaPhoto(
                    media=GAME_INSTRUCTIONS_IMAGE_URL,
                    caption=WELCOME_CAPTION
                ),
                reply_markup=game_instructions_keyboard()
            )
            await callback_query.answer()
            logger.debug("back_to_game_instructions callback completed")
        
        # Add to Group
        elif data == "add_to_group":
            logger.debug("Processing add_to_group callback")
            await callback_query.answer("🔗 Use the button below to add me to your group!")
        
        # Team mode callbacks (will be implemented later)
        elif data in ["team_start", "team_add", "team_remove", "team_startgame", "team_bowling", "team_batting"]:
            logger.debug(f"Processing {data} callback (coming soon)")
            await callback_query.answer("⚙️ This feature is coming soon! Use commands in group.", show_alert=True)
        
        else:
            logger.warning(f"Unknown callback data: {data}")
            await callback_query.answer("Unknown command!", show_alert=True)
            
    except Exception as e:
        logger.error(f"===== CALLBACK FAILED =====")
        logger.error(f"Callback data: {data}")
        logger.error(f"Error: {e}")
        logger.exception("Full traceback:")
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)
