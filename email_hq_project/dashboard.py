import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime
import subprocess
import base64
import uuid

# === Load .env === #
load_dotenv()

EMAIL_ACCOUNTS = [
    {"label": "Team", "email": os.getenv("EMAIL_1"), "password": os.getenv("PASS_1")},
    {"label": "Press", "email": os.getenv("EMAIL_2"), "password": os.getenv("PASS_2")},
    {"label": "Info", "email": os.getenv("EMAIL_3"), "password": os.getenv("PASS_3")},
    {"label": "Donate", "email": os.getenv("EMAIL_4"), "password": os.getenv("PASS_4")}
]

# === Set up Streamlit page === #
st.set_page_config(page_title="Arthur Dixon War Room", layout="wide")

# === Style === #
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            background-color: #0d1117;
            color: #f5f7fa;
            font-family: 'Segoe UI', sans-serif;
        }
        .navbar {
            position: sticky;
            top: 0;
            z-index: 1000;
            background-color: #10172a;
            padding: 1rem 2rem;
            border-bottom: 1px solid #2f3b52;
            display: flex;
            justify-content: space-between;
        }
        .navbar a {
            margin-right: 1.5rem;
            color: #38bdf8;
            text-decoration: none;
            font-weight: 600;
        }
        .hero {
            background-image: url('https://arthurdixonforcongress.com/banner.jpg');
            background-size: cover;
            background-position: center;
            padding: 6rem 2rem;
            text-align: center;
        }
        .hero h1 {
            font-size: 3rem;
            background: linear-gradient(90deg, #16a34a, #4ade80);
            -webkit-background-clip: text;
            background-clip: text; /* ← Add this line */
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px #00000020;
        }
        .hero p {
            font-size: 1.25rem;
            color: #f0f9ff;
            font-weight: 500;
            text-shadow: 1px 1px #000;
        }
        .glow-box {
            background: linear-gradient(145deg, #1e293b, #0f172a);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(56,189,248,0.2);
        }
        .data-box {
            padding: 1.5rem;
            background: #111827;
            border-radius: 12px;
            color: #f0f0f0;
            text-align: center;
            box-shadow: 0 0 10px rgba(255,255,255,0.05);
        }
    </style>
""", unsafe_allow_html=True)

# === Hero Section === #
st.markdown("""
<div class="hero">
    <h1>Arthur Dixon for Congress</h1>
    <p>Bold Progressive Change Starts Here: The Digital War Room for CA-34</p>
    <p style="
        background: linear-gradient(90deg, #4ade80, #16a34a);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        color: transparent;
        font-weight: 500;
        text-shadow: 1px 1px #00000020;
    ">
        Bold Progressive Change Starts Here: The Digital War Room for CA-34
    </p>
    
</div>
""", unsafe_allow_html=True)

# === Tabs === #
tabs = st.tabs(["Home", "📨 Email Ops", "📞 Calls", "💬 Texts", "📁 Contact Lists", "📊 Logs", "🧠 Strategy Notes"])

# === HOME === #
with tabs[0]:
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown("""<div class='data-box'><h3>📬 Emails Sent</h3><h2>1,447</h2></div>""", unsafe_allow_html=True)
    col2.markdown("""<div class='data-box'><h3>🔥 Open Rate</h3><h2>44.1%</h2></div>""", unsafe_allow_html=True)
    col3.markdown("""<div class='data-box'><h3>💸 Donations</h3><h2>$5,760</h2></div>""", unsafe_allow_html=True)
    col4.markdown("""<div class='data-box'><h3>📉 Bounce Rate</h3><h2>0.7%</h2></div>""", unsafe_allow_html=True)

# === EMAIL OPS === #
with tabs[1]:
    st.subheader("📨 Compose & Send Campaign Email")
    sender_labels = [f"{acc['label']} – {acc['email']}" for acc in EMAIL_ACCOUNTS if acc['email']]
    sender_option = st.selectbox("Choose sender email:", sender_labels)
    selected_account = next((acc for acc in EMAIL_ACCOUNTS if acc['email'] and acc['email'] in sender_option), EMAIL_ACCOUNTS[0])

    uploaded_file = st.file_uploader("Upload Contact CSV", type="csv")
    subject = st.text_input("Email Subject", "🔥 Arthur Dixon Is Rising — Join the Movement")
    preheader = st.text_input("Email Preheader", "CA-34’s future starts now. This is your invitation.")
    image = st.file_uploader("Optional: Upload inline image (JPG/PNG)", type=["jpg", "jpeg", "png"])

    html_body = st.text_area("HTML Email Body", height=240, value="""
<p>Dear {name},</p>
<p>Arthur Dixon is rising. A candidate born from struggle, built for battle, and leading the charge for justice in Los Angeles.</p>
<p><a href='https://arthurdixonforcongress.com'>Join the movement →</a></p>
<p>– Arthur Dixon</p>
""")

    plain_body = st.text_area("Plain Text Backup", height=180, value="""
Dear {name},
Arthur Dixon is rising. Join the movement: https://arthurdixonforcongress.com
– Arthur Dixon
""")

    if st.button("🚀 Send Emails"):
        if uploaded_file:
            with open("contacts.csv", "wb") as f:
                f.write(uploaded_file.getbuffer())
            subprocess.Popen(["python3", "email_sender.py"])
            st.success("📤 Emails queued for sending. Check email_log.txt soon.")
        else:
            st.error("Please upload a contact file.")

# === CALL OPS === #
with tabs[2]:
    st.subheader("📞 Call Tracking")
    call_count = st.number_input("Calls Made Today", min_value=0, value=14)
    total_calls = st.number_input("Total Calls to Date", min_value=0, value=103)
    call_donations = st.number_input("Donations from Calls", min_value=0, value=5)
    call_signups = st.number_input("Volunteers from Calls", min_value=0, value=3)
    st.info("Phase 2.2 will include autodial, call logging, recording, and live analytics.")

# === TEXT OPS === #
with tabs[3]:
    st.subheader("💬 SMS Tracking")
    sms_today = st.number_input("Texts Sent Today", min_value=0, value=32)
    sms_replies = st.number_input("Replies Received", min_value=0, value=14)
    sms_donations = st.number_input("Donations from SMS", min_value=0, value=2)
    sms_rsvp = st.number_input("Event RSVPs", min_value=0, value=1)
    st.info("Phase 2.2 will add Twilio Broadcast, Inbox View, and Message Templates")

# === CONTACT LISTS === #
with tabs[4]:
    st.subheader("📁 Manage Contact Lists")
    if st.button("📤 Upload New Contact List"):
        contact_list_file = st.file_uploader("Choose CSV", type="csv")
        if contact_list_file:
            name = st.text_input("Name this list (e.g. David Kim Donors)")
            if name:
                path = f"contacts/{name}.csv"
                with open(path, "wb") as f:
                    f.write(contact_list_file.getbuffer())
                st.success(f"Uploaded and saved as {path}")
    else:
        lists = os.listdir("contacts") if os.path.exists("contacts") else []
        st.write("Available Lists:", lists)
        if lists:
            chosen_list = st.selectbox("View List:", lists)
            df = pd.read_csv(f"contacts/{chosen_list}")
            st.dataframe(df)

# === LOGS === #
with tabs[5]: 
    st.subheader("📊 Dispatch Logs")
    if os.path.exists("email_log.txt"):
        with open("email_log.txt", "r") as log:
            st.text_area("📬 Email Log", value=log.read(), height=300)
    if os.path.exists("call_sms_log.txt"):
        with open("call_sms_log.txt", "r") as log:
            st.text_area("📞 Call/SMS Log", value=log.read(), height=300)

# === NOTES === #
with tabs[6]:
    st.subheader("🧠 Campaign Notes & Strategy")
    notes = st.text_area("Brain dump, to-dos, scripts, ideas", height=400)
    st.button("💾 Save Notes (Coming Soon)")
