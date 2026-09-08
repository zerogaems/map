import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# ==================== البيانات الخاصة بك ====================
BOT_TOKEN = "ضع_التوكن_هنا_بين_التنصيص"      # توكن البوت من BotFather
ADMIN_ID = 123456789                         # آيدي حسابك الشخصي (أرقام فقط)
LOG_CHANNEL_ID = -1001234567890              # آيدي قناة السجلات الخاصة (يبدأ بـ 100- غالباً)
# ============================================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BLACKLIST_WORDS = [
    r"معهد", r"مكتبة", r"دورة", r"خصوصي", r"أستاذ", r"استاذ",
    r"اشترك", r"قناة", r"مـعـهـد", r"مـكـتـبـة",
]

def contains_blacklisted_word(text: str) -> bool:
    if not text:
        return False
    
    # إزالة المسافات للحد من حيل التمويه (م ع ه د)
    cleaned_text = re.sub(r'[\s\-_.]+', '', text)
    
    for pattern in BLACKLIST_WORDS:
        if re.search(pattern, text, re.IGNORECASE) or re.search(pattern, cleaned_text, re.IGNORECASE):
            return True
    return False

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if not message or not message.text:
        return

    user_id = update.effective_user.id

    # استثناء الأدمن الرئيسي من القيود
    if user_id == ADMIN_ID:
        return

    # فحص الكلمات المحظورة
    if contains_blacklisted_word(message.text):
        try:
            user_mention = message.from_user.mention_html()
            chat_title = message.chat.title or "مجموعة"
            deleted_text = message.text

            # 1. حذف الرسالة المخالفة من المجموعة
            await message.delete()
            
            # 2. إرسال تحذير للمستخدم داخل المجموعة
            await message.reply_text(
                f"عذراً {user_mention}، رسالتك فيها كلمات ممنوعة 🚫",
                parse_mode="HTML"
            )

            # 3. إرسال سجل الحذف إلى قناة السجلات الخاصة
            log_text = (
                f"🚨 <b>تنبيه: تم حذف رسالة مخالفة</b>\n\n"
                f"👤 <b>المُرسل:</b> {user_mention} (<code>{user_id}</code>)\n"
                f"📍 <b>المجموعة:</b> {chat_title}\n"
                f"💬 <b>الرسالة المحذوفة:</b>\n<code>{deleted_text}</code>"
            )
            
            await context.bot.send_message(
                chat_id=LOG_CHANNEL_ID,
                text=log_text,
                parse_mode="HTML"
            )
            
            logging.info(f"تم حذف رسالة من {user_id} وإرسال السجل إلى القناة {LOG_CHANNEL_ID}")

        except Exception as e:
            logging.error(f"خطأ أثناء معالجة الرسالة أو إرسال السجل للقناة: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_messages))

    logging.info("البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()
