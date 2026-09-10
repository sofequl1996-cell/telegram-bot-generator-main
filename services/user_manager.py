from datetime import datetime, timedelta
from database.models import User, GeneratedAccount, Transaction, PlanType
from database.db import SessionLocal

class UserManager:
    """Manage user operations"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def get_or_create_user(self, telegram_id, username=None, first_name=None, last_name=None):
        """Get existing user or create new one"""
        user = self.db.query(User).filter(User.telegram_id == telegram_id).first()
        
        if not user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                plan=PlanType.FREE
            )
            self.db.add(user)
            self.db.commit()
        
        return user
    
    def can_generate(self, user_id):
        """Check if user can generate new account"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False, "User not found"
        
        if user.is_banned:
            return False, "Your account has been banned"
        
        if not user.subscription_active:
            return False, "Subscription expired"
        
        # Check plan limits
        max_generations = self._get_plan_limit(user.plan)
        
        if max_generations != -1 and user.generations_used >= max_generations:
            return False, f"Monthly limit reached ({max_generations})"
        
        return True, "OK"
    
    def _get_plan_limit(self, plan):
        """Get generation limit for plan"""
        limits = {
            PlanType.FREE: 5,
            PlanType.BASIC: 100,
            PlanType.PRO: 500,
            PlanType.ENTERPRISE: -1  # unlimited
        }
        return limits.get(plan, 5)
    
    def increment_generation_count(self, user_id):
        """Increment user's generation count"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.generations_used += 1
            self.db.commit()
    
    def upgrade_plan(self, user_id, plan, duration_days=30):
        """Upgrade user's subscription plan"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.plan = plan
            user.subscription_active = True
            user.subscription_end_date = datetime.utcnow() + timedelta(days=duration_days)
            user.generations_used = 0  # Reset counter
            self.db.commit()
            return True
        return False
    
    def get_user_stats(self, user_id):
        """Get user statistics"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        generated_count = self.db.query(GeneratedAccount).filter(
            GeneratedAccount.user_id == user_id
        ).count()
        
        max_limit = self._get_plan_limit(user.plan)
        
        return {
            'username': user.username,
            'plan': user.plan.value,
            'generated_accounts': generated_count,
            'monthly_used': user.generations_used,
            'monthly_limit': max_limit if max_limit != -1 else 'Unlimited',
            'subscription_active': user.subscription_active,
            'subscription_end': user.subscription_end_date,
            'is_admin': user.is_admin,
            'joined_date': user.created_at
        }
    
    def ban_user(self, user_id):
        """Ban a user"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_banned = True
            self.db.commit()
            return True
        return False
    
    def unban_user(self, user_id):
        """Unban a user"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_banned = False
            self.db.commit()
            return True
        return False
    
    def make_admin(self, user_id):
        """Make user an admin"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_admin = True
            self.db.commit()
            return True
        return False
    
    def close(self):
        """Close database session"""
        self.db.close()
