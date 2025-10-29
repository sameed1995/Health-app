import streamlit as st
import re
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Hospital Appointment System", page_icon="🏥", layout="wide")

# Lab Tests with Pricing
lab_tests = {
    "X-ray": 1000,
    "MRI": 12000,
    "CT Scan": 10000,
    "LFT": 800,
    "RFT": 700,
    "CBC": 200
}

# Department and Doctor data
department = {
    "General Medicine": [
        {"name": "Dr. Meera Shah", "room": "101", "experience": 5, "patients": 0},
        {"name": "Dr. Raj Patel", "room": "102", "experience": 7, "patients": 0},
        {"name": "Dr. Neha Sharma", "room": "103", "experience": 3, "patients": 0}
    ],
    "Cardiology": [
        {"name": "Dr. Ravi Kumar", "room": "201", "experience": 6, "patients": 0},
        {"name": "Dr. Priya Gupta", "room": "202", "experience": 4, "patients": 0},
        {"name": "Dr. Anjali Singh", "room": "203", "experience": 2, "patients": 0}
    ],
    "Neurology": [
        {"name": "Dr. Sanjay Verma", "room": "301", "experience": 8, "patients": 0},
        {"name": "Dr. Anjali Sharma", "room": "302", "experience": 5, "patients": 0},
        {"name": "Dr. Ravi Patel", "room": "303", "experience": 3, "patients": 0}
    ],
    "Pediatrician": [
        {"name": "Dr. Neha Gupta", "room": "401", "experience": 4, "patients": 0},
        {"name": "Dr. Sanjay Singh", "room": "402", "experience": 6, "patients": 0},
        {"name": "Dr. Priya Patel", "room": "403", "experience": 2, "patients": 0}
    ],
    "Nephrologist": [
        {"name": "Dr. Ravi Sharma", "room": "501", "experience": 7, "patients": 0},
        {"name": "Dr. Neha Patel", "room": "502", "experience": 5, "patients": 0},
        {"name": "Dr. Sanjay Gupta", "room": "503", "experience": 3, "patients": 0}
    ],
    "Radiology": [
        {"name": "Dr. Priya Singh", "room": "601", "experience": 6, "patients": 0},
        {"name": "Dr. Anjali Patel", "room": "602", "experience": 4, "patients": 0},
        {"name": "Dr. Ravi Gupta", "room": "603", "experience": 2, "patients": 0}
    ]
}

symptom_to_dept = {
    "fever": "General Medicine",
    "cough": "General Medicine",
    "cold": "General Medicine",
    "vomiting": "General Medicine",
    "chest pain": "Cardiology",
    "heart pain": "Cardiology",
    "palpitations": "Cardiology",
    "headache": "Neurology",
    "migraine": "Neurology",
    "dizziness": "Neurology",
    "child fever": "Pediatrician",
    "vaccination": "Pediatrician",
    "kidney pain": "Nephrologist",
    "urinary issues": "Nephrologist",
    "x-ray": "Radiology",
    "scan": "Radiology"
}

# Validation functions
def validate_name(name):
    if not name or not name.strip():
        return False, "Name cannot be empty"
    if not name.replace(" ", "").isalpha():
        return False, "Name should only contain letters and spaces"
    if len(name.strip()) < 2:
        return False, "Name must be at least 2 characters"
    return True, ""

def validate_age(age):
    if age < 1 or age > 120:
        return False, "Age must be between 1 and 120"
    return True, ""

def validate_mobile(mobile):
    mobile_clean = mobile.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    if not mobile_clean.isdigit():
        return False, "Mobile number should contain only digits"
    if len(mobile_clean) != 10:
        return False, "Mobile number must be exactly 10 digits"
    return True, ""

def validate_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "Please enter a valid email address"
    return True, ""

def validate_billing(amount):
    if amount <= 0:
        return False, "Billing amount must be greater than 0"
    if amount > 1000000:
        return False, "Billing amount seems unusually high"
    return True, ""

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {}
if 'department_data' not in st.session_state:
    st.session_state.department_data = department
if 'all_appointments' not in st.session_state:
    st.session_state.all_appointments = []

