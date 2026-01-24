# ⚡ Quick Start Guide - Blood Bank Management System

Get the Blood Bank Management System running in 5 minutes!

## 🎯 Minimum Requirements

- Python 3.8+
- 300MB disk space
- Windows/Mac/Linux

## 🚀 Quick Setup (Windows)

```bash
# 1. Open Command Prompt in project folder
cd bloody-blood-bank

# 2. Create environment
python -m venv venv

# 3. Activate environment
venv\Scripts\activate

# 4. Install packages
pip install -r requirements.txt

# 5. Run application
python app.py
```

**Open browser:** `http://localhost:5000`

## 🚀 Quick Setup (macOS/Linux)

```bash
cd bloody-blood-bank
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

**Open browser:** `http://localhost:5000`

## 👤 Demo Accounts

| Role | Username | Password |
|------|----------|----------|
| 🔑 Admin | admin | admin123 |
| 👷 Staff | staff1 | staff123 |
| 🩸 Donor | donor1 | donor123 |

## 📝 What to Try First

### As Admin:
1. Login with `admin / admin123`
2. Go to Admin Panel
3. Add a new donor
4. Add blood units
5. Create purchase orders

### As Staff:
1. Login with `staff1 / staff123`
2. Create a blood request
3. Create a delivery
4. Update delivery status

### As Donor:
1. Login with `donor1 / donor123`
2. View profile
3. Schedule a donation
4. Purchase blood units

## ❌ Troubleshooting

### "Command not found: python"
Use `python3` instead of `python`:
```bash
python3 -m venv venv
```

### "Module not found"
Make sure venv is activated and requirements installed:
```bash
pip install -r requirements.txt
```

### "Port 5000 already in use"
Edit last line of app.py:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### "Database errors"
Delete database and restart:
```bash
rm blood_bank.db
python app.py
```

## 📁 Important Files

- `app.py` - Main application
- `blood_bank.db` - Database (auto-created)
- `action_log.txt` - Activity log
- `README.md` - Full documentation
- `DEPLOYMENT.md` - Deployment guide

## 🔥 Features Overview

✅ **3 User Roles**: Admin, Staff, Donor
✅ **Blood Inventory**: Track by type and expiry
✅ **Delivery Tracking**: 3-stage process
✅ **Purchase Orders**: From suppliers
✅ **Audit Logging**: All actions tracked
✅ **Responsive Design**: Works on all devices
✅ **Sample Data**: Pre-loaded for testing

## 📊 What Happens First Run

1. Creates SQLite database (`blood_bank.db`)
2. Creates all tables
3. Adds 1 admin, 2 staff, 5 donors
4. Adds 40 blood units (5 of each type)
5. Creates sample requests & purchases

## 🎨 UI Navigation

**Home Page:**
- Dashboard with statistics
- Blood inventory breakdown
- Recent requests & purchases
- Purchase blood units

**Admin Panel:**
- Manage donors (add/edit/delete)
- Manage staff
- Blood inventory
- Blood requests
- Purchase orders

**Staff Panel:**
- Create blood requests
- Manage deliveries (3-stage tracking)
- View blood inventory

**Donor Panel:**
- View profile
- Schedule donations
- Donation history
- Purchase blood

## 💾 Backing Up Data

```bash
# Copy database
copy blood_bank.db blood_bank_backup.db

# Or compress everything
tar -czf backup.tar.gz blood_bank.db action_log.txt
```

## 🔐 Security Notes

- Passwords are hashed (not stored plain text)
- Change SECRET_KEY before production
- Set debug=False for production
- Use HTTPS in production

## 📚 Full Documentation

See `README.md` for:
- Complete feature list
- API routes
- Database schema
- EC2 deployment
- Troubleshooting

## 🆘 Help

Still having issues?
- Check `README.md`
- Check `DEPLOYMENT.md`
- Contact: satavhariom775@gmail.com

---

**Enjoy your Blood Bank Management System! 🏥**
