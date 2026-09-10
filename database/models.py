from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class PlanType(enum.Enum):
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class User(Base):
    """User Model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(50), unique=True, nullable=False, index=True)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True)
    phone = Column(String(20))
    
    # Subscription
    plan = Column(Enum(PlanType), default=PlanType.FREE)
    subscription_active = Column(Boolean, default=True)
    subscription_end_date = Column(DateTime)
    
    # Usage tracking
    generations_used = Column(Integer, default=0)
    reset_date = Column(DateTime, default=datetime.utcnow)
    
    # Account info
    is_admin = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    generated_accounts = relationship("GeneratedAccount", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.username} ({self.telegram_id})>"

class GeneratedAccount(Base):
    """Generated Account Model"""
    __tablename__ = 'generated_accounts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    # Account details
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    
    # Generated address
    full_name = Column(String(255))
    street_address = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100))
    phone = Column(String(20))
    
    # Additional info
    recovery_email = Column(String(255))
    recovery_phone = Column(String(20))
    birth_date = Column(String(20))
    
    # Account status
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String(10))
    inbox_access = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="generated_accounts")
    
    def __repr__(self):
        return f"<GeneratedAccount {self.email}>"

class Transaction(Base):
    """Transaction Model for Payments"""
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    plan = Column(Enum(PlanType), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default='USD')
    
    status = Column(String(50), default='pending')  # pending, completed, failed, cancelled
    payment_method = Column(String(50))  # stripe, razorpay, manual
    transaction_id = Column(String(255), unique=True)
    
    duration_days = Column(Integer, default=30)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction {self.transaction_id} - {self.status}>"

class AdminLog(Base):
    """Admin Action Log"""
    __tablename__ = 'admin_logs'
    
    id = Column(Integer, primary_key=True)
    admin_id = Column(String(50), nullable=False)
    action = Column(String(255), nullable=False)
    target_user_id = Column(String(50))
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<AdminLog {self.action} by {self.admin_id}>"

class SystemConfig(Base):
    """System Configuration"""
    __tablename__ = 'system_config'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(255), unique=True, nullable=False)
    value = Column(Text)
    description = Column(String(500))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<SystemConfig {self.key}>"
