import os
import subprocess

def create_video():
    print("💰 Creating video with FFmpeg...")
    
    # Create video using FFmpeg directly (most reliable)
    output_file = "monetized_video.mp4"
    
    try:
        # Create 60-second test pattern video
        cmd = [
            'ffmpeg', '-f', 'lavfi',
            '-i', 'color=c=blue:s=1280x720:d=60',
            '-vf', "drawtext=text='Make Money on YouTube':fontsize=70:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-t', '60',
            output_file,
            '-y'
        ]
        
        print("Running FFmpeg command...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"✅ VIDEO CREATED: {output_file}")
            print(f"📏 Size: {size_mb:.1f} MB")
            return output_file
        else:
            print(f"FFmpeg error: {result.stderr[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    video = create_video()
    if video:
        print("🎉 SUCCESS!")
        exit(0)
    else:
        print("❌ FAILED")
        exit(1)
