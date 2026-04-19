# ViroScope Clone

A complete clone of the viral YouTube idea generator — with both frontend (static) and backend (API) versions.

## 🎯 What It Does

- Analyzes trending YouTube content in any niche
- Extracts viral patterns from top-performing videos
- Generates 10+ viral video ideas with scores
- Shows difficulty level and content angle for each idea
- Provides tags and descriptions

## 📁 Project Structure

```
viroscope-clone/
├── index.html              # Frontend (works standalone)
├── backend/
│   ├── app.py             # Flask API with real YouTube analysis
│   ├── requirements.txt   # Python dependencies
│   └── .env.template      # Environment variables
└── README.md
```

## 🚀 Quick Start

### Option 1: Frontend Only (No Setup Required)

Just open `index.html` in your browser. It uses mock data but looks and works exactly like the original.

```bash
# Or serve with Python for better experience
cd viroscope-clone
python3 -m http.server 8000
# Open http://localhost:8000
```

### Option 2: Full Backend (Real YouTube Data)

```bash
cd viroscope-clone/backend

# Install dependencies
pip3 install -r requirements.txt

# Setup environment
cp .env.template .env
# Edit .env and add your YouTube API key

# Run the API
python3 app.py

# API will be at http://localhost:5000
```

**Get YouTube API Key:** https://console.cloud.google.com/

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/generate` | POST | Generate viral ideas for a niche |
| `/api/trending/<niche>` | GET | Get trending videos for a niche |
| `/api/health` | GET | Health check |

### Example API Call

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"niche": "Business"}'
```

### Example Response

```json
{
  "success": true,
  "niche": "Business",
  "ideas_count": 10,
  "ideas": [
    {
      "title": "The Truth About Passive Income Nobody Talks About",
      "viral_score": 92,
      "difficulty": "hard",
      "angle": "myth-busting",
      "description": "Based on viral pattern from top business channel...",
      "tags": ["business", "passive income", "myths"]
    }
  ]
}
```

## 🎨 Frontend Features

- ✅ Click-to-select popular niches
- ✅ Custom niche input (60 char limit)
- ✅ Loading animation
- ✅ 10 generated ideas with viral scores
- ✅ Difficulty indicators (easy/medium/hard)
- ✅ Content angle tags
- ✅ Click to copy titles
- ✅ Responsive design
- ✅ Mobile-friendly

## 🔥 Backend Features

- ✅ Real YouTube Data API integration
- ✅ Trending video analysis
- ✅ Viral score calculation
- ✅ Engagement velocity metrics
- ✅ Title variation generation
- ✅ CORS enabled for frontend integration
- ✅ Health check endpoint

## 💰 Cost

| Component | Cost |
|-----------|------|
| Frontend | FREE |
| YouTube API | FREE (10K quota/day) |
| **Total** | **$0** |

## 🎓 How Viral Scoring Works

```
Viral Score = (View Velocity × 40%) + (Engagement Rate × 30%) + (Recency × 30%)

Where:
- View Velocity = Views / Days Since Published
- Engagement Rate = (Likes + Comments) / Views
- Recency = Days since publish (newer = higher)
```

## 🚀 Deploy to Production

### Frontend (Static Hosting)
- GitHub Pages
- Netlify
- Vercel
- Any static host

### Backend (API)
```bash
# Using Gunicorn for production
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Deploy to:**
- Heroku
- Railway
- Render
- DigitalOcean
- AWS Lambda

## 📝 License

MIT — Free to use, modify, distribute.

## 🙏 Acknowledgments

Built as an educational clone. Original concept by ViroScope/GeekBotAI.

---

**Made with ❤️ for the creator economy.**
