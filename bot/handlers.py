import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.keyboards import main_menu_keyboard
from services.user_manager import UserManager
from services.account_generator import AccountGenerator

logger = logging.getLogger(__name__)
user_manager = UserManager()
account_generator = AccountGenerator()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""
    user = update.effective_user
    welcome_message = f"""
    🎉 আপনাকে স্বাগতম! Welcome! 🎉
    
    আমি একটি টেলিগ্রাম বট যা আপনাকে বিভিন্ন সেবা প্রদান করতে পারি।
    I'm a Telegram bot that can provide you various services.
    
    দয়া করে একটি বিকল্প নির্বাচন করুন:
    Please select an option:
    """
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=main_menu_keyboard()
    )
    
    # Save user to database
    try:
        user_manager.add_user(user.id, user.first_name, user.username, user.last_name)
        logger.info(f"User {user.id} added/updated to database")
    except Exception as e:
        logger.error(f"Error adding user: {e}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command handler"""
    help_text = """
    📚 সাহায্য / Help 📚
    
    উপলব্ধ কমান্ড:
    /start - বট শুরু করুন
    /help - এই সাহায্য বার্তা দেখুন
    /account - অ্যাকাউন্ট তৈরি করুন
    /status - আপনার স্ট্যাটাস দেখুন
    
    Available Commands:
    /start - Start the bot
    /help - Show this help message
    /account - Create an account
    /status - View your status
    """
    await update.message.reply_text(help_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular messages"""
    message_text = update.message.text
    user_id = update.effective_user.id
    
    responses = {
        '📧 অ্যাকাউন্ট তৈরি': 'অ্যাকাউন্ট তৈরি করার জন্য /account কমান্ড ব্যবহার করুন।',
        '🔐 লগইন': 'লগইন করতে আপনার ইউজারনেম এবং পাসওয়ার্ড প্রদান করুন।',
        '👤 প্রোফাইল': 'আপনার প্রোফাইল দেখতে /status কমান্ড ব্যবহার করুন।',
    }
    
    response = responses.get(message_text, 'আমি এই বার্তা বুঝতে পারিনি। /help টিপু���।')
    await update.message.reply_text(response, reply_markup=main_menu_keyboard())
