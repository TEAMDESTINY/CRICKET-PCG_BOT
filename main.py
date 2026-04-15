#!/usr/bin/env python3
import asyncio
import logging
from pyrogram import Client, filters
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create bot client
app = Client("cricket_bot", bot_token=BOT_TOKEN)

# ========== IMPORT ALL HANDLERS ==========

# DM/Help handlers
from handlers.start_help import start_private, start_group, help_command

# Team mode handlers
from team.host import create_team, end_match, show_teams, set_team_name, set_overs, show_host
from team.team_manager import add_to_team_a, add_to_team_b, remove_from_team_a, remove_from_team_b, show_teams_command
from team.commands import select_bowler, select_batsman, swap_teams

# ========== REGISTER DM/GROUP COMMANDS ==========

# Start commands
app.on_message(filters.command("start") & filters.private)(start_private)
app.on_message(filters.command("start") & filters.group)(start_group)

# Help command
app.on_message(filters.command("help"))(help_command)

# ========== REGISTER TEAM COMMANDS ==========

# Host commands
app.on_message(filters.command("create_team") & filters.group)(create_team)
app.on_message(filters.command("end_match") & filters.group)(end_match)
app.on_message(filters.command("teams") & filters.group)(show_teams)
app.on_message(filters.command("setname") & filters.group)(set_team_name)
app.on_message(filters.command("setovers") & filters.group)(set_overs)
app.on_message(filters.command("host") & filters.group)(show_host)

# Team management commands
app.on_message(filters.command("add_A") & filters.group)(add_to_team_a)
app.on_message(filters.command("add_B") & filters.group)(add_to_team_b)
app.on_message(filters.command("remove_A") & filters.group)(remove_from_team_a)
app.on_message(filters.command("remove_B") & filters.group)(remove_from_team_b)
app.on_message(filters.command("show_teams") & filters.group)(show_teams_command)

# Game play commands
app.on_message(filters.command("bowling") & filters.group)(select_bowler)
app.on_message(filters.command("batting") & filters.group)(select_batsman)
app.on_message(filters.command("swap") & filters.group)(swap_teams)

# ========== CALLBACK QUERY HANDLER ==========
from handlers.callbacks import handle_callbacks
app.on_callback_query()(handle_callbacks)

# ========== MAIN ==========

def main():
    logger.info("🚀 Starting Cricket Master Bot...")
    logger.info("✅ All handlers registered!")
    app.run()

if __name__ == "__main__":
    main()
