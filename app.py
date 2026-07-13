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

# Connect to Google securely (FRESH connection every run, no caching to prevent dead network tunnels)
creds_dict = json.loads(st.secrets["google_credentials"])
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
gc = gspread.authorize(creds)

# ---- CSS / STYLING INJECTION ----
st.markdown("""
    <style>
        /* Primary buttons and components color configuration (#006E43) */
        div.stButton > button:first-child {
            background-color: #006E43 !important;
            color: white !important;
            border-radius: 6px !important;
            border: none !important;
            height: 45px !important;
        }

        /* Footer Container Styling */
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

        /* Spacing Tweak for Mobile Content so it doesn't get blocked by footer */
        [data-testid="stMain"] {
            padding-bottom: 180px;
        }
    </style>
""", unsafe_allow_html=True)


# ---- SITE HEADER (Main Logo) ----
st.image("https://raw.githubusercontent.com/abutula1023/fy27-kickoff-site/main/logo.png", use_column_width=True)

# Application Header UI
st.title(EVENT_META["title"])
st.subheader(f"🗓️ {EVENT_META['date']}")
st.caption(f"📍 {EVENT_META['venue']} | ⏰ {EVENT_META['hours']}")

st.divider()


# ---- NAVIGATION TABS ----
tab_agenda, tab_faqs, tab_rsvp, tab_dashboard = st.tabs([
    "📋 Agenda", "❓ FAQs & Info", "📝 Attendee Check-In", "🔒 Admin Tracker"
])


# ---- TAB 1: AGENDA & TIMELINE ----
with tab_agenda:
    st.header("Event Schedule")
    st.info(f"**👔 Dress Code:** {EVENT_META['dress_code']} | **🍽️ Catering by:** {EVENT_META['catering']}")
    st.write("Click on any schedule block below to view details.")
    
    for item in AGENDA:
        with st.expander(f"**{item['time']}** — {item['title']}"):
            st.write(item['desc'])


# ---- TAB 2: FAQS & LOGISTICS ----
with tab_faqs:
    st.header("Frequently Asked Questions")
    for faq in FAQS:
        st.markdown(f"**Q: {faq['question']}**")
        st.write(faq['answer'])
        st.write("")
        
    st.divider()
    
    # ACCOMMODATIONS TRACKER SECTION WITH NAVAN DIRECTION
    st.subheader("🏨 Overnight Accommodations")
    st.write("For team members traveling from out of town, recommended corporate lodging options are located close to Discovery World:")
    
    st.markdown("- 🏨 **[Home2 Suites by Hilton Milwaukee Downtown](https://www.hilton.com/en/hotels/mkesuht-home2-suites-milwaukee-downtown/)**")
    st.markdown("- 🏨 **[Aloft Milwaukee Downtown](https://www.marriott.com/en-us/hotels/mkeal-aloft-milwaukee-downtown/overview/)**")
    st.markdown("- 🏨 **[The Westin Milwaukee](https://www.marriott.com/en-us/hotels/mkeiw-the-westin-milwaukee/overview/)**")
    
    st.write("")
    st.info("✈️ **Travel Policy Note:** Please ensure you log into **Navan** to book your selected hotel room and complete your travel arrangements in accordance with company travel compliance guidelines.")
    
    st.write("")
    st.subheader("🚗 Parking Logistics")
    
    st.warning(
        f"{EVENT_META['parking']}\n\n"
        "⚠️ **Important Note:** On-site parking capacity at Discovery World is limited and there will not be enough individual stalls to accommodate everyone. "
        "**Carpooling is highly encouraged** for local team members driving in together to maximize available spaces."
    )


# ---- TAB 3: ATTENDEE RSVP ----
with tab_rsvp:
    st.header("Confirm Your Attendance Details")
    st.write("Please verify your details below for final seating and catering submittals.")
    
    # Session state message handler to survive the script rerun
    if "rsvp_success" in st.session_state:
        st.success(st.session_state["rsvp_success"])
        del st.session_state["rsvp_success"]
    
    # Standard Inputs (Bypassing the buggy st.form)
    name = st.text_input("Full Name *")
    
    dept = st.selectbox(
        "Department", 
        [
            "HR", "Finance", "Marketing", "Sales", "Operations", 
            "IT", "R&D", "Customer Service", "Procurement", 
            "S&OP", "Manufacturing", "Other"
        ]
    )
    
    diet = st.multiselect(
        "Dietary Restrictions / Allergies",
        ["None", "Vegetarian", "Vegan", "Gluten-Free", "Nut Allergy", "Dairy-Free"]
    )
    notes = st.text_area("Additional comments or concerns:")
    
    submit_rsvp = st.button("Submit Confirmation", type="primary", use_container_width=True)
    
    if submit_rsvp:
        if not name:
            st.error("Name is a required field.")
        else:
            diet_str = ", ".join(diet) if diet else "None"
            notes_str = notes if notes else "None"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            try:
                sheet = gc.open_by_url(SHEET_URL).sheet1
                existing_names = sheet.col_values(2)
                
                if name.strip().lower() in [n.strip().lower() for n in existing_names]:
                    st.warning(f"Hold on! It looks like we already have a registration on file for {name}.")
                else:
                    sheet.append_row([timestamp, name, dept, diet_str, notes_str])
                    st.session_state["rsvp_success"] = f"Thank you, {name}! Your check-in details have been logged."
                    st.rerun()
                    
            except Exception as e:
                st.error(f"An error occurred while communicating with Google Sheets: {e}")


# ---- TAB 4: PLANNING DASHBOARD (ADMIN) ----
with tab_dashboard:
    st.header("Internal Planning & Milestones")
    st.write("Track operations workflow and target timeline goals below.")
    
    df_dates = pd.DataFrame(DUE_DATES)
    st.table(df_dates)
    
    st.subheader("Live Registration Data (130 Guests Target)")
    
    try:
        sheet = gc.open_by_url(SHEET_URL).sheet1
        records = sheet.get_all_records()
        
        if records:
            df_reg = pd.DataFrame(records)
            st.dataframe(df_reg, use_container_width=True)
            st.metric(label="Total Confirmed Attendees", value=len(df_reg))
        else:
            st.info("No confirmations submitted yet. Test out the Attendee Check-In tab to populate data here live!")
            
    except Exception as e:
        st.error(f"Could not load data from Google Sheets. Error: {e}")


# ---- FIXED BRANDING FOOTER ----
st.markdown('<div class="fixed-footer">', unsafe_allow_html=True)

if os.path.exists("footer.png"):
    try:
        st.image("footer.png", width=650)
    except Exception:
        st.markdown('<p class="footer-text">Central Specialty Pet supports a family of brands.</p>', unsafe_allow_html=True)
else:
    st.markdown('<p class="footer-text">Central Specialty Pet supports a family of brands.</p>', unsafe_allow_html=True)

st.markdown('<p class="footer-text">FY27 Corporate Kickoff | Innovation & Collaboration | Discovery World, Milwaukee</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
