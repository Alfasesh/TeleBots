import os
import telebot
from telebot import types
from flask import Flask, request

# جلب التوكن من متغير البيئة
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("❌ لم يتم العثور على التوكن! أضفه في Render Environment Variables.")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ====== أوامر البوت ======
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("⏰ تذكير الآن")
    btn2 = types.KeyboardButton("📌 عن البوت")
    markup.add(btn1, btn2)

    bot.reply_to(
        message,
        "👋 أهلاً بك في *بوت التذكير بأوقات الصلاة* \n\n"
        "✅ سأقوم بنشر أوقات الصلاة في القناة بشكل تلقائي.\n"
        "✅ يمكنك أيضاً طلب تذكير يدوي بأي وقت.\n\n"
        "📢 اشتركوا في القناة: @ALTHlKR",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.message_handler(func=lambda msg: msg.text == "⏰ تذكير الآن")
def reminder_now(message):
    bot.reply_to(message, "🔔 هذا تذكير تجريبي للتأكد من أن البوت يعمل ✅")

@bot.message_handler(func=lambda msg: msg.text == "📌 عن البوت")
def about_bot(message):
    bot.reply_to(
        message,
        "📖 هذا البوت مخصص لنشر أوقات الصلاة والتذكيرات.\n"
        "🚀 تم تطويره باستخدام Python وTelegram Bot API.\n"
        "📢 تابع قناتنا: @ALTHlKR"
    )

# ====== إعداد الـ Webhook ======
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_str = request.stream.read().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # هنا يجب أن تضع رابط البوت من Render بعد النشر
    url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    bot.set_webhook(url=url)
    return "Webhook set!", 200

# ====== تشغيل Flask ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
