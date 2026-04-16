import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, CallbackQuery
from config import (
    IMAGE_URL, GAME_INSTRUCTIONS_IMAGE_URL,
    UPDATES_LINK, SUPPORT_LINK, PLAYZONE_LINK, LIVE_SCORE_LINK,
    OWNER_LINK, BOT_USERNAME, WELCOME_MESSAGE, HELP_MESSAGE,
    TEAM_START_VIDEO_URL, TEAM_BOWLING_VIDEO_URL, TEAM_BATTING_VIDEO_URL,
    TEAM_ADD_VIDEO_URL, TEAM_REMOVE_VIDEO_URL, TEAM_STARTGAME_VIDEO_URL
)

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========== MESSAGES ==========

WELCOME_CAPTION = """
🏏 **Welcome to Cricket Bot!**

🔴 **Live Cricket Scores:** Get real-time updates on live matches. Use /matches to see live scores.

🎮 **Manage Your Team:** Strategize, set your lineup, and play the game just like a pro captain.

🗽 **1 VS 1:** Find one vs one match /1v1

Use /help to learn more about the game.
"""

SOLO_MODE_MESSAGE = """
🏏 **Solo Mode:**

• /solo_start: Begin a solo match
• /joingame: Join an ongoing solo match
• /end_match: End the current game
• /feedback: Share your feedback

Ready to play? Let's see your skills on the field!
"""

TEAM_MODE_MESSAGE = """
🌟 **Members Adding:**

/add_A - add members to team A
/add_B - add members to team B

Example: /add_A 1 or /add_A @username

🌟 **Members Removing:**

/remove_A - remove members from team A
/remove_B - remove members from team B

Example: /remove_A 2

🌟 **Game Play Commands:**

/startgame - to start the game
/bowling - choose the bowling person
/batting - choose the batting person
/swap - to change the playing position
/end_match - to end the current game
/feedback - give your feedback
"""

AUCTION_MESSAGE = """
💰 **Auction Mode:**

/add_cap - add auction captain
/rm_cap - remove auction captain
/cap_change_auction - change the auction captain
/auction_id - send auction player id
/start_auction - start auction
/pause_auction - pause the auction
/resume_auction - resume the auction
/auction_host_change - change the auction host
/xp - auction player put value
/unsold - auction player unsold list
/rm_auction_id - remove auction sold player
"""


# ========== KEYBOARDS ==========

def start_keyboard():
    """Start command ke neeche buttons (DM mein)"""
    logger.debug("Creating start_keyboard")
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Updates", url=UPDATES_LINK),
            InlineKeyboardButton("Support", url=SUPPORT_LINK),
            InlineKeyboardButton("Play Zone", url=PLAYZONE_LINK),
            InlineKeyboardButton("Live Score", url=LIVE_SCORE_LINK)
        ],
        [
            InlineKeyboardButton("Add me to group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ]
    ])


def game_instructions_keyboard():
    """Game instructions ke neeche buttons"""
    logger.debug("Creating game_instructions_keyboard")
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Solo Play", callback_data="solo_play"),
            InlineKeyboardButton("Team Play", callback_data="team_play")
        ],
        [
            InlineKeyboardButton("Auction", callback_data="auction"),
            InlineKeyboardButton("Home", callback_data="home")
        ]
    ])


def help_keyboard():
    """Help command ke neeche buttons"""
    logger.debug("Creating help_keyboard")
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ADD ME TO GROUP", callback_data="add_to_group"),
            InlineKeyboardButton("Game Instructions", callback_data="game_instructions")
        ],
        [
            InlineKeyboardButton("UPDATES", url=UPDATES_LINK),
            InlineKeyboardButton("SUPPORT", url=SUPPORT_LINK)
        ],
        [
            InlineKeyboardButton("DEVELOPER", url=OWNER_LINK)
        ]
    ])


def back_keyboard():
    """Back button for returning to game instructions"""
    logger.debug("Creating back_keyboard")
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("BACK", callback_data="back_to_game_instructions")]
    ])


def team_mode_keyboard():
    """Team mode menu buttons"""
    logger.debug("Creating team_mode_keyboard")
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("START", callback_data="team_start"),
            InlineKeyboardButton("ADD", callback_data="team_add"),
            InlineKeyboardButton("REMOVE", callback_data="team_remove")
        ],
        [
            InlineKeyboardButton("START GAME", callback_data="team_startgame"),
            InlineKeyboardButton("BOWLING", callback_data="team_bowling"),
            InlineKeyboardButton("BATTING", callback_data="team_batting")
        ],
        [
            InlineKeyboardButton("BACK", callback_data="back_to_game_instructions")
        ]
    ])


# ========== HANDLERS ==========

