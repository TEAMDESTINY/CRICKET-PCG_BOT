from pyrogram import Client, filters
from pyrogram.types import Message
from database.mongodb import db
from database.models import Match
from utils.decorators import host_only
from team.messages import (
    CREATE_TEAM_SUCCESS, ALREADY_HOST_EXISTS, 
    NO_ACTIVE_GAME, END_MATCH_SUCCESS
)
from config import DEFAULT_OVERS
import asyncio


# ========== CREATE TEAM COMMAND ==========

@Client.on_message(filters.command("create_team") & filters.group)
async def create_team(client: Client, message: Message):
    """
    /create_team - Start a new game and become host
    Only one game can be active per group at a time
    """
    group_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    # Check if there's already an active game
    existing_match = await db.get_match(group_id)
    
    if existing_match:
        host_name = existing_match.get("host", {}).get("username", "Unknown")
        await message.reply(ALREADY_HOST_EXISTS.format(host_name=host_name))
        return
    
    # Create new match
    new_match = Match(
        group_id=group_id,
        host_id=user_id,
        host_name=user_name,
        total_overs=DEFAULT_OVERS
    )
    
    # Save to database
    await db.save_match(group_id, new_match.to_dict())
    
    # Send success message
    await message.reply(
        CREATE_TEAM_SUCCESS.format(host_name=user_name),
        disable_web_page_preview=True
    )


# ========== END MATCH COMMAND ==========

@Client.on_message(filters.command("end_match") & filters.group)
@host_only
async def end_match(client: Client, message: Message):
    """
    /end_match - End the current game (host only)
    """
    group_id = message.chat.id
    
    # Get current match
    match = await db.get_match(group_id)
    
    if not match:
        await message.reply(NO_ACTIVE_GAME)
        return
    
    # Send confirmation prompt
    confirm_msg = await message.reply(
        "⚠️ **Are you sure you want to end the current match?**\n\n"
        "Type /end_match_confirm within 10 seconds to confirm.\n"
        "Type /cancel to cancel."
    )
    
    # Wait for confirmation
    def is_confirmation(msg):
        return (msg.chat.id == group_id and 
                msg.from_user.id == match["host"]["user_id"] and
                msg.text in ["/end_match_confirm", "/cancel"])
    
    try:
        confirmation = await client.wait_for_message(
            timeout=10,
            filters=filters.create(is_confirmation)
        )
        
        if confirmation.text == "/end_match_confirm":
            # Save match to history before deleting
            await db.save_to_history(match)
            
            # Delete active match
            await db.delete_match(group_id)
            
            await confirm_msg.edit(END_MATCH_SUCCESS)
        else:
            await confirm_msg.edit("✅ Match end cancelled. Continue playing!")
            
    except asyncio.TimeoutError:
        await confirm_msg.edit("⏰ Timeout! Match end cancelled.")


@Client.on_message(filters.command("end_match_confirm") & filters.group)
async def end_match_confirm(client: Client, message: Message):
    """Handle end match confirmation (triggered by wait_for_message)"""
    # This is handled by the wait_for_message above
    # Just pass through
    pass


@Client.on_message(filters.command("cancel") & filters.group)
async def cancel_end_match(client: Client, message: Message):
    """Cancel end match command"""
    # This is handled by the wait_for_message above
    pass


# ========== CHECK TEAMS STATUS ==========

