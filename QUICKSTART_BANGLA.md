# 🚀 CINEFLIX Bot - দ্রুত শুরু করুন! (Short Code System)

## ✨ এই Bot কি করবে?

### 📹 Video Upload করলে:
```
1. Auto short code তৈরি হবে (VID0001, VID0002...)
2. MongoDB তে save হবে (restart হলেও থাকবে)
3. Admin কে notification যাবে deep link সহ
4. Mini app এ ব্যবহার করতে পারবেন
```

### 🔗 User Experience:
```
User mini app এ click করবে → Bot open হবে
→ Channel join check → Video পাঠাবে
→ পুরনো message clean হবে → সুন্দর experience!
```

---

## 📋 কি কি লাগবে? (7টা জিনিস)

1. **BOT_TOKEN** - @BotFather থেকে
2. **MONGO_URI** - MongoDB Atlas থেকে
3. **ADMIN_ID** - @userinfobot থেকে
4. **MINI_APP_URL** - আপনার web app URL
5. **CHANNEL_USERNAME** - @YourChannel
6. **CHANNEL_ID** - -1001234567890  
7. **CHANNEL_NAME** - CINEFLIX Main

---

## 🚀 Deploy করুন (মাত্র 5 মিনিট!)

### Step 1: GitHub এ Upload

```bash
# ZIP extract করুন
unzip cineflix_bot.zip
cd cineflix_bot_v2

# Git initialize
git init
git add .
git commit -m "CINEFLIX Bot Deploy"

# GitHub এ push
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

### Step 2: Railway Deploy

1. [Railway.app](https://railway.app) এ যান
2. "New Project" → "Deploy from GitHub"
3. আপনার repo select করুন

### Step 3: 7টা Variable যোগ করুন

Railway Variables tab এ:

```
BOT_TOKEN=আপনার_বট_টোকেন
MONGO_URI=আপনার_মংগো_uri
ADMIN_ID=আপনার_টেলিগ্রাম_আইডি
MINI_APP_URL=আপনার_মিনি_অ্যাপ_url
CHANNEL_USERNAME=@YourChannel
CHANNEL_ID=-1001234567890
CHANNEL_NAME=CINEFLIX Main
```

### Step 4: সম্পন্ন! ✅

Railway logs দেখুন:
```
✅ Connected to database
✅ Database initialized successfully!
Added default channel: @YourChannel
✅ CINEFLIX Bot is running!
🔗 Short Code System: Active
```

---

## 🎬 Video Upload Test

### আপনার channel এ video পোস্ট করুন:

**Bot automatically এই message পাঠাবে:**

```
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

---

## 📱 Mini App এ ব্যবহার করুন

### HTML Example:
```html
<a href="https://t.me/yourbot?start=VID0001">
  Watch Now
</a>
```

### JavaScript Example:
```javascript
const videoLink = `https://t.me/yourbot?start=VID0001`;
window.open(videoLink);
```

---

## ✅ কি কি সুবিধা?

### 🔐 Auto Short Code:
- ✅ VID0001, VID0002... automatic
- ✅ MongoDB তে save (restart-proof)
- ✅ Deep link ready
- ✅ Mini app friendly

### 🧹 Clean Experience:
- ✅ পুরনো message auto delete
- ✅ Force join working smoothly
- ✅ Video sending fast
- ✅ Professional look

### 💾 MongoDB Storage:
- ✅ সব video code save
- ✅ Restart হলেও কাজ করবে
- ✅ Unlimited videos
- ✅ Fast lookup

---

## 🎯 User Journey

```
1. User mini app খোলে
2. Video দেখে "Watch Now" click করে
3. Bot open হয় deep link দিয়ে
4. Force join message দেখায়
5. User channels join করে
6. "Verify" button click করে
7. পুরনো messages clean হয়ে যায়
8. Video পায় user
9. "Back to App" button দেখায়
10. Perfect experience! ✨
```

---

## 🔧 Admin Commands

```
/stats - সব statistics দেখুন
/broadcast msg - সবাইকে message পাঠান
/addchannel @ch -100123 Name - চ্যানেল যোগ করুন
/ban user_id - ban করুন
/help - help দেখুন
```

---

## 🐛 সমস্যা সমাধান

### Admin notification আসছে না?
- ADMIN_ID ঠিক আছে কিনা check করুন
- Bot এ /start করেছেন কিনা
- Bot আপনাকে message পাঠাতে পারে কিনা

### Short code কাজ করছে না?
- MongoDB connected আছে কিনা logs দেখুন
- Video save হয়েছে কিনা check করুন
- /stats command দিয়ে video count দেখুন

### Force join কাজ করছে না?
- Bot channel এ admin আছে কিনা
- CHANNEL_ID negative কিনা (-100...)
- CHANNEL_USERNAME এ @ আছে কিনা

### Video পাঠাচ্ছে না?
- Bot source channel এ admin আছে কিনা
- Message ID সঠিক কিনা
- Channel ID ঠিক আছে কিনা

---

## 💡 গুরুত্বপূর্ণ Tips

### ✅ MongoDB Setup:
1. IP Whitelist: `0.0.0.0/0` দিন
2. Database user: Read/Write permission
3. Connection string এ password ঠিক দিন

### ✅ Channel Setup:
1. Bot কে admin বানান
2. সব permission দিন
3. Chat ID negative number (-100...)

### ✅ Testing:
1. একটা video upload করুন
2. Admin notification check করুন
3. Short code copy করুন
4. Deep link test করুন (t.me/bot?start=CODE)
5. Force join test করুন

---

## 🎉 সফলতার চেকলিস্ট

- [ ] Bot শুরু হয়েছে (Railway logs green)
- [ ] /start command কাজ করছে
- [ ] Channel এ video upload করেছি
- [ ] Admin notification এসেছে
- [ ] Short code পেয়েছি (VID0001)
- [ ] Deep link কাজ করছে
- [ ] Force join working
- [ ] Video send হচ্ছে
- [ ] Old messages clean হচ্ছে
- [ ] /stats সঠিক data দেখাচ্ছে

---

## 🚀 এখন কি করবেন?

### 1. Deploy করুন:
```bash
unzip → git init → push → railway deploy → variables add
```

### 2. Test করুন:
```
Video upload → notification check → deep link test
```

### 3. Mini App এ integrate করুন:
```html
<a href="t.me/bot?start=VID0001">Watch</a>
```

### 4. Users দের share করুন! 🎬

---

## ✨ কেন এই System ভালো?

### আগে (পুরনো system):
```
❌ Manual message ID management
❌ Track করা কঠিন
❌ Restart হলে problem
❌ Messy workflow
```

### এখন (Short Code System):
```
✅ Auto short code (VID0001...)
✅ MongoDB storage (restart-proof)
✅ Clean notifications
✅ Easy mini app integration
✅ Deep link support
✅ Professional experience
```

---

## 🎯 Perfect For:

- 🎬 Movie streaming bots
- 📺 Series distribution
- 📚 Educational content
- 💎 Premium content delivery
- 🔐 Subscription services

---

**আপনার CINEFLIX Bot এখন সম্পূর্ণ প্রস্তুত!** 

**Deploy করুন এবং enjoy করুন! 🚀🎉**

**Happy Streaming! 🎬🍿**
