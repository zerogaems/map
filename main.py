import os
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# جلب التوكن من متغيرات البيئة (Environment Variables) في Render أو وضعه مباشرة
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8036903555:AAGroUTxYo2dghkMf-_ifFTxjlDauC2nLv4")
WEB_APP_URL = "https://zerogaems.github.io/map/"  # رابط موقعك الـ HTML الجاهز

bot = TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    
    welcome_text = (
        f"أهلاً بك يا {user_name} في **بوت خريطة الكلية والمستجدين** 🎓✨\n\n"
        "هذا البوت صُمم ليكون دليلك الشامل لجميع أقسام الكلية (الهمك، التوسع، العلوم، والأداب) "
        "لتسهيل الوصول للقاعات والمخابر عبر خريطة تفاعلية.\n\n"
        "💡 **تم تطوير البوت بواسطة:** [@Youssef_Sabra]\n\n"
        "اضغط على الزر أدناه لفتح الخريطة التفاعلية مباشرةً 👇"
    )

    markup = InlineKeyboardMarkup(row_width=1)
    
    # 1. زر الـ Web App لفتح خريطة الـ HTML التفاعلية
    web_app_btn = InlineKeyboardButton(
        text="🗺 فتح خريطة الكلية التفاعلية", 
        web_app=WebAppInfo(url=WEB_APP_URL)
    )
    
    # 2. زر التواصل مع المطور
    developer_btn = InlineKeyboardButton(
        text="💬 تواصل مع ممثل الدفعة / المطور", 
        url="https://t.me/Y0USSEF_SABRA"
    )

    # 3. زر قنوات الدفعة
    channels_btn = InlineKeyboardButton(
        text="📢 بوت الانضمام لقنوات سنتك", 
        url="https://t.me/YourChannelLink"
    )

    markup.add(web_app_btn, developer_btn, channels_btn)

    bot.send_message(
        chat_id=message.chat.id,
        text=welcome_text,
        parse_mode="Markdown",
        reply_markup=markup
    )

if __name__ == "__main__":
    bot.infinity_polling()

