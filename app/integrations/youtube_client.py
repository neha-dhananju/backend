import httpx
from app.core.config import settings


class YouTubeClient:
    BASE_URL = "https://www.googleapis.com/youtube/v3/search"

    def search_recipe_video(self, query: str):
        params = {
            "key": settings.YOUTUBE_API_KEY,
            "q": f"{query} recipe",
            "part": "snippet",
            "type": "video",
            "maxResults": 1
        }

        response = httpx.get(self.BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        items = response.json().get("items", [])
        if not items:
            return None

        video = items[0]
        return {
            "video_id": video["id"]["videoId"],
            "title": video["snippet"]["title"],
            "thumbnail": video["snippet"]["thumbnails"]["high"]["url"],
            "url": f"https://www.youtube.com/watch?v={video['id']['videoId']}"
        }
