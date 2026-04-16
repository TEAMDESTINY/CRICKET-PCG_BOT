from pyrogram import Client, filters
from pyrogram.types import Message
from database.mongodb import db
from database.models import Player
from utils.decorators import host_only
from utils.validators import is_valid_player_number
from utils.helpers import get_mention
from team.messages import (
    TEAM_ADD_SUCCESS, TEAM_ADD_REPORT, TEAM_FULL, PLAYER_ALREADY_IN_TEAM,
    PLAYER_ALREADY_IN_OTHER_TEAM, PLAYER_NOT_FOUND, TEAM_REMOVE_SUCCESS,
    TEAM_REMOVE_REPORT, PLAYER_NOT_IN_TEAM, INVALID_PLAYER_NUMBER,
    NO_ACTIVE_GAME, TEAM_DISPLAY
)
from datetime import datetime
import re


# ========== HELPER FUNCTIONS ==========

async def get_user_info(client, username: str):
    """Get user info from username or user_id"""
    try:
        clean_username = username.lstrip('@')
        user = await client.get_users(clean_username)
        return user
    except Exception:
        return None


def format_player_list(players):
    """Format player list for display"""
    if not players:
        return "No players yet.\n"
    
    player_lines = []
    for player in players:
        captain_icon = " [🧢]" if player.get("is_captain") else ""
        player_lines.append(f"{player.get('number')}. {player.get('username')}{captain_icon}")
    
    return "\n".join(player_lines)


async def add_single_player(client, team_data, player_number, username, user_id, is_captain=False):
    """Add a single player to team"""
    for p in team_data.get("players", []):
        if p.get("user_id") == user_id:
            return False, "already_in_team", None
    
    new_player = {
        "number": player_number,
        "username": username,
        "user_id": user_id,
        "mention": get_mention(user_id, username),
        "is_captain": is_captain,
        "runs": 0,
        "balls": 0,
        "fours": 0,
        "sixes": 0,
        "is_out": False,
        "ball_by_ball": []
    }
    
    team_data["players"].append(new_player)
    return True, "success", new_player


# ========== ADD TO TEAM A ==========

@Client.on_message(filters.command("add_A") & filters.group)
@host_only
async def add_to_team_a(client: Client, message: Message):
    await add_to_team(client, message, "A")


# ========== ADD TO TEAM B ==========

@Client.on_message(filters.command("add_B") & filters.group)
@host_only
async def add_to_team_b(client: Client, message: Message):
    await add_to_team(client, message, "B")


async def add_to_team(client: Client, message: Message, team_letter: str):
    """Generic function to add players to a team"""
    group_id = message.chat.id
    args = message.text.split()
    
    if len(args) < 2:
        await message.reply(f"❌ Usage: /add_{team_letter} @username or /add_{team_letter} 1\n"
                           f"Example: /add_{team_letter} @player_name\n"
                           f"Mass add: /add_{team_letter} @user1 @user2 @user3")
        return
    
    # Get current match
    match = await db.get_match(group_id)
    if not match:
        await message.reply(NO_ACTIVE_GAME)
        return
    
    # Fix: Use lowercase keys
    team_key = f"team_{team_letter.lower()}"  # "team_a" or "team_b"
    other_team_key = f"team_{'b' if team_letter == 'A' else 'a'}"  # "team_b" or "team_a"
    
    # Initialize if keys don't exist
    if team_key not in match:
        match[team_key] = {"name": f"Team {team_letter}", "players": [], "score": 0, "wickets": 0, "overs": 0.0}
    if other_team_key not in match:
        match[other_team_key] = {"name": f"Team {'B' if team_letter == 'A' else 'A'}", "players": [], "score": 0, "wickets": 0, "overs": 0.0}
    
    team_data = match[team_key]
    other_team_data = match[other_team_key]
    max_players = 11
    
    current_players = team_data.get("players", [])
    
    # Check if team is full
    if len(current_players) >= max_players:
        await message.reply(TEAM_FULL.format(team=team_letter, max_players=max_players))
        return
    
    # Extract usernames from args
    usernames = []
    for arg in args[1:]:
        if re.match(r'^\d+$', arg):
            usernames.append(arg)
        else:
            clean = arg.lstrip('@')
            usernames.append(clean)
    
    results = {
        "success": [],
        "already_in_team": [],
        "already_in_other": [],
        "not_found": [],
        "team_full": False
    }
    
    next_number = len(current_players) + 1
    
    for username in usernames:
        if len(team_data["players"]) >= max_players:
            results["team_full"] = True
            break
        
        # Check if already in this team
        already_in = False
        for p in team_data["players"]:
            if p.get("username") == username or str(p.get("user_id")) == username:
                results["already_in_team"].append(username)
                already_in = True
                break
        
        if already_in:
            continue
        
        # Check if already in other team
        in_other = False
        for p in other_team_data.get("players", []):
            if p.get("username") == username or str(p.get("user_id")) == username:
                results["already_in_other"].append(username)
                in_other = True
                break
        
        if in_other:
            continue
        
        # Get user info
        user = await get_user_info(client, username)
        
        if user:
            is_captain = len(team_data["players"]) == 0
            
            new_player = {
                "number": next_number,
                "username": user.first_name or user.username or str(user.id),
                "user_id": user.id,
                "mention": get_mention(user.id, user.first_name or user.username or "Player"),
                "is_captain": is_captain,
                "runs": 0,
                "balls": 0,
                "fours": 0,
                "sixes": 0,
                "is_out": False,
                "ball_by_ball": []
            }
            
            team_data["players"].append(new_player)
            results["success"].append({
                "name": new_player["username"],
                "number": next_number,
                "is_captain": is_captain
            })
            next_number += 1
        else:
            results["not_found"].append(username)
    
    # Save to database
    await db.save_match(group_id, match)
    
    # Send response
    if len(usernames) == 1 and results["success"]:
        player_added = results["success"][0]
        player_list = format_player_list(team_data["players"])
        
        await message.reply(
            TEAM_ADD_SUCCESS.format(
                player_name=player_added["name"],
                team=team_letter,
                current_count=len(team_data["players"]),
                max_players=max_players,
                player_list=player_list
            )
        )
    else:
        success_list = [f"✅ {p['name']} (#{p['number']}){' [🧢]' if p['is_captain'] else ''}" 
                       for p in results["success"]]
        already_list = [f"⚠️ {name}: Already in Team {team_letter}" for name in results["already_in_team"]]
        other_list = [f"⚠️ {name}: Already in Team {other_team_key[-1].upper()}" for name in results["already_in_other"]]
        not_found_list = [f"❌ {name}: User not found" for name in results["not_found"]]
        
        all_results = success_list + already_list + other_list + not_found_list
        
        await message.reply(
            TEAM_ADD_REPORT.format(
                team=team_letter,
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                success_count=len(results["success"]),
                issue_count=len(results["already_in_team"]) + len(results["already_in_other"]) + len(results["not_found"]),
                results="\n".join(all_results) if all_results else "No players processed."
            )
        )


