import time
import random
import webbrowser
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth

# Configuration
TARGET_URL = "https://resell.seetickets.com/dreamnation2026/category/7897/dream-nation-2026-pass-1-jour-vendredi"
CHECK_INTERVAL_MIN = 30  # secondes
CHECK_INTERVAL_MAX = 60  # secondes
KEYWORDS = ["ajouter", "achat", "disponible", "panier"]

def check_for_tickets(page):
    """Checks if any button/link contains the target keywords."""
    try:
        # Search for any element containing the keywords
        # We search for 'ajouter' as requested by the user
        content = page.content().lower()
        if any(word in content for word in KEYWORDS):
            # Refine search to see if it's actually a button/link
            elements = page.query_selector_all("button, a, .btn, [role='button']")
            for el in elements:
                text = el.inner_text()
                if text and any(word in text.lower() for word in KEYWORDS):
                    return True
    except Exception as e:
        print(f"Error during check: {e}")
    return False

def monitor():
    print(f"Starting monitor on: {TARGET_URL}")
    print(f"Checking every {CHECK_INTERVAL_MIN}-{CHECK_INTERVAL_MAX} seconds...")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        stealth(page)
        
        try:
            while True:
                print(f"[{time.strftime('%H:%M:%S')}] Checking for tickets...")
                try:
                    page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)
                    page.wait_for_timeout(5000) # Wait for JS rendering
                    
                    if check_for_tickets(page):
                        print("\n!!! TICKET FOUND !!!")
                        print(f"Opening {TARGET_URL} in your browser...")
                        webbrowser.open(TARGET_URL)
                        # We stop the bot here so the user can buy the ticket
                        return 
                    else:
                        print("No tickets available yet.")
                        
                except Exception as e:
                    print(f"Error loading page: {e}")
                
                # Random delay to avoid bot detection
                delay = random.randint(CHECK_INTERVAL_MIN, CHECK_INTERVAL_MAX)
                print(f"Waiting {delay}s before next check...")
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\nMonitor stopped by user.")
        finally:
            browser.close()

if __name__ == "__main__":
    monitor()
