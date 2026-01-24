# 🏥 Blood Bank Management System

A complete, production-ready web application for managing blood bank operations, donor registrations, blood requests, and deliveries. Built with Flask, SQLAlchemy, and SQLite.

## 📋 Features

### Core Functionality
- ✅ **Multi-user Authentication** - Admin, Staff, Donor roles with secure password hashing
- ✅ **Home Dashboard** - Overview of donors, blood units, requests, and statistics
- ✅ **Admin Panel** - Complete CRUD operations for donors, staff, blood units, requests, purchases
- ✅ **Staff Panel** - Handle blood requests, manage deliveries, update inventory
- ✅ **Donor Panel** - Register, view donation history, schedule donations, purchase blood
- ✅ **Delivery System** - 3-stage tracking: request created → processing → completed
- ✅ **Blood Inventory** - Track blood units by type, quantity, status, expiry dates
- ✅ **Purchase Management** - Create purchase orders from suppliers
- ✅ **Audit Logging** - All actions logged for system tracking

### Technical Features
- 🔐 Password hashing with Werkzeug security
- 🗄️ SQLite database with SQLAlchemy ORM
- 📱 Responsive design (mobile, tablet, desktop)
- 🎨 Modern UI with clean CSS styling
- ⚡ AJAX for dynamic form submissions
- 📊 Real-time statistics and charts
- 🔔 Error handling with custom error pages
- 📝 Sample data for testing

## 📁 Project Structure

