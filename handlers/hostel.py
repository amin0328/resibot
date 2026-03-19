import json
import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

DEADLINES_FILE = "data/deadlines.json"


async def show_hostel_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hostel_keyboard = [
        ["💳 Payment Details"],
        ["📅 Upcoming Deadlines"],
        ["⬅️ Back to Main Menu"]
    ]

    await update.message.reply_text(
        "🏦 Hostel Management — choose a topic:",
        reply_markup=ReplyKeyboardMarkup(
            hostel_keyboard,
            resize_keyboard=True
        )
    )


def load_deadlines():
    if not os.path.exists(DEADLINES_FILE):
        return []

    if os.path.getsize(DEADLINES_FILE) == 0:
        return []

    try:
        with open(DEADLINES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []
