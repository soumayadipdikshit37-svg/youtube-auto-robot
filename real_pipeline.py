#!/usr/bin/env python3
import os
import sys

print("=" * 50)
print("🎬 YOUTUBE VIDEO CREATOR")
print("=" * 50)

def main():
    try:
        # Import ONLY when needed
        print("\n1. Importing modules...")
        sys.path.append('.')
        
        # Try to import video creator
        try:
            from video_creator import create_video
            print("✅ video_creator imported")
        except Exception as e:
            print(f"❌ Cannot import video_creator: {e}")
            return False
        
        # Create video
        print("\n2. Creating video...")
        video_file = create_video()
        
        if not video_file or not os.path.exists(video_file):
            print(f"❌ Video file not found: {video_file}")
            # Look for any MP4
            for f in os.listdir('.'):
                if f.endswith('.mp4'):
                    print(f"Found MP4: {f}")
                    video_file = f
                    break
            
            if not os.path.exists(video_file):
                print("❌ No video file created")
                return False
        
        print(f"✅ Video created: {video_file}")
        print(f"📏 Size: {os.path.getsize(video_file) / (1024*1024):.1f} MB")
        
        # Try YouTube upload if credentials exist
        print("\n3. Checking YouTube credentials...")
        has_creds = all([
            os.getenv('YOUTUBE_CLIENT_ID'),
            os.getenv('YOUTUBE_CLIENT_SECRET'),
            os.getenv('YOUTUBE_REFRESH_TOKEN')
        ])
        
        if has_creds:
            print("✅ Credentials found, attempting upload...")
            try:
                from youtube_uploader import upload_video
                if upload_video(video_file):
                    print("✅ Uploaded to YouTube!")
                else:
                    print("⚠️ YouTube upload failed")
            except Exception as e:
                print(f"⚠️ Upload error: {e}")
        else:
            print("ℹ️ No YouTube credentials. Video saved locally.")
        
        # Rename to final_video.mp4
        if video_file != "final_video.mp4":
            os.rename(video_file, "final_video.mp4")
            print("📁 Renamed to: final_video.mp4")
        
        print("\n" + "=" * 50)
        print("✅ PROCESS COMPLETED SUCCESSFULLY")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
