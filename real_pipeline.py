#!/usr/bin/env python3
import os
import sys
import traceback

def main():
    print("=" * 60)
    print("🚀 YOUTUBE VIDEO AUTOMATION PIPELINE")
    print("=" * 60)
    
    try:
        # Step 1: Create Video
        print("\n" + "▸" * 30)
        print("STEP 1: CREATING VIDEO")
        print("▸" * 30)
        
        # Import and run video creator
        try:
            from video_creator import create_video
            video_file = create_video()
            
            if not video_file:
                video_file = "output_video.mp4"
                
            if not os.path.exists(video_file):
                print(f"❌ Video file not found: {video_file}")
                # Try to find any video
                for f in os.listdir('.'):
                    if f.endswith('.mp4') and os.path.getsize(f) > 1000:
                        print(f"Found alternative: {f}")
                        video_file = f
                        break
                
                if not os.path.exists(video_file):
                    print("❌ No video file created")
                    return False
        except Exception as e:
            print(f"❌ Video creation error: {e}")
            traceback.print_exc()
            return False
        
        print(f"✅ Video created successfully: {video_file}")
        size_mb = os.path.getsize(video_file) / (1024 * 1024)
        print(f"📏 File size: {size_mb:.2f} MB")
        
        # Step 2: Upload to YouTube
        print("\n" + "▸" * 30)
        print("STEP 2: UPLOADING TO YOUTUBE")
        print("▸" * 30)
        
        # Check credentials
        required_env = ['YOUTUBE_CLIENT_ID', 'YOUTUBE_CLIENT_SECRET', 'YOUTUBE_REFRESH_TOKEN']
        has_creds = all([os.getenv(var) for var in required_env])
        
        if has_creds:
            print("✅ YouTube credentials available")
            try:
                from youtube_uploader import upload_video
                success = upload_video(video_file)
                if success:
                    print("✅ Video uploaded to YouTube!")
                else:
                    print("⚠️ YouTube upload failed (check logs)")
            except Exception as e:
                print(f"⚠️ Upload error: {e}")
                # Continue anyway
        else:
            print("ℹ️ No YouTube credentials found")
            print("Add these GitHub Secrets to enable upload:")
            print("1. YOUTUBE_CLIENT_ID")
            print("2. YOUTUBE_CLIENT_SECRET")
            print("3. YOUTUBE_REFRESH_TOKEN")
        
        # Step 3: Rename to final file
        if video_file != "final_video.mp4":
            os.rename(video_file, "final_video.mp4")
            print(f"📁 Renamed to: final_video.mp4")
        
        print("\n" + "=" * 60)
        print("✅ PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ PIPELINE FAILED: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
