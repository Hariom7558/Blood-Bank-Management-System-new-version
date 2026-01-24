# 🔌 API Documentation - Blood Bank Management System

Complete API endpoint reference for the Blood Bank Management System.

## Base URL

```
http://localhost:5000
```

## Authentication

All protected endpoints require the user to be logged in (session-based).

### Login Flow
1. POST to `/login` with credentials
2. Session cookie is created
3. Use cookie for subsequent requests

## Endpoints

### 🔐 Authentication Endpoints

#### POST /login
Login with credentials

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:** Redirects to `/home` on success

**Status Codes:** 200 (OK), 302 (Redirect)

---

#### POST /register
Register new donor account

**Request:**
```json
{
  "username": "new_donor",
  "email": "donor@example.com",
  "password": "secure_password",
  "confirm_password": "secure_password",
  "full_name": "John Doe",
  "phone": "9876543210",
  "blood_type": "O+",
  "date_of_birth": "1990-05-15",
  "address": "123 Main St",
  "city": "Mumbai"
}
```

**Response:** Redirects to `/login` on success

**Status Codes:** 200 (OK), 302 (Redirect)

---

#### GET /logout
Logout current user

**Response:** Redirects to `/login`

**Status Codes:** 302 (Redirect)

---

### 🏠 Dashboard Endpoints

#### GET /home
View home dashboard

**Authentication:** Required  
**Response:** HTML page with statistics

**Status Codes:** 200 (OK), 302 (Redirect to login)

---

#### GET /admin/dashboard
View admin panel

**Authentication:** Required (Admin only)  
**Response:** Admin panel HTML

**Status Codes:** 200 (OK), 403 (Forbidden), 302 (Redirect)

---

#### GET /staff/dashboard
View staff panel

**Authentication:** Required (Staff only)  
**Response:** Staff panel HTML

**Status Codes:** 200 (OK), 403 (Forbidden)

---

#### GET /donor/profile
View donor profile

**Authentication:** Required (Donor only)  
**Response:** Donor profile HTML

**Status Codes:** 200 (OK), 403 (Forbidden)

---

### 👥 Donor Management Endpoints

#### POST /admin/donor/add
Add new donor (Admin only)

