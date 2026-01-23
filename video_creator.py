import os
import random
import requests
import tempfile
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import textwrap

class VideoCreator:
    def __init__(self):
        self.pexels_key = os.getenv("PEXELS_API_KEY")
        self.stability_key = os.getenv("STABILITY_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
    def generate_ai_image(self, prompt):
        """Generate AI image using Stability AI"""
        try:
            print(f"🖼️  Generating AI image: {prompt[:50]}...")
            
            # Stability AI API call
            headers = {
                "Authorization": f"Bearer {self.stability_key}",
                "Accept": "image/png"
            }
            
            data = {
                "prompt": f"{prompt}, high quality, trending on artstation, 4k",
                "output_format": "png"
            }
            
            # For now, simulate (real API needs specific endpoint)
            print("   ⚠️  Simulation mode - using placeholder")
            print("   ✅ Image concept generated successfully")
            
            # Create simple placeholder image
            img = Image.new('RGB', (1024, 1024), color=(73, 109, 137))
            d = ImageDraw.Draw(img)
            d.text((100, 500), prompt[:30], fill=(255, 255, 255))
            
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            img.save(temp_file.name)
            
            return temp_file.name
            
        except Exception as e:
            print(f"   ❌ AI image error: {e}")
            return None
    
    def get_stock_video(self, query):
        """Get stock video from Pexels"""
        try:
            print(f"🎬 Searching stock video: {query}")
            
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
            # Fallback: create simple video
            return self.create_fallback_video()
            
        except Exception as e:
            print(f"   ❌ Stock video error: {e}")
            return self.create_fallback_video()
    
    def create_fallback_video(self):
        """Create a simple fallback video"""
        print("   🎥 Creating fallback video...")
        
        # Create a simple colored clip
        clip = ColorClip((1280, 720), color=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        clip = clip.set_duration(5)
        
        temp_file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        clip.write_videofile(temp_file.name, fps=24, verbose=False, logger=None)
        
        return temp_file.name
    
    def create_video(self, topic, title):
        """Create complete video"""
        print(f"\n🎬 Creating video: {title}")
        print("=" * 50)
        
        # 1. Get background video
        background = self.get_stock_video(topic)
        
        # 2. Generate AI image for content
        image_prompt = f"Digital art about {topic}, futuristic, vibrant colors"
        ai_image = self.generate_ai_image(image_prompt)
        
        # 3. Combine into final video
        if background and ai_image:
            print("   🎞️  Editing video...")
            
            # Load clips
            bg_clip = VideoFileClip(background).subclip(0, 10)  # 10 seconds
            img_clip = ImageClip(ai_image).set_duration(5).resize(height=400)
            
            # Position image on video
            img_clip = img_clip.set_position(('center', 'center'))
            
            # Create text
            txt_clip = TextClip(title, fontsize=40, color='white', font='Arial')
            txt_clip = txt_clip.set_position(('center', 50)).set_duration(10)
            
            # Composite video
            final = CompositeVideoClip([bg_clip, img_clip.set_start(2), txt_clip])
            
            # Save final video
            output_file = f"video_{random.randint(1000,9999)}.mp4"
            final.write_videofile(output_file, fps=24)
            
            print(f"   ✅ Video created: {output_file}")
            
            # Cleanup temp files
            os.unlink(background)
            if ai_image and os.path.exists(ai_image):
                os.unlink(ai_image)
            
            return output_file
        
        return None
    
    def create_thumbnail(self, title, topic):
        """Create thumbnail image"""
        print(f"🖼️  Creating thumbnail for: {title}")
        
        # Create simple thumbnail
        img = Image.new('RGB', (1280, 720), color=(41, 128, 185))
        draw = ImageDraw.Draw(img)
        
        # Add title text
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # Wrap text
        lines = textwrap.wrap(title, width=30)
        y = 200
        for line in lines:
            draw.text((100, y), line, font=font, fill=(255, 255, 255))
            y += 70
        
        # Add topic
        draw.text((100, 500), f"# {topic}", font=font, fill=(255, 215, 0))
        
        # Save thumbnail
        thumb_file = f"thumbnail_{random.randint(1000,9999)}.png"
        img.save(thumb_file)
        
        print(f"   ✅ Thumbnail created: {thumb_file}")
        return thumb_file

def main():
    print("=" * 50)
    print("VIDEO CREATION PIPELINE")
    print("=" * 50)
    
    creator = VideoCreator()
    
    # Test with sample topic
    topics = ["AI Technology", "Future Tech", "Digital Revolution", "Smart AI"]
    topic = random.choice(topics)
    title = f"The Future of {topic} in 2024"
    
    print(f"\n📹 Topic: {topic}")
    print(f"🏷️  Title: {title}")
    
    # Create video
    video_file = creator.create_video(topic, title)
    
    # Create thumbnail
    if video_file:
        thumbnail = creator.create_thumbnail(title, topic)
        print(f"\n🎉 Pipeline complete!")
        print(f"   Video: {video_file}")
        print(f"   Thumbnail: {thumbnail}")
    else:
        print("\n❌ Video creation failed")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
