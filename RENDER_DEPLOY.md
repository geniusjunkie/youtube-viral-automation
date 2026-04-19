# ViroScope Clone — Render Deployment Guide

## 🚀 Deploy to Render (Free Tier)

### Step 1: Create Render Account
1. Go to https://dashboard.render.com/
2. Sign up with GitHub (recommended)
3. Connect your GitHub account

### Step 2: Create Web Service (Backend)

1. Click **"New"** → **"Web Service"**
2. Connect your repository: `geniusjunkie/youtube-viral-automation`
3. Configure:
   
   | Setting | Value |
   |---------|-------|
   | **Name** | `viroscope-api` |
   | **Environment** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn -w 4 -b 0.0.0.0:$PORT app:app` |
   | **Root Directory** | `backend` |

4. Click **"Create Web Service"**

### Step 3: Add Environment Variables

After deployment starts, go to **Environment** tab and add:

```
YOUTUBE_API_KEY=your_youtube_api_key_here
FLASK_ENV=production
```

**Get YouTube API Key:** https://console.cloud.google.com/apis/credentials

### Step 4: Deploy Static Frontend (Optional)

For the frontend, you have two options:

#### Option A: Render Static Site (Free)
1. Click **"New"** → **"Static Site"**
2. Same repository
3. Configure:
   | Setting | Value |
   |---------|-------|
   | **Name** | `viroscope` |
   | **Root Directory** | `.` |
   | **Build Command** | (leave empty) |
4. Your frontend will be at `https://viroscope.onrender.com`

#### Option B: GitHub Pages (Also Free)
Just enable GitHub Pages in your repo settings - even simpler.

### Step 5: Connect Frontend to Backend

Edit `index.html` and update the API URL:

```javascript
const API_URL = 'https://viroscope-api.onrender.com';
const USE_BACKEND = true;
```

Then commit and push:

```bash
git add index.html
git commit -m "Connect to Render backend"
git push
```

---

## 📋 Alternative: Blueprint Deploy

Render supports `render.yaml` for one-click deployment:

1. Push the `render.yaml` file to your repo
2. Go to https://dashboard.render.com/blueprints
3. Click **"New Blueprint Instance"**
4. Connect your repo
5. Render will create both services automatically!

---

## 🔧 Local Testing Before Deploy

```bash
cd backend
pip3 install -r requirements.txt
export YOUTUBE_API_KEY=your_key_here
python3 app.py
```

Test the API:
```bash
curl http://localhost:5000/api/health
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"niche": "Business"}'
```

---

## 💰 Render Free Tier Limits

| Resource | Limit |
|----------|-------|
| Web Services | 1 free instance (sleeps after 15 min idle) |
| Static Sites | Unlimited, always on |
| Bandwidth | 100 GB/month |
| Build Minutes | 500 min/month |

**Tip:** Static site doesn't sleep - better for frontend. Use web service just for API.

---

## ✅ Post-Deploy Checklist

- [ ] Backend API responding at `/api/health`
- [ ] Frontend loads without errors
- [ ] Generate button works and returns ideas
- [ ] YouTube API key added to environment variables
- [ ] CORS working (frontend can call backend)

---

## 🆘 Troubleshooting

**"CORS error" in browser:**
- Check `CORS(app, origins=...)` includes your frontend domain

**"No module named 'googleapiclient'" on build:**
- Make sure `requirements.txt` is committed to repo

**API returns empty ideas:**
- YouTube API key not set or invalid
- Check `/api/health` endpoint

**Frontend shows "Backend unavailable":**
- API_URL in index.html doesn't match deployed backend URL
- Backend is sleeping (first call will wake it, takes 30-60 sec)

---

**Ready to deploy?** Just follow Step 1-3 above. 🚀
