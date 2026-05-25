from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

import sqlite3

# =========================
# BOT SETTINGS
# =========================

TOKEN = "8686598628:AAFSsZaIsj0wHZ5jAG1AZvEj6zW5Om6_6X0"
OWNER_ID = 1286165147
CHANNEL_LINK = "https://t.me/+XyFq1BRVNERkYzNl"

# =========================
# DATABASE
# =========================

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY
)
""")

conn.commit()

# =========================
# SAVE USER
# =========================

def save_user(user_id):

    try:

        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,)
        )

        conn.commit()

    except:
        pass

# =========================
# START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    save_user(user_id)

    keyboard = [
        [InlineKeyboardButton("🔔 JOIN CHANNEL", url=CHANNEL_LINK)]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo="https://i.ibb.co/1JRBPy7s/6079886942251192249.jpg",
        caption="""
🔥 Welcome To Ravan Gift Bot 🔥

Bhaiyo Niche Diye Gaye Group Ko Join Karo Aur Apne Kismat Ke Darwaze Kholo 🌟

👇 Join Channel 👇
""",
        reply_markup=reply_markup
    )

    # Notify Admin
    try:

        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"🆕 New User Started Bot\n\n👤 USER ID: {user_id}"
        )

    except:
        pass

# =========================
# USER MESSAGE TO ADMIN
# =========================

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    user_id = update.effective_user.id

    save_user(user_id)

    # Ignore owner messages
    if user_id == OWNER_ID:
        return

    try:

        # Forward exact message
        await context.bot.forward_message(
            chat_id=OWNER_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )

    except Exception as e:
        print(e)

# =========================
# ADMIN AUTO REPLY
# =========================

async def reply_user(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    # Only owner
    if update.effective_user.id != OWNER_ID:
        return

    # Must reply to forwarded message
    if not update.message.reply_to_message:
        return

    try:

        replied_msg = update.message.reply_to_message

        # Get original user id
        if replied_msg.forward_from:

            user_id = replied_msg.forward_from.id

            # FORWARD exact admin message
            # Preserves premium emojis perfectly
            await context.bot.forward_message(
                chat_id=user_id,
                from_chat_id=update.message.chat_id,
                message_id=update.message.message_id
            )

            await update.message.reply_text("✅ Reply Sent")

    except Exception as e:
        print(e)

# =========================
# BROADCAST
# =========================

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        return

    # Must reply to message
    if not update.message.reply_to_message:

        await update.message.reply_text(
            "❌ Reply To Any Message With /broadcast"
        )

        return

    try:

        cursor.execute("SELECT user_id FROM users")

        users = cursor.fetchall()

        users = [user[0] for user in users]

        success = 0
        failed = 0

        dead_users = []

        for user in users:

            try:

                # Forward exact message
                await context.bot.forward_message(
                    chat_id=user,
                    from_chat_id=update.message.chat_id,
                    message_id=update.message.reply_to_message.message_id
                )

                success += 1

            except:

                failed += 1
                dead_users.append(user)

        # Remove blocked users
        for dead in dead_users:

            try:

                cursor.execute(
                    "DELETE FROM users WHERE user_id=?",
                    (dead,)
                )

                conn.commit()

            except:
                pass

        await update.message.reply_text(f"""
✅ Broadcast Completed

👥 Success: {success}
❌ Failed: {failed}
""")

    except Exception as e:

        await update.message.reply_text(str(e))

# =========================
# ADMIN PANEL
# =========================

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        return

    cursor.execute("SELECT COUNT(*) FROM users")

    total_users = cursor.fetchone()[0]

    await update.message.reply_text(f"""
👑 ADMIN PANEL

👥 TOTAL USERS: {total_users}

━━━━━━━━━━━━━━━

✅ TEXT BROADCAST

Reply To Any Message:
/broadcast

━━━━━━━━━━━━━━━

✅ IMAGE BROADCAST

Reply To Image:
/broadcast

━━━━━━━━━━━━━━━

✅ VIDEO BROADCAST

Reply To Video:
/broadcast

━━━━━━━━━━━━━━━

✅ AUTO REPLY SYSTEM

Just Reply To User Message

━━━━━━━━━━━━━━━

✅ SUPPORTS

🔥 Premium Emojis
✨ Telegram Formatting
📸 Photos
🎥 Videos
🎬 GIF
🎵 Audio
🎤 Voice
📄 Documents
🎯 Stickers
📩 Forward Messages
""")

# =========================
# MAIN
# =========================

app = Application.builder().token(TOKEN).build()

# Commands
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CommandHandler("admin", admin))

# Admin reply handler
app.add_handler(
    MessageHandler(
        filters.REPLY & ~filters.COMMAND,
        reply_user
    )
)

# User message handler
app.add_handler(
    MessageHandler(
        ~filters.COMMAND,
        user_message
    )
)

print("🚀 Bot Running 24/7...")

app.run_polling()