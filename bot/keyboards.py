from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def main_menu_keyboard():
    """Create main menu keyboard"""
    keyboard = [
        [KeyboardButton('📧 অ্যাকাউন্ট তৈরি'), KeyboardButton('🔐 লগইন')],
        [KeyboardButton('👤 প্রোফাইল'), KeyboardButton('⚙️ সেটিংস')],
        [KeyboardButton('❓ সাহায্য'), KeyboardButton('📞 যোগাযোগ')],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def account_creation_keyboard():
    """Keyboard for account creation"""
    keyboard = [
        [KeyboardButton('🎓 শিক্ষার্থী অ্যাকাউন্ট'), KeyboardButton('👨‍💼 শিক্ষক অ্যাকাউন্ট')],
        [KeyboardButton('← ফিরে যান')],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def country_selection_keyboard():
    """Keyboard for country selection"""
    keyboard = [
        [KeyboardButton('🇧🇩 বাংলাদেশ'), KeyboardButton('🇺🇸 USA')],
        [KeyboardButton('← ফিরে যান')],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def inline_confirm_keyboard():
    """Inline keyboard for confirmation"""
    keyboard = [
        [InlineKeyboardButton('✅ হ্যাঁ / Yes', callback_data='confirm_yes'),
         InlineKeyboardButton('❌ না / No', callback_data='confirm_no')],
    ]
    return InlineKeyboardMarkup(keyboard)
