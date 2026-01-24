"""
Blood Bank Management System - Flask Application
Complete backend with routes for Admin, Staff, and Donor panels
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from datetime import datetime, timedelta
from functools import wraps
import os
import json

# Import models and database
from models.db import db, init_db
from models.user import User, Admin, Staff, Donor
from models.blood_unit import BloodUnit
from models.request import BloodRequest
from models.purchase import Purchase
from models.delivery import Delivery

# Flask app initialization
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blood_bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Initialize database
init_db(app)

# ====================== UTILITY FUNCTIONS ======================

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Decorator to check user role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login first', 'warning')
                return redirect(url_for('login'))
            
            user = User.query.get(session['user_id'])
            if not user or user.user_type not in roles:
                flash('Unauthorized access', 'danger')
                return redirect(url_for('home'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_current_user():
    """Get currently logged-in user"""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

def log_action(action, details):
    """Log system actions for audit trail"""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    user = get_current_user()
    username = user.username if user else 'System'
    
    log_entry = f"[{timestamp}] {username}: {action} - {details}\n"
    
    with open('action_log.txt', 'a') as f:
        f.write(log_entry)
    
    print(f"✓ {log_entry.strip()}")

# ====================== AUTHENTICATION ROUTES ======================

@app.route('/')
def index():
    """Redirect to home"""
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_type'] = user.user_type
            session.permanent = True
            
            log_action('LOGIN', f"User {username} logged in")
            flash(f'Welcome {user.full_name}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Donor registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        blood_type = request.form.get('blood_type')
        date_of_birth = request.form.get('date_of_birth')
        address = request.form.get('address')
        city = request.form.get('city')
        
        # Validation
        if not all([username, email, password, full_name, blood_type]):
            flash('Please fill all required fields', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return render_template('register.html')
        
        # Create donor
        try:
            donor = Donor(
                username=username,
                email=email,
                full_name=full_name,
                phone=phone,
                blood_type=blood_type,
                date_of_birth=datetime.strptime(date_of_birth, '%Y-%m-%d') if date_of_birth else None,
                address=address,
                city=city
            )
            donor.set_password(password)
            
            db.session.add(donor)
            db.session.commit()
            
            log_action('REGISTRATION', f"New donor registered: {username} ({blood_type})")
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration error: {str(e)}', 'danger')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """User logout"""
    username = session.get('username')
    session.clear()
    log_action('LOGOUT', f"User {username} logged out")
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

# ====================== HOME PAGE ======================

@app.route('/home')
@login_required
def home():
    """Home page with overview and statistics"""
    user = get_current_user()
    
    # Calculate statistics
    total_donors = User.query.filter_by(user_type='donor').count()
    
    # Get all blood units (group by status)
    blood_units = BloodUnit.query.all()
    available_units = sum(u.quantity for u in blood_units if u.status == 'available')
    total_units = sum(u.quantity for u in blood_units)
    
    # Get pending requests
    pending_requests = BloodRequest.query.filter_by(status='pending').count()
    
    # Get completed requests this month
    today = datetime.utcnow()
    month_start = today.replace(day=1)
    completed_this_month = BloodRequest.query.filter(
        BloodRequest.status == 'fulfilled',
        BloodRequest.fulfilled_date >= month_start
    ).count()
    
    # Get blood type breakdown
    blood_type_breakdown = {}
    for unit in blood_units:
        if unit.status == 'available':
            blood_type_breakdown[unit.blood_type] = blood_type_breakdown.get(unit.blood_type, 0) + unit.quantity
    
    # Get recent requests
    recent_requests = BloodRequest.query.order_by(BloodRequest.created_at.desc()).limit(5).all()
    
    # Get recent purchases
    recent_purchases = Purchase.query.order_by(Purchase.created_at.desc()).limit(5).all()
    
    context = {
        'user': user,
        'total_donors': total_donors,
        'available_units': available_units,
        'total_units': total_units,
        'pending_requests': pending_requests,
        'completed_this_month': completed_this_month,
        'blood_type_breakdown': blood_type_breakdown,
        'recent_requests': recent_requests,
        'recent_purchases': recent_purchases,
        'owner_name': 'Hariom Satav, Meet Patil, Prajwal Shinde',
        'owner_contact': '7558671952',
        'owner_email': 'satavhariom775@gmail.com'
    }
    
    return render_template('home.html', **context)

# ====================== ADMIN ROUTES ======================

@app.route('/admin/dashboard')
@role_required('admin')
def admin_dashboard():
    """Admin dashboard"""
    user = get_current_user()
    
    # Statistics
    total_users = User.query.count()
    total_donors = User.query.filter_by(user_type='donor').count()
    total_staff = User.query.filter_by(user_type='staff').count()
    total_admins = User.query.filter_by(user_type='admin').count()
    
    blood_units = BloodUnit.query.all()
    total_blood_units = sum(u.quantity for u in blood_units if u.status == 'available')
    
    total_requests = BloodRequest.query.count()
    pending_requests = BloodRequest.query.filter_by(status='pending').count()
    
    total_purchases = Purchase.query.count()
    total_spending = sum(p.total_price for p in Purchase.query.all())
    
    # Get all data for tables
    donors = Donor.query.all()
    staff = Staff.query.all()
    blood_inventory = BloodUnit.query.filter_by(status='available').all()
    requests = BloodRequest.query.order_by(BloodRequest.created_at.desc()).all()
    purchases = Purchase.query.order_by(Purchase.created_at.desc()).all()
    
    context = {
        'user': user,
        'total_users': total_users,
        'total_donors': total_donors,
        'total_staff': total_staff,
        'total_admins': total_admins,
        'total_blood_units': total_blood_units,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'total_purchases': total_purchases,
        'total_spending': total_spending,
        'donors': donors,
        'staff': staff,
        'blood_inventory': blood_inventory,
        'requests': requests,
        'purchases': purchases
    }
    
    return render_template('admin.html', **context)

# DONOR MANAGEMENT
@app.route('/admin/donor/add', methods=['POST'])
@role_required('admin')
def add_donor():
    """Add new donor (admin)"""
    try:
        data = request.get_json()
        
        # Check if donor exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'status': 'error', 'message': 'Username already exists'}), 400
        
        donor = Donor(
            username=data['username'],
            email=data['email'],
            full_name=data['full_name'],
            phone=data['phone'],
            blood_type=data['blood_type'],
            address=data.get('address', ''),
            city=data.get('city', '')
        )
        donor.set_password(data.get('password', 'default123'))
        
        db.session.add(donor)
        db.session.commit()
        
        log_action('ADD_DONOR', f"Admin added new donor: {data['username']}")
        return jsonify({'status': 'success', 'message': 'Donor added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/admin/donor/edit/<int:donor_id>', methods=['POST'])
@role_required('admin')
def edit_donor(donor_id):
    """Edit donor details"""
    try:
        donor = Donor.query.get_or_404(donor_id)
        data = request.get_json()
        
        donor.full_name = data.get('full_name', donor.full_name)
        donor.phone = data.get('phone', donor.phone)
        donor.blood_type = data.get('blood_type', donor.blood_type)
        donor.address = data.get('address', donor.address)
        donor.city = data.get('city', donor.city)
        donor.is_eligible = data.get('is_eligible', donor.is_eligible)
        
        db.session.commit()
        log_action('EDIT_DONOR', f"Admin edited donor: {donor.username}")
        return jsonify({'status': 'success', 'message': 'Donor updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/admin/donor/delete/<int:donor_id>', methods=['DELETE'])
@role_required('admin')
def delete_donor(donor_id):
    """Delete donor"""
    try:
        donor = Donor.query.get_or_404(donor_id)
        username = donor.username
        
        db.session.delete(donor)
        db.session.commit()
        
        log_action('DELETE_DONOR', f"Admin deleted donor: {username}")
        return jsonify({'status': 'success', 'message': 'Donor deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# STAFF MANAGEMENT
@app.route('/admin/staff/add', methods=['POST'])
@role_required('admin')
def add_staff():
    """Add new staff member"""
    try:
        data = request.get_json()
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'status': 'error', 'message': 'Username already exists'}), 400
        
        staff = Staff(
            username=data['username'],
            email=data['email'],
            full_name=data['full_name'],
            phone=data['phone'],
            department=data.get('department', 'Blood Bank')
        )
        staff.set_password(data.get('password', 'default123'))
        
        db.session.add(staff)
        db.session.commit()
        
        log_action('ADD_STAFF', f"Admin added new staff: {data['username']}")
        return jsonify({'status': 'success', 'message': 'Staff member added'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/admin/staff/edit/<int:staff_id>', methods=['POST'])
@role_required('admin')
def edit_staff(staff_id):
    """Edit staff details"""
    try:
        staff = Staff.query.get_or_404(staff_id)
        data = request.get_json()
        
        staff.full_name = data.get('full_name', staff.full_name)
        staff.phone = data.get('phone', staff.phone)
        staff.department = data.get('department', staff.department)
        
        db.session.commit()
        log_action('EDIT_STAFF', f"Admin edited staff: {staff.username}")
        return jsonify({'status': 'success', 'message': 'Staff updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/admin/staff/delete/<int:staff_id>', methods=['DELETE'])
@role_required('admin')
def delete_staff(staff_id):
    """Delete staff member"""
    try:
        staff = Staff.query.get_or_404(staff_id)
        username = staff.username
        
        db.session.delete(staff)
        db.session.commit()
        
        log_action('DELETE_STAFF', f"Admin deleted staff: {username}")
        return jsonify({'status': 'success', 'message': 'Staff deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# BLOOD UNIT MANAGEMENT
@app.route('/admin/blood/add', methods=['POST'])
@role_required('admin')
def add_blood_unit():
    """Add blood unit to inventory"""
    try:
        data = request.get_json()
        
        expiry_date = None
        if data.get('expiry_date'):
            expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%d')
        
        blood_unit = BloodUnit(
            blood_type=data['blood_type'],
            quantity=int(data.get('quantity', 1)),
            expiry_date=expiry_date,
            status='available',
            added_by=session['user_id'],
            notes=data.get('notes', '')
        )
        
        db.session.add(blood_unit)
        db.session.commit()
        
        log_action('ADD_BLOOD_UNIT', f"Added {data['blood_type']} x{data.get('quantity', 1)} units")
        return jsonify({'status': 'success', 'message': 'Blood unit added'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/admin/blood/edit/<int:unit_id>', methods=['POST'])
@role_required('admin')
def edit_blood_unit(unit_id):
    """Edit blood unit"""
    try:
        unit = BloodUnit.query.get_or_404(unit_id)
        data = request.get_json()
        
        unit.quantity = int(data.get('quantity', unit.quantity))
        unit.status = data.get('status', unit.status)
        unit.notes = data.get('notes', unit.notes)
        
        db.session.commit()
        log_action('EDIT_BLOOD_UNIT', f"Updated blood unit {unit.blood_type}")
        return jsonify({'status': 'success', 'message': 'Blood unit updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/admin/blood/delete/<int:unit_id>', methods=['DELETE'])
@role_required('admin')
def delete_blood_unit(unit_id):
    """Delete blood unit"""
    try:
        unit = BloodUnit.query.get_or_404(unit_id)
        blood_type = unit.blood_type
        
        db.session.delete(unit)
        db.session.commit()
        
        log_action('DELETE_BLOOD_UNIT', f"Deleted {blood_type} units")
        return jsonify({'status': 'success', 'message': 'Blood unit deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# REQUEST MANAGEMENT
@app.route('/admin/request/edit/<int:req_id>', methods=['POST'])
@role_required('admin')
def edit_request(req_id):
    """Edit blood request"""
    try:
        blood_request = BloodRequest.query.get_or_404(req_id)
        data = request.get_json()
        
        blood_request.status = data.get('status', blood_request.status)
        blood_request.notes = data.get('notes', blood_request.notes)
        
        if blood_request.status == 'fulfilled':
            blood_request.fulfilled_date = datetime.utcnow()
            blood_request.fulfilled_quantity = int(data.get('fulfilled_quantity', 0))
        
        db.session.commit()
        log_action('EDIT_REQUEST', f"Updated request for {blood_request.patient_name}")
        return jsonify({'status': 'success', 'message': 'Request updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/admin/request/delete/<int:req_id>', methods=['DELETE'])
@role_required('admin')
def delete_request(req_id):
    """Delete blood request"""
    try:
        blood_request = BloodRequest.query.get_or_404(req_id)
        patient_name = blood_request.patient_name
        
        db.session.delete(blood_request)
        db.session.commit()
        
        log_action('DELETE_REQUEST', f"Deleted request for {patient_name}")
        return jsonify({'status': 'success', 'message': 'Request deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# PURCHASE MANAGEMENT
@app.route('/admin/purchase/add', methods=['POST'])
@role_required('admin')
def add_purchase():
    """Create purchase order"""
    try:
        data = request.get_json()
        
        quantity = int(data.get('quantity', 1))
        unit_price = float(data.get('unit_price', 0))
        total_price = quantity * unit_price
        
        purchase = Purchase(
            blood_type=data['blood_type'],
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price,
            supplier_name=data['supplier_name'],
            supplier_contact=data.get('supplier_contact', ''),
            purchased_by=session['user_id'],
            status='pending',
            notes=data.get('notes', '')
        )
        
        db.session.add(purchase)
        db.session.commit()
        
        log_action('ADD_PURCHASE', f"New purchase: {data['blood_type']} x{quantity} from {data['supplier_name']}")
        return jsonify({'status': 'success', 'message': 'Purchase order created'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/admin/purchase/edit/<int:purchase_id>', methods=['POST'])
@role_required('admin')
def edit_purchase(purchase_id):
    """Edit purchase order"""
    try:
        purchase = Purchase.query.get_or_404(purchase_id)
        data = request.get_json()
        
        purchase.status = data.get('status', purchase.status)
        if data.get('delivery_date'):
            purchase.delivery_date = datetime.strptime(data['delivery_date'], '%Y-%m-%d')
        purchase.notes = data.get('notes', purchase.notes)
        
        db.session.commit()
        log_action('EDIT_PURCHASE', f"Updated purchase order #{purchase.id}")
        return jsonify({'status': 'success', 'message': 'Purchase updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/admin/purchase/delete/<int:purchase_id>', methods=['DELETE'])
@role_required('admin')
def delete_purchase(purchase_id):
    """Delete purchase order"""
    try:
        purchase = Purchase.query.get_or_404(purchase_id)
        
        db.session.delete(purchase)
        db.session.commit()
        
        log_action('DELETE_PURCHASE', f"Deleted purchase order #{purchase.id}")
        return jsonify({'status': 'success', 'message': 'Purchase deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ====================== STAFF ROUTES ======================

@app.route('/staff/dashboard')
@role_required('staff')
def staff_dashboard():
    """Staff dashboard"""
    user = get_current_user()
    
    # Get requests assigned to this staff
    assigned_deliveries = Delivery.query.filter_by(staff_assigned=user.id).all()
    pending_requests = BloodRequest.query.filter_by(status='pending').count()
    processing_requests = BloodRequest.query.filter_by(status='processing').count()
    
    # Get all requests
    all_requests = BloodRequest.query.order_by(BloodRequest.created_at.desc()).all()
    
    # Get blood inventory
    blood_inventory = BloodUnit.query.filter_by(status='available').all()
    
    context = {
        'user': user,
        'assigned_deliveries': assigned_deliveries,
        'pending_requests': pending_requests,
        'processing_requests': processing_requests,
        'all_requests': all_requests,
        'blood_inventory': blood_inventory
    }
    
    return render_template('staff.html', **context)

@app.route('/staff/request/add', methods=['POST'])
@role_required('staff')
def staff_add_request():
    """Staff adds blood request"""
    try:
        data = request.get_json()
        
        blood_request = BloodRequest(
            patient_name=data['patient_name'],
            blood_type=data['blood_type'],
            quantity_needed=int(data.get('quantity_needed', 1)),
            hospital_name=data['hospital_name'],
            hospital_contact=data.get('hospital_contact', ''),
            reason=data.get('reason', ''),
            requested_by=session['user_id'],
            status='pending'
        )
        
        db.session.add(blood_request)
        db.session.commit()
        
        log_action('ADD_REQUEST', f"Staff created request for {data['patient_name']} ({data['blood_type']})")
        return jsonify({'status': 'success', 'message': 'Request created', 'request_id': blood_request.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/staff/delivery/update/<int:delivery_id>', methods=['POST'])
@role_required('staff')
def update_delivery(delivery_id):
    """Update delivery status"""
    try:
        delivery = Delivery.query.get_or_404(delivery_id)
        data = request.get_json()
        
        old_status = delivery.status
        new_status = data.get('status')
        
        if new_status == 'processing' and old_status == 'request_created':
            delivery.status = 'processing'
            delivery.processing_started_at = datetime.utcnow()
        elif new_status == 'completed' and old_status == 'processing':
            delivery.status = 'completed'
            delivery.completed_at = datetime.utcnow()
            delivery.actual_delivery_date = datetime.utcnow()
        
        db.session.commit()
        log_action('UPDATE_DELIVERY', f"Delivery #{delivery.id} status updated to {new_status}")
        return jsonify({'status': 'success', 'message': 'Delivery status updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/staff/delivery/<int:req_id>/create', methods=['POST'])
@role_required('staff')
def create_delivery(req_id):
    """Create delivery for a request"""
    try:
        blood_request = BloodRequest.query.get_or_404(req_id)
        data = request.get_json()
        
        delivery = Delivery(
            request_id=req_id,
            quantity_dispatched=int(data.get('quantity', 1)),
            status='request_created',
            staff_assigned=session['user_id'],
            delivery_address=data.get('delivery_address', ''),
            expected_delivery_date=datetime.strptime(data['expected_date'], '%Y-%m-%d') if data.get('expected_date') else None,
            delivery_notes=data.get('notes', '')
        )
        
        db.session.add(delivery)
        blood_request.status = 'processing'
        db.session.commit()
        
        log_action('CREATE_DELIVERY', f"Delivery created for request #{req_id}")
        return jsonify({'status': 'success', 'message': 'Delivery created', 'delivery_id': delivery.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ====================== DONOR ROUTES ======================

@app.route('/donor/profile')
@role_required('donor')
def donor_profile():
    """Donor profile page"""
    user = get_current_user()
    
    # Get donor details
    donor = Donor.query.get(user.id)
    
    # Get donation history
    donation_history = BloodUnit.query.filter_by(donor_id=donor.id).all()
    
    # Get requests made by donor
    donor_requests = BloodRequest.query.filter_by(requested_by=donor.id).all()
    
    context = {
        'user': user,
        'donor': donor,
        'donation_history': donation_history,
        'donation_count': len(donation_history),
        'donor_requests': donor_requests
    }
    
    return render_template('donor.html', **context)

@app.route('/donor/schedule-donation', methods=['POST'])
@role_required('donor')
def schedule_donation():
    """Schedule donation"""
    try:
        data = request.get_json()
        donor = Donor.query.get(session['user_id'])
        
        # Add blood unit for this donation
        blood_unit = BloodUnit(
            blood_type=donor.blood_type,
            quantity=1,
            donor_id=donor.id,
            added_by=donor.id,
            status='available',
            expiry_date=datetime.utcnow() + timedelta(days=42)  # Typical shelf life
        )
        
        donor.last_donation_date = datetime.utcnow()
        db.session.add(blood_unit)
        db.session.commit()
        
        log_action('SCHEDULE_DONATION', f"Donor {donor.username} scheduled donation ({donor.blood_type})")
        return jsonify({'status': 'success', 'message': 'Donation scheduled successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/donor/purchase', methods=['POST'])
@login_required
def purchase_blood():
    """Purchase blood units"""
    try:
        data = request.get_json()
        
        # Create purchase order
        purchase = Purchase(
            blood_type=data['blood_type'],
            quantity=int(data.get('quantity', 1)),
            unit_price=float(data.get('unit_price', 100)),
            total_price=int(data.get('quantity', 1)) * float(data.get('unit_price', 100)),
            supplier_name='Direct Purchase',
            purchased_by=session['user_id'],
            status='pending'
        )
        
        db.session.add(purchase)
        db.session.commit()
        
        log_action('PURCHASE', f"Blood purchase: {data['blood_type']} x{data.get('quantity', 1)} units")
        return jsonify({'status': 'success', 'message': 'Purchase order created', 'total': purchase.total_price}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ====================== ERROR HANDLERS ======================

@app.errorhandler(404)
def page_not_found(e):
    """404 error handler"""
    return render_template('error.html', error_code=404, error_message='Page Not Found'), 404

@app.errorhandler(500)
def internal_error(e):
    """500 error handler"""
    db.session.rollback()
    return render_template('error.html', error_code=500, error_message='Internal Server Error'), 500

@app.errorhandler(403)
def forbidden(e):
    """403 error handler"""
    return render_template('error.html', error_code=403, error_message='Forbidden'), 403

# ====================== SAMPLE DATA INITIALIZATION ======================

def create_sample_data():
    """Create sample data for testing"""
    if User.query.first():
        print("✓ Database already has data")
        return
    
    print("Creating sample data...")
    
    # Create Admin
    admin = Admin(
        username='admin',
        email='admin@bloodbank.com',
        full_name='Admin User',
        phone='7558671952'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Create Staff
    staff1 = Staff(
        username='staff1',
        email='staff1@bloodbank.com',
        full_name='John Staff',
        phone='9876543210',
        department='Blood Collection'
    )
    staff1.set_password('staff123')
    db.session.add(staff1)
    
    staff2 = Staff(
        username='staff2',
        email='staff2@bloodbank.com',
        full_name='Jane Staff',
        phone='9876543211',
        department='Blood Processing'
    )
    staff2.set_password('staff123')
    db.session.add(staff2)
    
    # Create Donors
    donors_data = [
        ('donor1', 'donor1@bloodbank.com', 'Ram Kumar', 'O+', '1990-05-15'),
        ('donor2', 'donor2@bloodbank.com', 'Priya Singh', 'A+', '1992-08-22'),
        ('donor3', 'donor3@bloodbank.com', 'Amit Patel', 'B+', '1988-11-30'),
        ('donor4', 'donor4@bloodbank.com', 'Neha Sharma', 'AB+', '1995-03-18'),
        ('donor5', 'donor5@bloodbank.com', 'Rohan Gupta', 'O-', '1991-07-12'),
    ]
    
    donors = []
    for username, email, full_name, blood_type, dob in donors_data:
        donor = Donor(
            username=username,
            email=email,
            full_name=full_name,
            blood_type=blood_type,
            date_of_birth=datetime.strptime(dob, '%Y-%m-%d'),
            phone='9876543212',
            address='123 Main Street',
            city='Mumbai'
        )
        donor.set_password('donor123')
        donors.append(donor)
        db.session.add(donor)
    
    db.session.commit()
    
    # Create Blood Units
    blood_types = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
    for blood_type in blood_types:
        for i in range(5):
            unit = BloodUnit(
                blood_type=blood_type,
                quantity=2,
                status='available',
                added_by=admin.id,
                expiry_date=datetime.utcnow() + timedelta(days=42)
            )
            db.session.add(unit)
    
    db.session.commit()
    
    # Create Blood Requests
    requests_data = [
        ('Patient A', 'O+', 2, 'Apollo Hospital', '9999999999', 'Emergency'),
        ('Patient B', 'A+', 1, 'Fortis Hospital', '9999999998', 'Surgery'),
        ('Patient C', 'B+', 3, 'Max Healthcare', '9999999997', 'Regular'),
    ]
    
    for patient_name, blood_type, qty, hospital, contact, reason in requests_data:
        blood_req = BloodRequest(
            patient_name=patient_name,
            blood_type=blood_type,
            quantity_needed=qty,
            hospital_name=hospital,
            hospital_contact=contact,
            reason=reason,
            requested_by=staff1.id,
            status='pending'
        )
        db.session.add(blood_req)
    
    db.session.commit()
    
    # Create Purchases
    purchases_data = [
        ('O+', 10, 100, 'Red Cross Blood Bank', '9876543200'),
        ('A+', 8, 105, 'Government Blood Bank', '9876543201'),
        ('B+', 5, 110, 'Private Blood Center', '9876543202'),
    ]
    
    for blood_type, qty, price, supplier, contact in purchases_data:
        purchase = Purchase(
            blood_type=blood_type,
            quantity=qty,
            unit_price=price,
            total_price=qty * price,
            supplier_name=supplier,
            supplier_contact=contact,
            purchased_by=admin.id,
            status='received'
        )
        db.session.add(purchase)
    
    db.session.commit()
    
    print("✓ Sample data created successfully")

# ====================== MAIN ======================

if __name__ == '__main__':
    with app.app_context():
        # Create sample data
        create_sample_data()
        
        # Run Flask app
        print("\n" + "="*60)
        print("🏥 Blood Bank Management System")
        print("="*60)
        print("🚀 Server running at: http://localhost:5000")
        print("📚 Database: SQLite (blood_bank.db)")
        print("👤 Demo Credentials:")
        print("   Admin: admin / admin123")
        print("   Staff: staff1 / staff123")
        print("   Donor: donor1 / donor123")
        print("="*60 + "\n")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
