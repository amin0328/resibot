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
<img width="590" height="397" alt="Screenshot 2026-03-20 at 10 33 10 AM" src="https://github.com/user-attachments/assets/583ca5c9-357f-44e0-889d-b6af4fcb2359" />

---

## 🏦 Hostel Management

* 💳 **Payment Details**

  * UHMS navigation instructions
  * Fee breakdown for different room types
<img width="590" height="657" alt="Screenshot 2026-03-20 at 10 33 44 AM" src="https://github.com/user-attachments/assets/dc13b217-e32c-4f5b-8329-763f52d9f103" />

* 📅 **Upcoming Deadlines**

  * Hostel fee deadlines
  * Room renewal dates
  * Check-out deadlines
<img width="590" height="1012" alt="Screenshot 2026-03-20 at 10 34 06 AM" src="https://github.com/user-attachments/assets/2f4f412d-55d1-459c-a166-77efc562bc8d" />

---

## 🎉 Events System

<img width="590" height="616" alt="Screenshot 2026-03-20 at 10 34 40 AM" src="https://github.com/user-attachments/assets/73a4e1a0-9344-4049-be92-ab70863c0bd5" />

### 📅 Upcoming Events

* 🏠 House Events (filtered by user’s house)
* 🏫 RC Events (filtered by user’s RC)
* 🌍 Inter-RC Events
<img width="590" height="576" alt="Screenshot 2026-03-20 at 10 35 05 AM" src="https://github.com/user-attachments/assets/ed8d09d7-25a8-4840-be33-f92598d2676a" />
<img width="590" height="897" alt="Screenshot 2026-03-20 at 10 35 31 AM" src="https://github.com/user-attachments/assets/1c53c5e9-4af9-4c79-8c07-04ead8d6a43e" />


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
<img width="590" height="768" alt="Screenshot 2026-03-20 at 10 38 14 AM" src="https://github.com/user-attachments/assets/19209adb-0933-4906-8d1b-c62e031ec0bd" />
<img width="590" height="456" alt="Screenshot 2026-03-20 at 10 38 59 AM" src="https://github.com/user-attachments/assets/b0bb76ea-862e-4864-96d3-94f8b32c1352" />

---

### 🔍 Keyword Search

Search events using keywords across:

* title
* description
* venue
<img width="590" height="793" alt="Screenshot 2026-03-20 at 10 38 35 AM" src="https://github.com/user-attachments/assets/f0f38cfa-5053-4874-ad20-d0ec87dcc4d7" />
<img width="590" height="483" alt="Screenshot 2026-03-20 at 10 39 33 AM" src="https://github.com/user-attachments/assets/493989ae-faf0-4487-a226-b746fddd55b4" />

---

### 🤖 AI Event Recommendation

Recommends events based on a simple scoring system:

| Factor         | Score        |
| -------------- | ------------ |
| Interest match | +3 per match |
| Same house     | +3           |
| Same RC        | +2           |
| Inter-RC event | +1           |

This function is not fully implemented yet, but we are planning to develop it further using AI (e.g. chatGPT).
---

### 🗓 My Event Schedule

Users can manage their personal event list:

* ⭐ Mark events as *Interested*
<img width="590" height="356" alt="Screenshot 2026-03-20 at 10 36 04 AM" src="https://github.com/user-attachments/assets/1ebac5d6-37f7-4b85-bc1e-8509993f648d" />

* 🔔 Add *Reminder* events
<img width="590" height="274" alt="Screenshot 2026-03-20 at 10 36 30 AM" src="https://github.com/user-attachments/assets/20fadab0-62c5-4d10-ba1c-437bb4be15a1" />


* ❌ Remove events
<img width="590" height="291" alt="Screenshot 2026-03-20 at 10 37 01 AM" src="https://github.com/user-attachments/assets/b2122722-0629-4952-8532-b914b4cfca53" />

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
