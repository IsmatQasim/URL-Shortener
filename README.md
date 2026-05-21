# ✂️ iURL — URL Shortener

A full-stack URL shortener built with **React**, **FastAPI**, and **MongoDB** — featuring Base62 encoding, click analytics, custom aliases, and URL expiry.

🔗 **Live Demo:** [iurl.netlify.app](https://iurl.netlify.app)

---

## ✨ Features

- 🔗 Shorten long URLs instantly
- 🧮 **Base62 encoding** with MD5 hashing (no third-party ID libraries)
- 💥 Collision handling — regenerates ID if conflict found
- ✏️ Custom alias support (`iurl.netlify.app/mylink`)
- 📊 Click analytics tracking
- ⏳ Auto URL expiry after 7 days
- 📋 Copy to clipboard
- 🕓 Session history (persisted in MongoDB)
- 🔁 Smooth redirect with loading screen

---

## 🛠️ Tech Stack

### Frontend
- React + Vite
- Tailwind CSS
- Deployed on **Netlify**

### Backend
- Python + FastAPI
- Motor (async MongoDB driver)
- Deployed on **Hugging Face Spaces** (Docker)

### Database
- MongoDB Atlas (free tier)

---

## ⚙️ System Design

```
User → iurl.netlify.app
          ↓
     Netlify (_redirects proxy)
          ↓
     FastAPI (Hugging Face)
          ↓
     MongoDB Atlas
```

### Base62 Algorithm
```
Long URL
   ↓
MD5 Hash → "8ffdefbdec956b59..."
   ↓
First 8 hex chars → integer
   ↓
Base62 encode (a-z A-Z 0-9)
   ↓
6 character short ID → "eKAhRt"
```

**Why Base62?**
- 62^6 = ~56 billion unique URLs
- URL-safe characters only
- Shorter than MD5/UUID
- Same as Bitly, TinyURL

**Why not nanoid/random?**
- MD5 is deterministic — same URL always gives same hash
- Reduces duplicate entries in DB
- Real system design approach

### Collision Handling
If generated ID already exists in DB → try next 8 hex chars of MD5 → repeat up to 5 times (practically impossible to fail with 56B possibilities)

---

## 📁 Project Structure

```
url-shortener/
├── Dockerfile               # HF deployment
├── requirements.txt         # Python dependencies
├── README.md
├── backend/
│   ├── main.py              # FastAPI app + CORS
│   ├── routes/
│   │   └── url_routes.py    # API endpoints
│   ├── services/
│   │   └── url_service.py   # Business logic
│   ├── models/
│   │   └── url_model.py     # Pydantic schemas
│   ├── database/
│   │   └── connection.py    # MongoDB connection
│   └── utils/
│       └── base62.py        # Base62 algorithm
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── components/
    │   │   ├── URLInput.jsx
    │   │   ├── ResultCard.jsx
    │   │   └── HistoryList.jsx
    │   └── services/
    │       └── api.js
    └── public/
        └── _redirects        # Netlify proxy rules
```

---

## 🚀 Run Locally

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt

# Create .env file
MONGO_URL=mongodb://localhost:27017
DB_NAME=urlshortener
BASE_URL=http://localhost:8000

uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/shorten` | Create short URL |
| GET | `/api/urls` | Get user's URL history |
| GET | `/api/resolve/{id}` | Get original URL |
| GET | `/api/stats/{id}` | Get URL click stats |
| GET | `/{short_id}` | Redirect to original URL |

### Example Request
```json
POST /api/shorten
{
  "url": "https://google.com/very-long-path",
  "custom_alias": "google"
}
```

### Example Response
```json
{
  "short_id": "eKAhRt",
  "short_url": "https://iurl.netlify.app/eKAhRt",
  "original_url": "https://google.com/very-long-path",
  "clicks": 0,
  "created_at": "2024-01-15T10:30:00"
}
```

---

## 🧠 What I Learned

- Async Python with FastAPI + Motor
- Base62 encoding from scratch
- MongoDB document design
- CORS configuration
- Docker deployment on Hugging Face
- Netlify proxy redirects (`_redirects`)
- React state management + useEffect
- Client identification without authentication

---

## 📌 Future Improvements

- [ ] JWT Authentication (login/signup)
- [ ] QR code generation
- [ ] Dashboard with charts (clicks over time)
- [ ] Redis caching for frequently visited URLs
- [ ] Custom domain support
- [ ] Rate limiting

---

## 👩‍💻 Author

**Ismat Qasim** — [GitHub](https://github.com/IsmatQasim)

---

> Built as a portfolio project to demonstrate full-stack development and system design concepts.