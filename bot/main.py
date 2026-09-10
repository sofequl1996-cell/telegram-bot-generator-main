import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from bot.handlers import start, help_command, handle_message
from bot.keyboards import main_menu_keyboard

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.application = None

    async def start_bot(self):
        """Start the Telegram bot"""
        self.application = Application.builder().token(self.token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", start))
        self.application.add_handler(CommandHandler("help", help_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Start the bot
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        logger.info("Bot started successfully!")

    async def stop_bot(self):
        """Stop the bot"""
        await self.application.stop()
        logger.info("Bot stopped")


async def main():
    """Main function"""
    bot = TelegramBot(TELEGRAM_BOT_TOKEN)
    await bot.start_bot()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
