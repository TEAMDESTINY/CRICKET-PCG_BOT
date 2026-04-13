from pyrogram import Client, filters
from config import ADMIN_IDS, OWNER_ID
from database.mongodb import db


def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_IDS or user_id == OWNER_ID


@Client.on_message(filters.command("stats") & filters.private)
async def bot_stats(client: Client, message):
    """Show bot statistics (admin only)"""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        await message.reply("❌ You are not authorized to use this command!")
        return
    
    # Get stats from database
    try:
        active_matches = await db.db.active_matches.count_documents({})
        total_users = await db.db.users.count_documents({})
        match_history = await db.db.match_history.count_documents({})
        
        stats_text = f"""
📊 **Bot Statistics**

🤖 Bot Name: Cricket Master Bot
📅 Status: Active

📈 **Database Stats:**
• Active Matches: {active_matches}
• Total Users: {total_users}
• Match History: {match_history}

⚡ **Bot is running smoothly!**
"""
        await message.reply(stats_text)
    except Exception as e:
        await message.reply(f"❌ Error fetching stats: {e}")


@Client.on_message(filters.command("broadcast") & filters.private)
async def broadcast_message(client: Client, message):
    """Broadcast message to all users (admin only)"""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        await message.reply("❌ You are not authorized to use this command!")
        return
    
    broadcast_text = message.text.replace("/broadcast", "").strip()
    
    if not broadcast_text:
        await message.reply(
            "📢 **Broadcast Command**\n\n"
            "Usage: /broadcast <message>\n"
            "Example: /broadcast Hello everyone!"
        )
        return
    
    # Get all users
    users = await db.db.users.find({}).to_list(None)
    
    success = 0
    failed = 0
    
    status_msg = await message.reply("📢 Broadcasting message...")
    
    for user in users:
        try:
            await client.send_message(user.get("user_id"), broadcast_text)
            success += 1
            await asyncio.sleep(0.05)  # Avoid flood wait
        except Exception:
            failed += 1
    
    await status_msg.edit(
        f"✅ **Broadcast Complete**\n\n"
        f"📤 Sent to: {success} users\n"
        f"❌ Failed: {failed} users\n"
        f"📝 Message: {broadcast_text[:100]}..."
    )


@Client.on_message(filters.command("restart") & filters.private)
async def restart_bot(client: Client, message):
    """Restart the bot (admin only)"""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        await message.reply("❌ You are not authorized to use this command!")
        return
    
    await message.reply("🔄 Restarting bot...")
    logger.info("Bot restart initiated by admin")
    
    # Exit with code 0 - process manager will restart
    import sys
    sys.exit(0)
