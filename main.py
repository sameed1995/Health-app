import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

# Page configuration
st.set_page_config(page_title="Hospital Admin Analytics", page_icon="📊", layout="wide")

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
departments_doctors = {
    "General Medicine": [
        {"name": "Dr. Meera Shah", "room": "101", "experience": 5},
        {"name": "Dr. Raj Patel", "room": "102", "experience": 7},
        {"name": "Dr. Neha Sharma", "room": "103", "experience": 3}
    ],
    "Cardiology": [
        {"name": "Dr. Ravi Kumar", "room": "201", "experience": 6},
        {"name": "Dr. Priya Gupta", "room": "202", "experience": 4},
        {"name": "Dr. Anjali Singh", "room": "203", "experience": 2}
    ],
    "Neurology": [
        {"name": "Dr. Sanjay Verma", "room": "301", "experience": 8},
        {"name": "Dr. Anjali Sharma", "room": "302", "experience": 5},
        {"name": "Dr. Ravi Patel", "room": "303", "experience": 3}
    ],
    "Pediatrician": [
        {"name": "Dr. Neha Gupta", "room": "401", "experience": 4},
        {"name": "Dr. Sanjay Singh", "room": "402", "experience": 6},
        {"name": "Dr. Priya Patel", "room": "403", "experience": 2}
    ],
    "Nephrologist": [
        {"name": "Dr. Ravi Sharma", "room": "501", "experience": 7},
        {"name": "Dr. Neha Patel", "room": "502", "experience": 5},
        {"name": "Dr. Sanjay Gupta", "room": "503", "experience": 3}
    ],
    "Radiology": [
        {"name": "Dr. Priya Singh", "room": "601", "experience": 6},
        {"name": "Dr. Anjali Patel", "room": "602", "experience": 4},
        {"name": "Dr. Ravi Gupta", "room": "603", "experience": 2}
    ]
}

symptoms_by_dept = {
    "General Medicine": ["fever", "cough", "cold", "vomiting", "headache", "fatigue"],
    "Cardiology": ["chest pain", "heart pain", "palpitations", "shortness of breath"],
    "Neurology": ["headache", "migraine", "dizziness", "numbness", "seizures"],
    "Pediatrician": ["child fever", "vaccination", "cough", "rash", "stomach pain"],
    "Nephrologist": ["kidney pain", "urinary issues", "swelling", "blood in urine"],
    "Radiology": ["x-ray", "scan", "imaging required"]
}

# Generate dummy data for 100 patients
@st.cache_data
def generate_dummy_data(num_patients=100):
    np.random.seed(42)
    random.seed(42)
    
    first_names = ["Amit", "Priya", "Raj", "Neha", "Sanjay", "Anjali", "Ravi", "Meera", 
                   "Vikram", "Pooja", "Arun", "Kavita", "Rahul", "Sneha", "Karan"]
    last_names = ["Sharma", "Patel", "Kumar", "Singh", "Gupta", "Verma", "Shah", "Mehta"]
    
    data = []
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(num_patients):
        # Random date within last year
        random_days = random.randint(0, 365)
        appointment_date = start_date + timedelta(days=random_days)
        
        # Select department and doctor
        dept = random.choice(list(departments_doctors.keys()))
        doctor = random.choice(departments_doctors[dept])
        
        # Generate symptoms based on department
        num_symptoms = random.randint(1, 3)
        symptoms = random.sample(symptoms_by_dept[dept], min(num_symptoms, len(symptoms_by_dept[dept])))
        
        # Lab tests
        num_tests = random.randint(0, 3)
        selected_tests = random.sample(list(lab_tests.keys()), num_tests)
        lab_cost = sum(lab_tests[test] for test in selected_tests)
        
        # Consultation fee varies by department
        base_fee = 500
        if dept == "Cardiology":
            consultation_fee = random.randint(800, 1500)
        elif dept == "Neurology":
            consultation_fee = random.randint(700, 1200)
        elif dept == "Radiology":
            consultation_fee = random.randint(300, 800)
        else:
            consultation_fee = random.randint(400, 1000)
        
        patient = {
            "patient_id": f"P{i+1:03d}",
            "name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "age": random.randint(1, 80),
            "gender": random.choice(["Male", "Female"]),
            "blood_group": random.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
            "mobile": f"{random.randint(7000000000, 9999999999)}",
            "email": f"patient{i+1}@email.com",
            "department": dept,
            "doctor_name": doctor["name"],
            "doctor_room": doctor["room"],
            "doctor_experience": doctor["experience"],
            "symptoms": ", ".join(symptoms),
            "num_symptoms": len(symptoms),
            "appointment_date": appointment_date.date(),
            "appointment_time": random.choice(["10:00 AM", "11:00 AM", "2:00 PM", "4:00 PM", "5:00 PM"]),
            "patient_type": random.choice(["New Patient", "Existing Patient"]),
            "lab_tests": ", ".join(selected_tests) if selected_tests else "None",
            "num_lab_tests": len(selected_tests),
            "lab_cost": lab_cost,
            "consultation_fee": consultation_fee,
            "total_billing": consultation_fee + lab_cost,
            "day_of_week": appointment_date.strftime("%A"),
            "month": appointment_date.strftime("%B"),
            "year": appointment_date.year,
            "quarter": f"Q{(appointment_date.month-1)//3 + 1}"
        }
        data.append(patient)
    
    return pd.DataFrame(data)

