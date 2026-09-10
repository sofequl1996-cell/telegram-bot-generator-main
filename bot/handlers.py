from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.account_generator import AccountGenerator, EmailService
from services.user_manager import UserManager
from database.models import GeneratedAccount, PlanType
from database.db import SessionLocal

user_manager = UserManager()
email_service = EmailService()
db = SessionLocal()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    
    # Create or get user
    user_manager.get_or_create_user(
        telegram_id=str(user.id),
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    keyboard = [
        [InlineKeyboardButton("🔄 Generate Account", callback_data='generate_account')],
        [InlineKeyboardButton("📊 My Stats", callback_data='my_stats')],
        [InlineKeyboardButton("💳 Upgrade Plan", callback_data='upgrade_plan')],
        [InlineKeyboardButton("🛠️ Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = f"""
👋 Welcome to **Telegram Account Generator Bot**!

Hi {user.first_name}! This bot helps you generate:
✅ Random email addresses
✅ Secure passwords
✅ Complete addresses
✅ Phone numbers & more

**Your Plan:** FREE (5 generations/month)

Choose an option below:
"""
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')

async def generate_account_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle account generation"""
    query = update.callback_query
    user_id = query.from_user.id
    
    # Get user from database
    db_user = db.query(db.query(db.session).model).filter_by(telegram_id=str(user_id)).first()
    
    if not db_user:
        await query.answer("User not found!", show_alert=True)
        return
    
    # Check if user can generate
    can_gen, message = user_manager.can_generate(db_user.id)
    
    if not can_gen:
        await query.answer(message, show_alert=True)
        return
    
    # Generate account
    account_data = AccountGenerator.generate_complete_account()
    
    # Save to database
    generated_account = GeneratedAccount(
        user_id=db_user.id,
        email=account_data['email'],
        password=account_data['password'],
        full_name=account_data['full_name'],
        street_address=account_data['street_address'],
        city=account_data['city'],
        state=account_data['state'],
        postal_code=account_data['postal_code'],
        country=account_data['country'],
        phone=account_data['phone'],
        birth_date=account_data['birth_date'],
        recovery_email=account_data['recovery_email'],
        recovery_phone=account_data['recovery_phone']
    )
    
    db.add(generated_account)
    db.commit()
    
    # Increment counter
    user_manager.increment_generation_count(db_user.id)
    
    # Format response
    account_text = f"""
✅ **Account Generated Successfully!**

📧 Email: `{account_data['email']}`
🔐 Password: `{account_data['password']}`

**Address Information:**
👤 Name: {account_data['full_name']}
🏠 Address: {account_data['street_address']}
🏙️ City: {account_data['city']}
📍 State: {account_data['state']}
📮 Postal: {account_data['postal_code']}
🌍 Country: {account_data['country']}
📱 Phone: {account_data['phone']}
🎂 Birth Date: {account_data['birth_date']}

**Recovery Options:**
📧 Recovery Email: {account_data['recovery_email']}
📱 Recovery Phone: {account_data['recovery_phone']}
"""
    
    await query.edit_message_text(account_text, parse_mode='Markdown')
    
    # Send email with details
    if db_user.email:
        email_service.send_account_details(db_user.email, account_data)

async def my_stats_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics"""
    query = update.callback_query
    user_id = query.from_user.id
    
    # Get user stats
    db_user = db.query(db.query(db.session).model).filter_by(telegram_id=str(user_id)).first()
    
    if not db_user:
        await query.answer("User not found!", show_alert=True)
        return
    
    stats = user_manager.get_user_stats(db_user.id)
    
    stats_text = f"""
📊 **Your Statistics**

👤 Username: @{stats['username'] or 'Not set'}
💳 Plan: {stats['plan'].upper()}
📝 Accounts Generated: {stats['generated_accounts']}
📅 This Month: {stats['monthly_used']}/{stats['monthly_limit']}
✅ Active: {'Yes' if stats['subscription_active'] else 'No'}
📌 Joined: {stats['joined_date'].strftime('%Y-%m-%d')}
"""
    
    if stats['subscription_end']:
        stats_text += f"\n📅 Expires: {stats['subscription_end'].strftime('%Y-%m-%d %H:%M')}"
    
    keyboard = [
        [InlineKeyboardButton("⬅️ Back", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(stats_text, reply_markup=reply_markup, parse_mode='Markdown')

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Go back to main menu"""
    query = update.callback_query
    
    keyboard = [
        [InlineKeyboardButton("🔄 Generate Account", callback_data='generate_account')],
        [InlineKeyboardButton("📊 My Stats", callback_data='my_stats')],
        [InlineKeyboardButton("💳 Upgrade Plan", callback_data='upgrade_plan')],
        [InlineKeyboardButton("🛠️ Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("**Main Menu**", reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help information"""
    help_text = """
🛠️ **Help & Information**

**Commands:**
/start - Start the bot
/help - Show this help
/stats - View your statistics
/account - Generate new account
/plans - View pricing plans

**Features:**
✅ Generate random emails
✅ Create secure passwords
✅ Generate complete addresses
✅ Inbox access (Premium)
✅ Admin panel for admins

**Plans:**
🟢 FREE - 5 generations/month
🔵 BASIC - 100 generations/month ($0.99)
🟣 PRO - 500 generations/month ($2.99)
🟡 ENTERPRISE - Unlimited ($9.99)

Need help? Contact admin!
"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')
