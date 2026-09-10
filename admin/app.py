from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from functools import wraps
from datetime import datetime
from database.db import init_db, SessionLocal
from database.models import User, GeneratedAccount, Transaction, AdminLog, PlanType
from services.user_manager import UserManager
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
app.config['ADMIN_USERNAME'] = os.getenv('ADMIN_USERNAME', 'admin')
app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD', 'admin123')

user_manager = UserManager()

# Authentication Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def log_admin_action(action, target_user_id=None, details=None):
    """Log admin actions"""
    db = SessionLocal()
    try:
        admin_log = AdminLog(
            admin_id=session.get('admin_id', 'Unknown'),
            action=action,
            target_user_id=target_user_id,
            details=details
        )
        db.add(admin_log)
        db.commit()
    finally:
        db.close()

# ==================== AUTH ROUTES ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
            session['admin_id'] = username
            log_admin_action('Login', None, f'Admin {username} logged in')
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Admin logout"""
    admin_id = session.get('admin_id')
    log_admin_action('Logout', None, f'Admin {admin_id} logged out')
    session.clear()
    return redirect(url_for('login'))

# ==================== DASHBOARD ====================

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    db = SessionLocal()
    try:
        total_users = db.query(User).count()
        total_generated = db.query(GeneratedAccount).count()
        total_revenue = db.query(Transaction).filter(
            Transaction.status == 'completed'
        ).count()
        
        # Get recent activities
        recent_users = db.query(User).order_by(User.created_at.desc()).limit(5).all()
        recent_accounts = db.query(GeneratedAccount).order_by(
            GeneratedAccount.created_at.desc()
        ).limit(5).all()
        
        stats = {
            'total_users': total_users,
            'total_generated': total_generated,
            'total_revenue': total_revenue,
            'recent_users': recent_users,
            'recent_accounts': recent_accounts
        }
        
        return render_template('dashboard.html', stats=stats)
    finally:
        db.close()

# ==================== USER MANAGEMENT ====================

@app.route('/api/users', methods=['GET'])
@login_required
def get_users():
    """Get all users"""
    db = SessionLocal()
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        users = db.query(User).paginate(page=page, per_page=per_page)
        
        users_data = []
        for user in users.items:
            generated_count = db.query(GeneratedAccount).filter(
                GeneratedAccount.user_id == user.id
            ).count()
            
            users_data.append({
                'id': user.id,
                'telegram_id': user.telegram_id,
                'username': user.username,
                'plan': user.plan.value,
                'generated': generated_count,
                'is_admin': user.is_admin,
                'is_banned': user.is_banned,
                'created_at': user.created_at.isoformat()
            })
        
        return jsonify({
            'users': users_data,
            'total': users.total,
            'pages': users.pages,
            'current_page': page
        })
    finally:
        db.close()

@app.route('/users')
@login_required
def users_page():
    """Users management page"""
    return render_template('users.html')

@app.route('/api/users/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_detail(user_id):
    """Get/update user details"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if request.method == 'POST':
            data = request.get_json()
            
            if 'plan' in data:
                user.plan = PlanType(data['plan'])
            
            if 'is_admin' in data:
                user.is_admin = data['is_admin']
            
            if 'is_banned' in data:
                user.is_banned = data['is_banned']
            
            db.commit()
            log_admin_action('Update User', user_id, f'User {user.username} updated')
            
            return jsonify({'message': 'User updated successfully'})
        
        # GET request
        generated_count = db.query(GeneratedAccount).filter(
            GeneratedAccount.user_id == user_id
        ).count()
        
        accounts = db.query(GeneratedAccount).filter(
            GeneratedAccount.user_id == user_id
        ).all()
        
        return jsonify({
            'id': user.id,
            'telegram_id': user.telegram_id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'plan': user.plan.value,
            'subscription_active': user.subscription_active,
            'generated_count': generated_count,
            'generations_used': user.generations_used,
            'is_admin': user.is_admin,
            'is_banned': user.is_banned,
            'created_at': user.created_at.isoformat(),
            'accounts': [
                {
                    'id': acc.id,
                    'email': acc.email,
                    'created_at': acc.created_at.isoformat()
                }
                for acc in accounts
            ]
        })
    finally:
        db.close()