# Load data
df = generate_dummy_data(100)

# Sidebar Navigation
st.sidebar.title("🏥 Admin Dashboard")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    ["📊 Overview", "👨‍⚕️ Doctor Analytics", "🩺 Department Analytics", 
     "💰 Revenue Analytics", "📈 Trend Analysis", "📋 Patient Details"]
)

st.sidebar.markdown("---")
st.sidebar.info(f"Total Patients: {len(df)}")
st.sidebar.info(f"Total Revenue: ₹{df['total_billing'].sum():,.2f}")

# Main Title
st.title("🏥 Hospital Admin Analytics Dashboard")
st.markdown("---")

# ==================== OVERVIEW PAGE ====================
if menu == "📊 Overview":
    st.header("📊 Hospital Overview")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Patients", len(df))
    with col2:
        st.metric("Total Revenue", f"₹{df['total_billing'].sum():,.0f}")
    with col3:
        st.metric("Avg Revenue/Patient", f"₹{df['total_billing'].mean():,.0f}")
    with col4:
        st.metric("Total Doctors", sum(len(docs) for docs in departments_doctors.values()))
    
    st.markdown("---")
    
    # Row 1: Department Distribution and Patient Type
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Patients by Department")
        dept_counts = df['department'].value_counts()
        fig = px.pie(values=dept_counts.values, names=dept_counts.index, 
                     hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Patient Type Distribution")
        patient_type_counts = df['patient_type'].value_counts()
        fig = px.bar(x=patient_type_counts.index, y=patient_type_counts.values,
                     color=patient_type_counts.index,
                     labels={'x': 'Patient Type', 'y': 'Count'})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Row 2: Gender and Age Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Gender Distribution")
        gender_counts = df['gender'].value_counts()
        fig = px.pie(values=gender_counts.values, names=gender_counts.index,
                     color_discrete_sequence=['#FF6B6B', '#4ECDC4'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Age Distribution")
        fig = px.histogram(df, x='age', nbins=20, 
                          labels={'age': 'Age', 'count': 'Number of Patients'})
        fig.update_traces(marker_color='#95E1D3')
        st.plotly_chart(fig, use_container_width=True)
    
    # Monthly Patient Trend
    st.subheader("Monthly Patient Trend")
    monthly_data = df.groupby(df['appointment_date'].apply(lambda x: x.strftime('%Y-%m'))).size().reset_index()
    monthly_data.columns = ['Month', 'Patients']
    fig = px.line(monthly_data, x='Month', y='Patients', markers=True)
    fig.update_traces(line_color='#F38181', line_width=3)
    st.plotly_chart(fig, use_container_width=True)

# ==================== DOCTOR ANALYTICS PAGE ====================
elif menu == "👨‍⚕️ Doctor Analytics":
    st.header("👨‍⚕️ Doctor Performance Analytics")
    
    # Doctor-wise patient count
    doctor_stats = df.groupby('doctor_name').agg({
        'patient_id': 'count',
        'total_billing': 'sum',
        'consultation_fee': 'mean',
        'department': 'first',
        'doctor_experience': 'first'
    }).reset_index()
    doctor_stats.columns = ['Doctor', 'Patients', 'Total Revenue', 'Avg Consultation Fee', 'Department', 'Experience']
    doctor_stats = doctor_stats.sort_values('Patients', ascending=False)
    
    # Top Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        top_doctor = doctor_stats.iloc[0]
        st.metric("Top Doctor by Patients", top_doctor['Doctor'], f"{int(top_doctor['Patients'])} patients")
    with col2:
        top_revenue_doctor = doctor_stats.sort_values('Total Revenue', ascending=False).iloc[0]
        st.metric("Top Doctor by Revenue", top_revenue_doctor['Doctor'], f"₹{top_revenue_doctor['Total Revenue']:,.0f}")
    with col3:
        st.metric("Average Patients/Doctor", f"{doctor_stats['Patients'].mean():.1f}")
    
    st.markdown("---")
    
    # Doctor Performance Table
    st.subheader("📋 Doctor Performance Summary")
    st.dataframe(doctor_stats.style.format({
        'Patients': '{:.0f}',
        'Total Revenue': '₹{:,.0f}',
        'Avg Consultation Fee': '₹{:,.0f}',
        'Experience': '{:.0f} years'
    }), use_container_width=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Patients per Doctor")
        fig = px.bar(doctor_stats, x='Doctor', y='Patients', color='Department',
                     hover_data=['Experience', 'Total Revenue'])
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Revenue per Doctor")
        fig = px.bar(doctor_stats, x='Doctor', y='Total Revenue', color='Department')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Experience vs Performance
    st.subheader("Experience vs Patients Correlation")
    fig = px.scatter(doctor_stats, x='Experience', y='Patients', size='Total Revenue',
                     color='Department', hover_name='Doctor', size_max=60)
    st.plotly_chart(fig, use_container_width=True)
    
    # Time-wise analysis for selected doctor
    st.markdown("---")
    st.subheader("🕐 Time Slot Analysis by Doctor")
    selected_doctor = st.selectbox("Select Doctor", doctor_stats['Doctor'].tolist())
    
    doctor_time_data = df[df['doctor_name'] == selected_doctor]
    time_dist = doctor_time_data['appointment_time'].value_counts().sort_index()
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(x=time_dist.index, y=time_dist.values,
                     labels={'x': 'Time Slot', 'y': 'Number of Patients'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        day_dist = doctor_time_data['day_of_week'].value_counts()
        fig = px.pie(values=day_dist.values, names=day_dist.index, title="Day-wise Distribution")
        st.plotly_chart(fig, use_container_width=True)

# ==================== DEPARTMENT ANALYTICS PAGE ====================
elif menu == "🩺 Department Analytics":
    st.header("🩺 Department Analytics")
    
    dept_stats = df.groupby('department').agg({
        'patient_id': 'count',
        'total_billing': 'sum',
        'consultation_fee': 'mean',
        'lab_cost': 'sum',
        'num_lab_tests': 'mean'
    }).reset_index()
    dept_stats.columns = ['Department', 'Patients', 'Total Revenue', 'Avg Consultation', 'Lab Revenue', 'Avg Lab Tests']
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Departments", len(dept_stats))
    with col2:
        top_dept = dept_stats.sort_values('Patients', ascending=False).iloc[0]
        st.metric("Busiest Department", top_dept['Department'])
    with col3:
        st.metric("Highest Revenue Dept", dept_stats.sort_values('Total Revenue', ascending=False).iloc[0]['Department'])
    with col4:
        st.metric("Avg Patients/Dept", f"{dept_stats['Patients'].mean():.1f}")
    
    st.markdown("---")
    
    # Department Stats Table
    st.subheader("📊 Department Performance Summary")
    st.dataframe(dept_stats.style.format({
        'Patients': '{:.0f}',
        'Total Revenue': '₹{:,.0f}',
        'Avg Consultation': '₹{:,.0f}',
        'Lab Revenue': '₹{:,.0f}',
        'Avg Lab Tests': '{:.2f}'
    }), use_container_width=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Patient Distribution by Department")
        fig = px.pie(dept_stats, values='Patients', names='Department', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Revenue by Department")
        fig = px.bar(dept_stats, x='Department', y='Total Revenue', color='Department')
        fig.update_layout(xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Symptoms Analysis
    st.markdown("---")
    st.subheader("🩺 Symptom Analysis by Department")
    selected_dept = st.selectbox("Select Department", df['department'].unique())
    
    dept_data = df[df['department'] == selected_dept]
    
    # Flatten symptoms
    all_symptoms = []
    for symptoms in dept_data['symptoms']:
        all_symptoms.extend([s.strip() for s in symptoms.split(',')])
    
    symptom_counts = pd.Series(all_symptoms).value_counts()
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(x=symptom_counts.index[:10], y=symptom_counts.values[:10],
                     labels={'x': 'Symptom', 'y': 'Frequency'},
                     title=f"Top 10 Symptoms in {selected_dept}")
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric("Total Patients", len(dept_data))
        st.metric("Avg Age", f"{dept_data['age'].mean():.1f} years")
        st.metric("Total Revenue", f"₹{dept_data['total_billing'].sum():,.0f}")

# ==================== REVENUE ANALYTICS PAGE ====================
elif menu == "💰 Revenue Analytics":
    st.header("💰 Revenue Analytics")
    
    # Date filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", df['appointment_date'].min())
    with col2:
        end_date = st.date_input("End Date", df['appointment_date'].max())
    
    filtered_df = df[(df['appointment_date'] >= start_date) & (df['appointment_date'] <= end_date)]
    
    # Revenue Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Revenue", f"₹{filtered_df['total_billing'].sum():,.0f}")
    with col2:
        st.metric("Consultation Revenue", f"₹{filtered_df['consultation_fee'].sum():,.0f}")
    with col3:
        st.metric("Lab Revenue", f"₹{filtered_df['lab_cost'].sum():,.0f}")
    with col4:
        st.metric("Avg Revenue/Patient", f"₹{filtered_df['total_billing'].mean():,.0f}")
    
    st.markdown("---")
    
    # Revenue Breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue Composition")
        revenue_comp = pd.DataFrame({
            'Type': ['Consultation Fees', 'Lab Tests'],
            'Amount': [filtered_df['consultation_fee'].sum(), filtered_df['lab_cost'].sum()]
        })
        fig = px.pie(revenue_comp, values='Amount', names='Type', 
                     color_discrete_sequence=['#FF6B6B', '#4ECDC4'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Revenue by Department")
        dept_revenue = filtered_df.groupby('department')['total_billing'].sum().sort_values(ascending=True)
        fig = px.bar(x=dept_revenue.values, y=dept_revenue.index, orientation='h',
                     labels={'x': 'Revenue (₹)', 'y': 'Department'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Time-based Revenue Analysis
    st.subheader("📅 Revenue Trends")
    
    period = st.radio("Select Period", ["Daily", "Weekly", "Monthly", "Quarterly"], horizontal=True)
    
    if period == "Daily":
        time_revenue = filtered_df.groupby('appointment_date')['total_billing'].sum().reset_index()
        time_revenue.columns = ['Date', 'Revenue']
        fig = px.line(time_revenue, x='Date', y='Revenue', markers=True)
    elif period == "Weekly":
        filtered_df['week'] = pd.to_datetime(filtered_df['appointment_date']).dt.isocalendar().week
        time_revenue = filtered_df.groupby('week')['total_billing'].sum().reset_index()
        time_revenue.columns = ['Week', 'Revenue']
        fig = px.bar(time_revenue, x='Week', y='Revenue')
    elif period == "Monthly":
        time_revenue = filtered_df.groupby('month')['total_billing'].sum().reset_index()
        time_revenue.columns = ['Month', 'Revenue']
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December']
        time_revenue['Month'] = pd.Categorical(time_revenue['Month'], categories=month_order, ordered=True)
        time_revenue = time_revenue.sort_values('Month')
        fig = px.bar(time_revenue, x='Month', y='Revenue', color='Revenue')
    else:  # Quarterly
        time_revenue = filtered_df.groupby('quarter')['total_billing'].sum().reset_index()
        time_revenue.columns = ['Quarter', 'Revenue']
        fig = px.bar(time_revenue, x='Quarter', y='Revenue', color='Revenue')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Doctor-wise Revenue
    st.subheader("👨‍⚕️ Revenue by Doctor")
    doctor_revenue = filtered_df.groupby(['doctor_name', 'department'])['total_billing'].sum().reset_index()
    doctor_revenue = doctor_revenue.sort_values('total_billing', ascending=False).head(10)
    
    fig = px.bar(doctor_revenue, x='doctor_name', y='total_billing', color='department',
                 labels={'doctor_name': 'Doctor', 'total_billing': 'Revenue (₹)'})
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# ==================== TREND ANALYSIS PAGE ====================
elif menu == "📈 Trend Analysis":
    st.header("📈 Trend Analysis")
    
    # Patient Growth Trend
    st.subheader("Patient Volume Trend")
    monthly_patients = df.groupby(df['appointment_date'].apply(lambda x: x.strftime('%Y-%m'))).size().reset_index()
    monthly_patients.columns = ['Month', 'Patients']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly_patients['Month'], y=monthly_patients['Patients'],
                            mode='lines+markers', name='Patients',
                            line=dict(color='#FF6B6B', width=3)))
    fig.update_layout(title='Monthly Patient Trend', xaxis_title='Month', yaxis_title='Number of Patients')
    st.plotly_chart(fig, use_container_width=True)
    
    # Multi-metric comparison
    st.subheader("Multi-Metric Monthly Comparison")
    monthly_metrics = df.groupby(df['appointment_date'].apply(lambda x: x.strftime('%Y-%m'))).agg({
        'patient_id': 'count',
        'total_billing': 'sum',
        'consultation_fee': 'mean',
        'num_lab_tests': 'mean'
    }).reset_index()
    monthly_metrics.columns = ['Month', 'Patients', 'Revenue', 'Avg Consultation', 'Avg Lab Tests']
    
    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=('Patients', 'Revenue', 'Avg Consultation Fee', 'Avg Lab Tests'))
    
    fig.add_trace(go.Bar(x=monthly_metrics['Month'], y=monthly_metrics['Patients'], name='Patients'),
                  row=1, col=1)
    fig.add_trace(go.Bar(x=monthly_metrics['Month'], y=monthly_metrics['Revenue'], name='Revenue'),
                  row=1, col=2)
    fig.add_trace(go.Scatter(x=monthly_metrics['Month'], y=monthly_metrics['Avg Consultation'], 
                            mode='lines+markers', name='Avg Consultation'),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=monthly_metrics['Month'], y=monthly_metrics['Avg Lab Tests'], 
                            mode='lines+markers', name='Avg Lab Tests'),
                  row=2, col=2)
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Day of Week Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Busiest Days of Week")
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_counts = df['day_of_week'].value_counts().reindex(day_order)
        fig = px.bar(x=day_counts.index, y=day_counts.values,
                     labels={'x': 'Day', 'y': 'Patients'},
                     color=day_counts.values, color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Peak Time Slots")
        time_counts = df['appointment_time'].value_counts()
        fig = px.bar(x=time_counts.index, y=time_counts.values,
                     labels={'x': 'Time Slot', 'y': 'Patients'},
                     color=time_counts.values, color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
    
    # Correlation Analysis
    st.subheader("Correlation Heatmap")
    corr_data = df[['age', 'num_symptoms', 'num_lab_tests', 'consultation_fee', 'lab_cost', 'total_billing', 'doctor_experience']]
    corr_matrix = corr_data.corr()
    
    fig = px.imshow(corr_matrix, text_auto='.2f', aspect='auto',
                    color_continuous_scale='RdBu_r')
    st.plotly_chart(fig, use_container_width=True)

# ==================== PATIENT DETAILS PAGE ====================
elif menu == "📋 Patient Details":
    st.header("📋 Patient Records")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        dept_filter = st.multiselect("Filter by Department", 
                                     options=['All'] + list(df['department'].unique()),
                                     default=['All'])
    with col2:
        gender_filter = st.multiselect("Filter by Gender",
                                      options=['All'] + list(df['gender'].unique()),
                                      default=['All'])
    with col3:
        patient_type_filter = st.multiselect("Filter by Patient Type",
                                            options=['All'] + list(df['patient_type'].unique()),
                                            default=['All'])
    
    # Apply filters
    filtered_df = df.copy()
    if 'All' not in dept_filter and dept_filter:
        filtered_df = filtered_df[filtered_df['department'].isin(dept_filter)]
    if 'All' not in gender_filter and gender_filter:
        filtered_df = filtered_df[filtered_df['gender'].isin(gender_filter)]
    if 'All' not in patient_type_filter and patient_type_filter:
        filtered_df = filtered_df[filtered_df['patient_type'].isin(patient_type_filter)]
    
    st.info(f"Showing {len(filtered_df)} of {len(df)} patients")
    
    # Display data
    display_df = filtered_df[[
        'patient_id', 'name', 'age', 'gender', 'department', 'doctor_name',
        'appointment_date', 'appointment_time', 'symptoms', 'lab_tests',
        'consultation_fee', 'lab_cost', 'total_billing'
    ]].copy()
    
    st.dataframe(display_df.style.format({
        'consultation_fee': '₹{:,.0f}',
        'lab_cost': '₹{:,.0f}',
        'total_billing': '₹{:,.0f}'
    }), use_container_width=True)
    
    # Download option
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Patient Data (CSV)",
        data=csv,
        file_name=f"patient_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
    # Search functionality
    st.markdown("---")
    st.subheader("🔍 Search Patient")
    search_term = st.text_input("Search by Patient ID, Name, or Mobile")
    
    if search_term:
        search_results = filtered_df[
            (filtered_df['patient_id'].str.contains(search_term, case=False)) |
            (filtered_df['name'].str.contains(search_term, case=False)) |
            (filtered_df['mobile'].str.contains(search_term, case=False))
        ]
        
        if len(search_results) > 0:
            st.success(f"Found {len(search_results)} matching patient(s)")
            for idx, row in search_results.iterrows():
                with st.expander(f"👤 {row['name']} - {row['patient_id']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Age:** {row['age']} years")
                        st.write(f"**Gender:** {row['gender']}")
                        st.write(f"**Blood Group:** {row['blood_group']}")
                        st.write(f"**Mobile:** {row['mobile']}")
                        st.write(f"**Email:** {row['email']}")
                    with col2:
                        st.write(f"**Department:** {row['department']}")
                        st.write(f"**Doctor:** {row['doctor_name']}")
                        st.write(f"**Date:** {row['appointment_date']}")
                        st.write(f"**Time:** {row['appointment_time']}")
                        st.write(f"**Room:** {row['doctor_room']}")
                    
                    st.write(f"**Symptoms:** {row['symptoms']}")
                    st.write(f"**Lab Tests:** {row['lab_tests']}")
                    st.markdown(f"**Total Billing:** ₹{row['total_billing']:,.2f}")
        else:
            st.warning("No patients found matching your search")
