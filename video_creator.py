import os
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_video():
    print("🎬 Starting video creation...")
    
    # Video settings
    width, height = 1280, 720  # HD resolution
    duration = 30  # 30 seconds video
    fps = 24
    
    try:
        # Create a simple color clip as background
        print("Creating background...")
        background = ColorClip(size=(width, height), color=(30, 60, 90))
        background = background.set_duration(duration)
        
        # Create text clips
        print("Adding text...")
        
        # Title text
        title_text = "Make $313/month\nwith Passive Income"
        title_clip = TextClip(
            title_text,
            fontsize=70,
            color='white',
            font='Arial-Bold',
            stroke_color='black',
            stroke_width=2,
            align='center',
            size=(width-100, 200)
        )
        title_clip = title_clip.set_position(('center', height//3))
        title_clip = title_clip.set_duration(duration).crossfadein(1).crossfadeout(1)
        
        # Subtitle text
        subtitle_text = "Step-by-Step Guide for Beginners"
        subtitle_clip = TextClip(
            subtitle_text,
            fontsize=40,
            color='yellow',
            font='Arial',
            align='center',
            size=(width-100, 100)
        )
        subtitle_clip = subtitle_clip.set_position(('center', height//2))
        subtitle_clip = subtitle_clip.set_duration(duration).crossfadein(1)
        
        # Create final composite
        print("Compositing video...")
        video = CompositeVideoClip([
            background,
            title_clip,
            subtitle_clip
        ])
        
        # Add silent audio if exists
        if os.path.exists("silent.mp4"):
            print("Adding audio...")
            audio = AudioFileClip("silent.mp4")
            video = video.set_audio(audio)
        else:
            print("No audio file, creating silent video...")
        
        # Write video file
        output_file = "output_video.mp4"
        print(f"Writing video to {output_file}...")
        
        # Use simple settings for reliability
        video.write_videofile(
            output_file,
            fps=fps,
            codec='libx264',
            audio_codec='aac' if os.path.exists("silent.mp4") else None,
            threads=4,
            verbose=False,
            logger=None
        )
        
        # Verify file was created
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            if file_size > 1000:  # At least 1KB
                print(f"✅ Video created successfully: {output_file}")
                print(f"📏 Size: {file_size / (1024*1024):.2f} MB")
                return output_file
            else:
                print("❌ Video file too small, may be corrupt")
                return None
        else:
            print("❌ Video file not created")
            return None
            
    except Exception as e:
        print(f"❌ Error creating video: {e}")
        import traceback
        traceback.print_exc()
        return None

# For direct testing
if __name__ == "__main__":
    result = create_video()
    if result:
        print(f"\n🎉 Video creation complete: {result}")
        exit(0)
    else:
        print("\n❌ Video creation failed")
        exit(1)
