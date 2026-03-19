import json
import os
from datetime import datetime, timedelta
from config import EVENTS_FILE


def load_events():
    if not os.path.exists(EVENTS_FILE):
        return []

    if os.path.getsize(EVENTS_FILE) == 0:
        return []

    try:
        with open(EVENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def parse_event_datetime(event):
    date_str = event.get("date", "")
    time_str = event.get("time", "00:00")

    try:
        return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        return None


def is_upcoming_within_days(event, days=7):
    event_dt = parse_event_datetime(event)
    if event_dt is None:
        return False

    now = datetime.now()
    end_date = now + timedelta(days=days)

    return now <= event_dt <= end_date


def get_house_events_for_user(user, days=7):
    events = load_events()
    user_rc = user.get("rc")
    user_house = user.get("house")

    matched = []

    for event in events:
        if not is_upcoming_within_days(event, days):
            continue

        if (
            event.get("scope") == "house"
            and event.get("rc") == user_rc
            and event.get("house") == user_house
        ):
            matched.append(event)

    matched.sort(key=parse_event_datetime)
    return matched


def get_rc_events_for_user(user, days=7):
    events = load_events()
    user_rc = user.get("rc")

    matched = []

    for event in events:
        if not is_upcoming_within_days(event, days):
            continue

        if (
            event.get("scope") == "rc"
            and event.get("rc") == user_rc
        ):
            matched.append(event)

    matched.sort(key=parse_event_datetime)
    return matched


def get_inter_rc_events(days=7):
    events = load_events()
    matched = []

    for event in events:
        if not is_upcoming_within_days(event, days):
            continue

        if event.get("scope") == "inter-rc":
            matched.append(event)

    matched.sort(key=parse_event_datetime)
    return matched


def get_events_by_interest(user, interest, days=7):
    events = load_events()
    user_rc = user.get("rc")
    user_house = user.get("house")

    matched = []

    for event in events:
        if not is_upcoming_within_days(event, days):
            continue

        tags = event.get("interest_tags", [])
        if interest not in tags:
            continue

        scope = event.get("scope")
        event_rc = event.get("rc")
        event_house = event.get("house")

        if scope == "house":
            if event_rc == user_rc and event_house == user_house:
                matched.append(event)

        elif scope == "rc":
            if event_rc == user_rc:
                matched.append(event)

        elif scope == "inter-rc":
            matched.append(event)

    matched.sort(key=parse_event_datetime)
    return matched


def get_event_by_id(event_id):
    events = load_events()

    for event in events:
        if event.get("id") == event_id:
            return event

    return None


def get_events_by_ids(event_ids):
    events = load_events()
    wanted = set(event_ids)

    matched = [event for event in events if event.get("id") in wanted]
    matched.sort(key=parse_event_datetime)
    return matched

def search_events_by_keyword(user, keyword, days=7):
    events = load_events()
    keyword = keyword.lower()

    matched = []

    for event in events:
        if not is_upcoming_within_days(event, days):
            continue

        text_blob = " ".join([
            event.get("title", ""),
            event.get("description", ""),
            event.get("venue", "")
        ]).lower()

        if keyword in text_blob:
            matched.append(event)

    matched.sort(key=parse_event_datetime)
    return matched
