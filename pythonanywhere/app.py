from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET'] = os.environ.get('JWT_SECRET', 'change-this-secret')
app.config['JWT_EXPIRES_IN'] = 7

CORS(app, origins=[os.environ.get('FRONTEND_URL', 'http://localhost:5173')])
db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='customer')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ServiceArea(db.Model):
    __tablename__ = 'service_areas'
    id = db.Column(db.String, primary_key=True)
    zip_code = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    electricity_available = db.Column(db.Boolean, default=True)
    natural_gas_available = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)

class Plan(db.Model):
    __tablename__ = 'plans'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    service_type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    rate = db.Column(db.Numeric(10, 4))
    rate_unit = db.Column(db.String(50))
    contract_length_months = db.Column(db.Integer)
    features = db.Column(db.JSON)
    benefits = db.Column(db.JSON)
    renewable_percentage = db.Column(db.Numeric(5, 2), default=0)
    is_popular = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)

# Auth decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        
        if not token:
            return jsonify({'success': False, 'error': 'Token required'}), 401
        
        try:
            data = jwt.decode(token, app.config['JWT_SECRET'], algorithms=['HS256'])
            current_user = User.query.filter_by(email=data['email']).first()
        except:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# Routes
@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # For demo - replace with actual user lookup
    if email == 'demo@energygas.local' and password == 'Customer123!':
        token = jwt.encode({
            'email': email,
            'role': 'customer',
            'exp': datetime.utcnow() + timedelta(days=7)
        }, app.config['JWT_SECRET'], algorithm='HS256')
        
        return jsonify({
            'success': True,
            'token': token,
            'user': {'email': email, 'role': 'customer'}
        })
    
    if email == 'admin@energygas.local' and password == 'Admin123!':
        token = jwt.encode({
            'email': email,
            'role': 'admin',
            'exp': datetime.utcnow() + timedelta(days=7)
        }, app.config['JWT_SECRET'], algorithm='HS256')
        
        return jsonify({
            'success': True,
            'token': token,
            'user': {'email': email, 'role': 'admin'}
        })
    
    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

@app.route('/api/availability/check', methods=['POST'])
def check_availability():
    data = request.get_json()
    zip_code = data.get('zipCode', '')
    
    # Demo ZIP codes
    demo_areas = {
        '77056': {'city': 'Houston', 'state': 'TX', 'electricity': True, 'gas': True},
        '10001': {'city': 'New York', 'state': 'NY', 'electricity': True, 'gas': False},
        '90001': {'city': 'Los Angeles', 'state': 'CA', 'electricity': True, 'gas': True},
    }
    
    if zip_code in demo_areas:
        area = demo_areas[zip_code]
        return jsonify({
            'success': True,
            'available': True,
            'data': {
                'zipCode': zip_code,
                'city': area['city'],
                'state': area['state'],
                'electricityAvailable': area['electricity'],
                'naturalGasAvailable': area['gas']
            }
        })
    
    return jsonify({'success': True, 'available': False, 'message': 'ZIP code not found'})

@app.route('/api/plans')
def get_plans():
    service_type = request.args.get('serviceType')
    
    demo_plans = [
        {'id': '1', 'name': 'Essential Electric', 'serviceType': 'electricity', 'rate': 0.12, 'contractLengthMonths': 12, 'features': ['Flexible options', 'Online account management'], 'isPopular': False},
        {'id': '2', 'name': 'Smart Choice', 'serviceType': 'electricity', 'rate': 0.11, 'contractLengthMonths': 24, 'features': ['Fixed-rate pricing', 'AutoPay support'], 'isPopular': True},
        {'id': '3', 'name': 'Green Energy', 'serviceType': 'electricity', 'rate': 0.13, 'contractLengthMonths': 12, 'features': ['100% renewable', 'Environmental impact'], 'isPopular': False},
        {'id': '4', 'name': 'Essential Gas', 'serviceType': 'natural_gas', 'rate': 0.85, 'contractLengthMonths': 12, 'features': ['Flexible options', 'Online management'], 'isPopular': False},
        {'id': '5', 'name': 'Smart Gas', 'serviceType': 'natural_gas', 'rate': 0.80, 'contractLengthMonths': 24, 'features': ['Fixed-rate', 'Budget predictability'], 'isPopular': True},
    ]
    
    if service_type:
        demo_plans = [p for p in demo_plans if p['serviceType'] == service_type]
    
    return jsonify({'success': True, 'data': demo_plans})

@app.route('/api/customer/dashboard')
@token_required
def customer_dashboard(current_user):
    return jsonify({
        'success': True,
        'data': {
            'accountNumber': 'EGUS-DEMO-001',
            'accountStatus': 'active',
            'currentBill': {'amount': 125.50, 'dueDate': '2026-10-20', 'status': 'pending'},
            'lastPayment': {'amount': 142.30, 'date': '2026-09-10'}
        }
    })

@app.route('/api/customer/bills')
@token_required
def get_bills(current_user):
    return jsonify({
        'success': True,
        'data': [
            {'id': '1', 'billNumber': 'BILL-2026-003', 'servicePeriodStart': '2026-09-01', 'servicePeriodEnd': '2026-09-30', 'dueDate': '2026-10-20', 'amount': 118.75, 'status': 'pending'},
            {'id': '2', 'billNumber': 'BILL-2026-002', 'servicePeriodStart': '2026-08-01', 'servicePeriodEnd': '2026-08-31', 'dueDate': '2026-09-20', 'amount': 142.30, 'status': 'paid'},
            {'id': '3', 'billNumber': 'BILL-2026-001', 'servicePeriodStart': '2026-07-01', 'servicePeriodEnd': '2026-07-31', 'dueDate': '2026-08-20', 'amount': 125.50, 'status': 'paid'},
        ]
    })

@app.route('/api/customer/payment-history')
@token_required
def get_payment_history(current_user):
    return jsonify({
        'success': True,
        'data': [
            {'id': '1', 'reference': 'PAY-2026-002', 'date': '2026-09-10', 'amount': 142.30, 'methodType': 'credit_card', 'status': 'completed'},
            {'id': '2', 'reference': 'PAY-2026-001', 'date': '2026-08-15', 'amount': 125.50, 'methodType': 'credit_card', 'status': 'completed'},
        ]
    })

@app.route('/api/admin/dashboard')
@token_required
def admin_dashboard(current_user):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    return jsonify({
        'success': True,
        'data': {
            'customers': {'total': 1, 'active': 1},
            'enrollments': {'total': 0, 'pending': 0},
            'serviceAreas': {'total': 40},
            'plans': {'total': 7}
        }
    })

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
