from telegram import Update
from telegram.ext import ContextTypes

from services.user_service import (
    get_user,
    update_user_field,
    add_interested_event,
    add_reminder_event,
    remove_event_from_user,
)
from handlers.hostel import show_hostel_menu, load_deadlines
from handlers.start import show_main_menu
from handlers.events import (
    show_events_menu,
    show_upcoming_events_menu,
    show_find_event_menu,
    show_event_actions_menu,
)
from services.event_service import (
    get_house_events_for_user,
    get_rc_events_for_user,
    get_inter_rc_events,
    get_events_by_interest,
    get_event_by_id,
    get_events_by_ids,
    search_events_by_keyword,
)
from services.recommendation_service import get_recommended_events_for_user


INTEREST_BUTTONS = {
    "sports",
    "performing arts",
    "arts",
    "food & cooking",
    "wellness",
    "social",
    "personal development",
}


async def send_event_list(update, context, events, title):
    if not events:
        await update.message.reply_text(f"😢 No upcoming events found for {title}.")
        return

    message = f"{title}\n\n"

    for event in events:
        event_id = event.get("id", "N/A")
        event_title = event.get("title", "Untitled Event")
        date = event.get("date", "TBA")
        time = event.get("time", "TBA")
        venue = event.get("venue", "TBA")

        message += (
            f"🎉 [ID: {event_id}] {event_title}\n"
            f"📅 {date}\n"
            f"⏰ {time}\n"
            f"📍 {venue}\n\n"
        )

    await update.message.reply_text(message.strip())
    await show_event_actions_menu(update, context)


async def send_recommendation_list(update, context, scored_events):
    if not scored_events:
        await update.message.reply_text(
            "😢 I couldn't find any good matches for you in the next 7 days."
        )
        return

    message = "🤖 Based on your interests, you might enjoy:\n\n"

    for score, event in scored_events:
        event_id = event.get("id", "N/A")
        title = event.get("title", "Untitled Event")
        date = event.get("date", "TBA")
        time = event.get("time", "TBA")
        venue = event.get("venue", "TBA")

        message += (
            f"⭐ [ID: {event_id}] {title}\n"
            f"📅 {date}\n"
            f"⏰ {time}\n"
            f"📍 {venue}\n"
            f"Match score: {score}\n\n"
        )

    await update.message.reply_text(message.strip())
    await show_event_actions_menu(update, context)


async def send_event_details(update, event):
    if not event:
        await update.message.reply_text("❌ Event not found.")
        return

    event_id = event.get("id", "N/A")
    title = event.get("title", "Untitled Event")
    date = event.get("date", "TBA")
    time = event.get("time", "TBA")
    venue = event.get("venue", "TBA")
    description = event.get("description", "")
    signup_link = event.get("signup_link", "")
    telegram_link = event.get("telegram_link", "")
    contact = event.get("contact", "")

    message = (
        f"📍 Event Details\n\n"
        f"ID: {event_id}\n"
        f"Event name: {title}\n"
        f"Date: {date}\n"
        f"Time: {time}\n"
        f"Venue: {venue}\n"
    )

    if description:
        message += f"Description: {description}\n"
    if signup_link:
        message += f"Sign-up link: {signup_link}\n"
    if telegram_link:
        message += f"Telegram link: {telegram_link}\n"
    if contact:
        message += f"Point of contact: {contact}\n"

    await update.message.reply_text(message.strip())


