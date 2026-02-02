# 🎬 CINEFLIX Bot - Short Code System

**Premium Telegram Streaming Bot with Auto Short Code Generation**

## 🌟 Key Features

### 🔐 Auto Short Code System
- ✅ **Auto-generates unique codes** (VID0001, VID0002, etc.)
- ✅ **Deep link support** - `t.me/yourbot?start=VID0001`
- ✅ **MongoDB storage** - Restart-proof, all codes saved
- ✅ **Admin notifications** with ready-to-use links
- ✅ **Mini app integration** - Direct video access

### 💫 Complete Bot Features
- 🔒 Force join verification
- 🧹 Auto message cleanup (clean UX)
- ⚡ Anti-spam protection
- 📊 Statistics tracking
- 📢 Broadcasting system
- 🚫 Ban/unban users
- 📱 Mini app integration
- 🗄️ MongoDB database

---

## 🎯 How It Works

### 1️⃣ Upload Video to Channel
```
You post/forward video → Bot saves it
```

### 2️⃣ Admin Gets Notification
```
📹 New Video Added!
📌 Title: Movie Name
🔐 Short Code: VID0001
🆔 Message ID: 12345
🔗 Deep Link: t.me/yourbot?start=VID0001
```

### 3️⃣ User Clicks Link from Mini App
```
User clicks → Bot opens → Force join check → Video sent!
```

### 4️⃣ Clean Experience
```
- Old messages auto-deleted
- Smooth video delivery
- Back to app button shown
```

---

## 🚀 Deploy to Railway (5 Minutes!)

### Step 1: Collect These 7 Values

1. **BOT_TOKEN** - @BotFather থেকে
2. **MONGO_URI** - MongoDB Atlas থেকে  
3. **ADMIN_ID** - @userinfobot থেকে
4. **MINI_APP_URL** - আপনার web app URL
5. **CHANNEL_USERNAME** - @YourChannel
6. **CHANNEL_ID** - -1001234567890
7. **CHANNEL_NAME** - CINEFLIX Main

### Step 2: Deploy

```bash
# Extract ZIP
unzip cineflix_bot.zip
cd cineflix_bot_v2

# Push to GitHub
git init
git add .
git commit -m "CINEFLIX Bot Deploy"
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

### Step 3: Railway Environment Variables

Go to Railway → Variables → Add these 7:

```
BOT_TOKEN=123456:ABCdef...
MONGO_URI=mongodb+srv://...
ADMIN_ID=1234567890
MINI_APP_URL=https://app.vercel.app/
CHANNEL_USERNAME=@YourChannel
CHANNEL_ID=-1001234567890
CHANNEL_NAME=CINEFLIX Main
```

### Step 4: Done! ✅

Bot will:
- ✅ Connect to database
- ✅ Load your channel
- ✅ Start generating short codes
- ✅ Send you notifications

---

## 📹 Video Upload Flow

### When You Upload/Forward Video:

**1. Bot Automatically:**
- Generates unique short code (VID0001, VID0002...)
- Saves to MongoDB with message ID
- Extracts video title

**2. Admin Gets Message:**
```markdown
📹 New Video Added!

📌 Title: Avengers Endgame

🔐 Short Code: VID0001

🆔 Message ID: 54321

📢 Channel: CINEFLIX Main

🔗 Deep Link:
t.me/your_bot?start=VID0001

✅ Video saved! Use the short code in your mini app.

Mini App Link Format:
t.me/your_bot?start=VID0001
```

**3. Copy Short Code to Mini App:**
```javascript
// In your mini app
const videoLink = `https://t.me/your_bot?start=VID0001`;
```

**4. User Experience:**
```
User clicks → Opens bot → 
Shows force join → User joins →
Cleans old messages → Sends video →
Shows "back to app" button
```

---

## 🔗 Deep Link Examples

```
Single video:
t.me/yourbot?start=VID0001

Episode 1:
t.me/yourbot?start=EP1_001

Season 2 Episode 5:
t.me/yourbot?start=S2E5_002

Movie:
t.me/yourbot?start=MOVIE_042
```

---

## 💾 MongoDB Structure

### Videos Collection:
```json
{
  "short_code": "VID0001",
  "message_id": 12345,
  "title": "Movie Name",
  "channel_id": -1001234567890,
  "added_date": "2026-02-02T10:30:00Z"
}
```

### Benefits:
- ✅ **Restart-proof** - All codes saved permanently
- ✅ **Fast lookup** - Indexed by short_code
- ✅ **Scalable** - Unlimited videos
- ✅ **Reliable** - MongoDB handles everything

---

## 🎮 Admin Commands

```
/stats - View statistics (includes video count)
/broadcast message - Send to all users
/addchannel @channel -1001234 Name - Add channel
/removechannel @channel - Remove channel  
/listchannels - Show all channels
/ban user_id - Ban user
/unban user_id - Unban user
/getid - Get IDs
/help - Show help
```

---

## 🧪 Testing Your Bot

### Test 1: Upload Video
1. Upload/forward video to your channel
2. Check admin notification (you should get short code)
3. Verify video saved in database

### Test 2: Deep Link
1. Open: `t.me/yourbot?start=VID0001`
2. Should show force join (if not joined)
3. Join channels → Click verify
4. Video should be sent
5. Old messages should be cleaned

### Test 3: Mini App Integration
```html
<!-- In your mini app -->
<a href="https://t.me/yourbot?start=VID0001">
  Watch Now
