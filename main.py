import os
from telegram import Bot

# دریافت توکن و چت آیدی از محیط
TOKEN = os.getenv("7758220854:AAFVjFJJNTGwIKGl72hZpMCcVSa1xqO68_s")  # نام متغیر محیطی باید TELEGRAM_TOKEN باشد
CHAT_ID = os.getenv("90476610"
                    
                    
def send_test():
    try:
        bot = Bot(token=TOKEN)
        bot.send_message(
            chat_id=CHAT_ID,
            text="✅ تست موفقیت‌آمیز! GitHub Actions به تلگرام متصل شد!"
        )
        print("پیام با موفقیت ارسال شد!")
    except Exception as e:
        print(f"خطا در ارسال پیام: {e}")

if __name__ == "__main__":
    send_test()
    
  