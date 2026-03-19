import json
import os
from config import USERS_FILE


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    if os.path.getsize(USERS_FILE) == 0:
        return {}

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def save_user(user_data):
    users = load_users()
    telegram_id = str(user_data["telegram_id"])

    # 기본 필드 누락 방지
    if "interested_events" not in user_data:
        user_data["interested_events"] = []

    if "reminder_events" not in user_data:
        user_data["reminder_events"] = []

    users[telegram_id] = user_data
    save_users(users)


def get_user(telegram_id):
    users = load_users()
    return users.get(str(telegram_id))


def update_user_field(telegram_id, field, value):
    users = load_users()
    telegram_id = str(telegram_id)

    if telegram_id not in users:
        return False

    users[telegram_id][field] = value
    save_users(users)
    return True


def add_interested_event(telegram_id, event_id):
    users = load_users()
    telegram_id = str(telegram_id)

    if telegram_id not in users:
        return False

    if "interested_events" not in users[telegram_id]:
        users[telegram_id]["interested_events"] = []

    if event_id not in users[telegram_id]["interested_events"]:
        users[telegram_id]["interested_events"].append(event_id)

    save_users(users)
    return True


def add_reminder_event(telegram_id, event_id):
    users = load_users()
    telegram_id = str(telegram_id)

    if telegram_id not in users:
        return False

    if "reminder_events" not in users[telegram_id]:
        users[telegram_id]["reminder_events"] = []

    if event_id not in users[telegram_id]["reminder_events"]:
        users[telegram_id]["reminder_events"].append(event_id)

    save_users(users)
    return True


def remove_event_from_user(telegram_id, event_id):
    users = load_users()
    telegram_id = str(telegram_id)

    if telegram_id not in users:
        return False

    if "interested_events" in users[telegram_id]:
        users[telegram_id]["interested_events"] = [
            eid for eid in users[telegram_id]["interested_events"] if eid != event_id
        ]

    if "reminder_events" in users[telegram_id]:
        users[telegram_id]["reminder_events"] = [
            eid for eid in users[telegram_id]["reminder_events"] if eid != event_id
        ]

    save_users(users)
    return True
