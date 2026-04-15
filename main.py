#!/usr/bin/env python3
"""
Cricket Master Bot - Main Entry Point
A complete cricket game bot for Telegram
"""

import asyncio
import logging
from pyrogram import Client, idle
from config import BOT_TOKEN, BOT_USERNAME, OWNER_ID

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # DEBUG mode for more info
)
logger = logging.getLogger(__name__)

# Bot information
BOT_INFO = {
    "name": "Cricket Master Bot",
    "version": "1.0.0",
    "author": "Sparsh",
    "description": "A complete cricket game bot for Telegram with Team Mode and Solo Mode"
}


class CricketBot:
    """Main bot class"""
    
    def __init__(self):
        # Pyrogram will auto-detect API credentials from telegram.org
        # Sirf bot_token do, baaki auto handle hoga
        self.app = Client(
            "cricket_bot",
            bot_token=BOT_TOKEN
            # API ID and Hash optional - Pyrogram handles automatically
        )
    
    async def start(self):
        """Start the bot and load all handlers"""
        logger.info(f"Starting {BOT_INFO['name']} v{BOT_INFO['version']}...")
        
        # Import all handlers to register them
        try:
            import handlers.start_help
            import handlers.callbacks
            import handlers.admin
            import team.host
            import team.team_manager
            import team.commands
            logger.info("All handlers loaded successfully!")
        except Exception as e:
            logger.error(f"Failed to load handlers: {e}")
            raise
        
        # Start the bot
        await self.app.start()
        logger.info(f"Bot @{BOT_USERNAME} is running!")
        
        # Send startup message to owner
        try:
            await self.app.send_message(
                OWNER_ID,
                f"✅ {BOT_INFO['name']} v{BOT_INFO['version']} has started!"
            )
        except Exception as e:
            logger.warning(f"Could not send startup message to owner: {e}")
        
        # Keep bot running
        await idle()
        
        # Cleanup
        await self.stop()
    
    async def stop(self):
        """Stop the bot and cleanup"""
        logger.info("Stopping bot...")
        await self.app.stop()
        logger.info("Bot stopped!")


def main():
    """Main entry point"""
    bot = CricketBot()
    
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        raise


if __name__ == "__main__":
    main()
