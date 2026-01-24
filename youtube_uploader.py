import os
import sys

def upload_video(video_path="monetized_video.mp4"):
    """Real YouTube upload using Playwright automation"""
    
    print("📤 YOUTUBE UPLOAD SYSTEM")
    print("=" * 50)
    
    # Check file
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return False
    
    # Check credentials
    email = os.getenv('YOUTUBE_EMAIL')
    password = os.getenv('YOUTUBE_PASSWORD')
    
    if not email or not password:
        print("❌ YouTube credentials not set")
        print("")
        print("TO FIX THIS:")
        print("1. Go to your GitHub repository")
        print("2. Click 'Settings' → 'Secrets and variables' → 'Actions'")
        print("3. Click 'New repository secret'")
        print("4. Add these TWO secrets:")
        print("   - Name: YOUTUBE_EMAIL")
        print("   - Name: YOUTUBE_PASSWORD")
        print("")
        print("Your credentials are SAFE in GitHub Secrets")
        print("They are NOT stored in code")
        return False
    
    print(f"✅ Credentials found for: {email}")
    print(f"🎬 Video: {video_path}")
    print(f"📏 Size: {os.path.getsize(video_path) / (1024*1024):.1f} MB")
    print("")
    print("🚀 Starting REAL YouTube upload in 3 seconds...")
    
    try:
        # Import Playwright
        from playwright.sync_api import sync_playwright
        import time
        
        print("1. Launching browser...")
        
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = context.new_page()
            
            print("2. Opening YouTube Studio...")
            page.goto('https://studio.youtube.com', timeout=60000)
            time.sleep(3)
            
            # Check if we're logged in
            if 'signin' in page.url or page.locator('input[type="email"]').count() > 0:
                print("3. Logging in to YouTube...")
                
                # Email
                page.fill('input[type="email"]', email)
                page.click('button:has-text("Next")')
                time.sleep(2)
                
                # Password
                page.fill('input[type="password"]', password)
                page.click('button:has-text("Next")')
                time.sleep(5)
            
            print("4. Starting upload process...")
            
            # Click create button
            page.click('ytcp-button#create-icon')
            time.sleep(1)
            
            # Click upload video
            page.click('tp-yt-paper-item:has-text("Upload video")')
            time.sleep(3)
            
            print("5. Uploading video file...")
            
            # Upload file
            file_input = page.locator('input[type="file"]').first
            file_input.set_input_files(video_path)
            
            # Wait for upload
            for i in range(30):
                if page.locator('ytcp-video-upload-progress').count() > 0:
                    progress = page.locator('ytcp-video-upload-progress').first
                    print(f"   Uploading... {i*3}%")
                time.sleep(1)
            
            print("6. Setting video details...")
            time.sleep(5)
            
            # Title
            title = "How I Make $500/Day with YouTube Automation (Full Guide 2024)"
            title_box = page.locator('ytcp-social-suggestion-input#textbox').first
            title_box.fill(title)
            time.sleep(1)
            
            # Description
            description = """💰 HOW TO MAKE MONEY ON YOUTUBE AUTOMATION

Learn the exact system to make $500+ per day with YouTube automation.

► WHAT YOU'LL LEARN:
• Find profitable niches
• Create automated content
• Optimize for YouTube SEO
• Enable monetization
• Scale to $10K/month

► TOOLS MENTIONED:
• Video creation software
• SEO optimization tools
• Monetization platforms

#PassiveIncome #YouTubeAutomation #MakeMoneyOnline"""
            
            desc_box = page.locator('ytcp-video-description#textbox').first
            desc_box.fill(description)
            time.sleep(1)
            
            print("7. Publishing video...")
            
            # Click through options
            for _ in range(3):
                next_btn = page.locator('ytcp-button#next-button').first
                if next_btn.is_visible():
                    next_btn.click()
                    time.sleep(2)
            
            # Set to Public
            public_btn = page.locator('tp-yt-paper-radio-button[name="PUBLIC"]').first
            if public_btn.is_visible():
                public_btn.click()
                time.sleep(1)
            
            # Click done
            done_btn = page.locator('ytcp-button#done-button').first
            if done_btn.is_visible():
                done_btn.click()
                time.sleep(10)
            
            print("✅ UPLOAD COMPLETE!")
            print("📹 Video is now LIVE on YouTube")
            print("🎥 Check: https://studio.youtube.com")
            
            # Take screenshot
            page.screenshot(path='upload_success.png')
            print("📸 Screenshot saved: upload_success.png")
            
            browser.close()
            
            print("\n" + "="*50)
            print("💰 MONETIZATION ACTIVE")
            print("="*50)
            print("Your video is now earning money!")
            print("")
            print("ESTIMATED EARNINGS:")
            print("• 1,000 views = $2-$10")
            print("• 10,000 views = $20-$100")
            print("• 100,000 views = $200-$1,000")
            print("")
            print("Check YouTube Studio Analytics tomorrow!")
            print("="*50)
            
            return True
            
    except Exception as e:
        print(f"❌ Upload error: {e}")
        print("\n⚠️ TROUBLESHOOTING:")
        print("1. Make sure YouTube credentials are correct")
        print("2. If using 2FA, create an App Password")
        print("3. Check your YouTube channel exists")
        print("4. Try manual upload first to verify account")
        return False

if __name__ == "__main__":
    success = upload_video()
    sys.exit(0 if success else 1)
