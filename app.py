# app.py
import streamlit as st
import pandas as pd
import os
from data import EVENT_META, AGENDA, FAQS, DUE_DATES

# ---- CORE CONFIGURATION ----
st.set_page_config(
    page_title="FY27 Corporate Kickoff",
    page_icon="🚀",
    layout="centered"
)

# ---- CSS / STYLING INJECTION ----
st.markdown("""
    <style>
        /* Primary buttons and components color configuration (#006E43) */
        div.stButton > button:first-child {
            background-color: #006E43 !important;
            color: white !important;
            border-radius: 6px !important;
            border: none !important;
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
# Switched to an unrestricted web delivery node to bypass corporate hotlink blocking policies
st.image("https://i.imgur.com/K7M6fO0.png", width=350)

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
    
    # Specific updated link targets
    st.markdown("- 🏨 **[Home2 Suites by Hilton Milwaukee Downtown](https://www.hilton.com/en/hotels/mkesuht-home2-suites-milwaukee-downtown/)**")
    st.markdown("- 🏨 **[Aloft Milwaukee Downtown](https://www.marriott.com/en-us/hotels/mkeal-aloft-milwaukee-downtown/overview/)**")
    st.markdown("- 🏨 **[The Westin Milwaukee](https://www.marriott.com/en-us/hotels/mkeiw-the-westin-milwaukee/overview/)**")
    
    st.write("")
    st.info("✈️ **Travel Policy Note:** Please ensure you log into **Navan** to book your selected hotel room and complete your travel arrangements in accordance with company travel compliance guidelines.")
    
    st.write("")
    st.subheader("🚗 Parking Logistics")
    
    # UPDATED PARKING WARNING TO ENCOURAGE CARPOOLING
    st.warning(
        f"{EVENT_META['parking']}\n\n"
        "⚠️ **Important Note:** On-site parking capacity at Discovery World is limited and there will not be enough individual stalls to accommodate everyone. "
        "**Carpooling is highly encouraged** for local team members driving in together to maximize available spaces."
    )


# ---- TAB 3: ATTENDEE RSVP ----
with tab_rsvp:
    st.header("Confirm Your Attendance Details")
    st.write("Please verify your details below for final seating and catering submittals.")
    
    with st.form("rsvp_form", clear_on_submit=True):
        name = st.text_input("Full Name *")
        
        # UPDATED DEPARTMENT LIST
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
        
        # Complete form button setup
        submitted = st.form_submit_button("Submit Confirmation")
        
        if submitted:
            if not name:
                st.error("Name is a required field.")
            else:
                # Save input data directly to local operational file system
                csv_file = "registrations.csv"
                new_data = pd.DataFrame([{
                    "Name": name, "Department": dept, "Dietary": ", ".join(diet), "Notes": notes
                }])
                
                if not os.path.isfile(csv_file):
                    new_data.to_csv(csv_file, index=False)
                else:
                    new_data.to_csv(csv_file, mode='a', header=False, index=False)
                    
                st.success(f"Thank you, {name}! Your check-in details have been logged.")


# ---- TAB 4: PLANNING DASHBOARD (ADMIN) ----
with tab_dashboard:
    st.header("Internal Planning & Milestones")
    st.write("Track operations workflow and target timeline goals below.")
    
    # Render Milestone Table
    df_dates = pd.DataFrame(DUE_DATES)
    st.table(df_dates)
    
    # Interactive CSV reader to view live RSVPs
    st.subheader("Live Registration Data (130 Guests Target)")
    if os.path.isfile("registrations.csv"):
        df_reg = pd.read_csv("registrations.csv")
        st.dataframe(df_reg)
        st.metric(label="Total Confirmed Attendees", value=len(df_reg))
    else:
        st.info("No confirmations submitted yet. Test out the Attendee Check-In tab to populate data here live!")


# ---- FIXED BRANDING FOOTER ----
st.markdown('<div class="fixed-footer">', unsafe_allow_html=True)

# Wrapped in try/except to prevent footer data stream corruption from crashing layout
if os.path.exists("footer.png"):
    try:
        st.image("footer.png", width=650)
    except Exception:
        st.markdown('<p class="footer-text">Central Specialty Pet supports a family of brands.</p>', unsafe_allow_html=True)
else:
    st.markdown('<p class="footer-text">Central Specialty Pet supports a family of brands.</p>', unsafe_allow_html=True)

st.markdown('<p class="footer-text">FY27 Corporate Kickoff | Innovation & Collaboration | Discovery World, Milwaukee</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
