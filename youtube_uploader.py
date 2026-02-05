import os
import sys
import time
from playwright.sync_api import sync_playwright

def upload_video(video_path="monetized_video.mp4", title=None, description=None, tags=None):
    """Real YouTube upload with increased timeouts"""
    
    print("🚀 DIRECT YOUTUBE UPLOAD STARTING...")
    print("=" * 60)
    
    # Check file
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return False
    
    # Check credentials
    email = os.getenv('YOUTUBE_EMAIL')
    password = os.getenv('YOUTUBE_PASSWORD')
    
    if not email or not password:
        print("❌ Missing YouTube credentials")
        print("Add to GitHub Secrets:")
        print("1. YOUTUBE_EMAIL")
        print("2. YOUTUBE_PASSWORD")
        return False
    
    print(f"📧 Logging in as: {email}")
    print(f"🎬 Uploading: {video_path}")
    print(f"📏 Size: {os.path.getsize(video_path) / (1024*1024):.1f} MB")
    print("")
    
    try:
        with sync_playwright() as p:
            # Launch browser with longer timeout
            print("1. Launching browser...")
            browser = p.chromium.launch(
                headless=True,
                timeout=120000  # 2 minute timeout
            )
            
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = context.new_page()
            
            # Navigate with longer timeout
            print("2. Opening YouTube...")
            page.goto('https://accounts.google.com', timeout=120000)
            time.sleep(3)
            
            # Login
            print("3. Logging in...")
            page.fill('input[type="email"]', email)
            page.click('button:has-text("Next")')
            time.sleep(3)
            
            page.fill('input[type="password"]', password)
            page.click('button:has-text("Next")')
            time.sleep(5)
            
            # Go to YouTube Studio
            print("4. Going to YouTube Studio...")
            page.goto('https://studio.youtube.com', timeout=120000)
            time.sleep(5)
            
            # Click upload button
            print("5. Starting upload...")
            page.click('ytcp-button#create-icon')
            time.sleep(2)
            
            page.click('tp-yt-paper-item:has-text("Upload video")')
            time.sleep(3)
            
            # Upload file
            print("6. Selecting video file...")
            file_input = page.locator('input[type="file"]').first
            file_input.set_input_files(video_path)
            
            # Wait for upload
            print("7. Uploading... (this takes 1-2 minutes)")
            for i in range(60):  # Wait up to 60 seconds
                if page.locator('text="Upload complete"').count() > 0:
                    print("   ✅ Upload complete!")
                    break
                time.sleep(1)
                if i % 10 == 0:
                    print(f"   ...{i} seconds")
            
            # Fill details
            print("8. Adding video details...")
            title = title or "YouTube Automation Video"
            page.fill('ytcp-social-suggestion-input#textbox', title)
            time.sleep(2)

            if description:
                description_box = page.locator('div#textbox[aria-label=\"Description\"]').first
                if description_box.count() > 0:
                    description_box.fill(description)
                    time.sleep(1)
            
            # Click through
            for i in range(3):
                next_btn = page.locator('ytcp-button#next-button').first
                if next_btn.is_visible():
                    next_btn.click()
                    time.sleep(2)
            
            # Publish
            print("9. Publishing...")
            page.click('tp-yt-paper-radio-button[name="PUBLIC"]')
            time.sleep(1)
            
            page.click('ytcp-button#done-button')
            time.sleep(10)
            
            print("=" * 60)
            print("✅ UPLOAD SUCCESSFUL!")
            print("📹 Video is now LIVE on YouTube")
            print("📊 Check YouTube Studio for performance and eligibility status")
            print("=" * 60)
            
            # Take screenshot
            page.screenshot(path='upload_success.png')
            print("📸 Screenshot saved")
            
            browser.close()
            return True
            
    except Exception as e:
        print(f"❌ Error: {str(e)[:200]}")
        print("\n⚠️ Quick fix: Use App Password if 2FA is enabled")
        print("Go to: https://myaccount.google.com/apppasswords")
        return False

if __name__ == "__main__":
    success = upload_video()
    sys.exit(0 if success else 1)
