"""
Blood Unit model
Tracks blood inventory and stock management
"""

from models.db import db
from datetime import datetime

class BloodUnit(db.Model):
    """Blood inventory units"""
    __tablename__ = 'blood_units'
    
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(5), nullable=False)  # A+, A-, B+, B-, AB+, AB-, O+, O-
    quantity = db.Column(db.Integer, default=1)  # in units (bags)
    collection_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='available')  # available, used, expired, discarded
    donor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<BloodUnit {self.blood_type} - {self.status}>'
    
    def is_expired(self):
        """Check if blood unit has expired"""
        if self.expiry_date:
            return datetime.utcnow() > self.expiry_date
        return False
    
    def get_remaining_days(self):
        """Get days until expiration"""
        if self.expiry_date:
            delta = self.expiry_date - datetime.utcnow()
            return delta.days
        return None
