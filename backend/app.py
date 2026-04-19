"""
ViroScope Clone — Backend API
Real YouTube viral analysis using YouTube Data API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import random
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# YouTube API
youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))

def calculate_viral_score(views, likes, comments, days_since):
    """Calculate viral potential score (0-100)"""
    engagement = ((likes + comments) / views * 100) if views > 0 else 0
    velocity = views / max(1, days_since)
    recency = max(0, 30 - days_since)
    
    score = min(100, (velocity / 10000 * 40) + (engagement * 3) + recency)
    return round(score, 1)

def get_trending_videos(niche, max_results=20):
    """Fetch trending videos for a niche"""
    try:
        # Search for recent popular videos in niche
        published_after = (datetime.now() - timedelta(days=7)).isoformat() + 'Z'
        
        search_response = youtube.search().list(
            q=niche,
            type='video',
            order='viewCount',
            publishedAfter=published_after,
            maxResults=max_results,
            part='snippet'
        ).execute()
        
        video_ids = [item['id']['videoId'] for item in search_response['items']]
        
        if not video_ids:
            return []
        
        # Get detailed stats
        videos_response = youtube.videos().list(
            id=','.join(video_ids),
            part='statistics,snippet,contentDetails'
        ).execute()
        
        videos = []
        for video in videos_response['items']:
            stats = video['statistics']
            snippet = video['snippet']
            
            published = datetime.fromisoformat(snippet['publishedAt'].replace('Z', '+00:00'))
            days_since = (datetime.now(published.tzinfo) - published).days
            
            views = int(stats.get('viewCount', 0))
            likes = int(stats.get('likeCount', 0))
            comments = int(stats.get('commentCount', 0))
            
            viral_score = calculate_viral_score(views, likes, comments, days_since)
            
            videos.append({
                'video_id': video['id'],
                'title': snippet['title'],
                'channel': snippet['channelTitle'],
                'views': views,
                'likes': likes,
                'comments': comments,
                'days_since': days_since,
                'viral_score': viral_score,
                'thumbnail': snippet['thumbnails']['high']['url'] if 'high' in snippet['thumbnails'] else snippet['thumbnails']['default']['url'],
                'tags': snippet.get('tags', [])
            })
        
        # Sort by viral score
        return sorted(videos, key=lambda x: x['viral_score'], reverse=True)
        
    except Exception as e:
        print(f"Error fetching videos: {e}")
        return []

def generate_viral_ideas(niche, trending_videos):
    """Generate viral video ideas based on trending patterns"""
    
    if not trending_videos:
        # Fallback to template-based generation
        return generate_template_ideas(niche)
    
    ideas = []
    
    # Extract patterns from top performing videos
    for i, video in enumerate(trending_videos[:5]):
        # Create variations of successful titles
        original_title = video['title']
        
        # Generate 2 variations per trending video
        for j in range(2):
            title_variation = create_title_variation(original_title, niche, j)
            
            ideas.append({
                'title': title_variation,
                'inspired_by': original_title,
                'viral_score': min(95, video['viral_score'] + random.randint(-5, 5)),
                'difficulty': 'hard' if video['viral_score'] > 85 else 'medium' if video['viral_score'] > 75 else 'easy',
                'angle': extract_angle(title_variation),
                'description': f"Based on viral pattern from '{video['channel']}'. This angle targets similar audience with fresh perspective.",
                'tags': video['tags'][:5] if video['tags'] else ['viral', niche.lower(), 'trending'],
                'metrics': {
                    'inspired_views': video['views'],
                    'inspired_likes': video['likes']
                }
            })
    
    # Sort by viral score
    ideas.sort(key=lambda x: x['viral_score'], reverse=True)
    return ideas[:10]

def create_title_variation(original, niche, variation_type):
    """Create variations of successful titles"""
    
    variations = {
        0: lambda t: f"The Truth About {t.split(' - ')[0] if ' - ' in t else t[:40]} (It's Not What You Think)",
        1: lambda t: f"I Tried {t[:30]} for 30 Days — Here's What Happened",
        2: lambda t: f"Stop {t[:25]} — Do This Instead",
        3: lambda t: f"{t[:35]} Explained in 60 Seconds",
        4: lambda t: f"Why {t[:30]} Is Actually a Scam"
    }
    
    # Clean up the title
    clean = original.replace(niche, '').replace('  ', ' ').strip()
    
    return variations.get(variation_type, variations[0])(clean)

def extract_angle(title):
    """Extract content angle from title"""
    angles = ['myth-busting', 'challenge', 'tutorial', 'review', 'story', 'comparison', 'secrets']
    
    if 'truth' in title.lower() or 'scam' in title.lower():
        return 'myth-busting'
    elif 'tried' in title.lower() or 'days' in title.lower():
        return 'challenge'
    elif 'how to' in title.lower() or 'explained' in title.lower():
        return 'tutorial'
    elif 'stop' in title.lower() or 'instead' in title.lower():
        return 'comparison'
    else:
        return random.choice(angles)

def generate_template_ideas(niche):
    """Generate ideas from templates when API fails"""
    
    templates = [
        f"The Truth About {niche} Nobody Talks About",
        f"5 {niche} Secrets That Will Change Everything",
        f"I Tried {niche} for 30 Days — Here's What Happened",
        f"Stop Making These 3 {niche} Mistakes",
        f"How to Master {niche} in 5 Simple Steps",
        f"7 {niche} Hacks That Actually Work",
        f"The 10 Best {niche} Tips for Beginners",
        f"Why Your {niche} Strategy Is Failing",
        f"5 Ways to 10x Your {niche} Results",
        f"The Dark Side of {niche} Nobody Warns You About"
    ]
    
    ideas = []
    for i, template in enumerate(templates):
        viral_score = random.randint(75, 95)
        ideas.append({
            'title': template,
            'inspired_by': 'template',
            'viral_score': viral_score,
            'difficulty': 'hard' if viral_score > 85 else 'medium' if viral_score > 80 else 'easy',
            'angle': ['tutorial', 'secrets', 'challenge', 'myth-busting', 'comparison'][i % 5],
            'description': f"Proven {niche} content format with high engagement potential.",
            'tags': ['viral', niche.lower(), 'trending', 'tutorial', 'tips'],
            'metrics': None
        })
    
    return ideas

@app.route('/api/generate', methods=['POST'])
def generate_ideas():
    """Main API endpoint for generating viral ideas"""
    data = request.json
    niche = data.get('niche', '').strip()
    
    if not niche:
        return jsonify({'error': 'Niche is required'}), 400
    
    # Get trending videos (real data if API key works, else fallback)
    trending = get_trending_videos(niche)
    
    # Generate ideas
    ideas = generate_viral_ideas(niche, trending)
    
    return jsonify({
        'success': True,
        'niche': niche,
        'ideas_count': len(ideas),
        'ideas': ideas,
        'trending_videos_found': len(trending),
        'generated_at': datetime.now().isoformat()
    })

@app.route('/api/trending/<niche>', methods=['GET'])
def get_trending(niche):
    """Get trending videos for a niche"""
    videos = get_trending_videos(niche, max_results=10)
    return jsonify({
        'niche': niche,
        'videos': videos
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'youtube_api_configured': bool(os.getenv('YOUTUBE_API_KEY'))
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
