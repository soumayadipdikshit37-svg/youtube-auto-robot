import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import googleapiclient.errors

def upload_video(video_path="final_video.mp4"):
    print(f"📤 Starting YouTube upload for: {video_path}")
    
    # Check if file exists
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return False
    
    # Get credentials
    client_id = os.getenv('YOUTUBE_CLIENT_ID')
    client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
    refresh_token = os.getenv('YOUTUBE_REFRESH_TOKEN')
    
    if not all([client_id, client_secret, refresh_token]):
        print("❌ Missing YouTube credentials")
        print("Set these environment variables:")
        print("1. YOUTUBE_CLIENT_ID")
        print("2. YOUTUBE_CLIENT_SECRET")
        print("3. YOUTUBE_REFRESH_TOKEN")
        return False
    
    try:
        print("Authenticating with YouTube API...")
        
        # Create credentials
        credentials = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_secret
        )
        
        # Build YouTube service
        youtube = build('youtube', 'v3', credentials=credentials)
        
        # Video metadata
        request_body = {
            'snippet': {
                'title': 'Make $313/month with Passive Income - Automated Video',
                'description': 'This video was created automatically using Python automation.\n\nTopics: passive income, online business, automation\n\n#PassiveIncome #Automation #MoneyMaking',
                'tags': ['passive income', 'automation', 'make money online', 'youtube automation'],
                'categoryId': '22'  # People & Blogs
            },
            'status': {
                'privacyStatus': 'private',  # Change to 'public' when ready
                'selfDeclaredMadeForKids': False
            }
        }
        
        print("Uploading video...")
        
        # Upload video
        media = MediaFileUpload(
            video_path,
            mimetype='video/mp4',
            resumable=True,
            chunksize=1024*1024
        )
        
        request = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media
        )
        
        response = request.execute()
        
        print(f"✅ Upload successful!")
        print(f"📺 Video ID: {response.get('id')}")
        print(f"📝 Title: {response['snippet']['title']}")
        print(f"🔒 Privacy: {response['status']['privacyStatus']}")
        
        return True
        
    except googleapiclient.errors.HttpError as e:
        print(f"❌ YouTube API Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False

# For direct testing
if __name__ == "__main__":
    success = upload_video()
    exit(0 if success else 1)
