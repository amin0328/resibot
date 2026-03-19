from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


async def show_events_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events_keyboard = [
        ["📅 Upcoming Events"],
        ["🔎 Find an Event"],
        ["🤖 AI Event Recommendation"],
        ["🗓 My Event Schedule"],
        ["⬅️ Back to Main Menu"]
    ]

    await update.message.reply_text(
        "🎉 What would you like to know about?",
        reply_markup=ReplyKeyboardMarkup(
            events_keyboard,
            resize_keyboard=True
        )
    )


async def show_upcoming_events_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    upcoming_keyboard = [
        ["🏠 House Events"],
        ["🏫 RC Events"],
        ["🌍 Inter-RC Events"],
        ["⬅️ Back to Events Menu"]
    ]

    await update.message.reply_text(
        "📅 Upcoming Events — choose a category:",
        reply_markup=ReplyKeyboardMarkup(
            upcoming_keyboard,
            resize_keyboard=True
        )
    )


async def show_find_event_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    find_keyboard = [
        ["sports"],
        ["performing arts"],
        ["arts"],
        ["food & cooking"],
        ["wellness"],
        ["social"],
        ["personal development"],
        ["🔍 Search by Keyword"],
        ["⬅️ Back to Events Menu"]
    ]

    await update.message.reply_text(
        "🔎 What type of event are you looking for?",
        reply_markup=ReplyKeyboardMarkup(
            find_keyboard,
            resize_keyboard=True
        )
    )


async def show_event_actions_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    action_keyboard = [
        ["📍 View Event Details"],
        ["⭐ I'm Interested"],
        ["🔔 Remind Me"],
        ["🗓 My Event Schedule"],
        ["❌ Remove Event"],
        ["⬅️ Back to Events Menu"]
    ]

    await update.message.reply_text(
        "Choose an action:",
        reply_markup=ReplyKeyboardMarkup(
            action_keyboard,
            resize_keyboard=True
        )
    )