# Sidebar for Analytics
with st.sidebar:
    st.title("📊 Analytics Dashboard")
    
    if st.button("🔄 Refresh Stats"):
        st.rerun()
    
    # Department selector for analytics
    selected_dept_analytics = st.selectbox(
        "Select Department for Analytics",
        list(department.keys())
    )
    
    # Get doctors from selected department
    doctors_in_dept = st.session_state.department_data[selected_dept_analytics]
    
    # Check if any doctor has patients
    total_patients = sum(doc['patients'] for doc in doctors_in_dept)
    
    if total_patients > 0:
        st.subheader(f"Patient Distribution - {selected_dept_analytics}")
        
        # Prepare data for pie chart
        doctor_names = [doc['name'] for doc in doctors_in_dept if doc['patients'] > 0]
        patient_counts = [doc['patients'] for doc in doctors_in_dept if doc['patients'] > 0]
        
        # Create pie chart
        fig = px.pie(
            values=patient_counts,
            names=doctor_names,
            title=f"Patients per Doctor",
            hole=0.3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        # Show detailed stats
        st.subheader("Detailed Statistics")
        for doc in doctors_in_dept:
            if doc['patients'] > 0:
                st.metric(
                    doc['name'],
                    f"{doc['patients']} patients",
                    f"Room {doc['room']}"
                )
    else:
        st.info(f"No patients registered yet in {selected_dept_analytics}")
    
    st.markdown("---")
    st.metric("Total Appointments", len(st.session_state.all_appointments))

# Main UI
st.title("🏥 Hospital Appointment System")
st.markdown("---")

# Step 1: Patient Information
if st.session_state.step >= 1:
    st.header("📋 Step 1: Patient Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name *", value=st.session_state.patient_data.get('name', ''))
        age = st.number_input("Age *", min_value=1, max_value=120, value=st.session_state.patient_data.get('age', 25))
        blood_group = st.selectbox("Blood Group *", 
                                   ['Select', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
                                   index=0 if 'blood_group' not in st.session_state.patient_data else 
                                   ['Select', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'].index(st.session_state.patient_data['blood_group']))
    
    with col2:
        gender = st.selectbox("Gender *", ['Select', 'Male', 'Female', 'Other'],
                             index=0 if 'gender' not in st.session_state.patient_data else
                             ['Select', 'Male', 'Female', 'Other'].index(st.session_state.patient_data['gender']))
        mobile = st.text_input("Mobile Number *", value=st.session_state.patient_data.get('mobile', ''),
                              placeholder="e.g., 9876543210")
        email = st.text_input("Email Address *", value=st.session_state.patient_data.get('email', ''),
                             placeholder="e.g., example@email.com")
    
    dob = st.date_input("Date of Birth *", 
                       value=st.session_state.patient_data.get('dob', date(2000, 1, 1)),
                       min_value=date(1900, 1, 1),
                       max_value=date.today())
    
    if st.button("Continue to Symptoms →", key="step1_btn", type="primary"):
        errors = []
        
        is_valid, msg = validate_name(name)
        if not is_valid:
            errors.append(f"Name: {msg}")
        
        is_valid, msg = validate_age(age)
        if not is_valid:
            errors.append(f"Age: {msg}")
        
        if blood_group == 'Select':
            errors.append("Please select a blood group")
        
        if gender == 'Select':
            errors.append("Please select a gender")
        
        is_valid, msg = validate_mobile(mobile)
        if not is_valid:
            errors.append(f"Mobile: {msg}")
        
        is_valid, msg = validate_email(email)
        if not is_valid:
            errors.append(f"Email: {msg}")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            st.session_state.patient_data.update({
                'name': name,
                'age': age,
                'blood_group': blood_group,
                'gender': gender,
                'mobile': mobile,
                'email': email,
                'dob': dob
            })
            st.session_state.step = 2
            st.rerun()

# Step 2: Symptoms and Department
if st.session_state.step >= 2:
    st.markdown("---")
    st.header("🩺 Step 2: Symptoms")
    
    st.write("Select your symptoms (you can choose multiple):")
    
    symptoms_list = list(symptom_to_dept.keys())
    col1, col2, col3 = st.columns(3)
    
    selected_symptoms = []
    for i, symptom in enumerate(symptoms_list):
        col = [col1, col2, col3][i % 3]
        with col:
            if st.checkbox(symptom.title(), key=f"symptom_{symptom}"):
                selected_symptoms.append(symptom)
    
    if selected_symptoms:
        suggested_departments = set()
        for s in selected_symptoms:
            dept = symptom_to_dept.get(s.lower())
            if dept:
                suggested_departments.add(dept)
        
        if suggested_departments:
            st.success(f"✅ Suggested Department(s): {', '.join(suggested_departments)}")
            
            selected_dept = st.selectbox("Select Department *", 
                                        ['Select'] + list(suggested_departments))
            
            if selected_dept != 'Select':
                if st.button("Continue to Doctor Selection →", key="step2_btn", type="primary"):
                    st.session_state.patient_data['symptoms'] = selected_symptoms
                    st.session_state.patient_data['department'] = selected_dept
                    st.session_state.step = 3
                    st.rerun()
    else:
        st.info("ℹ️ Please select at least one symptom")
    
    if st.button("← Back", key="back1"):
        st.session_state.step = 1
        st.rerun()

# Step 3: Doctor Selection
if st.session_state.step >= 3:
    st.markdown("---")
    st.header("👨‍⚕️ Step 3: Select Doctor")
    
    selected_dept = st.session_state.patient_data['department']
    doctors = st.session_state.department_data[selected_dept]
    
    st.subheader(f"Available Doctors in {selected_dept}")
    
    cols = st.columns(len(doctors))
    selected_doctor_idx = None
    
    for i, doc in enumerate(doctors):
        with cols[i]:
            st.markdown(f"""
            <div style='border: 2px solid #ddd; padding: 15px; border-radius: 10px; text-align: center;'>
                <h4>{doc['name']}</h4>
                <p>Room: {doc['room']}</p>
                <p>Experience: {doc['experience']} years</p>
                <p>Patients: {doc['patients']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Select", key=f"doc_{i}"):
                selected_doctor_idx = i
    
    if selected_doctor_idx is not None:
        st.session_state.patient_data['doctor'] = doctors[selected_doctor_idx]
        st.session_state.patient_data['doctor_index'] = selected_doctor_idx
        st.session_state.step = 4
        st.rerun()
    
    if st.button("← Back", key="back2"):
        st.session_state.step = 2
        st.rerun()

# Step 4: Lab Tests Selection
if st.session_state.step >= 4:
    st.markdown("---")
    st.header("🧪 Step 4: Select Lab Tests")
    
    st.write("Select the lab tests required for this patient:")
    
    selected_tests = []
    total_lab_cost = 0
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        for test_name, price in lab_tests.items():
            if st.checkbox(f"{test_name} - ₹{price:,}", key=f"lab_{test_name}"):
                selected_tests.append(test_name)
                total_lab_cost += price
    
    with col2:
        st.metric("Total Lab Cost", f"₹{total_lab_cost:,}")
        st.metric("Tests Selected", len(selected_tests))
    
    if selected_tests:
        st.success(f"Selected Tests: {', '.join(selected_tests)}")
    else:
        st.info("ℹ️ No lab tests selected (optional)")
    
    if st.button("Continue to Appointment Details →", key="step4_btn", type="primary"):
        st.session_state.patient_data['lab_tests'] = selected_tests
        st.session_state.patient_data['lab_cost'] = total_lab_cost
        st.session_state.step = 5
        st.rerun()
    
    if st.button("← Back", key="back3"):
        st.session_state.step = 3
        st.rerun()

# Step 5: Time Slot and Additional Details
if st.session_state.step >= 5:
    st.markdown("---")
    st.header("🕐 Step 5: Select Time Slot & Additional Details")
    
    time_slots = ["10:00 AM", "11:00 AM", "2:00 PM", "4:00 PM", "5:00 PM"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_slot = st.selectbox("Time Slot *", ['Select'] + time_slots)
        appointment_date = st.date_input("Appointment Date *", 
                                        min_value=date.today(),
                                        value=date.today())
    
    with col2:
        patient_type = st.selectbox("Patient Type *", ['Select', 'New Patient', 'Existing Patient'])
        consultation_fee = st.number_input("Consultation Fee (₹) *", min_value=0.0, value=500.0, step=100.0)
    
    # Calculate total billing
    lab_cost = st.session_state.patient_data.get('lab_cost', 0)
    total_billing = consultation_fee + lab_cost
    
    st.markdown("---")
    st.subheader("💰 Billing Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Consultation Fee", f"₹{consultation_fee:,.2f}")
    with col2:
        st.metric("Lab Tests Cost", f"₹{lab_cost:,.2f}")
    with col3:
        st.metric("Total Amount", f"₹{total_billing:,.2f}", delta=None)
    
    if st.button("Confirm Appointment ✅", key="step5_btn", type="primary"):
        errors = []
        
        if selected_slot == 'Select':
            errors.append("Please select a time slot")
        if patient_type == 'Select':
            errors.append("Please select patient type")
        
        is_valid, msg = validate_billing(consultation_fee)
        if not is_valid:
            errors.append(f"Consultation Fee: {msg}")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            # Update doctor patient count
            dept = st.session_state.patient_data['department']
            doc_idx = st.session_state.patient_data['doctor_index']
            st.session_state.department_data[dept][doc_idx]['patients'] += 1
            
            # Store appointment data
            appointment_record = {
                **st.session_state.patient_data,
                'time_slot': selected_slot,
                'appointment_date': appointment_date,
                'patient_type': patient_type,
                'consultation_fee': consultation_fee,
                'total_billing': total_billing,
                'booking_time': datetime.now()
            }
            st.session_state.all_appointments.append(appointment_record)
            
            st.session_state.patient_data.update({
                'time_slot': selected_slot,
                'appointment_date': appointment_date,
                'patient_type': patient_type,
                'consultation_fee': consultation_fee,
                'total_billing': total_billing
            })
            st.session_state.step = 6
            st.rerun()
    
    if st.button("← Back", key="back4"):
        st.session_state.step = 4
        st.rerun()

# Step 6: Confirmation
if st.session_state.step >= 6:
    st.markdown("---")
    st.header("✅ Appointment Confirmed!")
    
    data = st.session_state.patient_data
    doctor = data['doctor']
    
    st.success("Your appointment has been successfully booked!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Patient Details")
        st.write(f"**Name:** {data['name']}")
        st.write(f"**Age:** {data['age']} years")
        st.write(f"**Gender:** {data['gender']}")
        st.write(f"**Blood Group:** {data['blood_group']}")
        st.write(f"**DOB:** {data['dob'].strftime('%d/%m/%Y')}")
        st.write(f"**Mobile:** {data['mobile']}")
        st.write(f"**Email:** {data['email']}")
        st.write(f"**Patient Type:** {data['patient_type']}")
    
    with col2:
        st.subheader("Appointment Details")
        st.write(f"**Doctor:** {doctor['name']}")
        st.write(f"**Department:** {data['department']}")
        st.write(f"**Room No:** {doctor['room']}")
        st.write(f"**Date:** {data['appointment_date'].strftime('%d/%m/%Y')}")
        st.write(f"**Time:** {data['time_slot']}")
    
    st.markdown("---")
    st.subheader("Symptoms")
    st.write(", ".join([s.title() for s in data['symptoms']]))
    
    st.markdown("---")
    st.subheader("🧪 Lab Tests Ordered")
    if data['lab_tests']:
        for test in data['lab_tests']:
            st.write(f"• {test} - ₹{lab_tests[test]:,}")
    else:
        st.write("No lab tests ordered")
    
    st.markdown("---")
    st.subheader("💰 Final Bill")
    bill_col1, bill_col2, bill_col3 = st.columns(3)
    with bill_col1:
        st.metric("Consultation Fee", f"₹{data['consultation_fee']:,.2f}")
    with bill_col2:
        st.metric("Lab Tests", f"₹{data['lab_cost']:,.2f}")
    with bill_col3:
        st.metric("Total Amount", f"₹{data['total_billing']:,.2f}")
    
    if st.button("Book Another Appointment", key="restart", type="primary"):
        st.session_state.step = 1
        st.session_state.patient_data = {}
        st.rerun()