# 🔧 Installation & Testing Guide

Complete step-by-step guide to install and test the Blood Bank Management System.

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.8 or higher installed
- [ ] pip (Python package manager)
- [ ] Git (optional, for cloning)
- [ ] 300MB free disk space
- [ ] A web browser (Chrome, Firefox, Safari, Edge)
- [ ] Text editor (VS Code, Sublime, etc.)

### Check Python Version

**Windows:**
```cmd
python --version
```

**macOS/Linux:**
```bash
python3 --version
```

Should show Python 3.8+

## 🚀 Installation Steps

### 1. Navigate to Project Directory

**Windows:**
```cmd
cd C:\Users\YourUsername\Bloody-Blood-Bank-VS-Code
```

**macOS/Linux:**
```bash
cd ~/Bloody-Blood-Bank-VS-Code
```

### 2. Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
```

**macOS/Linux:**
```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```cmd
venv\Scripts\activate
```

You should see `(venv)` in your command prompt.

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` before your username.

### 4. Upgrade pip (Recommended)

**Windows:**
```cmd
python -m pip install --upgrade pip
```

**macOS/Linux:**
```bash
python3 -m pip install --upgrade pip
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- SQLAlchemy 2.0.21
- Werkzeug 2.3.7
- python-dotenv 1.0.0

### 6. Run Setup Script (Optional but Recommended)

```bash
python setup.py
```

This creates and populates the database with sample data.

### 7. Start Application

**Windows:**
```cmd
python app.py
```

**macOS/Linux:**
```bash
python3 app.py
```

You should see:
```
============================================================
🏥 Blood Bank Management System
============================================================
🚀 Server running at: http://localhost:5000
📚 Database: SQLite (blood_bank.db)
👤 Demo Credentials:
   Admin: admin / admin123
   Staff: staff1 / staff123
   Donor: donor1 / donor123
============================================================
```

### 8. Open in Browser

Open your web browser and go to:
```
http://localhost:5000
```

You should see the login page! ✅

## 🧪 Testing Guide

### Test 1: Admin Features (10 minutes)

1. **Login as Admin**
   - Username: `admin`
   - Password: `admin123`
   - Click "Login"

2. **Check Dashboard**
   - Verify statistics display
   - Should show: Donors, Blood Units, Requests, Spending

3. **Manage Donors**
   - Click "Manage Donors" tab
   - Click "+ Add Donor"
   - Fill form:
     - Username: `test_donor`
     - Email: `test@example.com`
     - Full Name: `Test Person`
     - Blood Type: `O+`
   - Click "Add Donor"
   - Verify success message

4. **Add Blood Unit**
   - Click "Blood Inventory" tab
   - Click "+ Add Blood Unit"
   - Select: Blood Type: `A+`, Quantity: `5`
   - Set expiry date
   - Click "Add Unit"
   - Verify in table

5. **Create Purchase**
   - Click "Purchase Orders" tab
   - Click "+ New Purchase"
   - Fill: Blood Type: `B+`, Qty: `10`, Price: `100`
   - Supplier: `Test Supplier`
   - Click "Create Order"
   - Verify success

✅ **Admin test complete!**

### Test 2: Staff Features (10 minutes)

1. **Logout and Login as Staff**
   - Click Logout
   - Username: `staff1`
   - Password: `staff123`

2. **Check Staff Dashboard**
   - View pending requests
   - View blood inventory

3. **Create Blood Request**
   - Click "+ Create Request"
   - Patient: `John Doe`
   - Hospital: `City Hospital`
   - Blood Type: `O+`
   - Quantity: `2`
   - Click "Create Request"

4. **Create Delivery**
   - Find the request in table
   - Click "Create Delivery"
   - Enter delivery address
   - Enter expected date
   - Click confirm

5. **Update Delivery Status**
   - Go to "Deliveries" tab
   - Click "Start Processing" on delivery
   - Verify stage changes

✅ **Staff test complete!**

### Test 3: Donor Features (10 minutes)

1. **Logout and Login as Donor**
   - Click Logout
   - Username: `donor1`
   - Password: `donor123`

2. **View Profile**
   - Click "My Profile"
   - Verify all information displays
   - Check blood type: `O+`

3. **Schedule Donation**
   - Click "Schedule Donation"
   - Select date
   - Click "Confirm Donation"
   - Verify success message

4. **Purchase Blood**
   - Click "Purchase Blood"
   - Select Blood Type: `A+`
   - Quantity: `1`
   - Unit Price: `100`
   - Verify total: `$100`
   - Click "Complete Purchase"

5. **Check History**
   - View donation history
   - Should see new donation

✅ **Donor test complete!**

### Test 4: Registration (5 minutes)

1. **Logout**
   - Click Logout

2. **Register New Donor**
   - Click "Register as Donor"
   - Fill all required fields
   - Password: `testpass123`
   - Select Blood Type: `AB-`
   - Click "Register"

3. **Verify Registration**
   - Should redirect to login
   - Try logging in with new credentials
   - Should access donor panel

✅ **Registration test complete!**

### Test 5: Error Handling (5 minutes)

1. **Test Invalid Login**
   - Try: Username: `admin`, Password: `wrongpass`
   - Verify error message

