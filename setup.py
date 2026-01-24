#!/usr/bin/env python3
"""
Setup script for Blood Bank Management System
Run this to initialize the database with sample data
"""

import os
import sys
from app import app, db
from models.user import Admin, Staff, Donor
from models.blood_unit import BloodUnit
from models.request import BloodRequest
from models.purchase import Purchase
from datetime import datetime, timedelta

def setup_database():
    """Initialize and populate database"""
    print("\n" + "="*60)
    print("🏥 Blood Bank Management System - Setup")
    print("="*60 + "\n")
    
    with app.app_context():
        # Drop existing tables (optional - comment out to preserve data)
        # print("🔄 Dropping existing tables...")
        # db.drop_all()
        
        # Create tables
        print("📝 Creating database tables...")
        db.create_all()
        print("✓ Tables created successfully\n")
        
        # Check if data already exists
        if Admin.query.first():
            print("⚠️  Database already contains data. Skipping sample data creation.")
            print("   To reset, delete blood_bank.db and run this script again.\n")
            return
        
        # Create sample data
        print("📦 Creating sample data...")
        
        # Admin
        admin = Admin(
            username='admin',
            email='admin@bloodbank.com',
            full_name='System Administrator',
            phone='7558671952'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        print("✓ Admin user created")
        
        # Staff
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
        print("✓ Staff members created")
        
        # Donors
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
        print("✓ Donor users created")
        
        db.session.commit()
        
        # Blood Units
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
        print("✓ Blood units created (40 total)")
        
        db.session.commit()
        
        # Blood Requests
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
        print("✓ Blood requests created")
        
        db.session.commit()
        
        # Purchases
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
        print("✓ Purchase orders created")
        
        db.session.commit()
        
        print("\n" + "="*60)
        print("✅ Setup completed successfully!")
        print("="*60)
        print("\n📚 Demo Credentials:")
        print("   Admin:    admin / admin123")
        print("   Staff:    staff1 / staff123")
        print("   Donor:    donor1 / donor123")
        print("\n🚀 Run with: python app.py\n")

if __name__ == '__main__':
    setup_database()
