from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from admin.auth import login_required, api_token_required, verify_admin_password
from services.user_manager import UserManager
from services.account_generator import AccountGenerator
from services.email_service import EmailService
from services.email_inbox import EmailInboxService
from database.db import SessionLocal
from database.models import User, Account, EmailLog, Email
import logging

logger = logging.getLogger(__name__)
admin_bp = Blueprint('admin', __name__)

user_manager = UserManager()
account_generator = AccountGenerator()
email_service = EmailService()
inbox_service = EmailInboxService()


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


# ✅ INBOX ROUTES
@admin_bp.route('/inbox')
@login_required
def inbox():
    """📧 Display inbox with all emails"""
    try:
        # পেজিনেশন
        page = request.args.get('page', 1, type=int)
        per_page = 15
        
        # ফিল্টার অপশন
        filter_type = request.args.get('filter', 'all')
        
        # সার্চ কোয়েরি
        search_query = request.args.get('search', '')
        
        # প্রথম ইউজার (ডেমোর জন্য, পরে আপডেট করা যাবে)
        db = SessionLocal()
        first_user = db.query(User).first()
        
        if not first_user:
            return render_template('inbox.html', 
                                 emails=[], 
                                 pagination={'page': 1, 'per_page': per_page, 'total': 0, 'total_pages': 0},
                                 stats={'total': 0, 'unread': 0, 'starred': 0, 'archived': 0})
        
        user_id = first_user.id
        
        # সার্চ যদি থাকে
        if search_query:
            result = inbox_service.search_emails(user_id, search_query, page, per_page)
        else:
            result = inbox_service.get_inbox(user_id, page, per_page, filter_type)
        
        # স্ট্যাটিস্টিক্স পান
        stats = inbox_service.get_stats(user_id)
        
        emails = result['emails']
        pagination = {
            'page': result['page'],
            'per_page': result['per_page'],
            'total': result['total'],
            'total_pages': result['total_pages']
        }
        
        logger.info(f"ইনবক্স প্রদর্শিত হচ্ছে - পেজ: {page}, ফিল্টার: {filter_type}")
        
        return render_template('inbox.html', 
                             emails=emails,
                             pagination=pagination,
                             stats=stats,
                             current_filter=filter_type)
    except Exception as e:
        logger.error(f"ইনবক্স লোড করতে ত্রুটি: {e}")
        return render_template('inbox.html', 
                             emails=[], 
                             pagination={'page': 1, 'per_page': 15, 'total': 0, 'total_pages': 0},
                             stats={'total': 0, 'unread': 0, 'starred': 0, 'archived': 0},
                             error="ইনবক্স লোড করতে ব্যর্থ হয়েছে")
    finally:
        db.close()


@admin_bp.route('/inbox/<email_id>')
@login_required
def view_email(email_id):
    """📖 View individual email"""
    try:
        db = SessionLocal()
        
        # প্রথম ইউজার (ডেমোর জন্য)
        first_user = db.query(User).first()
        
        if not first_user:
            return redirect(url_for('admin.inbox'))
        
        user_id = first_user.id
        
        # ইমেইল পান এবং পড়া হিসেবে চিহ্নিত করুন
        email = inbox_service.get_email(email_id, user_id)
        
        if not email:
            return redirect(url_for('admin.inbox'))
        
        logger.info(f"ইমেইল দেখা হচ্ছে: {email_id}")
        
        return render_template('view_email.html', email=email)
    except Exception as e:
        logger.error(f"ইমেইল দেখতে ত্রুটি: {e}")
        return redirect(url_for('admin.inbox'))
    finally:
        db.close()


# ✅ INBOX API ENDPOINTS

