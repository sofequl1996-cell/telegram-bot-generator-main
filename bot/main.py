import logging
import os
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from bot.handlers import (
    start_command,
    generate_account_callback,
    my_stats_callback,
    back_to_menu,
    help_command
)
from database.db import init_db
from config import Config

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot"""
    # Initialize database
    init_db()
    
    # Create application
    application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    
    # Add callback query handlers
    application.add_handler(CallbackQueryHandler(generate_account_callback, pattern='generate_account'))
    application.add_handler(CallbackQueryHandler(my_stats_callback, pattern='my_stats'))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern='back_to_menu'))
    
    # Start the bot
    logger.info("🤖 Telegram Bot Started!")
    logger.info(f"📡 Token: {Config.TELEGRAM_BOT_TOKEN[:10]}...")
    
    application.run_polling()

if __name__ == '__main__':
    main()
