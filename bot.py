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

✅ Daily Updates
✅ Winning Posts
✅ Fast Join Access

👇 Join Channel 👇
""",
        reply_markup=reply_markup
    )

    # Notify owner
    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"🆕 New User Started Bot:\nID: {user_id}"
    )


# FORWARD USER MESSAGE TO OWNER
async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    text = update.message.text

    save_user(user_id)

    if user_id != OWNER_ID:

        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"""
📩 New Message

👤 User ID: {user_id}

💬 Message:
{text}
"""
        )


# REPLY COMMAND
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


# BROADCAST COMMAND
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        return

    message = " ".join(context.args)

    try:
        with open("users.txt", "r") as f:
            users = f.read().splitlines()

        success = 0

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

    except:
        await update.message.reply_text("No users found")


# ADMIN PANEL
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        return

    await update.message.reply_text("""
👑 ADMIN PANEL

Commands:

/broadcast yourmessage

/reply userid message
""")


# MAIN
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CommandHandler("reply", reply_user))
app.add_handler(CommandHandler("admin", admin))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, user_message)
)

print("Bot Running...")

app.run_polling()