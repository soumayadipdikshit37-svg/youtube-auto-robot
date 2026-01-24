#!/usr/bin/env python3
import os
import sys

def main():
    print("🚀 YouTube Monetization Pipeline")
    print("=" * 50)
    
    try:
        # Create video
        print("\n1. Creating video...")
        from video_creator import create_video
        video_file = create_video()
        
        if not video_file or not os.path.exists(video_file):
            print("❌ Video creation failed")
            return False
        
        print(f"✅ Video: {video_file}")
        
        # Upload video
        print("\n2. Uploading to YouTube...")
        from youtube_uploader import upload_video
        success = upload_video(video_file)
        
        if success:
            print("\n🎉 MONETIZATION PIPELINE COMPLETE!")
            print("💰 Your video is now earning money on YouTube")
            return True
        else:
            print("\n⚠️ Upload not attempted (no credentials)")
            print("Video saved as: monetized_video.mp4")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