async def send_my_schedule(update, context, user):
    interested_ids = user.get("interested_events", [])
    reminder_ids = user.get("reminder_events", [])

    combined_ids = list(dict.fromkeys(interested_ids + reminder_ids))
    events = get_events_by_ids(combined_ids)

    if not events:
        await update.message.reply_text("🗓 Your event schedule is empty.")
        return

    message = "🗓 Here are the events you're attending or interested in:\n\n"

    for event in events:
        event_id = event.get("id", "N/A")
        title = event.get("title", "Untitled Event")
        date = event.get("date", "TBA")
        time = event.get("time", "TBA")
        venue = event.get("venue", "TBA")

        tags = []
        if event_id in interested_ids:
            tags.append("⭐ Interested")
        if event_id in reminder_ids:
            tags.append("🔔 Reminder")

        tag_text = " | ".join(tags) if tags else ""

        message += (
            f"[ID: {event_id}] {title}\n"
            f"📅 {date}\n"
            f"⏰ {time}\n"
            f"📍 {venue}\n"
        )

        if tag_text:
            message += f"{tag_text}\n"

        message += "\n"

    await update.message.reply_text(message.strip())
    await show_event_actions_menu(update, context)

async def handle_pending_event_action(update, context, text, telegram_id, user):
    pending_action = context.user_data.get("pending_event_action")

    if not pending_action:
        return False

    if text in {"⬅️ Back to Events Menu", "⬅️ Back to Main Menu", "/cancel", "cancel"}:
        context.user_data.pop("pending_event_action", None)
        return False

    if pending_action == "keyword_search":
        context.user_data.pop("pending_event_action", None)

        keyword = text.strip()
        events = search_events_by_keyword(user, keyword, days=7)

        if not events:
            await update.message.reply_text(
                f"😢 No events found for '{keyword}'."
            )
            return True

        message = f"🔍 Results for '{keyword}':\n\n"

        for event in events:
            event_id = event.get("id", "N/A")
            title = event.get("title", "Untitled Event")
            date = event.get("date", "TBA")
            time = event.get("time", "TBA")
            venue = event.get("venue", "TBA")

            message += (
                f"🎉 [ID: {event_id}] {title}\n"
                f"📅 {date}\n"
                f"⏰ {time}\n"
                f"📍 {venue}\n\n"
            )

        await update.message.reply_text(message.strip())
        await show_event_actions_menu(update, context)
        return True

    if not text.isdigit():
        await update.message.reply_text("Please enter a valid numeric Event ID.")
        return True

    event_id = int(text)
    event = get_event_by_id(event_id)

    if pending_action == "details":
        context.user_data.pop("pending_event_action", None)

        if not event:
            await update.message.reply_text("❌ Event not found.")
            return True

        await send_event_details(update, event)
        return True

    if pending_action == "interested":
        context.user_data.pop("pending_event_action", None)

        if not event:
            await update.message.reply_text("❌ Event not found.")
            return True

        add_interested_event(telegram_id, event_id)
        await update.message.reply_text(f"⭐ Added event {event_id} to your schedule!")
        return True

    if pending_action == "remind":
        context.user_data.pop("pending_event_action", None)

        if not event:
            await update.message.reply_text("❌ Event not found.")
            return True

        add_reminder_event(telegram_id, event_id)
        await update.message.reply_text(f"🔔 Event {event_id} added to alert system!")
        return True

    if pending_action == "remove":
        context.user_data.pop("pending_event_action", None)

        if not event:
            await update.message.reply_text("❌ Event not found.")
            return True

        remove_event_from_user(telegram_id, event_id)
        await update.message.reply_text(f"❌ Event {event_id} removed from your schedule.")
        return True

    context.user_data.pop("pending_event_action", None)
    return False

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    telegram_id = update.effective_user.id
    user = get_user(telegram_id)

    if not user:
        await update.message.reply_text(
            "You are not registered yet. Please use /start first."
        )
        return

    if text == "⬅️ Back to Events Menu":
        context.user_data.pop("pending_event_action", None)
        await show_events_menu(update, context)
        return

    if text == "⬅️ Back to Main Menu":
        context.user_data.pop("pending_event_action", None)
        name = user["name"]
        await show_main_menu(update, context, name)
        return

    handled_pending = await handle_pending_event_action(
        update, context, text, telegram_id, user
    )
    if handled_pending:
        return

    if text == "❓ FAQs":
        await update.message.reply_text(
            "❓ FAQs\n\n"
            "• Dining hall hours: 7 AM – 9 PM\n"
            "• Laundry room: open 24/7\n"
            "• Gym access: 6 AM – 11 PM\n"
            "• Printing: please use the RC printing corner\n"
            "• For more help, contact your RC admin."
        )

    elif text == "🏦 Hostel Management":
        await show_hostel_menu(update, context)

    elif text == "💳 Payment Details":
        await update.message.reply_text(
            "💳 How to pay:\n"
            "- Log in to UHMS\n"
            "- Go to: Finance → Hostel Fees → Make Payment\n"
            "- Accepted: PayNow, eNETS, Credit/Debit Card\n\n"
            "Fee breakdown:\n"
            "- Single room (AC): ~$187/week\n"
            "- Single room (Non-AC): ~$165/week\n"
            "- 6-Bdrm Apt (AC): $200/week\n"
            "- 6-Bdrm Apt (Non-AC): $179/week"
        )

    elif text == "📅 Upcoming Deadlines":
        deadlines = load_deadlines()

        if not deadlines:
            await update.message.reply_text(
                "No deadline information is available right now."
            )
            return

        message = "📅 Upcoming Deadlines\n\n"

        for item in deadlines:
            title = item.get("title", "Untitled")
            due = item.get("due", "TBA")
            note = item.get("note", "")

            message += f"⚠️ {title}\n"
            message += f"Due: {due}\n"
            if note:
                message += f"{note}\n"
            message += "\n"

        await update.message.reply_text(message.strip())

    elif text == "🎉 Events":
        await show_events_menu(update, context)

    elif text == "📅 Upcoming Events":
        await show_upcoming_events_menu(update, context)

    elif text == "🏠 House Events":
        events = get_house_events_for_user(user, days=7)
        await send_event_list(update, context, events, "🏠 Upcoming House Events")

    elif text == "🏫 RC Events":
        events = get_rc_events_for_user(user, days=7)
        await send_event_list(update, context, events, "🏫 Upcoming RC Events")

    elif text == "🌍 Inter-RC Events":
        events = get_inter_rc_events(days=7)
        await send_event_list(update, context, events, "🌍 Upcoming Inter-RC Events")

    elif text == "🔎 Find an Event":
        await show_find_event_menu(update, context)

    elif text in INTEREST_BUTTONS:
        events = get_events_by_interest(user, text, days=7)
        await send_event_list(update, context, events, f"🔎 Found these {text} events")


    elif text == "🤖 AI Event Recommendation":
        recommended = get_recommended_events_for_user(user, days=7, limit=5)
        await send_recommendation_list(update, context, recommended)

    elif text == "🗓 My Event Schedule":
        await send_my_schedule(update, context, user)

    elif text == "📍 View Event Details":
        context.user_data["pending_event_action"] = "details"
        await update.message.reply_text("📍 Please enter the Event ID to view details.")

    elif text == "⭐ I'm Interested":
        context.user_data["pending_event_action"] = "interested"
        await update.message.reply_text("⭐ Please enter the Event ID to add to your schedule.")

    elif text == "🔔 Remind Me":
        context.user_data["pending_event_action"] = "remind"
        await update.message.reply_text("🔔 Please enter the Event ID to add to alerts.")

    elif text == "❌ Remove Event":
        context.user_data["pending_event_action"] = "remove"
        await update.message.reply_text("❌ Please enter the Event ID to remove from your schedule.")

    elif text == "🔔 Alerts":
        current_status = user.get("alerts_on", False)
        new_status = not current_status

        update_user_field(telegram_id, "alerts_on", new_status)

        if new_status:
            await update.message.reply_text("🔔 Alerts are now ON!")
        else:
            await update.message.reply_text("🔕 Alerts are now OFF!")

    elif text == "🔍 Search by Keyword":
        context.user_data["pending_event_action"] = "keyword_search"
        await update.message.reply_text(
            "🔍 Enter a keyword to search for events:"
        )
