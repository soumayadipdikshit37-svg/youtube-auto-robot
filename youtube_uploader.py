import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class YouTubeUploader:
    def __init__(self):
        self.service = None
        
    def authenticate(self):
        """Simple authentication - NO ERRORS"""
        print("🔐 Step 1: Getting service account...")
        
        # Get from environment
        sa_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
        if not sa_json:
            print("❌ ERROR: GOOGLE_SERVICE_ACCOUNT_JSON not found")
            return False
            
        try:
            print("🔐 Step 2: Parsing JSON...")
            sa_info = json.loads(sa_json)
            print(f"   Service Account: {sa_info['client_email']}")
            
            print("🔐 Step 3: Creating credentials...")
            credentials = service_account.Credentials.from_service_account_info(
                sa_info,
                scopes=['https://www.googleapis.com/auth/youtube.upload'],
                subject='soumayadipdikshit37@gmail.com'  # YOUR EMAIL
            )
            
            print("🔐 Step 4: Building YouTube service...")
            self.service = build('youtube', 'v3', credentials=credentials)
            
            print("✅ SUCCESS! Ready to upload videos")
            return True
            
        except Exception as e:
            print(f"❌ FAILED: {str(e)[:100]}")
            return False
    
    def upload_video(self, video_file, title, description="", category_id="22", tags=None):
        """Upload video - FIXED PARAMETER NAME"""
        if not self.service:
            print("❌ Not authenticated")
            return None
            
        print(f"📤 Uploading: {title}")
        print(f"   File: {video_file}")
        
        # Prepare video metadata
        body = {
            'snippet': {
                'title': title,
                'description': description or 'Automated video upload',
                'categoryId': category_id,
                'tags': tags or ["automation", "youtube", "money"]
            },
            'status': {
                'privacyStatus': 'public',  # Change to 'public'
                'selfDeclaredMadeForKids': False
            }
        }
        
        try:
            # Upload video
            media = MediaFileUpload(video_file, mimetype='video/mp4')
            
            request = self.service.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            response = request.execute()
            video_id = response.get('id')
            
            if video_id:
                print(f"🎉 UPLOADED! Video ID: {video_id}")
                print(f"🔗 URL: https://youtube.com/watch?v={video_id}")
                return video_id
            else:
                print("❌ Upload failed - no video ID")
                return None
                
        except Exception as e:
            print(f"❌ Upload error: {str(e)[:200]}")
            return None

# Simple test
if __name__ == "__main__":
    print("🧪 Testing YouTube Uploader")
    uploader = YouTubeUploader()
    if uploader.authenticate():
        print("✅ Test passed!")
    else:
        print("❌ Test failed")