</a>
```

---

## 🔧 Configuration

All settings via environment variables - NO CODE EDITING!

### Required Variables (7):
```env
BOT_TOKEN          # From @BotFather
MONGO_URI          # From MongoDB Atlas
ADMIN_ID           # Your Telegram ID
MINI_APP_URL       # Your web app
CHANNEL_USERNAME   # @YourChannel
CHANNEL_ID         # -1001234567890
CHANNEL_NAME       # Display name
```

### Optional Settings (in config.py):
```python
VIDEO_LOAD_DELAY = 4              # Loading animation
ANTI_SPAM_COOLDOWN = 5            # Rate limiting
MAX_CLEANUP_MESSAGES = 50         # Message cleanup limit
ENABLE_AUTO_CLEANUP = True        # Auto-delete messages
ENABLE_ANTI_SPAM = True           # Spam protection
ENABLE_DOWNLOAD_PROTECTION = True # Content protection
```

---

## 📱 Mini App Integration Guide

### HTML Example:
```html
<div class="video-card">
  <img src="thumbnail.jpg" />
  <h3>Movie Title</h3>
  <a href="https://t.me/yourbot?start=VID0001" 
     class="watch-btn">
    Watch Now
  </a>
</div>
```

### JavaScript Example:
```javascript
function watchVideo(shortCode) {
  const botUsername = "your_bot";
  const link = `https://t.me/${botUsername}?start=${shortCode}`;
  window.open(link, '_blank');
}
```

### React Example:
```jsx
function VideoCard({ video }) {
  const watchLink = `https://t.me/${BOT_USERNAME}?start=${video.code}`;
  
  return (
    <div className="video-card">
      <h3>{video.title}</h3>
      <a href={watchLink} target="_blank">
        Watch Now
      </a>
    </div>
  );
}
```

---

## 🐛 Troubleshooting

### Admin Not Getting Notifications?
- Check ADMIN_ID is correct
- Start bot first with /start
- Verify bot can message you

### Short Codes Not Working?
- Check MongoDB connection
- Verify bot saved the video (check logs)
- Try: `/stats` to see video count

### Force Join Not Working?
- Bot must be admin in channel
- Verify CHANNEL_ID is negative (-100...)
- Check CHANNEL_USERNAME has @

### Videos Not Sending?
- Bot needs admin access to source channel
- Verify message_id exists in channel
- Check channel_id in database matches

### Old Messages Not Deleting?
- Ensure ENABLE_AUTO_CLEANUP = True
- Bot needs permission to delete messages
- User must have interacted with bot before

---

## 📊 Statistics

Bot tracks:
- Total users
- Total videos (with short codes)
- Active channels
- Banned users
- Videos watched per user
- Last active timestamps

View with: `/stats`

---

## 🔐 Security

- ✅ Anti-spam protection (5s cooldown)
- ✅ User ban system
- ✅ Download protection (optional)
- ✅ Force join verification
- ✅ Admin-only commands
- ✅ MongoDB security

---

## ✨ Why This Bot is Better

### Before (Old System):
```
❌ Manual message ID management
❌ Hard to track videos
❌ No restart support
❌ Messy admin workflow
```

### After (Short Code System):
```
✅ Auto short codes (VID0001...)
✅ MongoDB storage (restart-proof)
✅ Clean admin notifications
✅ Easy mini app integration
✅ Deep link support
✅ Professional workflow
```

---

## 🎯 Perfect For:

- Movie streaming bots
- Series distribution
- Content delivery
- Educational videos
- Premium content
- Subscription services

---

## 📞 Support

### Check These First:
1. Railway deployment logs
2. All 7 environment variables set
3. MongoDB connection status
4. Bot admin permissions
5. Channel configuration

### Common Issues Solved:
- ✅ Zero code editing needed
- ✅ All configs via environment
- ✅ Auto short code generation
- ✅ MongoDB handles storage
- ✅ Clean message management
- ✅ Professional notifications

---

## 🎉 Success Checklist

- [ ] Bot responds to /start
- [ ] Welcome message shows
- [ ] Mini app button works
- [ ] Upload video to channel
- [ ] Admin gets short code notification
- [ ] Deep link works (t.me/bot?start=CODE)
- [ ] Force join enforced
- [ ] Old messages cleaned
- [ ] Video sent successfully
- [ ] /stats shows correct counts

---

## 🚀 Deploy Now!

**Everything is ready! Just:**

1. Extract ZIP
2. Push to GitHub
3. Deploy on Railway
4. Add 7 environment variables
5. Upload video to test
6. Get short code
7. Use in mini app
8. Enjoy! 🎬

**No code editing. No configuration files. Just works!** ✨

---

**Built with ❤️ for content creators**

🎬 Happy Streaming! 🍿
