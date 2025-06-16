
from googleapiclient.discovery import build
from services.IAService import GPTService
import os
class YoutubeService:
    def __init__(self):
        self.apiKey = os.getenv("YOUTUBE_API_KEY")
        self.youtube_client = build('youtube', 'v3', developerKey=self.apiKey)
        self.ia_service = GPTService()

    async def get_videos(self, subtema:str, descripcion:str):
        try:
            request = self.youtube_client.search().list(
                q=subtema,
                part="id,snippet",
                maxResults=30,
                type="video",
                videoCaption="any",
                relevanceLanguage="es",
                order="relevance"
            )
            response = request.execute()
            video_data = []
    
            for item in response['items']:
                video_data.append({'id':item['id']['videoId'],
                                'title':item['snippet']['title'],
                                'description':item['snippet'].get('description', '')
                                })
            texts = [f"{video['title']} {video['description']}" for video in video_data]
            ia_response = await self.ia_service.generateVideoSImilarity(texts, subtema)
            print("ia_response:", ia_response, type(ia_response))

            if isinstance(ia_response, list) and isinstance(ia_response[0], dict):
                ia_response = [item.get("similitud", 0.0) for item in ia_response]

            if isinstance(ia_response, dict):
                ia_response = [ia_response[str(i)] for i in range(len(video_data))]
            if not isinstance(ia_response, list):
                print("Error: ia_response is not a list")
                return None

            for i, video in enumerate(video_data):
                video['similarity'] = ia_response[i] if i < len(ia_response) else 0.0
            video_data.sort(key=lambda x: x['similarity'], reverse=True)
            respuesta =[]
            for i, video in enumerate(video_data[:5]):
                respuesta.append({
                    "id": video['id'],
                    "title": video['title'],
                    "similarity": video['similarity'],
                    "url": f"https://www.youtube.com/watch?v={video['id']}",
                    "thumbnail": f"https://img.youtube.com/vi/{video['id']}/hqdefault.jpg"
                })
            print("Videos encontrados:", respuesta)
            return respuesta
        except Exception as e:
            print(f"Error fetching video details: {e}")
            return None