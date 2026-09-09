import os
import threading
from flask import Flask
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# إعداد خادم وهمي لفتح Port على Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# ==================== [ إعدادات البوت ] ====================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8036903555:AAGroUTxYo2dghkMf-_ifFTxjlDauC2nLv4")
WEB_APP_URL = "https://zerogaems.github.io/map/"
DEVELOPER_USERNAME = "@Youssef_Sabra"
CHANNEL_URL = "https://t.me/Hamak456"

bot = TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_first_name = message.from_user.first_name
    
    welcome_text = (
        f"أهلاً بك يا **{user_first_name}** في بوت الخريطة التفاعلية للطلاب المستجدين! 🎓✨\n\n"
        "تم إعداد هذا البوت ليكون دليلك المباشر والسريع داخل الكلية، "
        "لتتمكن من العثور على القاعات، المخابر، والمدرجات بسهولة سواء في **مبنى الهمك** أو **مبنى التوسع (العلوم والآداب)**.\n\n"
        f"🛠 **تم تطوير وإعداد البوت بواسطة:** [@{DEVELOPER_USERNAME}]\n\n"
        "اضغط على الزر أدناه لفتح الخريطة التفاعلية واستكشاف الأقسام 👇"
    )

    markup = InlineKeyboardMarkup(row_width=1)
    
    btn_web_app = InlineKeyboardButton(
        text="🗺 فتح الخريطة التفاعلية", 
        web_app=WebAppInfo(url=WEB_APP_URL)
    )
    btn_developer = InlineKeyboardButton(
        text="💬 تواصل مع ممثل الدفعة / المطور", 
        url=f"https://t.me/{DEVELOPER_USERNAME}"
    )
    btn_channel = InlineKeyboardButton(
        text="📢 قناة الدفعة والإعلانات", 
        url=CHANNEL_URL
    )

    markup.add(btn_web_app, btn_developer, btn_channel)

    bot.send_message(
        chat_id=message.chat.id,
        text=welcome_text,
        parse_mode="Markdown",
        reply_markup=markup
    )

if __name__ == "__main__":
    # تشغيل سيرفر Flask في Thread منفصل
    threading.Thread(target=run_flask, daemon=True).start()
    
    # تشغيل البوت
    bot.infinity_polling()