**Authentication:** Required (Admin only)  
**Content-Type:** application/json

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "phone": "9876543210",
  "blood_type": "O+",
  "password": "default123",
  "address": "123 Main St",
  "city": "Mumbai"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Donor added successfully"
}
```

**Status Codes:** 201 (Created), 400 (Bad Request), 500 (Error)

---

#### POST /admin/donor/edit/<donor_id>
Edit donor details

**Authentication:** Required (Admin only)  
**Content-Type:** application/json

**Request:**
```json
{
  "full_name": "Updated Name",
  "phone": "9876543211",
  "blood_type": "A+",
  "address": "456 Second St",
  "city": "Pune",
  "is_eligible": true
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Donor updated"
}
```

---

#### DELETE /admin/donor/delete/<donor_id>
Delete donor

**Authentication:** Required (Admin only)

**Response:**
```json
{
  "status": "success",
  "message": "Donor deleted"
}
```

**Status Codes:** 200 (OK), 404 (Not Found), 500 (Error)

---

### 👷 Staff Management Endpoints

#### POST /admin/staff/add
Add new staff member

**Authentication:** Required (Admin only)  
**Content-Type:** application/json

**Request:**
```json
{
  "username": "staff_john",
  "email": "staff@example.com",
  "full_name": "John Staff",
  "phone": "9876543210",
  "department": "Blood Collection",
  "password": "default123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Staff member added"
}
```

---

#### POST /admin/staff/edit/<staff_id>
Edit staff details

**Authentication:** Required (Admin only)

**Request:**
```json
{
  "full_name": "Updated Name",
  "phone": "9876543211",
  "department": "Blood Processing"
}
```

---

#### DELETE /admin/staff/delete/<staff_id>
Delete staff member

**Authentication:** Required (Admin only)

**Response:**
```json
{
  "status": "success",
  "message": "Staff deleted"
}
```

---

### 🩸 Blood Unit Endpoints

#### POST /admin/blood/add
Add blood unit to inventory

**Authentication:** Required (Admin only)  
**Content-Type:** application/json

**Request:**
```json
{
  "blood_type": "O+",
  "quantity": 5,
  "expiry_date": "2026-03-06",
  "notes": "From blood drive"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Blood unit added"
}
```

---

#### POST /admin/blood/edit/<unit_id>
Edit blood unit

**Authentication:** Required (Admin only)

**Request:**
```json
{
  "quantity": 4,
  "status": "available",
  "notes": "Updated notes"
}
```

---

#### DELETE /admin/blood/delete/<unit_id>
Delete blood unit

**Authentication:** Required (Admin only)

---

### 📋 Blood Request Endpoints

#### POST /staff/request/add
Create blood request

**Authentication:** Required (Staff only)  
**Content-Type:** application/json

**Request:**
```json
{
  "patient_name": "Patient Name",
  "blood_type": "O+",
  "quantity_needed": 2,
  "hospital_name": "Apollo Hospital",
  "hospital_contact": "9999999999",
  "reason": "Emergency surgery"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Request created",
  "request_id": 123
}
```

---

#### POST /admin/request/edit/<request_id>
Edit blood request (Admin)

**Authentication:** Required (Admin only)

**Request:**
```json
{
  "status": "processing",
  "fulfilled_quantity": 2,
  "notes": "In progress"
}
```

---

#### DELETE /admin/request/delete/<request_id>
Delete request

**Authentication:** Required (Admin only)

---

### 🚚 Delivery Endpoints

#### POST /staff/delivery/<request_id>/create
Create delivery for request

**Authentication:** Required (Staff only)

**Request:**
```json
{
  "quantity": 2,
  "delivery_address": "Hospital Address",
  "expected_date": "2026-01-25"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Delivery created",
  "delivery_id": 456
}
```

---

#### POST /staff/delivery/update/<delivery_id>
Update delivery status

**Authentication:** Required (Staff only)

**Request:**
```json
{
  "status": "processing"
}
```

**Valid statuses:**
- `request_created`
- `processing`
- `completed`

**Response:**
```json
{
  "status": "success",
  "message": "Delivery status updated"
}
```

---

### 🛒 Purchase Endpoints

#### POST /admin/purchase/add
Create purchase order

**Authentication:** Required (Admin only)

**Request:**
```json
{
  "blood_type": "O+",
  "quantity": 10,
  "unit_price": 100,
  "supplier_name": "Red Cross",
  "supplier_contact": "9876543200",
  "notes": "Regular order"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Purchase order created"
}
```

---

#### POST /admin/purchase/edit/<purchase_id>
Edit purchase order

**Authentication:** Required (Admin only)

**Request:**
```json
{
  "status": "received",
  "delivery_date": "2026-01-25",
  "notes": "Received and checked"
}
```

---

#### DELETE /admin/purchase/delete/<purchase_id>
Delete purchase order

**Authentication:** Required (Admin only)

---

### 💉 Donor Operations

#### POST /donor/schedule-donation
Schedule donation

**Authentication:** Required (Donor only)

**Request:**
```json
{
  "donation_date": "2026-02-01",
  "notes": "Available anytime"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Thank you for scheduling your donation!"
}
```

---

#### POST /donor/purchase
Purchase blood units

**Authentication:** Required (Any user)

**Request:**
```json
{
  "blood_type": "O+",
  "quantity": 2,
  "unit_price": 100
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Purchase order created",
  "total": 200
}
```

---

### ❌ Error Endpoints

#### GET 404
Page not found

**Response:** Error page HTML

---

#### GET 500
Server error

**Response:** Error page HTML

---

## Status Codes Reference

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 302 | Redirect - Page redirect |
| 400 | Bad Request - Invalid input |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error |

## Response Format

All AJAX responses follow this format:

**Success:**
```json
{
  "status": "success",
  "message": "Operation completed"
}
```

**Error:**
```json
{
  "status": "error",
  "message": "Description of error"
}
```

## Authentication Required

Protected endpoints marked with 🔒 require:
1. Valid session cookie
2. Correct user role

Redirect to login if not authenticated.

## Error Handling

Common error responses:

**Invalid Credentials:**
```json
{
  "status": "error",
  "message": "Invalid username or password"
}
```

**Duplicate Entry:**
```json
{
  "status": "error",
  "message": "Username already exists"
}
```

**Validation Error:**
```json
{
  "status": "error",
  "message": "Please fill all required fields"
}
```

**Access Denied:**
```
403 Forbidden - Unauthorized access
```

## Example Usage

### Using cURL

```bash
# Login
curl -X POST http://localhost:5000/login \
  -d "username=admin&password=admin123"

# Add Donor (requires login session)
curl -X POST http://localhost:5000/admin/donor/add \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","full_name":"John Doe","blood_type":"O+"}'
```

### Using JavaScript

```javascript
// Login
fetch('/login', {
  method: 'POST',
  body: new FormData(formElement)
})

// Add Donor
fetch('/admin/donor/add', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'john',
    email: 'john@example.com',
    full_name: 'John Doe',
    blood_type: 'O+'
  })
})
.then(r => r.json())
.then(data => console.log(data))
```

## Rate Limiting

Currently no rate limiting. Recommended for production:
- 100 requests per minute per IP
- 1000 requests per hour per IP

## CORS

CORS not enabled by default. To enable:
```python
from flask_cors import CORS
CORS(app)
```

## Documentation

Full documentation available in:
- `README.md` - User guide
- `QUICKSTART.md` - Quick setup
- `DEPLOYMENT.md` - Deployment guide

---

**API Version:** 1.0  
**Last Updated:** January 24, 2026
