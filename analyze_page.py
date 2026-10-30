from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        # Launch browser with a real-looking profile
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        # We'll check both URLs
        urls = [
            "https://resell.seetickets.com/dreamnation2026/category/7898/dream-nation-2026-pass-1-jour-samedi",
            "https://resell.seetickets.com/dreamnation2026/category/7897/dream-nation-2026-pass-1-jour-vendredi"
        ]
        
        for url in urls:
            print(f"\n--- Analyzing {url} ---")
            try:
                page.goto(url, wait_until="networkidle", timeout=60000)
                # Wait longer for potential ticket lists to load via AJAX
                page.wait_for_timeout(10000) 
                
                content = page.content()
                if "ajouter au panier" in content.lower():
                    print("FOUND: 'ajouter au panier' text in page HTML!")
                    # Try to find the exact element
                    elements = page.query_selector_all("button, a, span, div")
                    for el in elements:
                        text = el.inner_text()
                        if text and "ajouter au panier" in text.lower():
                            print(f"Exact element found: HTML={page.evaluate('el => el.outerHTML', el)}")
                else:
                    print("NOT FOUND: 'ajouter au panier' not in HTML.")
                    
            except Exception as e:
                print(f"Error loading {url}: {e}")
        
        browser.close()

if __name__ == "__main__":
    run()