@Client.on_message(filters.command("start") & filters.private)
async def start_private(client: Client, message: Message):
    """/start command in private chat (DM)"""
    try:
        logger.info(f"Start received from {message.from_user.id}")
        
        await client.send_photo(
            chat_id=message.chat.id,
            photo=IMAGE_URL,
            caption=WELCOME_CAPTION,
            reply_markup=start_keyboard()
        )
        
        logger.info("Start command success")
    except Exception as e:
        logger.error(f"Start command failed: {e}")
        await message.reply(f"Error: {str(e)}")


@Client.on_message(filters.command("start") & filters.group)
async def start_group(client: Client, message: Message):
    """/start command in group chat"""
    try:
        logger.info(f"Start in group from {message.from_user.id}")
        
        await message.reply(
            "🏏 Cricket Bot Active!\n\n"
            "Use /create_team to start a match!\n"
            "Use /help for all commands."
        )
        
        logger.info("Start group command success")
    except Exception as e:
        logger.error(f"Start group command failed: {e}")
        await message.reply(f"Error: {str(e)}")


@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """/help command"""
    try:
        logger.info(f"Help received from {message.from_user.id}")
        
        await message.reply_text(HELP_MESSAGE, reply_markup=help_keyboard())
        
        logger.info("Help command success")
    except Exception as e:
        logger.error(f"Help command failed: {e}")
        await message.reply(f"Error: {str(e)}")


# ========== CALLBACKS ==========

@Client.on_callback_query()
async def start_help_callbacks(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    logger.info(f"Callback received: {data} from {callback_query.from_user.id}")
    
    try:
        # Game Instructions
        if data == "game_instructions":
            await callback_query.message.delete()
            await callback_query.message.reply_photo(
                photo=GAME_INSTRUCTIONS_IMAGE_URL,
                caption=WELCOME_CAPTION,
                reply_markup=game_instructions_keyboard()
            )
            await callback_query.answer()
        
        # Solo Play Menu
        elif data == "solo_play":
            await callback_query.message.edit_text(
                SOLO_MODE_MESSAGE,
                reply_markup=back_keyboard()
            )
            await callback_query.answer()
        
        # Team Play Menu
        elif data == "team_play":
            await callback_query.message.edit_text(
                TEAM_MODE_MESSAGE,
                reply_markup=team_mode_keyboard()
            )
            await callback_query.answer()
        
        # Auction Menu
        elif data == "auction":
            await callback_query.message.edit_text(
                AUCTION_MESSAGE,
                reply_markup=back_keyboard()
            )
            await callback_query.answer()
        
        # Home
        elif data == "home":
            await callback_query.message.delete()
            await callback_query.message.reply_photo(
                photo=IMAGE_URL,
                caption=WELCOME_CAPTION,
                reply_markup=start_keyboard()
            )
            await callback_query.answer()
        
        # Back to Game Instructions
        elif data == "back_to_game_instructions":
            await callback_query.message.edit_media(
                media=InputMediaPhoto(
                    media=GAME_INSTRUCTIONS_IMAGE_URL,
                    caption=WELCOME_CAPTION
                ),
                reply_markup=game_instructions_keyboard()
            )
            await callback_query.answer()
        
        # Add to Group
        elif data == "add_to_group":
            await callback_query.answer("Use the button below to add me to your group!")
        
        # Team mode video callbacks
        elif data == "team_start":
            await callback_query.answer("Opening video...")
            await callback_query.message.reply_video(
                video=TEAM_START_VIDEO_URL,
                caption="START - Use /create_team in your group to begin!"
            )
        
        elif data == "team_bowling":
            await callback_query.answer("Opening video...")
            await callback_query.message.reply_video(
                video=TEAM_BOWLING_VIDEO_URL,
                caption="BOWLING - Use /bowling command in group to select bowler!"
            )
        
        elif data == "team_batting":
            await callback_query.answer("Opening video...")
            await callback_query.message.reply_video(
                video=TEAM_BATTING_VIDEO_URL,
                caption="BATTING - Use /batting command in group to select batsman!"
            )
        
        elif data == "team_add":
            await callback_query.answer("Opening video...")
            await callback_query.message.reply_video(
                video=TEAM_ADD_VIDEO_URL,
                caption="ADD PLAYERS - Use /add_A and /add_B commands in group!"
            )
        
        elif data == "team_remove":
            await callback_query.answer("Opening video...")
            await callback_query.message.reply_video(
                video=TEAM_REMOVE_VIDEO_URL,
                caption="REMOVE PLAYERS - Use /remove_A and /remove_B commands in group!"
            )
        
        elif data == "team_startgame":
            await callback_query.answer("Opening video...")
            await callback_query.message.reply_video(
                video=TEAM_STARTGAME_VIDEO_URL,
                caption="START GAME - Use /startgame command in group when teams are ready!"
            )
        
        else:
            await callback_query.answer("Coming soon!", show_alert=True)
            
    except Exception as e:
        logger.error(f"Callback failed: {data} - {e}")
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)
