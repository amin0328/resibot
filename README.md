# 🏠 nus_resiBot, Your RC Butler!

nus_resiBot is a Telegram chatbot designed to streamline the residential college (RC) experience by centralizing event discovery, hostel information, and personalized recommendations into a single interface.

---

## 🚀 Overview

Residents often face fragmented information across multiple Telegram groups and platforms. nus_resiBot solves this by:

* Aggregating events across houses and RCs
* Providing personalized recommendations
* Allowing users to track and manage their own event schedule

---

## 📝 Registration Flow

When a user starts the bot for the first time, nus_resiBot guides them through a simple onboarding process:

1. **Start Command**

   * User sends `/start`
   * Bot initiates registration

2. **Name Input**

   * User enters their name

3. **RC Selection**

   * User selects their Residential College (RC)

4. **House Selection**

   * User selects their House within the RC

5. **Interest Selection**

   * User chooses one interest category:

     * sports
     * performing arts
     * arts
     * food & cooking
     * wellness
     * social
     * personal development

6. **Registration Complete**

   * User data is stored in `users.json`
   * Bot redirects user to main menu
<img width="1190" height="703" alt="Screenshot 2026-03-20 at 10 32 44 AM" src="https://github.com/user-attachments/assets/4845b4f9-b197-464f-a5fa-6d988da080e4" />

---

### 📌 Example Stored User

```json id="user-example"
{
  "name": "Amin",
  "telegram_id": 123456789,
  "rc": "NUSC",
  "house": "Idalia",
  "role": "User",
  "interests": ["social"],
  "alerts_on": false,
  "interested_events": [],
  "reminder_events": []
}
```

---

## ✨ Key Features

### 🧭 Main Menu

* ❓ FAQs
* 🏦 Hostel Management
* 🎉 Events
* 🔔 Alerts

---

## 🏦 Hostel Management

* 💳 **Payment Details**

  * UHMS navigation instructions
  * Fee breakdown for different room types

* 📅 **Upcoming Deadlines**

  * Hostel fee deadlines
  * Room renewal dates
  * Check-out deadlines

---

## 🎉 Events System

### 📅 Upcoming Events

* 🏠 House Events (filtered by user’s house)
* 🏫 RC Events (filtered by user’s RC)
* 🌍 Inter-RC Events

---

### 🔎 Find an Event

Browse events by category:

* sports
* performing arts
* arts
* food & cooking
* wellness
* social
* personal development

---

### 🔍 Keyword Search

Search events using keywords across:

* title
* description
* venue

---

### 🤖 AI Event Recommendation

Recommends events based on a simple scoring system:

| Factor         | Score        |
| -------------- | ------------ |
| Interest match | +3 per match |
| Same house     | +3           |
| Same RC        | +2           |
| Inter-RC event | +1           |

---

### 🗓 My Event Schedule

Users can manage their personal event list:

* ⭐ Mark events as *Interested*
* 🔔 Add *Reminder* events
* ❌ Remove events

---

### 📍 Event Interaction

For each event:

* 📍 View full details
* ⭐ Add to schedule
* 🔔 Set reminder

---

## 🧠 System Design

### 📂 Project Structure

```
handlers/
  ├── start.py
  ├── menu.py
  ├── events.py
  ├── hostel.py

services/
  ├── user_service.py
  ├── event_service.py
  ├── recommendation_service.py

data/
  ├── users.json
  ├── events.json

config.py
start.py
```

---

### 🧾 Data Storage

#### `users.json`

```json
{
  "telegram_id": {
    "name": "Amin",
    "rc": "NUSC",
    "house": "Idalia",
    "interests": ["social", "arts"],
    "alerts_on": false,
    "interested_events": [1],
    "reminder_events": []
  }
}
```

#### `events.json`

```json
{
  "id": 1,
  "title": "Event Name",
  "scope": "house | rc | inter-rc",
  "rc": "NUSC",
  "house": "Idalia",
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "venue": "Location",
  "description": "...",
  "interest_tags": ["sports", "social"]
}
```

---

### ⚙️ Core Logic

* **Handlers** → Manage Telegram interactions
* **Services** → Business logic & filtering
* **JSON storage** → Lightweight persistence

A **pending-action system** is used to manage multi-step user inputs (e.g. entering Event ID or keyword).

---

## ⚙️ Setup

### 1. Install dependencies

```bash
pip install python-telegram-bot
```

### 2. Configure bot token

```python
# config.py
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
```

### 3. Run the bot

```bash
python start.py
```

---

## ⚠️ Limitations

* No real-time push notifications for reminders
* JSON-based storage (not scalable)
* Basic keyword search (no fuzzy matching)
* No image support for events

---

## 🔮 Future Improvements

* Real-time reminder system (scheduler / cron)
* Fuzzy search and NLP-based search
* Admin dashboard for event approval
* Database integration (PostgreSQL)
* Inline buttons instead of ID-based input
* UI/UX improvements

---
