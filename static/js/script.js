/**
 * Blood Bank Management System - JavaScript
 * Frontend interactivity and AJAX requests
 */

// ===== TAB SWITCHING =====
function switchTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Remove active from buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab
    const activeTab = document.getElementById(tabName);
    if (activeTab) {
        activeTab.classList.add('active');
    }
    
    // Mark button as active
    event.target.classList.add('active');
}

// ===== FORM MODAL FUNCTIONS =====

// Donor Management
function showAddDonorForm() {
    document.getElementById('addDonorForm').style.display = 'flex';
}

function closeAddDonorForm() {
    document.getElementById('addDonorForm').style.display = 'none';
}

function addDonor() {
    const data = {
        username: document.getElementById('donor_username').value,
        email: document.getElementById('donor_email').value,
        full_name: document.getElementById('donor_full_name').value,
        phone: document.getElementById('donor_phone').value,
        blood_type: document.getElementById('donor_blood_type').value,
        password: document.getElementById('donor_password').value || 'default123',
        address: document.getElementById('donor_address').value,
        city: document.getElementById('donor_city').value
    };
    
    if (!data.username || !data.email || !data.full_name || !data.blood_type) {
        alert('Please fill all required fields');
        return;
    }
    
    fetch('/admin/donor/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            showAlert('Donor added successfully!', 'success');
            closeAddDonorForm();
            location.reload();
        } else {
            showAlert(result.message, 'error');
        }
    })
    .catch(error => showAlert('Error: ' + error, 'error'));
}

function editDonor(donorId) {
    alert('Edit functionality - get donor details and populate form');
}

function deleteDonor(donorId) {
    if (!confirm('Are you sure you want to delete this donor?')) return;
    
    fetch(`/admin/donor/delete/${donorId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            showAlert('Donor deleted successfully!', 'success');
            location.reload();
        }
    })
    .catch(error => showAlert('Error: ' + error, 'error'));
}

// Staff Management
function showAddStaffForm() {
    document.getElementById('addStaffForm').style.display = 'flex';
}

function closeAddStaffForm() {
    document.getElementById('addStaffForm').style.display = 'none';
}

function addStaff() {
    const data = {
        username: document.getElementById('staff_username').value,
        email: document.getElementById('staff_email').value,
        full_name: document.getElementById('staff_full_name').value,
        phone: document.getElementById('staff_phone').value,
        department: document.getElementById('staff_department').value || 'Blood Bank',
        password: document.getElementById('staff_password').value || 'default123'
    };
    
    if (!data.username || !data.email || !data.full_name) {
        alert('Please fill all required fields');
        return;
    }
    
    fetch('/admin/staff/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            showAlert('Staff member added successfully!', 'success');
            closeAddStaffForm();
            location.reload();
        }
    })
    .catch(error => showAlert('Error: ' + error, 'error'));
}

function editStaff(staffId) {
    alert('Edit functionality');
}

function deleteStaff(staffId) {
    if (!confirm('Are you sure?')) return;
    
    fetch(`/admin/staff/delete/${staffId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            showAlert('Staff deleted successfully!', 'success');
            location.reload();
        }
    })
    .catch(error => showAlert('Error: ' + error, 'error'));
}

// Blood Unit Management
function showAddBloodForm() {
    document.getElementById('addBloodForm').style.display = 'flex';
}

function closeAddBloodForm() {
    document.getElementById('addBloodForm').style.display = 'none';
}

function addBloodUnit() {
    const data = {
        blood_type: document.getElementById('blood_type').value,
        quantity: document.getElementById('blood_quantity').value,
        expiry_date: document.getElementById('blood_expiry').value,
        notes: document.getElementById('blood_notes').value
    };
    
    if (!data.blood_type || !data.quantity) {
        alert('Please fill all required fields');
        return;
    }
    
    fetch('/admin/blood/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            showAlert('Blood unit added successfully!', 'success');
            closeAddBloodForm();
            location.reload();
        }
    })
    .catch(error => showAlert('Error: ' + error, 'error'));
}

function editBlood(unitId) {
    alert('Edit functionality');
}

function deleteBlood(unitId) {
    if (!confirm('Are you sure?')) return;
    
    fetch(`/admin/blood/delete/${unitId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            showAlert('Blood unit deleted!', 'success');
            location.reload();
        }
    })
    .catch(error => showAlert('Error: ' + error, 'error'));
}

// Request Management
function editRequest(requestId) {
    alert('Edit request functionality');
}

function deleteRequest(requestId) {
    if (!confirm('Are you sure?')) return;
    
    fetch(`/admin/request/delete/${requestId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            showAlert('Request deleted!', 'success');
            location.reload();
        }
    })
    .catch(error => showAlert('Error: ' + error, 'error'));
}

// Purchase Management
function showAddPurchaseForm() {
    document.getElementById('addPurchaseForm').style.display = 'flex';
}

function closeAddPurchaseForm() {
    document.getElementById('addPurchaseForm').style.display = 'none';
}

function addPurchase() {
    const data = {
        blood_type: document.getElementById('purchase_blood_type').value,
        quantity: document.getElementById('purchase_qty').value,
        unit_price: document.getElementById('purchase_unit_price').value,
        supplier_name: document.getElementById('purchase_supplier').value,
        supplier_contact: document.getElementById('purchase_contact').value,
        notes: document.getElementById('purchase_notes').value
    };
    
    if (!data.blood_type || !data.quantity || !data.unit_price || !data.supplier_name) {
        alert('Please fill all required fields');
        return;
    }
    
    fetch('/admin/purchase/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            showAlert('Purchase order created!', 'success');
            closeAddPurchaseForm();
            location.reload();
        }
    })
    .catch(error => showAlert('Error: ' + error, 'error'));
}

