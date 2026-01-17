from app.integrations.youtube_client import YouTubeClient

client = YouTubeClient()


class VideoService:
    def get_video(self, recipe_title: str):
        return client.search_recipe_video(recipe_title)
