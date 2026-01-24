"""
Blood Request model
Handles blood requests for patients
"""

from models.db import db
from datetime import datetime

class BloodRequest(db.Model):
    """Blood requests from hospitals/patients"""
    __tablename__ = 'blood_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(120), nullable=False)
    blood_type = db.Column(db.String(5), nullable=False)
    quantity_needed = db.Column(db.Integer, nullable=False)  # in units
    hospital_name = db.Column(db.String(150), nullable=False)
    hospital_contact = db.Column(db.String(15), nullable=False)
    reason = db.Column(db.String(255))
    requested_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default='pending')  # pending, processing, fulfilled, rejected
    fulfilled_quantity = db.Column(db.Integer, default=0)
    requested_date = db.Column(db.DateTime, default=datetime.utcnow)
    fulfilled_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to Delivery
    deliveries = db.relationship('Delivery', backref='request', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<BloodRequest {self.patient_name} - {self.blood_type}>'
    
    def get_status_color(self):
        """Get CSS color for status badge"""
        colors = {
            'pending': '#FFC107',
            'processing': '#17A2B8',
            'fulfilled': '#28A745',
            'rejected': '#DC3545'
        }
        return colors.get(self.status, '#6C757D')
