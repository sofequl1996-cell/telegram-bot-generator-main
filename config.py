import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', False)
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///telegram_bot.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_ADMIN_ID = os.getenv('TELEGRAM_ADMIN_ID')
    
    # Admin Panel
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
    
    # Email
    EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_SERVICE = os.getenv('EMAIL_SERVICE', 'gmail')
    
    # Features
    MAX_FREE_GENERATIONS = 5
    SUBSCRIPTION_PLANS = {
        'free': {'price': 0, 'monthly_limit': 5},
        'basic': {'price': 99, 'monthly_limit': 100},
        'pro': {'price': 299, 'monthly_limit': 500},
        'enterprise': {'price': 999, 'monthly_limit': 'unlimited'}
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
