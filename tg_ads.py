from playwright.sync_api import sync_playwright
import urllib.parse

def intercept_api_payload():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(storage_state="session.json")
        page = context.new_page()

        print("Заходим в кабинет...")

        def analyze_request(request):
            # Ловим только запросы к API с хешем и только те, которые отправляют данные (POST)
            if "ads.telegram.org/api?hash=" in request.url and request.method == "POST":
                print(f"\n--- ПОЙМАНА КОМАНДА! ---")
                print(f"URL: {request.url}")
                
                # Получаем и расшифровываем данные, чтобы они были читаемыми
                raw_data = request.post_data
                if raw_data:
                    decoded_data = urllib.parse.unquote(raw_data)
                    print(f"Отправленные данные: {decoded_data}")

        page.on("request", analyze_request)
        page.goto("https://ads.telegram.org/account")
        
        print("\nГотово! Теперь зайди в создание кампании (Create a new ad).")
        print("Заполни поля любым тестовым текстом и нажми кнопку создания/сохранения.")
        
        try:
            page.wait_for_event("close", timeout=0)
        except Exception:
            pass
            
        browser.close()

if __name__ == "__main__":
    intercept_api_payload()
    