from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

TOKEN = "8686598628:AAFSsZaIsj0wHZ5jAG1AZvEj6zW5Om6_6X0"
OWNER_ID = 1798646489
CHANNEL_LINK = "https://t.me/+XyFq1BRVNERkYzNl"


# SAVE USER
def save_user(user_id):
    user_id = str(user_id)

    try:
        with open("users.txt", "r") as f:
            users = f.read().splitlines()
    except:
        users = []

    if user_id not in users:
        with open("users.txt", "a") as f:
            f.write(user_id + "\n")


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

        # TEXT
        if update.message.text:

            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=f"""
📩 New Message

👤 USER ID: {user_id}

💬 MESSAGE:
{update.message.text}
"""
            )

        # PHOTO
        elif update.message.photo:

            photo = update.message.photo[-1].file_id

            await context.bot.send_photo(
                chat_id=OWNER_ID,
                photo=photo,
                caption=f"📸 Photo From User\n\nUSER ID: {user_id}"
            )

        # VIDEO
        elif update.message.video:

            video = update.message.video.file_id

            await context.bot.send_video(
                chat_id=OWNER_ID,
                video=video,
                caption=f"🎥 Video From User\n\nUSER ID: {user_id}"
            )


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
            "Use:\n/reply USERID message"
        )


# BROADCAST
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        return

    try:

        with open("users.txt", "r") as f:
            users = f.read().splitlines()

        success = 0

        # PHOTO BROADCAST
        if update.message.reply_to_message and update.message.reply_to_message.photo:

            photo = update.message.reply_to_message.photo[-1].file_id
            caption = update.message.reply_to_message.caption or ""

            for user in users:
                try:
                    await context.bot.send_photo(
                        chat_id=user,
                        photo=photo,
                        caption=caption
                    )
                    success += 1
                except:
                    pass

        # VIDEO BROADCAST
        elif update.message.reply_to_message and update.message.reply_to_message.video:

            video = update.message.reply_to_message.video.file_id
            caption = update.message.reply_to_message.caption or ""

            for user in users:
                try:
                    await context.bot.send_video(
                        chat_id=user,
                        video=video,
                        caption=caption
                    )
                    success += 1
                except:
                    pass

        # TEXT BROADCAST
        else:

            message = " ".join(context.args)

            for user in users:
                try:
                    await context.bot.send_message(
                        chat_id=user,
                        text=message
                    )
                    success += 1
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

    await update.message.reply_text("""
👑 ADMIN PANEL

✅ TEXT BROADCAST:
/broadcast hello

✅ IMAGE BROADCAST:
Reply To Image With:
/broadcast

✅ VIDEO BROADCAST:
Reply To Video With:
/broadcast

✅ REPLY USER:
/reply userid message
""")


# MAIN
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CommandHandler("reply", reply_user))
app.add_handler(CommandHandler("admin", admin))

app.add_handler(
    MessageHandler(
        filters.TEXT | filters.PHOTO | filters.VIDEO,
        user_message
    )
)

print("Bot Running...")

app.run_polling()