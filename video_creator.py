import os
import random
import requests
import tempfile
import subprocess
from PIL import Image, ImageDraw, ImageFont

class VideoCreator:
    def __init__(self):
        self.pexels_key = os.getenv("PEXELS_API_KEY")
        
    def get_stock_video(self, query):
        """Get stock video from Pexels"""
        try:
            print(f"🎬 Searching stock video: {query}")
            
            if not self.pexels_key:
                print("   ⚠️  No Pexels key, using fallback")
                return self.create_color_video()
            
            # Pexels API call
            headers = {"Authorization": self.pexels_key}
            url = f"https://api.pexels.com/videos/search?query={query}&per_page=1"
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('videos'):
                    video_url = data['videos'][0]['video_files'][0]['link']
                    
                    # Download video
                    print(f"   📥 Downloading video...")
                    video_response = requests.get(video_url)
                    
                    temp_file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
                    temp_file.write(video_response.content)
                    temp_file.close()
                    
                    print(f"   ✅ Video downloaded: {os.path.basename(temp_file.name)}")
                    return temp_file.name
            
            print("   ⚠️  Using fallback video")
            return self.create_color_video()
            
        except Exception as e:
            print(f"   ❌ Stock video error: {e}")
            return self.create_color_video()
    
    def create_color_video(self):
        """Create a simple colored video with FFmpeg"""
        print("   🎥 Creating color video...")
        
        colors = ["red", "blue", "green", "purple", "orange"]
        color = random.choice(colors)
        
        temp_file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        
        # Create video with FFmpeg (no ImageMagick needed)
        cmd = f'ffmpeg -f lavfi -i color=c={color}:s=1280x720:d=30 -c:v libx264 {temp_file.name} -y'
        subprocess.run(cmd, shell=True, capture_output=True)
        
        return temp_file.name
    
    def create_video(self, topic, title):
        """Create complete video using ONLY FFmpeg (no ImageMagick)"""
        print(f"\n🎬 Creating video: {title}")
        print("=" * 50)
        
        # 1. Get background video
        background = self.get_stock_video(topic)
        
        # 2. Create final video with text using FFmpeg
        output_file = f"video_{random.randint(1000,9999)}.mp4"
        
        # Simple FFmpeg command to add text
        # This uses FFmpeg's built-in drawtext filter (no ImageMagick needed)
        cmd = f"""
        ffmpeg -y -i {background} \
        -vf "drawtext=text='{title}':fontcolor=white:fontsize=48:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=(h-text_h)/2" \
        -c:v libx264 -preset fast -crf 25 \
        -c:a aac -b:a 128k \
        -t 30 \
        {output_file}
        """
        
        print("   🎞️  Adding text to video...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   ✅ Video created: {output_file}")
            
            # Cleanup temp file
            if os.path.exists(background):
                os.unlink(background)
            
            return output_file
        else:
            print(f"   ❌ FFmpeg failed: {result.stderr[:200]}")
            return None
    
    def create_thumbnail(self, title, topic):
        """Create thumbnail using PIL (no ImageMagick)"""
        print(f"🖼️  Creating thumbnail: {title}")
        
        # Create simple thumbnail with PIL
        img = Image.new('RGB', (1280, 720), color=(30, 30, 46))
        draw = ImageDraw.Draw(img)
        
        # Simple text
        try:
            # Try to use default font
            from PIL import ImageFont
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", 60)
            except:
                font = ImageFont.load_default()
        except:
            font = None
        
        # Draw title (simple, split into two lines if too long)
        if len(title) > 40:
            lines = [title[:40], title[40:80]] if len(title) > 80 else [title]
        else:
            lines = [title]
        
        y = 250
        for line in lines:
            if font:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (1280 - text_width) / 2
                draw.text((x, y), line, font=font, fill=(255, 255, 255))
            else:
                draw.text((100, y), line, fill=(255, 255, 255))
            y += 80
        
        # Save thumbnail
        thumb_file = f"thumbnail_{random.randint(1000,9999)}.png"
        img.save(thumb_file)
        
        print(f"   ✅ Thumbnail created: {thumb_file}")
        return thumb_file

# Simple test function
def main():
    print("=" * 50)
    print("SIMPLE VIDEO CREATOR TEST")
    print("=" * 50)
    
    creator = VideoCreator()
    
    # Test
    title = "Make $500/Month with AI"
    video_file = creator.create_video("AI Technology", title)
    
    if video_file:
        thumbnail = creator.create_thumbnail(title, "AI Technology")
        print(f"\n✅ SUCCESS! Video: {video_file}, Thumbnail: {thumbnail}")
    else:
        print("\n❌ Failed to create video")

if __name__ == "__main__":
    main()
