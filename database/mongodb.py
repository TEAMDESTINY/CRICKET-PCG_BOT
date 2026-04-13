import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

class Database:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[DB_NAME]
    
    async def save_match(self, group_id, match_data):
        await self.db.active_matches.update_one(
            {"group_id": group_id},
            {"$set": match_data},
            upsert=True
        )
    
    async def get_match(self, group_id):
        return await self.db.active_matches.find_one({"group_id": group_id})
    
    async def delete_match(self, group_id):
        await self.db.active_matches.delete_one({"group_id": group_id})
    
    async def save_to_history(self, match_data):
        await self.db.match_history.insert_one(match_data)
    
    async def update_user_stats(self, user_id, stats):
        await self.db.users.update_one(
            {"user_id": user_id},
            {"$set": stats},
            upsert=True
        )

db = Database()