2. **Test Duplicate Username**
   - Try registering with existing username
   - Verify error message

3. **Test 404 Error**
   - Go to: `http://localhost:5000/nonexistent`
   - Should see 404 error page

✅ **Error handling test complete!**

## ✅ Verification Checklist

After installation, verify:

- [ ] Application starts without errors
- [ ] Database file created (`blood_bank.db`)
- [ ] Login page displays correctly
- [ ] Can login with demo credentials
- [ ] Admin panel accessible by admin
- [ ] Staff panel accessible by staff
- [ ] Donor panel accessible by donor
- [ ] Forms submit successfully
- [ ] Data displays in tables
- [ ] Responsive design works (try resizing)
- [ ] No errors in browser console
- [ ] All links work

## 🐛 Troubleshooting

### Issue: "python: command not found"

**Solution:** Use `python3` instead:
```bash
python3 app.py
```

Or add Python to PATH (Windows).

### Issue: "No module named flask"

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"

**Solution:** Kill process or use different port:
```bash
# Edit app.py last line to:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: "Database locked"

**Solution:** Delete database and restart:
```bash
rm blood_bank.db
python app.py
```

### Issue: Virtual environment won't activate (Windows)

**Solution:** Enable script execution:
```cmd
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

### Issue: "No module named models"

**Solution:** Make sure you're in project directory:
```bash
cd /path/to/bloody-blood-bank
```

## 📊 Database Verification

After first run, verify database:

```bash
# List database contents
python3 -c "
from app import app
from models import *
with app.app_context():
    print('Admins:', Admin.query.count())
    print('Staff:', Staff.query.count())
    print('Donors:', Donor.query.count())
    print('Blood Units:', BloodUnit.query.count())
    print('Requests:', BloodRequest.query.count())
"
```

## 🔐 Security Testing

1. **Test Password Hashing**
   - Verify passwords not stored as plain text
   - Check database with SQLite browser

2. **Test Session Security**
   - Logout
   - Try accessing protected page
   - Should redirect to login

3. **Test Role-Based Access**
   - Login as donor
   - Try accessing `/admin/dashboard`
   - Should be denied

## 📱 Responsive Testing

Test on different screen sizes:

1. **Desktop (1920x1080)**
   - All features should work
   - Layout optimal

2. **Tablet (768x1024)**
   - Responsive layout applies
   - Navigation works

3. **Mobile (375x667)**
   - Layout stacks vertically
   - Buttons easily clickable

Use browser developer tools (F12) to test.

## ⚡ Performance Testing

1. **Load Dashboard**
   - Should load in < 2 seconds

2. **Submit Form**
   - Should respond in < 1 second

3. **Navigate Tabs**
   - Should switch instantly

## 📝 Logging Verification

Check action log:

```bash
cat action_log.txt
```

Should show entries like:
```
[2026-01-24 10:30:45] admin: LOGIN - User admin logged in
[2026-01-24 10:31:12] admin: ADD_DONOR - Admin added new donor
```

## 🎯 Feature Testing Matrix

| Feature | Admin | Staff | Donor |
|---------|-------|-------|-------|
| Login | ✅ | ✅ | ✅ |
| View Dashboard | ✅ | ✅ | ✅ |
| Add Donor | ✅ | ❌ | ❌ |
| Create Request | ✅ | ✅ | ✅ |
| Create Delivery | ❌ | ✅ | ❌ |
| Schedule Donation | ❌ | ❌ | ✅ |
| Purchase Blood | ✅ | ✅ | ✅ |
| View Inventory | ✅ | ✅ | ✅ |

## 📊 Testing Report Template

```
TESTING REPORT - Blood Bank Management System
Date: ___________
Tester: _________

✅ Installation: PASS / FAIL
✅ Admin Features: PASS / FAIL
✅ Staff Features: PASS / FAIL
✅ Donor Features: PASS / FAIL
✅ Registration: PASS / FAIL
✅ Error Handling: PASS / FAIL
✅ Responsive Design: PASS / FAIL
✅ Database: PASS / FAIL
✅ Security: PASS / FAIL
✅ Performance: PASS / FAIL

Issues Found:
- Issue 1
- Issue 2

Overall Status: PASS / FAIL
```

## 🎉 Success Criteria

Your installation is successful if:

1. ✅ Application runs without errors
2. ✅ All three user roles can login
3. ✅ CRUD operations work
4. ✅ Forms validate inputs
5. ✅ Error pages display
6. ✅ Database persists data
7. ✅ Responsive design works
8. ✅ No console errors
9. ✅ All links work
10. ✅ Logout works properly

## 📞 Support

If you encounter issues:

1. Check the error message carefully
2. Review this troubleshooting guide
3. Check `README.md`
4. Check `DEPLOYMENT.md`
5. Contact: satavhariom775@gmail.com

## 🚀 Next Steps After Testing

1. **Customize** - Modify for your needs
2. **Deploy** - Follow DEPLOYMENT.md
3. **Extend** - Add new features
4. **Integrate** - Connect to your systems
5. **Share** - Use in production

---

**Installation & Testing Guide v1.0**  
**Last Updated:** January 24, 2026
