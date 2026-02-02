"""
CINEFLIX Bot Configuration
"""

import os

class Config:
    # Bot Token
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    
    # MongoDB
    MONGO_URI = os.environ.get("MONGO_URI", "")
    DATABASE_NAME = "cineflix_ultimate"
    
    # Admin
    ADMIN_ID = int(os.environ.get("ADMIN_ID", "1858324638"))
    
    # Default Channels
    DEFAULT_CHANNELS = [
        {
            "username": "@Cinaflixsteem",
            "chat_id": -1003872857468,
            "name": "CINEFLIX Main",
            "position": 1
        }
    ]
    
    # Mini App
    MINI_APP_URL = os.environ.get("MINI_APP_URL", "https://cinaflix-streaming.vercel.app/")
    
    # Performance
    VIDEO_LOAD_DELAY = 4
    ANTI_SPAM_COOLDOWN = 5
    MAX_CLEANUP_MESSAGES = 50
    
    # Features
    ENABLE_AUTO_CLEANUP = True
    ENABLE_ANTI_SPAM = True
    ENABLE_DOWNLOAD_PROTECTION = True


class Messages:
    WELCOME = """🎬 **Welcome to CINEFLIX!**

Hello **{user_name}**! 👋

আপনার সব পছন্দের Movies, Series এবং Exclusive Content এক জায়গায়!

📢 **প্রথমে আমাদের চ্যানেলগুলো Join করুন:**
{channels_list}

✨ **Features:**
✅ Unlimited Movies & Series
✅ HD Quality Downloads
✅ Regular Updates
✅ Fast Streaming

👇 নিচে App খুলুন এবং দেখা শুরু করুন!"""

    FORCE_JOIN = """🔒 **Content Locked!**

📢 **এই চ্যানেলগুলো Join করুন video দেখতে:**

{channels_status}

**Steps:**
1️⃣ উপরের সব channels join করুন
2️⃣ "✅ I Joined - Verify" ক্লিক করুন
3️⃣ Instant access পাবেন! 🎉"""

    VERIFYING = "⏳ **Verifying...**\n\nPlease wait..."
    
    LOADING_VIDEO = "⏳ **Loading your video...**\n\nপ্রস্তুত হচ্ছে... 🎬"
    
    VIDEO_READY = "✅ **Enjoy Watching!** 🍿\n\nআরো content দেখতে App এ ফিরে যান!"
    
    VIDEO_NOT_FOUND = """❌ **Video Not Found!**

এই video টি হয়তো remove করা হয়েছে বা link ভুল আছে।
অন্য video try করুন।"""

    ADMIN_HELP = """🎛️ **CINEFLIX Admin Panel**

**Channel Management:**
/addchannel @username chat_id - Add channel
/removechannel @username - Remove channel
/listchannels - Show all channels

**User Management:**
/ban user_id - Ban user
/unban user_id - Unban user
/banlist - Banned users

**Statistics:**
/stats - Bot stats
/broadcast message - Send to all

**Other:**
/getid - Get IDs
/help - Help"""

    USER_HELP = """🎬 **CINEFLIX Help**

**How to Watch:**
1. Open CINEFLIX App
2. Select video
3. Click "Watch Now"
4. Enjoy! 🍿

Need help? Contact admin!"""


class Buttons:
    OPEN_APP = "🎬 Open CINEFLIX App"
    JOIN_CHANNEL = "📢 Join {channel_name}"
    VERIFY_JOIN = "✅ I Joined - Verify"
    BACK_TO_APP = "🔙 Back to App"
    HELP = "❓ Help"
