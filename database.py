"""
CINEFLIX Database Operations with Short Code System
MongoDB async operations using Motor
"""

import logging
from datetime import datetime
from typing import List, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

logger = logging.getLogger(__name__)

class Database:
    """Database handler for CINEFLIX bot with short code support"""
    
    def __init__(self):
        self.client = None
        self.db = None
        
    async def connect(self):
        """Connect to MongoDB database"""
        try:
            if not Config.MONGO_URI:
                logger.error("❌ MONGO_URI not set in environment variables!")
                return False
                
            self.client = AsyncIOMotorClient(
                Config.MONGO_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000
            )
            self.db = self.client[Config.DATABASE_NAME]
            
            # Test connection
            await self.client.admin.command('ping')
            logger.info(f"✅ Connected to database: {Config.DATABASE_NAME}")
            
            # Initialize collections
            self.users = self.db.users
            self.videos = self.db.videos
            self.channels = self.db.channels
            self.banned_users = self.db.banned_users
            self.user_messages = self.db.user_messages
            
            # Create indexes
            await self.users.create_index("user_id", unique=True)
            await self.videos.create_index("short_code", unique=True)
            await self.videos.create_index("message_id")
            await self.channels.create_index("username", unique=True)
            await self.user_messages.create_index("user_id", unique=True)
            await self.banned_users.create_index("user_id", unique=True)
            
            # Initialize default channels
            await self.initialize_defaults()
            
            logger.info("✅ Database initialized successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database connection error: {e}")
            return False
    
    async def initialize_defaults(self):
        """Initialize default channels from config"""
        try:
            for channel in Config.DEFAULT_CHANNELS:
                existing = await self.channels.find_one({"username": channel["username"]})
                if not existing:
                    await self.channels.insert_one({
                        **channel,
                        "is_active": True,
                        "added_date": datetime.now()
                    })
                    logger.info(f"Added default channel: {channel['username']}")
        except Exception as e:
            logger.error(f"Error initializing defaults: {e}")
    
    # ===================== USER OPERATIONS =====================
    
    async def add_user(self, user_id: int, username: str = None, first_name: str = None):
        """Add or update user in database"""
        try:
            await self.users.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "username": username,
                        "first_name": first_name,
                        "last_active": datetime.now()
                    },
                    "$setOnInsert": {
                        "join_date": datetime.now(),
                        "total_videos_watched": 0
                    }
                },
                upsert=True
            )
        except Exception as e:
            logger.error(f"Error adding user: {e}")
    
    async def get_total_users(self) -> int:
        """Get total number of users"""
        try:
            return await self.users.count_documents({})
        except:
            return 0
    
    async def get_all_user_ids(self) -> List[int]:
        """Get all user IDs"""
        try:
            users = await self.users.find({}, {"user_id": 1}).to_list(length=None)
            return [u["user_id"] for u in users]
        except:
            return []
    
    async def increment_watch_count(self, user_id: int):
        """Increment user's video watch count"""
        try:
            await self.users.update_one(
                {"user_id": user_id},
                {"$inc": {"total_videos_watched": 1}}
            )
        except:
            pass
    
    # ===================== VIDEO OPERATIONS WITH SHORT CODE =====================
    
    async def add_video(self, message_id: int, short_code: str, title: str = None, channel_id: int = None):
        """Add video to database with short code"""
        try:
            await self.videos.update_one(
                {"short_code": short_code},
                {
                    "$set": {
                        "message_id": message_id,
                        "short_code": short_code,
                        "title": title,
                        "channel_id": channel_id,
                        "added_date": datetime.now()
                    }
                },
                upsert=True
            )
            logger.info(f"✅ Video saved: {short_code} -> Message ID: {message_id}")
            return True
        except Exception as e:
            logger.error(f"Error adding video: {e}")
            return False
    
    async def get_video_by_code(self, short_code: str) -> Optional[Dict]:
        """Get video by short code"""
        try:
            video = await self.videos.find_one({"short_code": short_code.upper()})
            return video
        except Exception as e:
            logger.error(f"Error getting video: {e}")
            return None
    
    async def video_exists(self, message_id: int = None, short_code: str = None) -> bool:
        """Check if video exists in database"""
        try:
            if short_code:
                video = await self.videos.find_one({"short_code": short_code.upper()})
            elif message_id:
                video = await self.videos.find_one({"message_id": message_id})
            else:
                return False
            return video is not None
        except:
            return False
    
    async def get_total_videos(self) -> int:
        """Get total number of videos"""
        try:
            return await self.videos.count_documents({})
        except:
            return 0
    
    async def get_next_video_number(self) -> int:
        """Get next video number for auto-generation"""
        try:
            count = await self.videos.count_documents({})
            return count + 1
        except:
            return 1
    
    async def generate_short_code(self, prefix: str = "VID") -> str:
        """Generate unique short code"""
        try:
            number = await self.get_next_video_number()
            return f"{prefix}{number:04d}"
        except:
            import random
            return f"{prefix}{random.randint(1000, 9999)}"
    
    # ===================== CHANNEL OPERATIONS =====================
    
    async def get_all_channels(self) -> List[Dict]:
        """Get all active channels"""
        try:
            channels = await self.channels.find(
                {"is_active": True}
            ).sort("position", 1).to_list(length=None)
            return channels
        except:
            return []
    
    async def add_channel(self, username: str, chat_id: int, name: str = None) -> bool:
        """Add new channel"""
        try:
            channels = await self.get_all_channels()
            max_pos = max([c.get("position", 0) for c in channels], default=0)
            
            await self.channels.insert_one({
                "username": username,
                "chat_id": chat_id,
                "name": name or username,
                "position": max_pos + 1,
                "is_active": True,
                "added_date": datetime.now()
            })
            return True
        except Exception as e:
            logger.error(f"Error adding channel: {e}")
            return False
    
    async def remove_channel(self, username: str) -> bool:
        """Remove channel (mark as inactive)"""
        try:
            result = await self.channels.update_one(
                {"username": username},
                {"$set": {"is_active": False}}
            )
            return result.modified_count > 0
        except:
            return False
    
    # ===================== MESSAGE TRACKING =====================
    
    async def save_user_messages(self, user_id: int, message_ids: List[int]):
        """Save user's message IDs for cleanup"""
        try:
            await self.user_messages.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "message_ids": message_ids,
                        "updated_at": datetime.now()
                    }
                },
                upsert=True
            )
        except:
            pass
    
    async def get_user_messages(self, user_id: int) -> List[int]:
        """Get user's saved message IDs"""
        try:
            data = await self.user_messages.find_one({"user_id": user_id})
            return data.get("message_ids", []) if data else []
        except:
            return []
    
    async def clear_user_messages(self, user_id: int):
        """Clear user's saved messages"""
        try:
            await self.user_messages.delete_one({"user_id": user_id})
        except:
            pass
    
    # ===================== BAN OPERATIONS =====================
    
    async def ban_user(self, user_id: int, reason: str = None) -> bool:
        """Ban a user"""
        try:
            await self.banned_users.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "user_id": user_id,
                        "reason": reason,
                        "banned_at": datetime.now()
                    }
                },
                upsert=True
            )
            return True
        except:
            return False
    
    async def unban_user(self, user_id: int) -> bool:
        """Unban a user"""
        try:
            result = await self.banned_users.delete_one({"user_id": user_id})
            return result.deleted_count > 0
        except:
            return False
    
    async def is_user_banned(self, user_id: int) -> bool:
        """Check if user is banned"""
        try:
            banned = await self.banned_users.find_one({"user_id": user_id})
            return banned is not None
        except:
            return False
    
    async def get_banned_users(self) -> List[Dict]:
        """Get all banned users"""
        try:
            return await self.banned_users.find({}).to_list(length=None)
        except:
            return []
    
    # ===================== STATISTICS =====================
    
    async def get_stats(self) -> Dict:
        """Get bot statistics"""
        try:
            return {
                "total_users": await self.get_total_users(),
                "total_videos": await self.get_total_videos(),
                "total_channels": len(await self.get_all_channels()),
                "banned_users": len(await self.get_banned_users())
            }
        except:
            return {}

# Create global database instance
db = Database()
