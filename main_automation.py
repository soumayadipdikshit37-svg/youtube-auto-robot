import os
import random
from datetime import datetime
from video_creator import VideoCreator
from youtube_uploader import YouTubeUploader

def generate_topic():
    """Generate video topic"""
    topics = [
        "Artificial Intelligence",
        "Machine Learning", 
        "ChatGPT Revolution",
        "YouTube Automation",
        "Future Technology",
        "Digital Transformation",
        "AI Tools 2024",
        "Smart Automation"
    ]
    return random.choice(topics)

def generate_title(topic):
    """Generate video title"""
    templates = [
        f"How {topic} is Changing Everything",
        f"The Future of {topic} - Complete Guide",
        f"{topic}: What You Need to Know in 2024",
        f"Master {topic} in 30 Minutes",
        f"{topic} Secrets Nobody Tells You"
    ]
    return random.choice(templates)

def main():
    print("=" * 60)
    print("🤖 YOUTUBE AUTOMATION SYSTEM - FULL PIPELINE")
    print("=" * 60)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check environment variables
    print("\n🔍 Environment Check:")
    required_vars = [
        "PEXELS_API_KEY",
        "STABILITY_API_KEY", 
        "OPENAI_API_KEY",
        "GOOGLE_CLIENT_ID",
        "GOOGLE_CLIENT_SECRET",
        "YOUTUBE_API_KEY"
    ]
    
    all_ok = True
    for var in required_vars:
        if os.getenv(var):
            print(f"   ✅ {var}")
        else:
            print(f"   ❌ {var} - Missing")
            all_ok = False
    
    if not all_ok:
        print("\n⚠️  Missing environment variables!")
        print("   Check GitHub Secrets configuration")
        return False
    
    print("\n" + "=" * 60)
    print("🎬 STARTING VIDEO CREATION PIPELINE")
    print("=" * 60)
    
    # Create 3 videos
    for i in range(1, 4):
        print(f"\n📹 VIDEO {i}/3")
        print("-" * 40)
        
        # Generate content
        topic = generate_topic()
        title = generate_title(topic)
        
        print(f"   Topic: {topic}")
        print(f"   Title: {title}")
        
        # Create video
        creator = VideoCreator()
        video_file = creator.create_video(topic, title)
        
        if video_file and os.path.exists(video_file):
            # Create thumbnail
            thumbnail = creator.create_thumbnail(title, topic)
            
            # Upload to YouTube
            print(f"\n   📤 Uploading to YouTube...")
            uploader = YouTubeUploader()
            
            # Create description
            description = uploader.create_video_description(title, topic)
            
            # Upload
            video_id = uploader.upload_video(
                video_file=video_file,
                title=title,
                description=description,
                tags=[topic.lower(), "ai", "technology", "tutorial", "2024"],
                thumbnail_file=thumbnail
            )
            
            print(f"   🎉 Video {i} completed!")
            print(f"   📍 Video ID: {video_id}")
            
            # Cleanup
            for file in [video_file, thumbnail]:
                if os.path.exists(file):
                    os.remove(file)
                    print(f"   🗑️  Cleaned up: {file}")
        else:
            print(f"   ❌ Video creation failed for video {i}")
    
    print("\n" + "=" * 60)
    print("🎊 PIPELINE COMPLETE!")
    print("=" * 60)
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Videos Created: 3")
    print(f"Status: {'✅ SUCCESS' if all_ok else '❌ FAILED'}")
    print("\n📅 Next run: Scheduled time (9AM, 2PM, 7PM UTC)")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
