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
from database.mongodb import db
from database.models import Match
from config import DEFAULT_OVERS

logging.basicConfig(level=logging.INFO)
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

Eg: /add_A 1  or /add_A @username  
(Use the player number of your team)

🌟 **Members Removing:**

/remove_A - remove members from team A  
/remove_B - remove members from team B  

Eg: /remove_A 2  
(Use the player number of your team)

🌟 **Game Play Commands:**

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
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("UPDATES", url=UPDATES_LINK),
            InlineKeyboardButton("SUPPORT", url=SUPPORT_LINK)
        ],
        [
            InlineKeyboardButton("ADD ME TO YOUR GROUP!", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ],
        [
            InlineKeyboardButton("PLAY ZONE", url=PLAYZONE_LINK),
            InlineKeyboardButton("LIVE SCORE", url=LIVE_SCORE_LINK)
        ]
    ])


def group_start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("I'm the Host 🏀", callback_data="iam_host")]
    ])


def game_instructions_keyboard():
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
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("BACK", callback_data="back_to_game_instructions")]
    ])


def team_mode_keyboard():
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
    try:
        await client.send_photo(
            chat_id=message.chat.id,
            photo=IMAGE_URL,
            caption=WELCOME_CAPTION,
            reply_markup=start_keyboard()
        )
    except Exception as e:
        logger.error(f"Start failed: {e}")
        await message.reply(f"Error: {e}")


@Client.on_message(filters.command("start") & filters.group)
async def start_group(client: Client, message: Message):
    await message.reply(
        "New Game Alert!\n\n"
        "Who will be the game host for this match? 😊\n\n"
        "Start a new match or join an existing one with your friends. Just type /start in groups.",
        reply_markup=group_start_keyboard()
    )


@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    await message.reply_text(HELP_MESSAGE, reply_markup=help_keyboard())


# ========== CALLBACKS ==========

@Client.on_callback_query()
async def start_help_callbacks(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    
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
        
        # I'm the Host Button (Group mein)
        elif data == "iam_host":
            await callback_query.answer()
            
            group_id = callback_query.message.chat.id
            user_id = callback_query.from_user.id
            user_name = callback_query.from_user.first_name
            
            # Create clickable mention
            mention = f"[{user_name}](tg://user?id={user_id})"
            
            # Check if already a game exists
            existing_match = await db.get_match(group_id)
            
            if existing_match:
                await callback_query.message.reply("❌ A game is already active in this chat!")
            else:
                # Create new match
                new_match = Match(
                    group_id=group_id,
                    host_id=user_id,
                    host_name=user_name,
                    total_overs=DEFAULT_OVERS
                )
                await db.save_match(group_id, new_match.to_dict())
                
                # Send message with clickable name (exactly like screenshot)
                await callback_query.message.reply(
                    f"> {mention}\n\n"
                    f"> {mention} is now the game host! Game host can create teams now by using /create_team. Let's get the match started! 😍❤️"
                )
        
        # ========== TEAM MODE VIDEOS ==========
        
        elif data == "team_start":
            await callback_query.answer("Opening START guide...")
            await callback_query.message.reply_video(
                video=TEAM_START_VIDEO_URL,
                caption="START - Use /create_team in your group to begin the match!"
            )
        
        elif data == "team_add":
            await callback_query.answer("Opening ADD guide...")
            await callback_query.message.reply_video(
                video=TEAM_ADD_VIDEO_URL,
                caption="ADD - Use /add_A and /add_B commands to add players!"
            )
        
        elif data == "team_remove":
            await callback_query.answer("Opening REMOVE guide...")
            await callback_query.message.reply_video(
                video=TEAM_REMOVE_VIDEO_URL,
                caption="REMOVE - Use /remove_A and /remove_B commands to remove players!"
            )
        
        elif data == "team_startgame":
            await callback_query.answer("Opening START GAME guide...")
            await callback_query.message.reply_video(
                video=TEAM_STARTGAME_VIDEO_URL,
                caption="START GAME - Use /startgame command when both teams are ready!"
            )
        
        elif data == "team_bowling":
            await callback_query.answer("Opening BOWLING guide...")
            await callback_query.message.reply_video(
                video=TEAM_BOWLING_VIDEO_URL,
                caption="BOWLING - Use /bowling command to select the bowler!"
            )
        
        elif data == "team_batting":
            await callback_query.answer("Opening BATTING guide...")
            await callback_query.message.reply_video(
                video=TEAM_BATTING_VIDEO_URL,
                caption="BATTING - Use /batting command to select the batsman!"
            )
        
        else:
            await callback_query.answer("Coming soon!", show_alert=True)
            
    except Exception as e:
        logger.error(f"Callback error: {data} - {e}")
        await callback_query.answer(f"Error: {e}", show_alert=True)