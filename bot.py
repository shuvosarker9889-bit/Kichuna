"""
CINEFLIX Telegram Bot with Short Code System
Premium Streaming Bot with Deep Link Support
"""

import logging
import asyncio
from datetime import datetime
from typing import Dict

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, ContextTypes,
    MessageHandler, CallbackQueryHandler, filters
)

from config import Config, Messages, Buttons
from database import db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

user_last_request = {}

# ===================== HELPER FUNCTIONS =====================

async def check_spam(user_id: int) -> bool:
    """Anti-spam protection"""
    if not Config.ENABLE_ANTI_SPAM:
        return False
    
    current_time = datetime.now()
    if user_id in user_last_request:
        time_diff = (current_time - user_last_request[user_id]).total_seconds()
        if time_diff < Config.ANTI_SPAM_COOLDOWN:
            return True
    
    user_last_request[user_id] = current_time
    return False

async def is_user_member(context: ContextTypes.DEFAULT_TYPE, user_id: int, channel_id: int) -> bool:
    """Check if user is member of a channel"""
    try:
        member = await context.bot.get_chat_member(channel_id, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"Error checking membership: {e}")
        return False

async def check_all_channels(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> Dict:
    """Check membership of all required channels"""
    channels = await db.get_all_channels()
    results = {"all_joined": True, "channels": []}
    
    for channel in channels:
        is_member = await is_user_member(context, user_id, channel["chat_id"])
        results["channels"].append({
            "username": channel["username"],
            "name": channel.get("name", channel["username"]),
            "joined": is_member
        })
        if not is_member:
            results["all_joined"] = False
    
    return results

async def cleanup_old_messages(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Clean up old bot messages"""
    if not Config.ENABLE_AUTO_CLEANUP:
        return
    
    try:
        old_message_ids = await db.get_user_messages(user_id)
        for msg_id in old_message_ids[:Config.MAX_CLEANUP_MESSAGES]:
            try:
                await context.bot.delete_message(chat_id=user_id, message_id=msg_id)
                await asyncio.sleep(0.05)
            except Exception as e:
                logger.debug(f"Could not delete message {msg_id}: {e}")
        await db.clear_user_messages(user_id)
    except Exception as e:
        logger.error(f"Cleanup error: {e}")

def format_channels_list(channels, with_status=False):
    """Format channel list for display"""
    if not channels:
        return "No channels"
    
    lines = []
    for i, ch in enumerate(channels, 1):
        name = ch.get("name", ch["username"])
        username = ch["username"]
        if with_status and "joined" in ch:
            status = "✅" if ch["joined"] else "❌"
            lines.append(f"{status} {i}. {name} ({username})")
        else:
            lines.append(f"   • {name} - {username}")
    return "\n".join(lines)

# ===================== START COMMAND =====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with deep link support"""
    user = update.effective_user
    user_id = user.id
    
    # Check if banned
    if await db.is_user_banned(user_id):
        await update.message.reply_text(
            "🚫 You are banned from using this bot.\nContact admin for more info.",
            parse_mode='Markdown'
        )
        return
    
    # Add/update user in database
    await db.add_user(user_id, user.username, user.first_name)
    
    # Check if video request from deep link (short code)
    if context.args and len(context.args) > 0:
        short_code = context.args[0].upper()
        await handle_video_request(update, context, short_code)
        return
    
    # Show welcome message
    channels = await db.get_all_channels()
    channels_text = format_channels_list(channels)
    
    keyboard = [
        [InlineKeyboardButton(Buttons.OPEN_APP, web_app={"url": Config.MINI_APP_URL})]
    ]
    
    # Add channel join buttons
    for channel in channels:
        keyboard.append([
            InlineKeyboardButton(
                f"📢 Join {channel.get('name', channel['username'])}",
                url=f"https://t.me/{channel['username'].replace('@', '')}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton(Buttons.HELP, callback_data="help")])
    
    welcome_text = Messages.WELCOME.format(
        user_name=user.first_name,
        channels_list=channels_text
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# ===================== VIDEO REQUEST HANDLER WITH SHORT CODE =====================

async def handle_video_request(update: Update, context: ContextTypes.DEFAULT_TYPE, short_code: str):
    """Handle video watch request using short code"""
    user = update.effective_user
    user_id = user.id
    chat_id = update.effective_chat.id
    
    # Anti-spam check
    if await check_spam(user_id):
        return
    
    # Check if user is banned
    if await db.is_user_banned(user_id):
        await update.message.reply_text("🚫 You are banned.")
        return
    
    # Get video from database by short code
    video = await db.get_video_by_code(short_code)
    
    if not video:
        await update.message.reply_text(
            Messages.VIDEO_NOT_FOUND,
            parse_mode='Markdown'
        )
        return
    
    # Check channel membership
    membership = await check_all_channels(context, user_id)
    
    if not membership["all_joined"]:
        # Show force join message
        channels_status = format_channels_list(membership["channels"], with_status=True)
        
        keyboard = []
        for ch in membership["channels"]:
            if not ch["joined"]:
                keyboard.append([
                    InlineKeyboardButton(
                        f"📢 Join {ch['name']}",
                        url=f"https://t.me/{ch['username'].replace('@', '')}"
                    )
                ])
        
        keyboard.append([
            InlineKeyboardButton(Buttons.VERIFY_JOIN, callback_data=f"verify_{short_code}")
        ])
        
        force_join_msg = await update.message.reply_text(
            Messages.FORCE_JOIN.format(channels_status=channels_status),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        
        # Save message for cleanup
        await db.save_user_messages(user_id, [force_join_msg.message_id])
        return
    
    # User joined all channels - send video
    await send_video_to_user(update, context, video, user_id, chat_id)

async def send_video_to_user(update, context, video, user_id, chat_id):
    """Send video file to user"""
    try:
        # Show loading message
        loading_msg = await update.message.reply_text(Messages.LOADING_VIDEO)
        
        # Smooth UX delay
        await asyncio.sleep(Config.VIDEO_LOAD_DELAY)
        
        # Cleanup old messages (force join messages etc)
        await cleanup_old_messages(context, user_id)
        
        # Delete loading message
        try:
            await loading_msg.delete()
        except:
            pass
        
        # Get channel ID from video or use default
        source_channel_id = video.get("channel_id") or Config.DEFAULT_CHANNELS[0]["chat_id"]
        message_id = video["message_id"]
        
        # Send video from channel
        try:
            video_msg = await context.bot.copy_message(
                chat_id=chat_id,
                from_chat_id=source_channel_id,
                message_id=message_id,
                protect_content=Config.ENABLE_DOWNLOAD_PROTECTION
            )
        except Exception as e:
            logger.error(f"Video send error: {e}")
            await update.message.reply_text(Messages.VIDEO_NOT_FOUND, parse_mode='Markdown')
            return
        
        # Success message with back button
        keyboard = [[InlineKeyboardButton(Buttons.BACK_TO_APP, web_app={"url": Config.MINI_APP_URL})]]
        
        success_msg = await update.message.reply_text(
            Messages.VIDEO_READY,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        
        # Save messages for future cleanup
        await db.save_user_messages(user_id, [video_msg.message_id, success_msg.message_id])
        
        # Update watch count
        await db.increment_watch_count(user_id)
        
        logger.info(f"✅ Video {video['short_code']} sent to user {user_id}")
        
    except Exception as e:
        logger.error(f"Error sending video: {e}")
        await update.message.reply_text(
            "❌ Something went wrong. Please try again.",
            parse_mode='Markdown'
        )

# ===================== CALLBACK HANDLER =====================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    # Help button
    if data == "help":
        if user_id == Config.ADMIN_ID:
            help_text = Messages.ADMIN_HELP
        else:
            help_text = Messages.USER_HELP
        
        await query.message.edit_text(help_text, parse_mode='Markdown')
        return
    
    # Verify join button
    if data.startswith("verify_"):
        short_code = data.replace("verify_", "")
        
        # Show verifying message
        await query.message.edit_text(Messages.VERIFYING, parse_mode='Markdown')
        
        # Small delay
        await asyncio.sleep(1)
        
        # Check membership again
        membership = await check_all_channels(context, user_id)
        
        if membership["all_joined"]:
            # Delete verification message
            try:
                await query.message.delete()
            except:
                pass
            
            # Get video
            video = await db.get_video_by_code(short_code)
            
            if video:
                # Send video
                await send_video_to_user(update, context, video, user_id, query.message.chat_id)
            else:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=Messages.VIDEO_NOT_FOUND,
                    parse_mode='Markdown'
                )
        else:
            # Still not joined
            channels_status = format_channels_list(membership["channels"], with_status=True)
            
            keyboard = []
            for ch in membership["channels"]:
                if not ch["joined"]:
                    keyboard.append([
                        InlineKeyboardButton(
                            f"📢 Join {ch['name']}",
                            url=f"https://t.me/{ch['username'].replace('@', '')}"
                        )
                    ])
            
            keyboard.append([
                InlineKeyboardButton(Buttons.VERIFY_JOIN, callback_data=f"verify_{short_code}")
            ])
            
            await query.message.edit_text(
                Messages.FORCE_JOIN.format(channels_status=channels_status),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )

# ===================== CHANNEL POST HANDLER WITH AUTO SHORT CODE =====================

async def channel_post_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle new posts in channels - auto generate short code"""
    try:
        message = update.channel_post
        if not message:
            return
        
        # Get video title from caption or filename
        title = message.caption or "Untitled"
        if message.video:
            title = message.video.file_name or title
        elif message.document:
            title = message.document.file_name or title
        
        # Auto-generate short code
        short_code = await db.generate_short_code("VID")
        
        # Save to database
        await db.add_video(
            message_id=message.message_id,
            short_code=short_code,
            title=title,
            channel_id=message.chat_id
        )
        
        logger.info(f"✅ New video saved: {short_code} -> {title}")
        
        # Send notification to admin with short code
        try:
            bot_username = (await context.bot.get_me()).username
            deep_link = f"https://t.me/{bot_username}?start={short_code}"
            
            admin_msg = f"""📹 **New Video Added!**

📌 **Title:** {title}

🔐 **Short Code:** `{short_code}`

🆔 **Message ID:** `{message.message_id}`

📢 **Channel:** {message.chat.title or "Channel"}

🔗 **Deep Link:**
`{deep_link}`

✅ Video saved! Use the short code in your mini app.
Users will click and watch directly!

**Mini App Link Format:**
t.me/{bot_username}?start={short_code}"""
            
            await context.bot.send_message(
                chat_id=Config.ADMIN_ID,
                text=admin_msg,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Failed to notify admin: {e}")
        
    except Exception as e:
        logger.error(f"Channel post handler error: {e}")

# ===================== ADMIN COMMANDS =====================

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot statistics"""
    if update.effective_user.id != Config.ADMIN_ID:
        return
    
    stats = await db.get_stats()
    
    stats_text = f"""📊 **CINEFLIX Bot Statistics**

👥 Total Users: {stats.get('total_users', 0)}
🎬 Total Videos: {stats.get('total_videos', 0)}
📢 Active Channels: {stats.get('total_channels', 0)}
🚫 Banned Users: {stats.get('banned_users', 0)}

🤖 Status: ✅ Running
🌐 Mini App: Active
⚡ Database: Connected
🔗 Short Code System: Active"""
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Broadcast message to all users"""
    if update.effective_user.id != Config.ADMIN_ID:
        return
    
    if not context.args:
        await update.message.reply_text(
            "**Usage:** `/broadcast Your message here`",
            parse_mode='Markdown'
        )
        return
    
    message = ' '.join(context.args)
    user_ids = await db.get_all_user_ids()
    
    success = 0
    failed = 0
    
    status_msg = await update.message.reply_text("📤 Broadcasting...")
    
    for uid in user_ids:
        try:
            await context.bot.send_message(
                chat_id=uid,
                text=f"📢 **Broadcast:**\n\n{message}",
                parse_mode='Markdown'
            )
            success += 1
            await asyncio.sleep(0.05)
        except:
            failed += 1
    
    await status_msg.edit_text(
        f"✅ **Broadcast Complete!**\n\n"
        f"✔️ Sent: {success}\n"
        f"❌ Failed: {failed}",
        parse_mode='Markdown'
    )

async def addchannel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add a new channel"""
    if update.effective_user.id != Config.ADMIN_ID:
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "**Usage:** `/addchannel @username chat_id [name]`",
            parse_mode='Markdown'
        )
        return
    
    username = context.args[0]
    try:
        chat_id = int(context.args[1])
    except:
        await update.message.reply_text("❌ Invalid chat_id")
        return
    
    name = ' '.join(context.args[2:]) if len(context.args) > 2 else username
    
    success = await db.add_channel(username, chat_id, name)
    
    if success:
        await update.message.reply_text(f"✅ Channel **{username}** added!", parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ Failed to add channel", parse_mode='Markdown')

async def removechannel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove a channel"""
    if update.effective_user.id != Config.ADMIN_ID:
        return
    
    if not context.args:
        await update.message.reply_text("**Usage:** `/removechannel @username`", parse_mode='Markdown')
        return
    
    username = context.args[0]
    success = await db.remove_channel(username)
    
    if success:
        await update.message.reply_text(f"✅ Channel **{username}** removed!", parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ Channel not found", parse_mode='Markdown')

async def listchannels_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all channels"""
    if update.effective_user.id != Config.ADMIN_ID:
        return
    
    channels = await db.get_all_channels()
    
    if not channels:
        await update.message.reply_text("No channels configured")
        return
    
    text = "📢 **Active Channels:**\n\n"
    for i, ch in enumerate(channels, 1):
        text += f"{i}. **{ch.get('name', ch['username'])}**\n"
        text += f"   Username: {ch['username']}\n"
        text += f"   Chat ID: `{ch['chat_id']}`\n\n"
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban a user"""
    if update.effective_user.id != Config.ADMIN_ID:
        return
    
    if not context.args:
        await update.message.reply_text("**Usage:** `/ban user_id [reason]`", parse_mode='Markdown')
        return
    
    try:
        user_id = int(context.args[0])
    except:
        await update.message.reply_text("❌ Invalid user_id")
        return
    
    reason = ' '.join(context.args[1:]) if len(context.args) > 1 else "No reason provided"
    
    success = await db.ban_user(user_id, reason)
    
    if success:
        await update.message.reply_text(f"✅ User `{user_id}` banned!", parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ Failed to ban user", parse_mode='Markdown')

async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unban a user"""
    if update.effective_user.id != Config.ADMIN_ID:
        return
    
    if not context.args:
        await update.message.reply_text("**Usage:** `/unban user_id`", parse_mode='Markdown')
        return
    
    try:
        user_id = int(context.args[0])
    except:
        await update.message.reply_text("❌ Invalid user_id")
        return
    
    success = await db.unban_user(user_id)
    
    if success:
        await update.message.reply_text(f"✅ User `{user_id}` unbanned!", parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ User not found in ban list", parse_mode='Markdown')

async def banlist_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show banned users list"""
    if update.effective_user.id != Config.ADMIN_ID:
        return
    
    banned = await db.get_banned_users()
    
    if not banned:
        await update.message.reply_text("No banned users")
        return
    
    text = "🚫 **Banned Users:**\n\n"
    for b in banned:
        text += f"• User ID: `{b['user_id']}`\n"
        text += f"  Reason: {b.get('reason', 'N/A')}\n\n"
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message"""
    user_id = update.effective_user.id
    
    if user_id == Config.ADMIN_ID:
        help_text = Messages.ADMIN_HELP
    else:
        help_text = Messages.USER_HELP
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def getid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get chat and user IDs"""
    if update.effective_user.id != Config.ADMIN_ID:
        return
    
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    await update.message.reply_text(
        f"**User ID:** `{user_id}`\n"
        f"**Chat ID:** `{chat_id}`",
        parse_mode='Markdown'
    )

# ===================== ERROR HANDLER =====================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error: {context.error}")

# ===================== MAIN APPLICATION =====================

def main():
    """Main function to run the bot"""
    logger.info("🚀 Starting CINEFLIX Bot with Short Code System...")
    
    # Create application
    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(CommandHandler("addchannel", addchannel_command))
    application.add_handler(CommandHandler("removechannel", removechannel_command))
    application.add_handler(CommandHandler("listchannels", listchannels_command))
    application.add_handler(CommandHandler("ban", ban_command))
    application.add_handler(CommandHandler("unban", unban_command))
    application.add_handler(CommandHandler("banlist", banlist_command))
    application.add_handler(CommandHandler("getid", getid_command))
    
    # Callback query handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Channel post handler for auto short code generation
    application.add_handler(MessageHandler(
        filters.ChatType.CHANNEL & (filters.VIDEO | filters.Document.ALL | filters.ANIMATION),
        channel_post_handler
    ))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Database initialization
    async def post_init(application: Application):
        connected = await db.connect()
        if not connected:
            logger.error("❌ Failed to connect to MongoDB!")
            logger.error("⚠️ Bot will continue but database features won't work.")
        else:
            logger.info("✅ Database connected successfully!")
    
    application.post_init = post_init
    
    logger.info("✅ CINEFLIX Bot is running!")
    logger.info("🔗 Short Code System: Active")
    logger.info("📡 Listening for updates...")
    
    # Run bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
