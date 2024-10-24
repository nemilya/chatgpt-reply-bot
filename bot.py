import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

from openai_chat import OpenAIChat

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
BOT_INTRO = os.getenv('BOT_INTRO')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(BOT_INTRO)

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response_text = OpenAIChat().get_response(update.message.text)
    text_with_bold = response_text.replace('**', '*')
    await update.message.reply_text(
        text_with_bold,
        parse_mode="Markdown"
    )

def main() -> None:
    print('started...')
    application = ApplicationBuilder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    application.run_polling()

if __name__ == '__main__':
    main()