@Client.on_message(filters.command("teams") & filters.group)
async def show_teams(client: Client, message: Message):
    """
    /teams - Show current teams status
    """
    group_id = message.chat.id
    match = await db.get_match(group_id)
    
    if not match:
        await message.reply(NO_ACTIVE_GAME)
        return
    
    team_a = match.get("team_a", {})
    team_b = match.get("team_b", {})
    
    # Format team A players
    team_a_players = ""
    for player in team_a.get("players", []):
        captain_icon = " [🧢]" if player.get("is_captain") else ""
        team_a_players += f"{player.get('number')}. {player.get('username')}{captain_icon}\n"
    
    # Format team B players
    team_b_players = ""
    for player in team_b.get("players", []):
        captain_icon = " [🧢]" if player.get("is_captain") else ""
        team_b_players += f"{player.get('number')}. {player.get('username')}{captain_icon}\n"
    
    if not team_a_players:
        team_a_players = "No players yet. Use /add_A to add players.\n"
    if not team_b_players:
        team_b_players = "No players yet. Use /add_B to add players.\n"
    
    team_display = f"""
👽 **Game Host:** {match.get('host', {}).get('username')}

🏏 **Batting:** Team {match.get('batting_team', 'None')} (Innings {match.get('current_innings', 'None')})
🎯 **Bowling:** Team {match.get('bowling_team', 'None')}

🎩 **Team A:** {team_a.get('name', 'Team A')}
👒 **Team B:** {team_b.get('name', 'Team B')}

🔵 **Team A** ({len(team_a.get('players', []))}/11 players)
{team_a_players}

🔴 **Team B** ({len(team_b.get('players', []))}/11 players)
{team_b_players}
"""
    
    await message.reply(team_display)


# ========== SET TEAM NAME ==========

@Client.on_message(filters.command("setname") & filters.group)
@host_only
async def set_team_name(client: Client, message: Message):
    """
    /setname A Team_Warriors - Set team name
    /setname B Team_Champions
    """
    group_id = message.chat.id
    args = message.text.split(maxsplit=2)
    
    if len(args) < 3:
        await message.reply(
            "❌ Usage: /setname A Team_Name\n"
            "Or: /setname B Team_Name\n\n"
            "Example: /setname A Royal Challengers"
        )
        return
    
    team_letter = args[1].upper()
    team_name = args[2]
    
    if team_letter not in ["A", "B"]:
        await message.reply("❌ Please specify A or B for team name.")
        return
    
    match = await db.get_match(group_id)
    if not match:
        await message.reply(NO_ACTIVE_GAME)
        return
    
    # Update team name
    team_key = f"team_{team_letter.lower()}"
    match[team_key]["name"] = team_name
    await db.save_match(group_id, match)
    
    await message.reply(f"✅ Team {team_letter} name changed to: **{team_name}**")


# ========== SET OVERS ==========

@Client.on_message(filters.command("setovers") & filters.group)
@host_only
async def set_overs(client: Client, message: Message):
    """
    /setovers 10 - Set number of overs for the match
    """
    group_id = message.chat.id
    args = message.text.split()
    
    if len(args) != 2:
        await message.reply("❌ Usage: /setovers <overs_count>\nExample: /setovers 10")
        return
    
    try:
        overs = int(args[1])
        if overs < 1 or overs > 20:
            await message.reply("❌ Overs must be between 1 and 20!")
            return
    except ValueError:
        await message.reply("❌ Please provide a valid number!")
        return
    
    match = await db.get_match(group_id)
    if not match:
        await message.reply(NO_ACTIVE_GAME)
        return
    
    match["total_overs"] = overs
    await db.save_match(group_id, match)
    
    await message.reply(f"✅ Match overs set to: **{overs} overs**")


# ========== HOST INFO ==========

@Client.on_message(filters.command("host") & filters.group)
async def show_host(client: Client, message: Message):
    """
    /host - Show current game host
    """
    group_id = message.chat.id
    match = await db.get_match(group_id)
    
    if not match:
        await message.reply(NO_ACTIVE_GAME)
        return
    
    host = match.get("host", {})
    host_name = host.get("username", "Unknown")
    host_id = host.get("user_id")
    
    await message.reply(
        f"👑 **Game Host:** [{host_name}](tg://user?id={host_id})\n\n"
        f"📊 **Match Status:** {match.get('status', 'unknown')}\n"
        f"🏏 **Overs:** {match.get('total_overs', 10)} overs"
    )
