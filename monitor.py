import time
import random
import webbrowser
from playwright.sync_api import sync_playwright

# Configuration
TARGET_URL = "https://resell.seetickets.com/dreamnation2026/category/7897/dream-nation-2026-pass-1-jour-vendredi"
CHECK_INTERVAL_MIN = 30  # secondes
CHECK_INTERVAL_MAX = 60  # secondes
# We only want very specific "Call to Action" phrases to avoid false positives from the header/footer
TICKET_PHRASES = ["ajouter au panier", "billet disponible", "acheter maintenant", "disponible"]

def check_for_tickets(page):
    """Checks if any button/link in the main content contains the ticket phrases."""
    try:
        # 1. Quick check in the whole HTML first (case insensitive)
        content = page.content().lower()
        if not any(phrase in content for phrase in TICKET_PHRASES):
            return False

        # 2. Deep check: look for interactive elements but exclude common header/footer IDs
        # We ignore elements with 'cart', 'login', 'nav', 'footer' in their ID or class
        elements = page.query_selector_all("button, a, .btn, [role='button']")
        for el in elements:
            # Exclude header/footer/nav elements to avoid false positives like the cart icon
            attr_html = el.outer_html().lower()
            if any(ignore in attr_html for ignore in ["cart-dropdown", "nav-", "footer", "header", "login"]):
                continue
                
            text = el.inner_text().lower()
            if text and any(phrase in text for phrase in TICKET_PHRASES):
                print(f"Match found: '{text}'")
                return True
    except Exception as e:
        print(f"Error during check: {e}")
    return False

def monitor():
    print(f"Starting monitor on: {TARGET_URL}")
    print(f"Checking every {CHECK_INTERVAL_MIN}-{CHECK_INTERVAL_MAX} seconds...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        # Manual Stealth Implementation (more reliable than the library)
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        try:
            while True:
                print(f"[{time.strftime('%H:%M:%S')}] Checking for tickets...")
                try:
                    page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)
                    page.wait_for_timeout(5000) 
                    
                    if check_for_tickets(page):
                        print("\n!!! TICKET FOUND !!!")
                        print(f"Opening {TARGET_URL} in your browser...")
                        webbrowser.open(TARGET_URL)
                        return 
                    else:
                        print("No tickets available yet.")
                        
                except Exception as e:
                    print(f"Error loading page: {e}")
                
                delay = random.randint(CHECK_INTERVAL_MIN, CHECK_INTERVAL_MAX)
                print(f"Waiting {delay}s before next check...")
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\nMonitor stopped by user.")
        finally:
            browser.close()

if __name__ == "__main__":
    monitor()
