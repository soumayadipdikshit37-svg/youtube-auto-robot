import os
import json
import sys
from datetime import datetime
from video_creator import VideoCreator
from youtube_uploader import YouTubeUploader

def main():
    print("=" * 60)
    print("🤖 REAL YOUTUBE AUTOMATION PIPELINE")
    print("=" * 60)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Environment check
    print("🔍 Environment Check:")
    if not os.environ.get('PEXELS_API_KEY'):
        print("   ❌ PEXELS_API_KEY not found")
        return
    print("   ✅ PEXELS_API_KEY - Ready for video downloads")
    
    # Import check
    try:
        from video_creator import VideoCreator
        print("   ✅ Video Creator imported")
    except:
        print("   ❌ Video Creator import failed")
        return
        
    try:
        from youtube_uploader import YouTubeUploader
        print("   ✅ YouTube Uploader imported")
    except:
        print("   ❌ YouTube Uploader import failed")
        return
    
    print("⚡ Starting automation...")
    print("=" * 60)
    
    # Step 1: Create video
    print("\n🚀 CREATING REAL YOUTUBE VIDEO")
    print("=" * 60)
    
    # Video details (you can customize these)
    topics = [
        "YouTube Automation", "Passive Income", "Online Business",
        "Make Money Online", "AI Tools", "Side Hustle",
        "Digital Marketing", "Content Creation", "Freelancing"
    ]
    
    import random
    topic = random.choice(topics)
    earnings = random.randint(300, 1000)
    
    video_title = f"Make ${earnings}/Month with {topic}"
    video_description = f"Learn how to make ${earnings}/month with {topic}. This is an automated video created using Python and AI tools."
    video_tags = [topic.lower(), "automation", "make money", "passive income", "youtube"]
    
    print(f"📹 Video Details:")
    print(f"   Topic: {topic}")
    print(f"   Title: {video_title}")
    print(f"   Earnings: ${earnings}/month")
    
    # Create video
    print("\n🎬 Step 1: Creating video...")
    creator = VideoCreator()
    video_file = creator.create_video(
        search_query=topic,
        title=video_title,
        earnings=earnings
    )
    
    if not video_file or not os.path.exists(video_file):
        print("   ❌ Video creation failed")
        return
    
    print(f"   ✅ Video created: {video_file}")
    print(f"   Size: {os.path.getsize(video_file)} bytes")
    
    # Create thumbnail
    print("\n🖼️  Step 2: Creating thumbnail...")
    thumbnail_file = creator.create_thumbnail(
        title=video_title,
        earnings=earnings
    )
    
    if thumbnail_file and os.path.exists(thumbnail_file):
        print(f"   ✅ Thumbnail created: {thumbnail_file}")
    else:
        print("   ⚠️  Thumbnail creation failed or skipped")
        thumbnail_file = None
    
    # Upload to YouTube
    print("\n📤 Step 3: Uploading to YouTube...")
    uploader = YouTubeUploader()
    
    if uploader.authenticate():
        print("   ✅ Authenticated with YouTube")
        
        try:
            # FIXED: Correct parameters for upload_video
            video_id = uploader.upload_video(
                video_file=video_file,           # Required
                title=video_title,               # Required
                description=video_description,   # Optional
                category_id="22",                # Optional (22 = People & Blogs)
                tags=video_tags                  # Optional
                # thumbnail_file removed - not supported in basic upload
            )
            
            if video_id:
                print(f"   🎉 UPLOAD SUCCESS!")
                print(f"   Video ID: {video_id}")
                print(f"   🔗 YouTube URL: https://youtube.com/watch?v={video_id}")
            else:
                print("   ❌ Upload failed - no video ID returned")
                
        except Exception as e:
            print(f"   ⚠️  Upload error: {e}")
            video_id = None
    else:
        print("   ❌ YouTube authentication failed")
        video_id = None
    
    # Save results
    print("\n💾 Results saved to: video_result.json")
    results = {
        "title": video_title,
        "video_file": video_file,
        "thumbnail_file": thumbnail_file,
        "video_id": video_id,
        "youtube_url": f"https://youtube.com/watch?v={video_id}" if video_id else None,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "topic": topic,
        "earnings": earnings
    }
    
    with open('video_result.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 EXECUTION SUMMARY")
    print("=" * 60)
    
    if video_file and os.path.exists(video_file):
        print("🎉 SUCCESS! Video created successfully!")
        print(f"   Title: {video_title}")
        print(f"   Video File: {video_file}")
        print(f"   Created at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if video_id:
            print(f"   ✅ Uploaded to YouTube: {video_id}")
        else:
            print("   ⚠️  Not uploaded to YouTube (check logs)")
    else:
        print("❌ FAILED! Video creation failed")
    
    print("\n📁 All created files:")
    for file in [video_file, thumbnail_file, 'video_result.json', 'requirements.txt']:
        if file and os.path.exists(file):
            print(f"   • {file}")
    
    print(f"\n⏰ End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 Status: {'SUCCESS' if video_file else 'FAILED'}")
    print("=" * 60)

if __name__ == "__main__":
    main()
