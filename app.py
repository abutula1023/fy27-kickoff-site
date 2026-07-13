# app.py
import streamlit as st
import pandas as pd
import os
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from data import EVENT_META, AGENDA, FAQS, DUE_DATES

# ---- GOOGLE SHEETS CONNECTION ----
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ZLDMKpkS36tRaXvLYdhgIdQ48_CvuS0xrbkrWiuTnYw/edit?gid=0#gid=0"

# ---- CORE CONFIGURATION ----
st.set_page_config(
    page_title="FY27 Corporate Kickoff",
    page_icon="🚀",
    layout="centered"
)

# Connect to Google securely using a TTL (Time-To-Live) cache
# This refreshes the connection every 30 minutes (1800 seconds), 
# preventing both the 60-minute Google token expiration AND server memory leaks!
@st.cache_resource(ttl=1800)
def get_google_client():
    creds_dict = json.loads(st.secrets["google_credentials"])
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return gspread.authorize(creds)

try:
    gc = get_google_client()
except Exception as e:
    st.error(f"Configuration Error: Could not connect to Google Sheets. Check your Secrets settings. ({e})")
    st.stop()

# ---- CSS / STYLING INJECTION ----
st.markdown("""
    <style>
        div.stButton > button:first-child {
            background-color: #006E43 !important;
            color: white !important;
            border-radius: 6px !important;
            border: none !important;
            height: 45px !important;
        }
        .fixed-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: white;
            border-top: 1px solid #006E43;
            padding-top: 5px;
            padding-bottom: 5px;
            z-index: 100;
            text-align: center;
        }
        .footer-text {
            color: #64748b;
            font-size: 12px;
            margin-top: 2px;
            margin-bottom: 2px;
        }
        [data-testid="stMain"] {
            padding-bottom: 180px;
        }
    </style>
""", unsafe_allow_html=True)

# ---- SITE HEADER ----
st.image("https://raw.githubusercontent.com/abutula1023/fy27-kickoff-site/main/logo.png", use_column_width=True)
st.title(EVENT_META["title"])
st.subheader(f"🗓️ {EVENT_META['date']}")
st.caption(f"📍 {EVENT_META['venue']} | ⏰ {EVENT_META['hours']}")
st.divider()

# ---- NAVIGATION TABS ----
tab_agenda, tab_faqs, tab_rsvp, tab_dashboard = st.tabs([
    "📋 Agenda", "❓ FAQs & Info", "📝 Attendee Check-In", "🔒 Admin Tracker"
])

# ---- TAB 1: AGENDA ----
with tab_agenda:
    st.header("Event Schedule")
    st.info(f"**👔 Dress Code:** {EVENT_META['dress_code']} | **🍽️ Catering by:** {EVENT_META['catering']}")
    for item in AGENDA:
        with st.expander(f"**{item['time']}** — {item['title']}"):
            st.write(item['desc'])

# ---- TAB 2: FAQS ----
with tab_faqs:
    st.header("Frequently Asked Questions")
    for faq in FAQS:
        st.markdown(f"**Q: {faq['question']}**")
        st.write(faq['answer'])
    st.divider()
    st.subheader("🏨 Overnight Accommodations")
    st.markdown("- 🏨 **[Home2 Suites by Hilton Milwaukee Downtown](https://www.hilton.com/en/hotels/mkesuht-home2-suites-milwaukee-downtown/)**")
    st.markdown("- 🏨 **[Aloft Milwaukee Downtown](https://www.marriott.com/en-us/hotels/mkeal-aloft-milwaukee-downtown/overview/)**")
    st.markdown("- 🏨 **[The Westin Milwaukee](https://www.marriott.com/en-us/hotels/mkeiw-the-westin-milwaukee/overview/)**")
    st.warning("⚠️ **Parking:** On-site garage limited to 100 spaces. Carpooling highly encouraged!")

# ---- TAB 3: RSVP ----
with tab_rsvp:
    st.header("Confirm Your Attendance Details")
    if "rsvp_success" in st.session_state:
        st.success(st.session_state["rsvp_success"])
        del st.session_state["rsvp_success"]
    
    name = st.text_input("Full Name *")
    dept = st.selectbox("Department", ["HR", "Finance", "Marketing", "Sales", "Operations", "IT", "R&D", "Customer Service", "Procurement", "S&OP", "Manufacturing", "Other"])
    diet = st.multiselect("Dietary Restrictions", ["None", "Vegetarian", "Vegan", "Gluten-Free", "Nut Allergy", "Dairy-Free"])
    notes = st.text_area("Additional comments:")
    
    if st.button("Submit Confirmation", type="primary", use_container_width=True):
        if not name:
            st.error("Name is a required field.")
        else:
            try:
                sheet = gc.open_by_url(SHEET_URL).sheet1
                if name.strip().lower() in [n.strip().lower() for n in sheet.col_values(2)]:
                    st.warning(f"Registration already exists for {name}.")
                else:
                    sheet.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, dept, ", ".join(diet) if diet else "None", notes if notes else "None"])
                    st.session_state["rsvp_success"] = f"Thank you, {name}!"
                    st.rerun()
            except Exception as e:
                st.error(f"Error submitting data: {e}")

# ---- TAB 4: ADMIN ----
with tab_dashboard:
    st.header("Internal Planning")
    st.table(pd.DataFrame(DUE_DATES))
    st.subheader("Live Registration Data")
    try:
        df = pd.DataFrame(gc.open_by_url(SHEET_URL).sheet1.get_all_records())
        st.dataframe(df, use_container_width=True)
        st.metric("Total Attendees", len(df))
    except Exception as e:
        st.error(f"Could not load data: {e}")

# ---- FOOTER ----
st.markdown('<div class="fixed-footer"><p class="footer-text">FY27 Corporate Kickoff | Innovation & Collaboration | Discovery World, Milwaukee</p></div>', unsafe_allow_html=True)
