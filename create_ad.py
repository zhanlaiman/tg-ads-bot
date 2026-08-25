from playwright.sync_api import sync_playwright

def create_telegram_ad_fast():
    api_hash = "e9cc72690a04103947" 
    url = f"https://ads.telegram.org/api?hash={api_hash}"
    
    # Теперь данные собраны в аккуратный словарь. Здесь легко менять текст и бюджет!
    payload = {
        "owner_id": "NnMn7WF3HxS3VrJ5qL9nyHg-w1RWXOwhvpP03Xl0tctnAXuIa0l76mWV7m6q0bM1",
        "title": "AUTO SCRIPT TEST",
        "text": "Тестовое объявление через код!",
        "promote_url": "t.me/astana_gb_eng",
        "cpm": "0.13",
        "budget": "1",
        "views_per_user": "1",
        "daily_budget": "0",
        "active": "0", # 0 означает, что объявление появится со статусом "On Hold" (не спишет деньги сразу)
        
        # Настройки таргетинга (таргет на русскоязычные каналы)
        "target_type": "channels",
        "langs": "ru",
        "placement": "channel_post",
        "picture": "1",
        
        # Обязательные пустые поля (чтобы сервер не ругался)
        "website_name": "", "website_photo": "", "media": "", "ad_info": "", 
        "device": "", "topics": "", "exclude_topics": "", "channels": "", 
        "exclude_channels": "", "countries": "", "locations": "", 
        "user_langs": "", "user_topics": "", "exclude_user_topics": "", 
        "user_channels": "", "exclude_user_channels": "", "bots": "", 
        "search_queries": "",
        
        "method": "createAd"
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state="session.json")
        
        print("Отправляю запрос через невидимый браузер...")
        
        # Обрати внимание: теперь мы используем form=payload вместо data=payload
        # Playwright сам правильно запакует наш словарь!
        response = context.request.post(
            url,
            form=payload,
            headers={
                "X-Requested-With": "XMLHttpRequest"
            }
        )
        
        response_text = response.text()
        
        if '"error"' not in response_text:
            print("\n✅ УСПЕХ! Ответ сервера:")
            print(response_text)
            print("\nЗайди в кабинет Telegram Ads — объявление 'AUTO SCRIPT TEST' должно быть там!")
        else:
            print(f"\n❌ Ошибка сервера: {response_text}")
            
        browser.close()

if __name__ == "__main__":
    create_telegram_ad_fast()
    