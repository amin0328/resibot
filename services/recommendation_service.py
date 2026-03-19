from services.event_service import load_events, is_upcoming_within_days, parse_event_datetime


def calculate_event_score(user, event):
    score = 0

    user_rc = user.get("rc", "")
    user_house = user.get("house", "")
    user_interests = user.get("interests", [])

    event_scope = event.get("scope", "")
    event_rc = event.get("rc", "")
    event_house = event.get("house", "")
    event_tags = event.get("interest_tags", [])

    # interest match
    common_tags = [tag for tag in event_tags if tag in user_interests]
    score += len(common_tags) * 3

    # same house
    if event_scope == "house" and event_rc == user_rc and event_house == user_house:
        score += 3

    # same RC
    elif event_scope in ["house", "rc"] and event_rc == user_rc:
        score += 2

    # inter-RC events still get some base score
    elif event_scope == "inter-rc":
        score += 1

    return score


def get_recommended_events_for_user(user, days=7, limit=5):
    events = load_events()
    scored_events = []

    for event in events:
        if not is_upcoming_within_days(event, days):
            continue

        score = calculate_event_score(user, event)

        if score > 0:
            scored_events.append((score, event))

    scored_events.sort(
        key=lambda item: (-item[0], parse_event_datetime(item[1]))
    )

    return scored_events[:limit]
