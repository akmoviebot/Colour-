import telebot
import random
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# =========================
# BOT TOKEN
# =========================
TOKEN = "PASTE_YOUR_BOT_TOKEN"

bot = telebot.TeleBot(TOKEN)

# =========================
# USER DATABASE
# =========================
users = {}

# =========================
# START COMMAND
# =========================
@bot.message_handler(commands=['start'])
def start(message):

    user_id = message.from_user.id

    if user_id not in users:
        users[user_id] = {
            "balance": 1000
        }

    balance = users[user_id]["balance"]

    text = f"""
🎮 Welcome To DW Color Prediction

💰 Demo Balance: ₹{balance}

Choose Your Color 👇
"""

    markup = InlineKeyboardMarkup(row_width=3)

    red = InlineKeyboardButton("🔴 RED", callback_data="red")
    green = InlineKeyboardButton("🟢 GREEN", callback_data="green")
    violet = InlineKeyboardButton("🟣 VIOLET", callback_data="violet")

    markup.add(red, green, violet)

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=markup
    )

# =========================
# BALANCE COMMAND
# =========================
@bot.message_handler(commands=['balance'])
def balance(message):

    user_id = message.from_user.id

    if user_id not in users:
        users[user_id] = {
            "balance": 1000
        }

    balance = users[user_id]["balance"]

    bot.reply_to(
        message,
        f"💰 Your Balance: ₹{balance}"
    )

# =========================
# GAME LOGIC
# =========================
@bot.callback_query_handler(func=lambda call: True)
def game(call):

    user_id = call.from_user.id

    if user_id not in users:
        users[user_id] = {
            "balance": 1000
        }

    balance = users[user_id]["balance"]

    # Minimum play amount
    if balance < 10:
        bot.answer_callback_query(
            call.id,
            "❌ Low Balance"
        )
        return

    # Deduct 10
    users[user_id]["balance"] -= 10

    choice = call.data

    msg = bot.send_message(
        call.message.chat.id,
        "⏳ Result in 5 seconds..."
    )

    time.sleep(5)

    number = random.randint(0, 9)

    # Result Logic
    if number == 0:
        result = "violet"

    elif number % 2 == 0:
        result = "green"

    else:
        result = "red"

    # Win Logic
    if choice == result:

        users[user_id]["balance"] += 20

        status = "✅ YOU WIN"

    else:

        status = "❌ YOU LOSE"

    final_balance = users[user_id]["balance"]

    final_text = f"""
🎲 Result Number: {number}

🎨 Result Color: {result.upper()}

{status}

💰 Balance: ₹{final_balance}
"""

    markup = InlineKeyboardMarkup(row_width=3)

    red = InlineKeyboardButton("🔴 RED", callback_data="red")
    green = InlineKeyboardButton("🟢 GREEN", callback_data="green")
    violet = InlineKeyboardButton("🟣 VIOLET", callback_data="violet")

    markup.add(red, green, violet)

    bot.edit_message_text(
        final_text,
        call.message.chat.id,
        msg.message_id,
        reply_markup=markup
    )

# =========================
# HELP COMMAND
# =========================
@bot.message_handler(commands=['help'])
def help_command(message):

    text = """
📌 Commands

/start - Start Bot
/balance - Check Balance
/help - Help Menu
"""

    bot.reply_to(message, text)

# =========================
# BOT START
# =========================
print("DW Bot Running...")

bot.infinity_polling()
