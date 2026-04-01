# 📬 Notification Service (FastAPI + Celery + Redis)

A scalable notification service built with FastAPI that supports:

* 📧 Email notifications
* 📱 SMS notifications
* 🔔 Push notifications (Pushover)
* ⚡ Priority-based processing (high / medium / low)
* 🔁 Background processing using Celery
* 🧾 Centralized logging

---

# 🚀 Tech Stack

* FastAPI
* PostgreSQL
* Redis
* Celery
* Pushover (Push Notifications)
* Twilio (SMS)
* SMTP (Email)

---

# 📁 Project Structure

```
notificationservice/
│
├── main.py
├── celery_app.py
├── tasks.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
│
├── routers/
│   ├── user_router.py
│   ├── notification_router.py
│
├── services/
│   ├── email_service.py
│   ├── sms_service.py
│   ├── push_service.py
│
├── utils/
│   ├── logger.py
│   ├── get_current_user.py
│
├── logs/
└── README.md
```

---

# ⚙️ Setup Instructions

## 1️⃣ Clone Repository

```
git clone <your-repo-url>
cd notification_service
```

---

## 2️⃣ Create Virtual Environment

```
python -m venv .venv
.venv\Scripts\activate   # Windows
```

---

## 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

## 4️⃣ Configure PostgreSQL

Update `database.py`:

```
DATABASE_URL = "postgresql://username:password@localhost/db_name"
```

---

## 5️⃣ Start Redis

```
redis-server
```

---

## 6️⃣ Start Celery Worker

### ✅ Windows (IMPORTANT)

```
celery -A notification_service.celery_app worker --loglevel=info -P solo -Q high,medium,low
```

---

## 7️⃣ Start FastAPI

```
uvicorn main:app --reload
```

---

# 📡 API Endpoints

---

## 🔐 User APIs

### ➤ Register User

```
POST /user/register
```

---

### ➤ Login

```
POST /user/login
```

---

## 🔔 Notification APIs

---

### ➤ Send Notification

```
POST /notifications
```

### Request Body

```
{
  "message": "Hello User",
  "priority": "medium"
}
```

### Response

```
{
  "id": "uuid",
  "status": "medium notification queued"
}
```

---

### ➤ Get Notification Status

```
GET /notifications/{id}
```

---

### ➤ Get User Notifications

```
GET /users/me/notifications
```

---

### ➤ Set Preferences

```
POST /users/me/preferences
```

```
{
  "pref_email": true,
  "pref_sms": false,
  "pref_push": true
}
```

---

### ➤ Get Preferences

```
GET /users/me/preferences
```

---

# ⚡ How It Works

```
FastAPI → Redis → Celery Worker → Email/SMS/Push
```

1. API receives request
2. Notification stored in DB
3. Task sent to Redis queue
4. Celery worker processes task
5. Notification delivered

---

# 🔥 Priority Queues

| Priority | Queue  |
| -------- | ------ |
| high     | high   |
| medium   | medium |
| low      | low    |

---

# 📊 Logging

Logs are stored in:

```
logs/app.log
```

Example:

```
2026-04-01 | INFO | api.notifications | Notification queued
```

---

# 🔐 Authentication

* JWT-based authentication
* Protected routes use `get_current_user`

---

# ⚠️ Important Notes

### Windows Users

Always run Celery with:

```
-P solo
```

---

### Redis Configuration

If needed, use separate DB:

```
redis://localhost:6379/1
```

---

### Email Setup (Gmail)

* Enable 2FA
* Generate App Password
* Use it in SMTP configuration

---

# 🧪 Testing

You can test APIs using:

* Swagger UI → http://127.0.0.1:8000/docs
* Postman

---

# 🚀 Future Improvements

* Notification status tracking (sent / failed)
* Retry & failure handling
* Bulk notifications
* Scheduled notifications
* Monitoring dashboard (Flower)

---

# 👨‍💻 Author

Krushnakant Shaha

