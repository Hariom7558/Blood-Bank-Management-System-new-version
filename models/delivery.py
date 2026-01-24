"""
Delivery model
Handles delivery tracking and timeline
"""

from models.db import db
from datetime import datetime

class Delivery(db.Model):
    """Delivery tracking for blood requests"""
    __tablename__ = 'deliveries'
    
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('blood_requests.id'), nullable=False)
    blood_units_id = db.Column(db.Integer, db.ForeignKey('blood_units.id'))
    quantity_dispatched = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='request_created')  # request_created, processing, completed
    staff_assigned = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Timeline tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processing_started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Delivery details
    delivery_address = db.Column(db.String(255))
    expected_delivery_date = db.Column(db.DateTime)
    actual_delivery_date = db.Column(db.DateTime)
    delivery_notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Delivery {self.id} - {self.status}>'
    
    def get_stage_number(self):
        """Get current stage (1=created, 2=processing, 3=completed)"""
        stages = {
            'request_created': 1,
            'processing': 2,
            'completed': 3
        }
        return stages.get(self.status, 1)
