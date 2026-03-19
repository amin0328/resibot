from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters

from config import RC_OPTIONS, HOUSE_OPTIONS_BY_RC, INTEREST_OPTIONS
from services.user_service import save_user, get_user

ASK_NAME, ASK_RC, ASK_HOUSE, ASK_INTEREST = range(4)


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str):
    menu_keyboard = [
        ["❓ FAQs", "🏦 Hostel Management"],
        ["🎉 Events", "🔔 Alerts"]
    ]

    await update.message.reply_text(
        f"👋 Hey {name}! I'm nus_resiBot, your RC butler.\nWhat would you like to know?",
        reply_markup=ReplyKeyboardMarkup(
            menu_keyboard,
            resize_keyboard=True
        )
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    existing_user = get_user(telegram_id)

    if existing_user:
        name = existing_user["name"]
        await show_main_menu(update, context, name)
        return ConversationHandler.END

    await update.message.reply_text(
        "👋 Welcome to ResiBot! 🤖\nHow would you like to be addressed?"
    )
    return ASK_NAME


async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    context.user_data["name"] = name

    rc_keyboard = [[rc] for rc in RC_OPTIONS]

    await update.message.reply_text(
        "🏫 Which Residential College are you from?",
        reply_markup=ReplyKeyboardMarkup(
            rc_keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )
    return ASK_RC


async def handle_rc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rc = update.message.text.strip()

    if rc not in RC_OPTIONS:
        await update.message.reply_text(
            "Please choose a valid RC from the keyboard."
        )
        return ASK_RC

    context.user_data["rc"] = rc
    houses = HOUSE_OPTIONS_BY_RC.get(rc, [])

    if not houses:
        await update.message.reply_text(
            "No house options found for this RC. Please contact admin."
        )
        return ConversationHandler.END

    house_keyboard = [[house] for house in houses]

    await update.message.reply_text(
        "🏠 Which house are you from?",
        reply_markup=ReplyKeyboardMarkup(
            house_keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )
    return ASK_HOUSE


async def handle_house(update: Update, context: ContextTypes.DEFAULT_TYPE):
    house = update.message.text.strip()
    rc = context.user_data["rc"]

    valid_houses = HOUSE_OPTIONS_BY_RC.get(rc, [])
    if house not in valid_houses:
        await update.message.reply_text(
            "Please choose a valid house from the keyboard."
        )
        return ASK_HOUSE

    context.user_data["house"] = house

    context.user_data["interests"] = []

    interest_keyboard = [[i] for i in INTEREST_OPTIONS]
    interest_keyboard.append(["✅ Done"])

    await update.message.reply_text(
        "✨ What are your interests?\nYou can choose multiple.\nPress ✅ Done when finished.",
        reply_markup=ReplyKeyboardMarkup(
            interest_keyboard,
            resize_keyboard=True
        )
    )

    return ASK_INTEREST

async def handle_interest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text.strip()

    if choice == "✅ Done":
        interests = context.user_data.get("interests", [])

        telegram_id = update.effective_user.id
        name = context.user_data["name"]
        rc = context.user_data["rc"]
        house = context.user_data["house"]

        user_data = {
            "name": name,
            "telegram_id": telegram_id,
            "rc": rc,
            "house": house,
            "role": "User",
            "interests": interests,
            "alerts_on": False
        }

        save_user(user_data)

        await update.message.reply_text(
            f"✅ Registration complete!\nInterests: {', '.join(interests) if interests else 'None'}"
        )

        await show_main_menu(update, context, name)

        return ConversationHandler.END

    if choice in INTEREST_OPTIONS:

        interests = context.user_data.get("interests", [])

        if choice not in interests:
            interests.append(choice)

        context.user_data["interests"] = interests

        await update.message.reply_text(
            f"Added: {choice}\nCurrent: {', '.join(interests)}"
        )

        return ASK_INTEREST

    await update.message.reply_text(
        "Please choose from the keyboard."
    )

    return ASK_INTEREST

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    user = get_user(telegram_id)

    if not user:
        await update.message.reply_text(
            "You are not registered yet. Please use /start first."
        )
        return

    name = user["name"]
    await show_main_menu(update, context, name)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Registration cancelled.")
    return ConversationHandler.END


start_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)],
        ASK_RC: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_rc)],
        ASK_HOUSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_house)],
        ASK_INTEREST: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_interest)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