function editPurchase(purchaseId) {
    alert('Edit purchase functionality');
}

function deletePurchase(purchaseId) {
    if (!confirm('Are you sure?')) return;
    
    fetch(`/admin/purchase/delete/${purchaseId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            showAlert('Purchase deleted!', 'success');
            location.reload();
        }
    })
    .catch(error => showAlert('Error: ' + error, 'error'));
}

// ===== STAFF FUNCTIONS =====

function showAddRequestForm() {
    document.getElementById('addRequestForm').style.display = 'flex';
}

function closeAddRequestForm() {
    document.getElementById('addRequestForm').style.display = 'none';
}

function staffAddRequest() {
    const data = {
        patient_name: document.getElementById('req_patient_name').value,
        hospital_name: document.getElementById('req_hospital_name').value,
        blood_type: document.getElementById('req_blood_type').value,
        quantity_needed: document.getElementById('req_quantity').value,
        hospital_contact: document.getElementById('req_hospital_contact').value,
        reason: document.getElementById('req_reason').value
    };
    
    if (!data.patient_name || !data.hospital_name || !data.blood_type || !data.quantity_needed) {
        alert('Please fill all required fields');
        return;
    }
    
    fetch('/staff/request/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            showAlert('Request created successfully!', 'success');
            closeAddRequestForm();
            location.reload();
        }
    })
    .catch(error => showAlert('Error: ' + error, 'error'));
}

function createDelivery(requestId) {
    const address = prompt('Enter delivery address:');
    const expectedDate = prompt('Enter expected delivery date (YYYY-MM-DD):');
    
    if (!address || !expectedDate) return;
    
    const data = {
        quantity: 1,
        delivery_address: address,
        expected_date: expectedDate
    };
    
    fetch(`/staff/delivery/${requestId}/create`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            showAlert('Delivery created! ID: ' + result.delivery_id, 'success');
            location.reload();
        }
    })
    .catch(error => showAlert('Error: ' + error, 'error'));
}

function updateDeliveryStatus(deliveryId, newStatus) {
    const data = {
        status: newStatus
    };
    
    fetch(`/staff/delivery/update/${deliveryId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            showAlert('Delivery status updated!', 'success');
            location.reload();
        }
    })
    .catch(error => showAlert('Error: ' + error, 'error'));
}

// ===== DONOR FUNCTIONS =====

function showScheduleDonationForm() {
    document.getElementById('scheduleDonationForm').style.display = 'flex';
}

function closeScheduleDonationForm() {
    document.getElementById('scheduleDonationForm').style.display = 'none';
}

function scheduleDonation() {
    const data = {
        donation_date: document.getElementById('donation_date').value,
        notes: document.getElementById('donation_notes').value
    };
    
    fetch('/donor/schedule-donation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            showAlert('Thank you for scheduling your donation!', 'success');
            closeScheduleDonationForm();
            location.reload();
        }
    })
    .catch(error => showAlert('Error: ' + error, 'error'));
}

function showPurchaseForm() {
    document.getElementById('purchaseForm').style.display = 'flex';
}

function closePurchaseForm() {
    document.getElementById('purchaseForm').style.display = 'none';
}

function doPurchaseBlood() {
    const data = {
        blood_type: document.getElementById('purchase_type').value,
        quantity: document.getElementById('purchase_qty').value,
        unit_price: document.getElementById('purchase_unit_price').value
    };
    
    if (!data.blood_type || !data.quantity) {
        alert('Please fill all fields');
        return;
    }
    
    fetch('/donor/purchase', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            showAlert(`Purchase successful! Total: $${result.total}`, 'success');
            closePurchaseForm();
            location.reload();
        }
    })
    .catch(error => showAlert('Error: ' + error, 'error'));
}

function purchaseBlood() {
    const bloodType = document.getElementById('purchase_blood_type').value;
    const quantity = document.getElementById('purchase_quantity').value;
    const price = document.getElementById('purchase_price').value;
    
    if (!bloodType || !quantity) {
        alert('Please select blood type and quantity');
        return;
    }
    
    const data = {
        blood_type: bloodType,
        quantity: quantity,
        unit_price: price
    };
    
    fetch('/donor/purchase', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            showAlert(`Purchase successful! Total: $${result.total}`, 'success');
            setTimeout(() => location.reload(), 1000);
        }
    })
    .catch(error => showAlert('Error: ' + error, 'error'));
}

// ===== UTILITY FUNCTIONS =====

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    // Insert at top of main content
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.insertBefore(alertDiv, mainContent.firstChild);
    }
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Close modals when clicking outside
document.addEventListener('click', function(event) {
    const modals = document.querySelectorAll('.form-modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});

// Close modals on Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const modals = document.querySelectorAll('.form-modal');
        modals.forEach(modal => {
            modal.style.display = 'none';
        });
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Activate first tab by default
    const firstTabButton = document.querySelector('.tab-button');
    if (firstTabButton) {
        firstTabButton.click();
    }
    
    console.log('Blood Bank Management System - Loaded successfully!');
});
