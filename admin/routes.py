from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from admin.auth import login_required, api_token_required, verify_admin_password
from services.user_manager import UserManager
from services.account_generator import AccountGenerator
from services.email_service import EmailService
from database.db import SessionLocal
from database.models import User, Account, EmailLog
import logging

logger = logging.getLogger(__name__)
admin_bp = Blueprint('admin', __name__)

user_manager = UserManager()
account_generator = AccountGenerator()
email_service = EmailService()


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and verify_admin_password(password):
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')


@admin_bp.route('/logout')
def logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    db = SessionLocal()
    try:
        total_users = db.query(User).count()
        total_accounts = db.query(Account).count()
        verified_users = db.query(User).filter(User.is_verified == True).count()
        total_emails_sent = db.query(EmailLog).filter(EmailLog.status == 'sent').count()
        
        demo_emails = account_generator.generate_demo_emails()
        
        stats = {
            'total_users': total_users,
            'total_accounts': total_accounts,
            'verified_users': verified_users,
            'total_emails_sent': total_emails_sent,
            'demo_emails_bd': len(demo_emails['BD']),
            'demo_emails_us': len(demo_emails['US']),
        }
        
        return render_template('dashboard.html', stats=stats, demo_emails=demo_emails)
    finally:
        db.close()


@admin_bp.route('/users')
@login_required
def users():
    """List all users"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return render_template('users.html', users=users)
    finally:
        db.close()


@admin_bp.route('/api/demo-emails')
@api_token_required
def api_demo_emails():
    """API endpoint for demo emails"""
    demo_emails = account_generator.generate_demo_emails()
    return jsonify(demo_emails)


@admin_bp.route('/api/users')
@api_token_required
def api_users():
    """API endpoint for users"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        users_data = [
            {
                'id': user.id,
                'telegram_id': user.telegram_id,
                'username': user.username,
                'email': user.email,
                'country': user.country,
                'is_verified': user.is_verified,
                'created_at': user.created_at.isoformat()
            }
            for user in users
        ]
        return jsonify(users_data)
    finally:
        db.close()


@admin_bp.route('/api/accounts')
@api_token_required
def api_accounts():
    """API endpoint for accounts"""
    db = SessionLocal()
    try:
        accounts = db.query(Account).all()
        accounts_data = [
            {
                'id': account.id,
                'email': account.email,
                'university': account.university,
                'country': account.country,
                'is_email_verified': account.is_email_verified,
                'created_at': account.created_at.isoformat()
            }
            for account in accounts
        ]
        return jsonify(accounts_data)
    finally:
        db.close()


@admin_bp.route('/api/email-logs')
@api_token_required
def api_email_logs():
    """API endpoint for email logs"""
    db = SessionLocal()
    try:
        logs = db.query(EmailLog).all()
        logs_data = [
            {
                'id': log.id,
                'recipient_email': log.recipient_email,
                'subject': log.subject,
                'status': log.status,
                'sent_at': log.sent_at.isoformat() if log.sent_at else None,
                'created_at': log.created_at.isoformat()
            }
            for log in logs
        ]
        return jsonify(logs_data)
    finally:
        db.close()
