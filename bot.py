from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import random
from gtts import gTTS
import os

TOKEN = "7249434959:AAHHL5ohHRPf2wO_jyxs3ZdQWrJMPI1OkKA"

# Список тем для общения
topics = [
    "📖 Какую последнюю книгу ты прочитал?",
    "🌍 Если бы ты мог жить в любой стране, что бы ты выбрал?",
    "💬 Какое твое любимое английское выражение?",
    "🎬 Какой твой любимый фильм и почему?",
    "🍽 Какое блюдо было самым вкусным в твоей жизни?"
]

# Список слов дня с примерами и переводом
words = [
    {"word": "Serendipity", "translation": "счастливая случайность", "examples": ["✨ Это была чистая удача, что они встретились.", "🍀 Найти эту книгу было настоящим везением!"]},
    {"word": "Eloquent", "translation": "красноречивый", "examples": ["🗣 Она произнесла красноречивую речь.", "📢 Его слова были убедительными и трогательными."]},
    {"word": "Oblivious", "translation": "не обращающий внимания", "examples": ["🙉 Он не замечал шума вокруг.", "🚶‍♀️ Она прошла мимо, не замечая взглядов."]},
    {"word": "Resilient", "translation": "стойкий, устойчивый", "examples": ["💪 Она невероятно стойкая в сложных ситуациях.", "🌱 Это растение очень устойчиво к изменениям климата."]},
    {"word": "Diligent", "translation": "прилежный, усердный", "examples": ["📖 Он был прилежным учеником и всегда делал домашнюю работу.", "💼 Она очень усердно работает и никогда не пропускает дедлайны."]}
]

async def start(update: Update, context: CallbackContext) -> None:
    welcome_message = (
        "👋 Добро пожаловать в BFF English Community Bot! 🎉\n\n"
        "Я помогу тебе практиковать английский язык в интересной и увлекательной форме. Вот что я умею: \n\n"
        "🗣 Предложу тему для разговора.\n"
        "📖 Покажу слово дня с примерами и произношением.\n"
        "🧠 Проведу веселый тест на знание английского.\n"
        "📋 Помогу разобраться с временами английского языка.\n"
        "✍️ Запишу тебя на бесплатное первое занятие с преподавателем!\n\n"
        "Выбери нужную команду ниже! 🚀"
    )
    await update.message.reply_text(welcome_message, reply_markup=main_menu())

async def word_of_the_day(update: Update, context: CallbackContext) -> None:
    word_data = random.choice(words)
    message = (f"📚 Слово дня: {word_data['word']} ({word_data['translation']})\n\n"
               f"✍️ Примеры:\n- {word_data['examples'][0]}\n- {word_data['examples'][1]}")
    
    await update.message.reply_text(message)
    
    tts = gTTS(text=word_data['word'], lang='en')
    tts.save("word.mp3")
    with open("word.mp3", "rb") as audio:
        await update.message.reply_voice(audio)
    os.remove("word.mp3")
    
    await update.message.reply_text("⏰ Хочешь получать слово дня каждый день?", 
                                   reply_markup=ReplyKeyboardMarkup([["Да", "Нет"], ["🏠 Главное меню"]], resize_keyboard=True, one_time_keyboard=True))

async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text

    if text == "🗣 Тема для разговора":
        topic = random.choice(topics)
        await update.message.reply_text(f"💬 Вот тема для разговора:\n\n{topic}")
    
    elif text == "Да":
        await update.message.reply_text("✅ Отлично! Я буду напоминать тебе каждый день в выбранное время.")
    
    elif text == "Нет":
        await update.message.reply_text("👍 Хорошо! Ты всегда можешь включить это позже.")

    elif text == "📖 Слово дня":
        await word_of_the_day(update, context)
    
    elif text == "✍️ Записаться на первое бесплатное занятие":
        signup_text = ("Первое занятие в BFF Community проводится с одним из наших преподавателей абсолютно бесплатно. "
                       "Для этого тебе нужно заполнить анкету по данной ссылке: "
                       "https://docs.google.com/forms/d/e/1FAIpQLSdDutaMxpkQ94dO7koAdd7Impo21sBdVzeRlsBc6SwVMfjzdQ/viewform?usp=sharing")
        await update.message.reply_text(signup_text)

    elif text == "🏠 Главное меню":
        await update.message.reply_text("🔙 Возвращаемся в главное меню!", reply_markup=main_menu())

def main_menu():
    keyboard = [
        ["🗣 Тема для разговора", "📖 Слово дня"],
        ["🧠 Викторина", "📋 Тест: времена"],
        ["✍️ Записаться на первое бесплатное занятие"],
        ["🏠 Главное меню"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("word_of_the_day", word_of_the_day))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == "__main__":
    main()
