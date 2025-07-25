from typing import Final

from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, filters, _contexttypes
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN: Final = os.getenv('TOKEN')
BOT_USERNAME: Final = os.getenv('BOT_USERNAME')


# commands


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('hello! whats up?')
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am Milles Morales. I can help you with various tasks!')
    
    
async def custom_command (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('wait for it...')
    
    
    
    
# responses

def handle_response(text:str) -> str:
    proccesed: str = text.lower()
    
    if 'hello' in proccesed:
        return 'Hello there!'
    elif 'how are you' in proccesed:
        return 'Im doing great, thanks for asking!'
    elif 'bye' in proccesed:
        return 'Goodbye! Have a great day!'
    else:
        return 'I am not sure how to respond to that. Can you please rephrase?'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
        
    print('bot:', response)
    await update.message.reply_text(response)
    

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
    

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()
    
    
    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    
    # mesages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # errors
    app.add_error_handler(error)
    
    print('Polling updates...')
    app.run_polling(poll_interval=3)
    
    
    