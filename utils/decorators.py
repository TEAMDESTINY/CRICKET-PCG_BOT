from functools import wraps
from database.mongodb import db

def host_only(func):
    """Decorator to check if user is the game host"""
    @wraps(func)
    async def wrapper(client, message):
        group_id = message.chat.id
        user_id = message.from_user.id
        
        match = await db.get_match(group_id)
        if not match:
            await message.reply("❌ No active game found! Use /create_team first.")
            return
        
        if match.get("host", {}).get("user_id") != user_id:
            await message.reply("❌ Only the game host can use this command!")
            return
        
        return await func(client, message)
    return wrapper

def game_active(func):
    """Decorator to check if game is active"""
    @wraps(func)
    async def wrapper(client, message):
        group_id = message.chat.id
        match = await db.get_match(group_id)
        
        if not match or match.get("status") == "completed":
            await message.reply("❌ No active game is going on in this chat!")
            return
        
        return await func(client, message)
    return wrapper

def captain_only(func):
    """Decorator to check if user is team captain"""
    @wraps(func)
    async def wrapper(client, message):
        group_id = message.chat.id
        user_id = message.from_user.id
        match = await db.get_match(group_id)
        
        if not match:
            await message.reply("❌ No active game found!")
            return
        
        # Check if user is captain of either team
        is_captain = False
        for team in ["team_a", "team_b"]:
            for player in match.get(team, {}).get("players", []):
                if player.get("user_id") == user_id and player.get("is_captain"):
                    is_captain = True
                    break
        
        if not is_captain:
            await message.reply("❌ Only team captains can use this command!")
            return
        
        return await func(client, message)
    return wrapper
