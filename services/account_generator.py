import random
import string
from faker import Faker
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

fake = Faker()

class AccountGenerator:
    """Generate realistic accounts and addresses"""
    
    @staticmethod
    def generate_email(domain='gmail.com'):
        """Generate random email address"""
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        return f"{username}@{domain}"
    
    @staticmethod
    def generate_password(length=16):
        """Generate secure password"""
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choices(characters, k=length))
        return password
    
    @staticmethod
    def generate_full_address():
        """Generate complete realistic address"""
        return {
            'full_name': fake.name(),
            'street_address': fake.street_address(),
            'city': fake.city(),
            'state': fake.state(),
            'postal_code': fake.postcode(),
            'country': fake.country(),
            'phone': fake.phone_number(),
            'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d')
        }
    
    @staticmethod
    def generate_complete_account():
        """Generate complete account data"""
        address = AccountGenerator.generate_full_address()
        return {
            'email': AccountGenerator.generate_email(),
            'password': AccountGenerator.generate_password(),
            'recovery_email': fake.email(),
            'recovery_phone': fake.phone_number(),
            **address
        }

class EmailService:
    """Handle email operations"""
    
    def __init__(self):
        self.email = Config.EMAIL_USERNAME
        self.password = Config.EMAIL_PASSWORD
        self.smtp_server = self._get_smtp_server()
    
    def _get_smtp_server(self):
        """Get SMTP server based on email provider"""
        if 'gmail' in self.email:
            return 'smtp.gmail.com'
        elif 'outlook' in self.email:
            return 'smtp-mail.outlook.com'
        else:
            return 'smtp.google.com'
    
    def send_verification_email(self, to_email, verification_code):
        """Send verification email"""
        try:
            subject = "Email Verification - Telegram Bot Generator"
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>Email Verification</h2>
                    <p>Your verification code is:</p>
                    <h1 style="color: #007bff; letter-spacing: 2px;">{verification_code}</h1>
                    <p>This code will expire in 10 minutes.</p>
                </body>
            </html>
            """
            
            self._send_email(to_email, subject, body)
            return True
        except Exception as e:
            print(f"Error sending verification email: {e}")
            return False
    
    def send_account_details(self, to_email, account_data):
        """Send generated account details"""
        try:
            subject = "Your Generated Account Details"
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>Account Generated Successfully!</h2>
                    <hr>
                    <h3>Account Information:</h3>
                    <p><strong>Email:</strong> {account_data['email']}</p>
                    <p><strong>Password:</strong> {account_data['password']}</p>
                    <hr>
                    <h3>Address Information:</h3>
                    <p><strong>Name:</strong> {account_data['full_name']}</p>
                    <p><strong>Address:</strong> {account_data['street_address']}</p>
                    <p><strong>City:</strong> {account_data['city']}</p>
                    <p><strong>State:</strong> {account_data['state']}</p>
                    <p><strong>Postal Code:</strong> {account_data['postal_code']}</p>
                    <p><strong>Country:</strong> {account_data['country']}</p>
                    <p><strong>Phone:</strong> {account_data['phone']}</p>
                    <p><strong>Birth Date:</strong> {account_data['birth_date']}</p>
                    <hr>
                    <p><strong>Recovery Email:</strong> {account_data['recovery_email']}</p>
                    <p><strong>Recovery Phone:</strong> {account_data['recovery_phone']}</p>
                    <hr>
                    <p style="color: #999; font-size: 12px;">Keep this information safe!</p>
                </body>
            </html>
            """
            
            self._send_email(to_email, subject, body)
            return True
        except Exception as e:
            print(f"Error sending account details: {e}")
            return False
    
    def _send_email(self, to_email, subject, body):
        """Internal method to send email"""
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = self.email
        message['To'] = to_email
        
        message.attach(MIMEText(body, 'html'))
        
        with smtplib.SMTP_SSL(self.smtp_server, 465) as server:
            server.login(self.email, self.password)
            server.sendmail(self.email, to_email, message.as_string())
