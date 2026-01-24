"""
User models: Admin, Staff, and Donor
Handles authentication and user management
"""

from models.db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """Base User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # admin, staff, donor
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __mapper_args__ = {
        'polymorphic_on': user_type,
        'polymorphic_identity': 'user'
    }
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Admin(User):
    """Admin user - manages entire system"""
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }
    
    def __repr__(self):
        return f'<Admin {self.username}>'


class Staff(User):
    """Staff user - handles blood operations and deliveries"""
    __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    department = db.Column(db.String(100), default='Blood Bank')
    
    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }
    
    def __repr__(self):
        return f'<Staff {self.username}>'


class Donor(User):
    """Donor user - can donate blood"""
    __tablename__ = 'donors'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    blood_type = db.Column(db.String(5))  # A+, A-, B+, B-, AB+, AB-, O+, O-
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    is_eligible = db.Column(db.Boolean, default=True)
    last_donation_date = db.Column(db.DateTime)
    
    # Relationships
    donations = db.relationship('BloodUnit', backref='donor', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'donor'
    }
    
    def __repr__(self):
        return f'<Donor {self.username} ({self.blood_type})>'
