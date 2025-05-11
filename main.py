import os
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_TOKEN") 
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print("=== شروع اجرای برنامه ===")
print(f"TOKEN موجود است؟ {'بله ✅' if TOKEN else '❌ خیر'}")
print(f"CHAT_ID موجود است؟ {'بله ✅' if CHAT_ID else '❌ خیر'}")

def send_test():
    try:
        bot = Bot(token=TOKEN)
        print("ربات ساخته شد ✅")

        bot.send_message(
            chat_id=CHAT_ID,
            text="✅ تست موفقیت‌آمیز! GitHub Actions به تلگرام متصل شد!"
        )
        print("📨 پیام با موفقیت ارسال شد!")
    except Exception as e:
        print(f"⚠️ خطا در ارسال پیام: {e}")

if __name__ == "__main__":
    send_test()
