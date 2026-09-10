import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Tuple
import logging
from config import EMAIL_FROM, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT
from database.db import SessionLocal
from database.models import EmailLog
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.from_email = EMAIL_FROM
        self.password = EMAIL_PASSWORD
        self.db = SessionLocal()
    
    def send_email(self, to_email: str, subject: str, html_body: str, text_body: str = None) -> Tuple[bool, str]:
        """Send email"""
        try:
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            
            # Attach text and HTML parts
            if text_body:
                msg.attach(MIMEText(text_body, 'plain'))
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.from_email, self.password)
                server.send_message(msg)
            
            # Log email
            self._log_email(to_email, subject, html_body, 'sent')
            logger.info(f"Email sent to {to_email}")
            return True, "Email sent successfully"
        
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error sending email to {to_email}: {error_msg}")
            self._log_email(to_email, subject, html_body, 'failed', error_msg)
            return False, error_msg
    
    def send_verification_email(self, to_email: str, verification_link: str, name: str = "User") -> Tuple[bool, str]:
        """Send verification email"""
        subject = "📧 Email Verification / ইমেইল যাচাইকরণ"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Email Verification / ইমেইল যাচাইকরণ</h2>
                <p>Dear {name},</p>
                <p>প্রিয় {name},</p>
                <p>Click the link below to verify your email address:</p>
                <p>আপনার ইমেইল ঠিকানা যাচাই করতে নিচের লিংকটি ক্লিক করুন:</p>
                <a href="{verification_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                    Verify Email / ইমেইল যাচাই করুন
                </a>
                <p>This link will expire in 24 hours.</p>
                <p>এই লিংকটি ২৪ ঘন্টার মধ্যে মেয়াদ উত্তীর্ণ হবে।</p>
            </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_body)
    
    def send_welcome_email(self, to_email: str, name: str, university: str) -> Tuple[bool, str]:
        """Send welcome email"""
        subject = "🎉 Welcome to Telegram Bot Generator / স্বাগতম"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>🎉 Welcome! স্বাগতম! 🎉</h2>
                <p>Dear {name},</p>
                <p>প্রিয় {name},</p>
                <p>Thank you for registering with Telegram Bot Generator!</p>
                <p>Telegram Bot Generator এ রেজিস্টার করার জন্য ধন্যবাদ!</p>
                <p><strong>Your Registration Details:</strong></p>
                <ul>
                    <li>Email: {to_email}</li>
                    <li>University: {university}</li>
                </ul>
                <p>আপনার নিবন্ধন বিবরণী:</p>
                <ul>
                    <li>ইমেইল: {to_email}</li>
                    <li>বিশ্ববিদ্যালয়: {university}</li>
                </ul>
                <p>Happy coding! কোডিং করুন!</p>
            </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_body)
    
    def _log_email(self, recipient_email: str, subject: str, body: str, status: str, error_message: str = None):
        """Log email in database"""
        try:
            email_log = EmailLog(
                id=str(uuid.uuid4()),
                recipient_email=recipient_email,
                subject=subject,
                body=body,
                status=status,
                error_message=error_message,
                sent_at=datetime.utcnow() if status == 'sent' else None
            )
            self.db.add(email_log)
            self.db.commit()
        except Exception as e:
            logger.error(f"Error logging email: {e}")
            self.db.rollback()