@admin_bp.route('/api/email/<email_id>/star', methods=['POST'])
@login_required
def api_toggle_star(email_id):
    """⭐ Toggle email star"""
    try:
        db = SessionLocal()
        first_user = db.query(User).first()
        
        if not first_user:
            return jsonify({'success': False, 'message': 'ইউজার পাওয়া যায়নি'}), 404
        
        success = inbox_service.toggle_star(email_id, first_user.id)
        
        if success:
            logger.info(f"ইমেইল স্টার টগল করা হয়েছে: {email_id}")
            return jsonify({'success': True, 'message': 'স্টার টগল করা হয়েছে'})
        else:
            return jsonify({'success': False, 'message': 'ইমেইল পাওয়া যায়নি'}), 404
    except Exception as e:
        logger.error(f"স্টার টগলে ত্রুটি: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()


@admin_bp.route('/api/email/<email_id>/archive', methods=['POST'])
@login_required
def api_toggle_archive(email_id):
    """📌 Toggle email archive"""
    try:
        db = SessionLocal()
        first_user = db.query(User).first()
        
        if not first_user:
            return jsonify({'success': False, 'message': 'ইউজার পাওয়া যায়নি'}), 404
        
        success = inbox_service.toggle_archive(email_id, first_user.id)
        
        if success:
            logger.info(f"ইমেইল আর্কাইভ টগল করা হয়েছে: {email_id}")
            return jsonify({'success': True, 'message': 'আর্কাইভ টগল করা হয়েছে'})
        else:
            return jsonify({'success': False, 'message': 'ইমেইল পাওয়া যায়নি'}), 404
    except Exception as e:
        logger.error(f"আর্কাইভ টগলে ত্রুটি: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()


@admin_bp.route('/api/email/<email_id>/delete', methods=['POST'])
@login_required
def api_delete_email(email_id):
    """🗑️ Delete email"""
    try:
        db = SessionLocal()
        first_user = db.query(User).first()
        
        if not first_user:
            return jsonify({'success': False, 'message': 'ইউজার পাওয়া যায়নি'}), 404
        
        success = inbox_service.delete_email(email_id, first_user.id)
        
        if success:
            logger.info(f"ইমেইল ডিলিট করা হয়েছে: {email_id}")
            return jsonify({'success': True, 'message': 'ইমেইল ডিলিট করা হয়েছে'})
        else:
            return jsonify({'success': False, 'message': 'ইমেইল পাওয়া যায়নি'}), 404
    except Exception as e:
        logger.error(f"ডিলিটে ত্রুটি: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()


@admin_bp.route('/api/email/search')
@login_required
def api_search_email():
    """🔍 Search emails"""
    try:
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)
        
        if not query:
            return jsonify({'success': False, 'message': 'সার্চ কোয়েরি প্রয়োজন'}), 400
        
        db = SessionLocal()
        first_user = db.query(User).first()
        
        if not first_user:
            return jsonify({'success': False, 'message': 'ইউজার পাওয়া যায়নি'}), 404
        
        result = inbox_service.search_emails(first_user.id, query, page, 15)
        
        emails_data = [
            {
                'id': email.id,
                'subject': email.subject,
                'from': email.from_address,
                'to': email.to_address,
                'preview': email.get_preview(60),
                'created_at': email.created_at.isoformat(),
                'is_read': email.is_read,
                'is_starred': email.is_starred
            }
            for email in result['emails']
        ]
        
        logger.info(f"ইমেইল সার্চ করা হয়েছে: {query}")
        
        return jsonify({
            'success': True,
            'emails': emails_data,
            'total': result['total'],
            'page': result['page'],
            'total_pages': result['total_pages']
        })
    except Exception as e:
        logger.error(f"সার্চে ত্রুটি: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()


@admin_bp.route('/api/email/stats')
@login_required
def api_email_stats():
    """📊 Get email statistics"""
    try:
        db = SessionLocal()
        first_user = db.query(User).first()
        
        if not first_user:
            return jsonify({'success': False, 'message': 'ইউজার পাওয়া যায়নি'}), 404
        
        stats = inbox_service.get_stats(first_user.id)
        
        logger.info("ইমেইল স্ট্যাটিস্টিক্স পাওয়া হয়েছে")
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        logger.error(f"স্ট্যাটিস্টিক্স পেতে ত্রুটি: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()


# ✅ পুরানো API ENDPOINTS

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