# ========== REMOVE FROM TEAM A ==========

@Client.on_message(filters.command("remove_A") & filters.group)
@host_only
async def remove_from_team_a(client: Client, message: Message):
    await remove_from_team(client, message, "A")


# ========== REMOVE FROM TEAM B ==========

@Client.on_message(filters.command("remove_B") & filters.group)
@host_only
async def remove_from_team_b(client: Client, message: Message):
    await remove_from_team(client, message, "B")


async def remove_from_team(client: Client, message: Message, team_letter: str):
    """Generic function to remove players from a team"""
    group_id = message.chat.id
    args = message.text.split()
    
    if len(args) != 2:
        await message.reply(f"❌ Usage: /remove_{team_letter} <player_number>\n"
                           f"Example: /remove_{team_letter} 2\n"
                           f"Mass remove: /remove_{team_letter} 1,2,3")
        return
    
    match = await db.get_match(group_id)
    if not match:
        await message.reply(NO_ACTIVE_GAME)
        return
    
    team_key = f"team_{team_letter.lower()}"
    
    if team_key not in match:
        await message.reply(f"❌ Team {team_letter} not found!")
        return
    
    team_data = match[team_key]
    
    numbers_str = args[1]
    player_numbers = []
    
    if ',' in numbers_str:
        for num in numbers_str.split(','):
            try:
                player_numbers.append(int(num.strip()))
            except ValueError:
                pass
    else:
        try:
            player_numbers.append(int(numbers_str))
        except ValueError:
            await message.reply(INVALID_PLAYER_NUMBER.format(max_players=11))
            return
    
    results = {
        "success": [],
        "not_found": []
    }
    
    for player_num in player_numbers:
        player_found = None
        for player in team_data.get("players", []):
            if player.get("number") == player_num:
                player_found = player
                break
        
        if player_found:
            team_data["players"].remove(player_found)
            results["success"].append({"name": player_found["username"], "number": player_num})
            
            for idx, player in enumerate(team_data["players"], 1):
                player["number"] = idx
        else:
            results["not_found"].append(player_num)
    
    await db.save_match(group_id, match)
    
    if len(player_numbers) == 1 and results["success"]:
        player_removed = results["success"][0]
        player_list = format_player_list(team_data["players"])
        
        await message.reply(
            TEAM_REMOVE_SUCCESS.format(
                player_name=player_removed["name"],
                team=team_letter,
                current_count=len(team_data["players"]),
                max_players=11,
                player_list=player_list
            )
        )
    else:
        success_list = [f"✅ {p['name']} (#{p['number']})" for p in results["success"]]
        not_found_list = [f"❌ #{num}: Player not found" for num in results["not_found"]]
        
        all_results = success_list + not_found_list
        
        await message.reply(
            TEAM_REMOVE_REPORT.format(
                team=team_letter,
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                success_count=len(results["success"]),
                issue_count=len(results["not_found"]),
                results="\n".join(all_results) if all_results else "No players processed."
            )
        )


# ========== SHOW TEAMS ==========

@Client.on_message(filters.command("show_teams") & filters.group)
async def show_teams_command(client: Client, message: Message):
    group_id = message.chat.id
    match = await db.get_match(group_id)
    
    if not match:
        await message.reply(NO_ACTIVE_GAME)
        return
    
    team_a = match.get("team_a", {})
    team_b = match.get("team_b", {})
    
    team_a_players = format_player_list(team_a.get("players", []))
    team_b_players = format_player_list(team_b.get("players", []))
    
    if not team_a_players:
        team_a_players = "No players yet. Use /add_A to add players.\n"
    if not team_b_players:
        team_b_players = "No players yet. Use /add_B to add players.\n"
    
    await message.reply(
        TEAM_DISPLAY.format(
            host_name=match.get("host", {}).get("username", "Unknown"),
            batting_team=match.get("batting_team", "None"),
            innings=match.get("current_innings", "None"),
            bowling_team=match.get("bowling_team", "None"),
            team_a_name=team_a.get("name", "Unknown"),
            team_b_name=team_b.get("name", "Unknown"),
            team_a_players=team_a_players,
            team_b_players=team_b_players
        )
    )