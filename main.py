import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Bot
from telegram.error import TelegramError

# تنظیمات تلگرام
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TARGET_URL = os.getenv("DIVARURL")

# تنظیمات دیوار
CONTAINER_SELECTOR = "#post-list-container-id"
ITEM_SELECTOR = "article.unsafe-kt-post-card"  
LINK_SELECTOR = "a.unsafe-kt-post-card__action"  # انتخاب لینک آگهی
TITLE_SELECTOR = "h2.unsafe-kt-post-card__title"  # انتخاب عنوان
PRICE_SELECTOR = "div.unsafe-kt-post-card__description"  # انتخاب قیمت

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.binary_location = "/usr/bin/chromium-browser"
    return webdriver.Chrome(options=chrome_options)

def load_history():
    try:
        with open("ads_history.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_history(ads):
    with open("ads_history.json", "w") as f:
        json.dump(ads, f)

def send_telegram(message):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message)
    except TelegramError as e:
        print(f"Error sending message: {e}")

def scrape_ads():
    driver = init_driver()
    driver.get(TARGET_URL)
    container = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, CONTAINER_SELECTOR))
)

    # انتخاب کانتینر اصلی
    container = driver.find_element(By.CSS_SELECTOR, CONTAINER_SELECTOR)
    
    # انتخاب تمام آگهی‌ها
    ads = container.find_elements(By.CSS_SELECTOR, ITEM_SELECTOR)

    existing_ads = load_history()
    new_ads = []

    for ad in ads:
        try:
            # استخراج لینک
            link_element = ad.find_element(By.CSS_SELECTOR, LINK_SELECTOR)
            link = link_element.get_attribute("href")
            ad_id = link.split("/")[-1]  # استخراج آیدی از لینک
            
            if ad_id not in existing_ads:
                # استخراج عنوان
                title = ad.find_element(By.CSS_SELECTOR, TITLE_SELECTOR).text
                
                # استخراج قیمت
                price = ad.find_element(By.CSS_SELECTOR, PRICE_SELECTOR).text
                
                # ارسال پیام
                message = f"🏠 آگهی جدید\nعنوان: {title}\nقیمت: {price}\nلینک: {link}"
                send_telegram(message)
                new_ads.append(ad_id)
                
        except Exception as e:
            print(f"Error processing ad: {e}")

    if new_ads:
        save_history(existing_ads + new_ads)

    driver.quit()

if __name__ == "__main__":
    scrape_ads()