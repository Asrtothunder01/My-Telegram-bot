import urllib.request
import json
import logging
from datetime import datetime
import emoji
from typing import Final
from telegram import Update, Sticker
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
)

TOKEN: Final = '6348322828:AAHKwIryRDTL2sG_RHQTzuR6BSXwXDKXHJo'

# Set up logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# Retrieve logger after setting up configuration
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
     await update.message.reply_text('Hello! welcome to OLORUNFEMI BOT')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
     await update.message.reply_text('Please type something so I can respond')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
     await update.message.reply_text('This is a custom command')

def handle_response(text: str) -> str:
    processed: str = text
    if 'hello' in processed.lower():
        return 'Wassup Bobo!'

    if 'how are you ?' in processed.lower() or 'hw are you doing?'in processed.lower() or 'hw are you' in processed.lower():
        return 'I\'m good and you?'
    
    if 'good morning' in processed.lower():
        return 'Good morning Bobo'
    if 'good evening' in processed.lower():
         return 'Good Evening Boss'
    if 'am good' in processed.lower()or 'i\'m goood' in processed.lower() or 'I\'m cool' in processed.lower():
         return 'Eku Enjoyment'
    
    if 'hi' in processed.lower():
         return 'How are you doing?'
    if 'who are you?'in processed.lower():
         return 'I am OLORUNFEMI BOT'
    message = ('how was your day?','how was your day')
    
    if 'hello' in processed.lower() or 'hi' in processed.lower() or 'sup' in processed.lower() or 'yo' in processed.lower():
         
         return 'Wassup Bobo!'
    if any(message in processed.lower() for message in message):
        return 'cool and you?'

    if 'time' in processed.lower():
         now = datetime.now()
         date_time = now.strftime('%d/%m/%y, %H:%M:%S')
         return str(date_time)
         
         
    return 'I do not understand bro..'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    logger.info(f'User({update.message.chat.id}) in {message_type}: "{text}" ')
    response: str = handle_response(text)
    logger.info(f'Bot: {response}')
    await update.message.reply_text(response)

async def get_weather(lat: float, lon: float):
    url = f'https://api.aerisapi.com/forecasts/:auto?format=json&filter=daynight&limit=7&fields=periods.dateTimeISO,periods.weather,loc,periods.maxTempF,periods.pop&client_id=9lPwoWZ8uw3e3tesN00ei&client_secret=hs5PKo5Q3E68bXIAW7pL2c8tv5g9HdxZZHW6lS2o'
    with urllib.request.urlopen(url) as response:          
         data = json.loads(response.read())

    forecast = ""
    for period in data['response'][0]['periods']:
        forecast += f"{period['dateTimeISO']}: {period['weather']}, Max Temp: {period['maxTempF']}°F, Precipitation: {period['pop']}%\n"
    return forecast

async def horoscope_command(update: Update, context: ContextTypes):
    # Extract the command
    args = context.args
    logger.info(f'Command arguments: {args}')

    if len(args) < 2:
        await update.message.reply_text('Usage: /horoscope <type> <zodiac_sign>')
        return

    horoscope_type = args[0].lower()
    zodiac_sign = args[1]

    logger.info(f'Horoscope type: {horoscope_type}, Zodiac sign: {zodiac_sign}')

    valid_types = ['daily', 'weekly', 'monthly']
    if horoscope_type not in valid_types:
        await update.message.reply_text('Invalid horoscope type. Choose from: daily, weekly, monthly')
        return

    valid_signs = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]
    if zodiac_sign.lower() not in valid_signs:
        await update.message.reply_text("Invalid zodiac sign. Choose from: aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius, pisces")
        return

    # Call get_weather function
    lat = 7.1878
    lon = 3.4362
    weather_data = await get_weather(lat, lon)
    await update.message.reply_text('Weather data fetched successfully.')

    # Get horoscope data
    horoscope_data = get_horoscope(horoscope_type, zodiac_sign)
    await update.message.reply_text(horoscope_data)

    response = f'Fetching {horoscope_type} horoscope for {zodiac_sign}...'
    await update.message.reply_text(response)

def get_horoscope(horoscope_type: str, zodiac_sign: str) -> str:
    # Replace this with your actual implementation to fetch horoscope data
    return f"Horoscope for {horoscope_type} {zodiac_sign}: Lorem ipsum dolor sit amet, consectetur adipiscing elit."

async def  sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
     sticker_id ='sticker_id_here'
     await update.message.reply_sticker(sticker=Sticker(sticker_id))

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    logger.info('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('horoscope', horoscope_command))
    app.add_handler(CommandHandler('sticker',sticker))
    # Messages
    app.add_handler(MessageHandler(None, handle_message))

    # Errors
    app.add_error_handler(error)

    logger.info('Polling...')
    app.run_polling(poll_interval=1)
