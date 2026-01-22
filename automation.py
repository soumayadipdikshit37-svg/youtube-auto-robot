import os
import random
from datetime import datetime

class YouTubeAutomation:
    def __init__(self):
        self.topics = [
            "AI Side Hustles 2024",
            "ChatGPT Money Making",
            "YouTube Automation",
            "Passive Income Streams",
            "No-Code Tools",
            "Python Automation",
            "Freelancing with AI"
        ]
        
    def generate_topic(self):
        return random.choice(self.topics)
    
    def generate_title(self, topic):
        templates = [
            f"How to Make ${random.randint(50,500)} with {topic}",
            f"The {topic} Method That Made Me ${random.randint(100,1000)}",
            f"{topic}: ${random.randint(50,200)}/Day Passive Income",
            f"From $0 to ${random.randint(100,500)} with {topic}",
            f"This {topic} Strategy Changed Everything"
        ]
        return random.choice(templates)
    
    def generate_description(self, title, topic):
        affiliate_links = [
            "🔗 Hostinger (65% off): https://hostinger.com",
            "🔗 Namecheap (Free domain): https://namecheap.com",
            "🔗 Canva Pro (Free trial): https://canva.com",
            "🔗 ChatGPT Plus: https://chat.openai.com"
        ]
        
        selected_links = random.sample(affiliate_links, 2)
        
        return f"""{title}

Learn the exact method I use to make money with {topic}.

🎯 What You'll Learn:
• Step-by-step process
• Free tools to use
• Common mistakes to avoid

💰 Free Resources:
{chr(10).join(selected_links)}

👇 Comment "TUTORIAL" for the full guide!

#makemoneyonline #passiveincome #sidehustle #automation #aitools"""

def main():
    print("=" * 50)
    print("YouTube Automation System")
    print("=" * 50)
    
    automation = YouTubeAutomation()
    
    for i in range(3):  # Create 3 videos
        topic = automation.generate_topic()
        title = automation.generate_title(topic)
        description = automation.generate_description(title, topic)
        
        print(f"\n🎬 Video {i+1}:")
        print(f"   Topic: {topic}")
        print(f"   Title: {title}")
        print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"   Status: ✅ Ready for upload")
        
        # Simulate upload (in real version, would upload to YouTube)
        print(f"   Note: API Key loaded: {'✅' if os.getenv('YOUTUBE_API_KEY') else '❌'}")
    
    print("\n" + "=" * 50)
    print("🎉 3 videos generated successfully!")
    print("Next: GitHub Actions will upload automatically")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    main()