@app.route('/api/users/<int:user_id>/ban', methods=['POST'])
@login_required
def ban_user(user_id):
    """Ban a user"""
    success = user_manager.ban_user(user_id)
    if success:
        log_admin_action('Ban User', user_id, f'User {user_id} banned')
        return jsonify({'message': 'User banned successfully'})
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/users/<int:user_id>/unban', methods=['POST'])
@login_required
def unban_user(user_id):
    """Unban a user"""
    success = user_manager.unban_user(user_id)
    if success:
        log_admin_action('Unban User', user_id, f'User {user_id} unbanned')
        return jsonify({'message': 'User unbanned successfully'})
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/users/<int:user_id>/make-admin', methods=['POST'])
@login_required
def make_admin(user_id):
    """Make user an admin"""
    success = user_manager.make_admin(user_id)
    if success:
        log_admin_action('Make Admin', user_id, f'User {user_id} made admin')
        return jsonify({'message': 'User is now admin'})
    return jsonify({'error': 'User not found'}), 404

# ==================== ACCOUNTS MANAGEMENT ====================

@app.route('/accounts')
@login_required
def accounts_page():
    """Accounts management page"""
    return render_template('accounts.html')

@app.route('/api/accounts', methods=['GET'])
@login_required
def get_accounts():
    """Get all generated accounts"""
    db = SessionLocal()
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        accounts = db.query(GeneratedAccount).paginate(page=page, per_page=per_page)
        
        accounts_data = []
        for account in accounts.items:
            accounts_data.append({
                'id': account.id,
                'user_id': account.user_id,
                'email': account.email,
                'full_name': account.full_name,
                'city': account.city,
                'created_at': account.created_at.isoformat(),
                'is_verified': account.is_verified
            })
        
        return jsonify({
            'accounts': accounts_data,
            'total': accounts.total,
            'pages': accounts.pages,
            'current_page': page
        })
    finally:
        db.close()

@app.route('/api/accounts/<int:account_id>', methods=['GET', 'DELETE'])
@login_required
def account_detail(account_id):
    """Get/delete account"""
    db = SessionLocal()
    try:
        account = db.query(GeneratedAccount).filter(
            GeneratedAccount.id == account_id
        ).first()
        
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        
        if request.method == 'DELETE':
            db.delete(account)
            db.commit()
            log_admin_action('Delete Account', account.user_id, f'Account {account.email} deleted')
            return jsonify({'message': 'Account deleted'})
        
        # GET request
        return jsonify({
            'id': account.id,
            'user_id': account.user_id,
            'email': account.email,
            'password': account.password,
            'full_name': account.full_name,
            'street_address': account.street_address,
            'city': account.city,
            'state': account.state,
            'postal_code': account.postal_code,
            'country': account.country,
            'phone': account.phone,
            'birth_date': account.birth_date,
            'recovery_email': account.recovery_email,
            'recovery_phone': account.recovery_phone,
            'is_verified': account.is_verified,
            'created_at': account.created_at.isoformat()
        })
    finally:
        db.close()

# ==================== STATISTICS ====================

@app.route('/api/stats', methods=['GET'])
@login_required
def get_stats():
    """Get system statistics"""
    db = SessionLocal()
    try:
        total_users = db.query(User).count()
        total_accounts = db.query(GeneratedAccount).count()
        total_transactions = db.query(Transaction).filter(
            Transaction.status == 'completed'
        ).count()
        
        # Users by plan
        plan_stats = {}
        for plan in PlanType:
            count = db.query(User).filter(User.plan == plan).count()
            plan_stats[plan.value] = count
        
        return jsonify({
            'total_users': total_users,
            'total_accounts': total_accounts,
            'total_transactions': total_transactions,
            'plan_distribution': plan_stats
        })
    finally:
        db.close()

@app.route('/stats')
@login_required
def stats_page():
    """Statistics page"""
    return render_template('stats.html')

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
