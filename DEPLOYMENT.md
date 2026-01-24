# 🚀 Deployment Guide - Blood Bank Management System

This guide covers deploying the Blood Bank Management System to various environments.

## Local Development (Windows)

### Prerequisites
- Python 3.8+
- pip

### Setup Steps

```bash
# 1. Navigate to project directory
cd bloody-blood-bank

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run application
python app.py
```

Visit: `http://localhost:5000`

## Local Development (macOS/Linux)

```bash
# 1. Navigate to project directory
cd bloody-blood-bank

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run application
python3 app.py
```

## AWS EC2 Deployment

### Prerequisites
- AWS EC2 instance (Amazon Linux 2 or Ubuntu)
- SSH access configured
- Security group allows port 5000 or 80/443

### Step-by-Step Deployment

#### 1. Connect to EC2 Instance
```bash
ssh -i "your-key.pem" ec2-user@your-ec2-public-ip
```

#### 2. Update System & Install Dependencies
```bash
# For Amazon Linux 2
sudo yum update -y
sudo yum install python3 python3-pip python3-venv git -y

# For Ubuntu
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y
```

#### 3. Clone Project
```bash
git clone <your-repository-url>
cd bloody-blood-bank
```

Or if no Git repository:
```bash
# Upload files via SCP or download
wget https://your-download-link/bloody-blood-bank.zip
unzip bloody-blood-bank.zip
cd bloody-blood-bank
```

#### 4. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 5. Install Requirements
```bash
pip install -r requirements.txt
```

#### 6. Initialize Database
```bash
python3 setup.py
```

#### 7. Test Run
```bash
python3 app.py
```

Access: `http://your-ec2-public-ip:5000`

#### 8. Production Deployment with Gunicorn

Install Gunicorn:
```bash
pip install gunicorn
```

Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

Or with multiple workers:
```bash
gunicorn -w 8 -b 0.0.0.0:5000 app:app
```

#### 9. Configure Firewall

For Amazon Linux 2:
```bash
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

For Ubuntu:
```bash
sudo ufw allow 5000/tcp
```

#### 10. Setup Systemd Service (Recommended)

Create service file:
```bash
sudo nano /etc/systemd/system/bloodbank.service
```

Add content:
```ini
[Unit]
Description=Blood Bank Management System
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/bloody-blood-bank
Environment="PATH=/home/ec2-user/bloody-blood-bank/venv/bin"
ExecStart=/home/ec2-user/bloody-blood-bank/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable bloodbank
sudo systemctl start bloodbank
sudo systemctl status bloodbank
```

View logs:
```bash
sudo journalctl -u bloodbank -f
```

## Setup Nginx Reverse Proxy (Optional)

Install Nginx:
```bash
# Amazon Linux 2
sudo yum install nginx -y

# Ubuntu
sudo apt install nginx -y
```

Configure Nginx:
```bash
sudo nano /etc/nginx/conf.d/bloodbank.conf
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/ec2-user/bloody-blood-bank/static/;
    }
}
```

Enable Nginx:
```bash
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl restart nginx
```

## Setup SSL with Let's Encrypt (HTTPS)

Install Certbot:
```bash
# Amazon Linux 2
sudo yum install certbot certbot-nginx -y

# Ubuntu
sudo apt install certbot python3-certbot-nginx -y
```

Request certificate:
```bash
sudo certbot --nginx -d your-domain.com
```

Auto-renewal:
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## Database Setup

### SQLite (Default)
Database automatically created at first run: `blood_bank.db`

### MySQL Setup (Optional)

Install MySQL:
```bash
sudo yum install mysql-server -y
sudo systemctl start mysqld
```

Create database:
```bash
mysql -u root -p
CREATE DATABASE blood_bank;
CREATE USER 'bloodbank'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON blood_bank.* TO 'bloodbank'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Update connection in app.py:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://bloodbank:secure_password@localhost/blood_bank'
```

Install MySQL driver:
```bash
pip install PyMySQL
```

## Environment Variables

Create `.env` file:
```bash
nano .env
```

Add:
```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///blood_bank.db
DEBUG=False
```

Load in app.py:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Monitoring & Logs

View application logs:
```bash
tail -f /var/log/bloodbank.log
```

Monitor system:
```bash
top
free -h
df -h
```

Check port usage:
```bash
netstat -tuln | grep 5000
```

## Backup & Recovery

### Backup Database
```bash
cp blood_bank.db blood_bank_backup_$(date +%Y%m%d).db
```

### Backup Everything
```bash
tar -czf bloodbank_backup_$(date +%Y%m%d).tar.gz \
  blood_bank.db \
  action_log.txt \
  venv/ \
  templates/ \
  static/ \
  models/
```

### Upload to S3
```bash
aws s3 cp blood_bank_backup_20260124.db s3://your-bucket/backups/
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Permission Denied
```bash
chmod +x app.py
sudo chown -R ec2-user:ec2-user /home/ec2-user/bloody-blood-bank
```

### Database Locked
```bash
# Delete database and recreate
rm blood_bank.db
python3 setup.py
```

### Out of Memory
Increase Gunicorn workers:
```bash
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

### Application Not Starting
```bash
# Check logs
python3 app.py 2>&1 | tee app.log

# Verify dependencies
pip list
```

## Performance Optimization

### Enable Caching
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

### Database Indexing
Already optimized with SQLAlchemy relationships.

### CDN Setup
Serve static files via CloudFront or similar CDN.

## Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Enable HTTPS with SSL certificate
- [ ] Set DEBUG = False
- [ ] Use strong database password
- [ ] Configure firewall rules
- [ ] Implement rate limiting
- [ ] Regular backups enabled
- [ ] Monitor system resources
- [ ] Update dependencies regularly
- [ ] Review access logs

## Cost Optimization

- **EC2 Instance**: t3.micro (eligible for free tier)
- **Storage**: EBS gp3 volumes
- **Database**: SQLite (no additional cost)
- **Monitoring**: CloudWatch (free tier includes 10 metrics)

## Support & Help

For issues:
1. Check logs: `sudo journalctl -u bloodbank -n 50`
2. Verify services: `sudo systemctl status nginx`
3. Test connectivity: `curl localhost:5000`
4. Contact: satavhariom775@gmail.com

---

**Deployment Version:** 1.0  
**Last Updated:** January 24, 2026
