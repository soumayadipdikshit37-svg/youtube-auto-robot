import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime

class YouTubeUploader:
    def __init__(self):
        # Service account JSON from GitHub Secrets
        self.service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        
    def get_authenticated_service(self):
        """Authenticate using Service Account"""
        print("🔐 Authenticating with Service Account...")
        
        try:
            if not self.service_account_json:
                print("   ❌ GOOGLE_SERVICE_ACCOUNT_JSON not found")
                return None
            
            # Parse JSON from environment variable
            service_account_info = json.loads(self.service_account_json)
            
            # Create credentials
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info,
                scopes=['https://www.googleapis.com/auth/youtube.upload']
            )
            
            # Build YouTube service
            youtube = build('youtube', 'v3', credentials=credentials)
            
            print("   ✅ Authenticated successfully!")
            return youtube
            
        except Exception as e:
            print(f"   ❌ Authentication failed: {e}")
            return None
    
    def upload_video(self, video_file, title, description, tags, thumbnail_file=None):
        """REAL YouTube upload using Service Account"""
        print(f"\n📤 REAL YouTube Upload Starting...")
        print(f"   Title: {title}")
        print(f"   File: {video_file}")
        
        try:
            # Authenticate
            youtube = self.get_authenticated_service()
            if not youtube:
                print("   ❌ Cannot authenticate")
                return None
            
            # Check file exists
            if not os.path.exists(video_file):
                print(f"   ❌ File not found: {video_file}")
                return None
            
            # Video metadata
            body = {
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "categoryId": "22"  # Education
                },
                "status": {
                    "privacyStatus": "public",  # Change to "private" for testing
                    "selfDeclaredMadeForKids": False
                }
            }
            
            file_size = os.path.getsize(video_file)
            print(f"   📦 Uploading {file_size:,} bytes...")
            
            # Upload video
            media = MediaFileUpload(
                video_file,
                mimetype="video/mp4",
                resumable=True,
                chunksize=1024*1024  # 1MB chunks
            )
            
            # Insert request
            request = youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )
            
            # Execute with progress
            response = None
            print("   ⏳ Uploading...")
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    print(f"   📊 Progress: {progress}%")
            
            # Get video ID
            video_id = response['id']
            
            print(f"   ✅ REAL UPLOAD SUCCESSFUL!")
            print(f"   🎥 Video ID: {video_id}")
            print(f"   🔗 YouTube URL: https://youtube.com/watch?v={video_id}")
            
            # Upload thumbnail if provided
            if thumbnail_file and os.path.exists(thumbnail_file):
                print(f"   🖼️  Uploading thumbnail...")
                try:
                    youtube.thumbnails().set(
                        videoId=video_id,
                        media_body=MediaFileUpload(thumbnail_file)
                    ).execute()
                    print(f"   ✅ Thumbnail uploaded!")
                except Exception as thumb_error:
                    print(f"   ⚠️  Thumbnail upload failed: {thumb_error}")
            
            return video_id
            
        except Exception as e:
            print(f"   ❌ REAL Upload failed: {e}")
            return None
    
    def create_video_description(self, title, topic):
        """Create YouTube video description"""
        return f"""{title}

Learn how to automate {topic} for passive income. This automated system creates videos 24/7.

📌 In This Video:
• Introduction to {topic}
• Tools and platforms needed
• Step-by-step setup guide
• Monetization strategies

🛠️ Tools Used:
• Python automation
• AI content generation
• Free APIs for data
• Cloud platforms

👇 COMMENT below what you want to learn next!

🔔 SUBSCRIBE for daily automation tutorials!

#aitools #automation #passiveincome #makemoneyonline #{topic.lower().replace(' ', '')}"""

def main():
    print("=" * 60)
    print("REAL YouTube Uploader - Service Account Version")
    print("=" * 60)
    
    uploader = YouTubeUploader()
    
    # Test authentication
    print("\n🔍 Testing authentication...")
    service = uploader.get_authenticated_service()
    
    if service:
        print("✅ Ready for REAL YouTube uploads!")
        print("\n🎯 Next steps:")
        print("1. Run workflow to create videos")
        print("2. Videos will upload to YouTube automatically")
        print("3. Check your YouTube channel!")
    else:
        print("❌ Authentication failed")
        print("Check GOOGLE_SERVICE_ACCOUNT_JSON in GitHub Secrets")

if __name__ == "__main__":
    main()