```
bloody-blood-bank/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── blood_bank.db            # SQLite database (auto-created)
├── action_log.txt           # System audit log
├── models/
│   ├── db.py               # Database initialization
│   ├── user.py             # User models (Admin, Staff, Donor)
│   ├── blood_unit.py       # Blood unit inventory model
│   ├── request.py          # Blood request model
│   ├── purchase.py         # Purchase order model
│   └── delivery.py         # Delivery tracking model
├── templates/
│   ├── login.html          # Login page
│   ├── register.html       # Donor registration
│   ├── home.html           # Home dashboard
│   ├── admin.html          # Admin panel
│   ├── staff.html          # Staff panel
│   ├── donor.html          # Donor profile
│   └── error.html          # Error pages
├── static/
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   └── js/
│       └── script.js       # JavaScript functionality
└── venv/                    # Virtual environment
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone/Download the project**
   ```bash
   cd bloody-blood-bank
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://localhost:5000
   ```

## 👤 Demo Credentials

The application comes with pre-populated sample data:

| Role | Username | Password | Purpose |
|------|----------|----------|---------|
| Admin | `admin` | `admin123` | Full system management |
| Staff | `staff1` | `staff123` | Handle requests & deliveries |
| Donor | `donor1` | `donor123` | View profile & donate |

**New donors can register** using the "Register" link on login page.

## 📖 User Roles & Permissions

### Admin
- Manage all donors (create, edit, delete)
- Manage staff members
- Add/edit/delete blood units
- Create purchase orders
- View system statistics
- Manage all blood requests

### Staff
- Create blood requests
- Create deliveries from requests
- Update delivery status (3 stages)
- View blood inventory
- Cannot delete/modify existing data

### Donor
- View personal profile
- Schedule donations
- View donation history
- Purchase blood units
- Create blood requests

## 🎯 Key Features Explained

### 1. Delivery System (3-Stage)
- **Stage 1: Request Created** - Initial request registered
- **Stage 2: Processing** - Blood being prepared/dispatched
- **Stage 3: Completed** - Blood delivered to hospital

Each stage has timestamps for audit trail.

### 2. Blood Inventory
- Track by blood type (O+, O-, A+, A-, B+, B-, AB+, AB-)
- Monitor expiry dates
- Show remaining shelf life
- Track availability status

### 3. Authentication
- Secure password hashing with Werkzeug
- Session-based login
- Role-based access control
- Auto-logout after inactivity

### 4. Dashboard Statistics
- Total donors in system
- Available blood units
- Pending requests
- Completed requests (monthly)
- Blood type breakdown
- Recent activities

## 🛠️ API Routes

### Authentication
- `GET /` - Redirect to home/login
- `GET/POST /login` - User login
- `GET/POST /register` - Donor registration
- `GET /logout` - Logout

### Home & Dashboard
- `GET /home` - Home dashboard

### Admin Routes
- `GET /admin/dashboard` - Admin panel
- `POST /admin/donor/add` - Add donor
- `POST /admin/staff/add` - Add staff
- `POST /admin/blood/add` - Add blood unit
- `DELETE /admin/donor/delete/<id>` - Delete donor
- `DELETE /admin/staff/delete/<id>` - Delete staff
- `DELETE /admin/blood/delete/<id>` - Delete blood unit

### Staff Routes
- `GET /staff/dashboard` - Staff panel
- `POST /staff/request/add` - Create request
- `POST /staff/delivery/<id>/create` - Create delivery
- `POST /staff/delivery/update/<id>` - Update delivery status

### Donor Routes
- `GET /donor/profile` - Donor profile
- `POST /donor/schedule-donation` - Schedule donation
- `POST /donor/purchase` - Purchase blood units

## 🗄️ Database Models

### User (Base Model)
- id, username, email, password_hash
- user_type, full_name, phone
- is_active, created_at, updated_at

### Donor (extends User)
- blood_type, date_of_birth
- address, city
- is_eligible, last_donation_date
- relationships: donations

### Admin (extends User)
- No additional fields

### Staff (extends User)
- department

### BloodUnit
- blood_type, quantity, status
- collection_date, expiry_date
- donor_id, added_by
- Methods: is_expired(), get_remaining_days()

### BloodRequest
- patient_name, blood_type, quantity_needed
- hospital_name, hospital_contact
- status, fulfilled_quantity, requested_date
- relationships: deliveries

### Purchase
- blood_type, quantity, unit_price, total_price
- supplier_name, supplier_contact
- purchase_date, delivery_date, status

### Delivery
- request_id, quantity_dispatched, status
- staff_assigned, delivery_address
- created_at, processing_started_at, completed_at
- Methods: get_stage_number()

## 🎨 UI/UX Features

- **Responsive Design** - Works on desktop, tablet, mobile
- **Modern Styling** - Clean gradients, smooth transitions
- **Interactive Forms** - Modal forms with validation
- **Real-time Updates** - AJAX-based operations
- **Data Tables** - Sortable, searchable tables
- **Status Badges** - Color-coded status indicators
- **Timeline Visualization** - Delivery stage tracking
- **Quick Actions** - Easy access buttons for common tasks

## 📝 Audit Logging

All actions are logged to `action_log.txt`:
```
[2026-01-24 10:30:45] admin: LOGIN - User admin logged in
[2026-01-24 10:31:12] admin: ADD_DONOR - Admin added new donor: donor_john
[2026-01-24 10:32:00] admin: ADD_BLOOD_UNIT - Added O+ x5 units
```

## 🔒 Security Features

- ✅ Password hashing (Werkzeug)
- ✅ Session-based authentication
- ✅ Role-based access control
- ✅ CSRF protection ready
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Error handling without exposing details

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py line (last line)
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Database Issues
```bash
# Delete and recreate database
rm blood_bank.db
python app.py
```

### Missing Dependencies
```bash
pip install -r requirements.txt --upgrade
```

## 🚀 Deployment to EC2

### Step 1: Connect to EC2 instance
```bash
ssh -i your-key.pem ec2-user@your-instance-ip
```

### Step 2: Install Python & dependencies
```bash
sudo yum update -y
sudo yum install python3 python3-pip -y
sudo yum install git -y
```

### Step 3: Clone project
```bash
git clone <your-repo-url>
cd bloody-blood-bank
```

### Step 4: Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 5: Run application
```bash
# Development
python3 app.py

# Production (with Gunicorn)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Step 6: Configure firewall
```bash
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

### Step 7: Access application
```
http://your-instance-ip:5000
```

## 📊 Sample Data

The application automatically creates sample data on first run:
- 1 Admin user
- 2 Staff members
- 5 Donors (various blood types)
- 40 Blood units (5 of each type)
- 3 Blood requests
- 3 Purchase orders

## 🤝 Owner Information

**Blood Bank Owners:**
- Hariom Satav
- Meet Patil
- Prajwal Shinde

**Contact:** 7558671952  
**Email:** satavhariom775@gmail.com

## 📄 License

This project is created for educational and commercial use.

## 🔄 Future Enhancements

- [ ] Email notifications for requests/purchases
- [ ] SMS alerts for donors
- [ ] Advanced reporting and analytics
- [ ] Blood type compatibility matrix
- [ ] Donor eligibility checklist
- [ ] Payment gateway integration
- [ ] QR code scanning for units
- [ ] Mobile app
- [ ] Multi-language support
- [ ] API documentation (Swagger)

## 📞 Support

For issues or questions, contact: satavhariom775@gmail.com

---

**Built with ❤️ using Flask, SQLAlchemy & SQLite**

**Version:** 1.0  
**Last Updated:** January 24, 2026
