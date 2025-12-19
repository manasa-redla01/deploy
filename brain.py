import streamlit as st
import random
import numpy as np
from PIL import Image
import os
import webbrowser

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "users" not in st.session_state:
    st.session_state.users = {}

if "otp" not in st.session_state:
    st.session_state.otp = None

if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False

# ---------- LOGIN PAGE ----------
def login_page():
    st.title("🩺 Brain Tumor Detection System")
    
    phone = st.text_input("Phone Number", placeholder="+91XXXXXXXXXX")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Send OTP"):
            if phone in st.session_state.users:
                st.session_state.otp = random.randint(100000, 999999)
                st.session_state.otp_sent = True
                st.success("OTP sent successfully!")
                st.info(f"🔑 OTP (for demo): {st.session_state.otp}")
            else:
                st.warning("👤 User not registered. Please register first.")
    
    if st.session_state.otp_sent:
        otp_input = st.text_input("Enter OTP", type="password")
        
        if st.button("Verify OTP"):
            if otp_input == str(st.session_state.otp):
                st.session_state.page = "symptoms"
                st.session_state.otp_sent = False
                st.success("✅ Login Successful!")
                st.rerun()
            else:
                st.error("❌ Incorrect OTP")
    
    with col2:
        if st.button("New User? Register"):
            st.session_state.page = "register"
            st.rerun()

# ---------- REGISTRATION PAGE ----------
def register_page():
    st.title("👤 User Registration")
    
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number", placeholder="+91XXXXXXXXXX")
    age = st.number_input("Age", min_value=1, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    if st.button("✅ Register"):
        if phone in st.session_state.users:
            st.error("❌ User already exists")
        elif not name or not phone:
            st.warning("⚠ Please fill all required fields")
        else:
            st.session_state.users[phone] = {
                "name": name,
                "age": age,
                "gender": gender
            }
            st.success("🎉 Registration Successful!")
            st.balloons()
            st.session_state.page = "login"
            st.rerun()
    
    if st.button("🔙 Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# ---------- SYMPTOMS PAGE ----------
def symptoms_page():
    st.title("🧠 Brain Tumor Symptom Assessment")
    
    st.markdown("*Select all symptoms you are experiencing:*")
    
    col1, col2 = st.columns(2)
    with col1:
        headache = st.checkbox("🤕 Frequent Headache (especially mornings)")
        vision = st.checkbox("👁 Blurred / Double Vision")
        memory = st.checkbox("🧠 Memory Loss or Confusion")
    
    with col2:
        nausea = st.checkbox("🤮 Nausea or Vomiting")
        speech = st.checkbox("🗣 Speech Difficulty")
        balance = st.checkbox("⚖ Loss of Balance")
        seizures = st.checkbox("⚡ Seizures")
    
    if st.button("📊 Analyze Symptoms"):
        score = sum([headache, vision, memory, nausea, speech, balance, seizures])
        
        st.markdown("*Risk Assessment:*")
        if score <= 1:
            st.success("✅ *Low Risk* – Continue monitoring symptoms")
        elif score <= 3:
            st.warning("⚠ *Moderate Risk* – Consult a doctor soon")
        else:
            st.error("🚨 *High Risk* – Seek immediate medical attention")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 Next: MRI Analysis"):
            st.session_state.page = "mri"
            st.rerun()
    with col2:
        if st.button("🔙 Back to Login"):
            st.session_state.page = "login"
            st.session_state.otp = None
            st.session_state.otp_sent = False
            st.rerun()

# ---------- MRI PAGE ----------
def mri_page():
    st.title("🖼 MRI Scan Analysis")
    st.markdown("Upload an MRI image for AI analysis")
    
    uploaded_file = st.file_uploader("Choose MRI image...", type=['png', 'jpg', 'jpeg'])
    #<a href="https://www.google.com">open CROME</a>
    webbrowser.open("https://www.google.com")
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded MRI', use_column_width=True)
        
        # Demo prediction (replace with actual model later)
        if st.button("🔍 Analyze MRI"):
            with st.spinner("Analyzing MRI scan..."):
                # Simulated prediction for demo
                confidence = random.uniform(0.1, 0.9)
                if confidence > 0.5:
                    result = "🧠 *TUMOR DETECTED*"
                    prob = f"{confidence:.1%}"
                    st.error(result)
                else:
                    result = "✅ *No Tumor Detected*"
                    prob = f"{(1-confidence):.1%}"
                    st.success(result)
                
                col1, col2 = st.columns(2)
                col1.metric("Confidence", prob)
                col2.metric("Status", "Complete")
        
        st.info("⚠ This is for educational purposes. Always consult a doctor for medical diagnosis.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 Back to Symptoms"):
            st.session_state.page = "symptoms"
            st.rerun()
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.page = "login"
            st.session_state.otp = None
            st.session_state.otp_sent = False
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# ---------- ROUTER ----------
st.set_page_config(page_title="Brain Tumor Detection", page_icon="🧠", layout="wide")

if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "register":
    register_page()
elif st.session_state.page == "symptoms":
    symptoms_page()
elif st.session_state.page == "mri":
    mri_page()