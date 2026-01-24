"""
Purchase model
Handles blood unit purchases and inventory management
"""

from models.db import db
from datetime import datetime

class Purchase(db.Model):
    """Blood unit purchases for inventory"""
    __tablename__ = 'purchases'
    
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(5), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)  # in units
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    supplier_name = db.Column(db.String(150), nullable=False)
    supplier_contact = db.Column(db.String(15))
    purchased_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    delivery_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')  # pending, received, added_to_inventory
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Purchase {self.blood_type} x{self.quantity}>'
