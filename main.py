#!/usr/bin/env python3
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, BOT_USERNAME, OWNER_ID, IMAGE_URL

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create bot client
app = Client("cricket_bot", bot_token=BOT_TOKEN)

# ========== HANDLERS ==========

@app.on_message(filters.command("start") & filters.private)
async def start_private(client: Client, message: Message):
    """/start command in private chat"""
    logger.info(f"Start received from {message.from_user.id}")
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📢 Updates", url="https://t.me/your_updates"),
            InlineKeyboardButton("🔗 Support", url="https://t.me/your_support")
        ],
        [
            InlineKeyboardButton("➕ Add me to group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ]
    ])
    
    await message.reply_photo(
        photo=IMAGE_URL,
        caption="🏏 **Welcome to Cricket Master Bot!**\n\nCricket Game Bot provide Solo play and Team play option available.",
        reply_markup=keyboard
    )

@app.on_message(filters.command("start") & filters.group)
async def start_group(client: Client, message: Message):
    """/start command in group"""
    await message.reply("🏏 **Cricket Bot Active!**\n\nUse /create_team to start a match!")

@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """/help command"""
    await message.reply("Send /start to begin!")

@app.on_message(filters.command("create_team"))
async def create_team(client: Client, message: Message):
    """/create_team command"""
    await message.reply(f"🎮 {message.from_user.first_name} is now the game host!")

@app.on_message(filters.command("add_A"))
async def add_team_a(client: Client, message: Message):
    """/add_A command"""
    await message.reply(f"✅ Added to Team A")

@app.on_message(filters.command("add_B"))
async def add_team_b(client: Client, message: Message):
    """/add_B command"""
    await message.reply(f"✅ Added to Team B")

# ========== MAIN ==========

def main():
    logger.info("Starting Cricket Bot...")
    app.run()

if __name__ == "__main__":
    main()
