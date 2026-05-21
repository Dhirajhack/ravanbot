from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

import sqlite3

TOKEN = "8686598628:AAFSsZaIsj0wHZ5jAG1AZvEj6zW5Om6_6X0"
OWNER_ID = 1286165147
CHANNEL_LINK = "https://t.me/+XyFq1BRVNERkYzNl"


# DATABASE
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY
)
""")

conn.commit()


# SAVE USER
def save_user(user_id):

    try:

        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,)
        )

        conn.commit()

    except:
        pass


# START COMMAND
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

    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"🆕 New User Started Bot\n\n👤 USER ID: {user_id}"
    )


# USER MESSAGE TO ADMIN
async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    save_user(user_id)

    if user_id != OWNER_ID:

        try:

            await context.bot.forward_message(
                chat_id=OWNER_ID,
                from_chat_id=update.message.chat_id,
                message_id=update.message.message_id
            )

        except:
            pass


# REPLY USER
async def reply_user(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        return

    try:

        user_id = context.args[0]
        message = " ".join(context.args[1:])

        await context.bot.send_message(
            chat_id=user_id,
            text=message
        )

        await update.message.reply_text("✅ Reply Sent")

    except:

        await update.message.reply_text(
            "Use:\n/reply userid message"
        )


# BROADCAST
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        return

    if not update.message.reply_to_message:

        await update.message.reply_text(
            "Reply To Any Message With /broadcast"
        )

        return

    try:

        cursor.execute("SELECT user_id FROM users")

        users = cursor.fetchall()

        users = [user[0] for user in users]

        success = 0

        dead_users = []

        for user in users:

            try:

                await context.bot.copy_message(
                    chat_id=user,
                    from_chat_id=update.message.chat_id,
                    message_id=update.message.reply_to_message.message_id
                )

                success += 1

            except:

                dead_users.append(user)

        # REMOVE BLOCKED USERS
        for dead in dead_users:

            try:

                cursor.execute(
                    "DELETE FROM users WHERE user_id=?",
                    (dead,)
                )

                conn.commit()

            except:
                pass

        await update.message.reply_text(
            f"✅ Broadcast Sent To {success} Users"
        )

    except Exception as e:

        await update.message.reply_text(str(e))


# ADMIN PANEL
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

Send Message
Reply:
/broadcast

━━━━━━━━━━━━━━━

✅ IMAGE BROADCAST

Send Image + Caption
Reply:
/broadcast

━━━━━━━━━━━━━━━

✅ VIDEO BROADCAST

Send Video + Caption
Reply:
/broadcast

━━━━━━━━━━━━━━━

✅ REPLY USER

/reply userid message

━━━━━━━━━━━━━━━

✅ Supports:

🔥 Premium Emojis
📸 Images
🎥 Videos
🎬 GIF
✨ Formatting
📩 Forward Messages
""")


# MAIN
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CommandHandler("reply", reply_user))
app.add_handler(CommandHandler("admin", admin))

app.add_handler(
    MessageHandler(
        filters.TEXT | filters.PHOTO | filters.VIDEO | filters.ALL,
        user_message
    )
)

print("Bot Running 24/7...")

app.run_polling()