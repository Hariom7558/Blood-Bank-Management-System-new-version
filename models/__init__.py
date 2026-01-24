"""
Models package initialization
Imports all models for easier access
"""

from models.db import db, init_db
from models.user import User, Admin, Staff, Donor
from models.blood_unit import BloodUnit
from models.request import BloodRequest
from models.purchase import Purchase
from models.delivery import Delivery

__all__ = [
    'db',
    'init_db',
    'User',
    'Admin',
    'Staff',
    'Donor',
    'BloodUnit',
    'BloodRequest',
    'Purchase',
    'Delivery'
]
