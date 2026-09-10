from database.db import SessionLocal
from database.models import User, Account
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class UserManager:
    def __init__(self):
        self.db = SessionLocal()
    
    def add_user(self, telegram_id: int, first_name: str, username: Optional[str] = None, last_name: Optional[str] = None) -> User:
        """Add or update user"""
        try:
            user = self.db.query(User).filter(User.telegram_id == telegram_id).first()
            
            if user:
                user.first_name = first_name
                user.username = username
                user.last_name = last_name
                user.updated_at = __import__('datetime').datetime.utcnow()
            else:
                user = User(
                    telegram_id=telegram_id,
                    first_name=first_name,
                    username=username,
                    last_name=last_name
                )
                self.db.add(user)
            
            self.db.commit()
            logger.info(f"User {telegram_id} added/updated successfully")
            return user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error adding user: {e}")
            raise
    
    def get_user(self, telegram_id: int) -> Optional[User]:
        """Get user by telegram ID"""
        try:
            return self.db.query(User).filter(User.telegram_id == telegram_id).first()
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            return self.db.query(User).filter(User.email == email).first()
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    def update_user(self, telegram_id: int, **kwargs) -> Optional[User]:
        """Update user information"""
        try:
            user = self.db.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                self.db.commit()
                logger.info(f"User {telegram_id} updated successfully")
            return user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating user: {e}")
            return None
    
    def get_all_users(self) -> List[User]:
        """Get all users"""
        try:
            return self.db.query(User).all()
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            return []
    
    def verify_user(self, telegram_id: int) -> bool:
        """Mark user as verified"""
        try:
            user = self.db.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                user.is_verified = True
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error verifying user: {e}")
            return False
