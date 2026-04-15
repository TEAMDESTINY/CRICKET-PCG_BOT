#!/usr/bin/env python3
import asyncio
import logging
import os
from dotenv import load_dotenv
from pyrogram import Client, idle
from config import BOT_TOKEN, BOT_USERNAME, OWNER_ID

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# Get API credentials from .env
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")

class CricketBot:
    def __init__(self):
        if API_ID == 0 or not API_HASH:
            logger.error("API_ID and API_HASH are required!")
            logger.error("Get them from https://my.telegram.org")
            raise ValueError("Missing API credentials")
        
        self.app = Client(
            "cricket_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN
        )
    
    async def start(self):
        logger.info("Starting Cricket Master Bot...")
        
        import handlers.start_help
        import handlers.callbacks
        import handlers.admin
        import team.host
        import team.team_manager
        import team.commands
        
        logger.info("All handlers loaded!")
        await self.app.start()
        logger.info(f"Bot @{BOT_USERNAME} is running!")
        await idle()
        await self.stop()
    
    async def stop(self):
        logger.info("Stopping bot...")
        await self.app.stop()

def main():
    bot = CricketBot()
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")

if __name__ == "__main__":
    main()
