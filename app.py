# app.py
from __future__ import annotations

import base64
import hmac
import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

from data import AGENDA, EVENT_META, FAQS

logger = logging.getLogger(__name__)

CENTRAL_TIME = ZoneInfo("America/Chicago")
GOOGLE_SHEETS_SCOPE = "https://www.googleapis.com/auth/spreadsheets"
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

RSVP_HEADERS = [
    "Submitted At",
    "Full Name",
    "Department",
    "Dietary Restrictions",
    "Additional Comments",
    "Work Email",
    "Kickoff Question",
]

FORM_STATE_KEYS = [
    "rsvp_name",
    "rsvp_email",
    "rsvp_department",
    "rsvp_dietary",
    "rsvp_notes",
    "rsvp_question",
]


class AppConfigurationError(RuntimeError):
    """Raised when a required deployment setting is missing or malformed."""


st.set_page_config(
    page_title="FY27 Corporate Kickoff",
    page_icon="🚀",
    layout="centered",
)


def get_setting(name: str) -> object:
    try:
        value = st.secrets[name]
    except Exception:
        value = os.getenv(name.upper())

    if value is None or value == "":
        raise AppConfigurationError(f"Missing required setting: {name}")
    return value


def get_sheet() -> gspread.Worksheet:
    raw_credentials = get_setting("google_credentials")
    sheet_id = str(get_setting("google_sheet_id"))

    try:
        credentials_info = (
            json.loads(raw_credentials)
            if isinstance(raw_credentials, str)
            else dict(raw_credentials)
        )
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise AppConfigurationError("google_credentials is not valid JSON") from exc

    credentials = Credentials.from_service_account_info(
        credentials_info,
        scopes=[GOOGLE_SHEETS_SCOPE],
    )
    return gspread.authorize(credentials).open_by_key(sheet_id).sheet1


def ensure_rsvp_headers(sheet: gspread.Worksheet) -> list[str]:
    headers = [header.strip() for header in sheet.row_values(1)]

    if not headers:
        sheet.append_row(RSVP_HEADERS)
        return RSVP_HEADERS.copy()

    updated_headers = headers.copy()
    for required_header in RSVP_HEADERS:
        if required_header not in updated_headers:
            updated_headers.append(required_header)

    if updated_headers != headers:
        sheet.update(values=[updated_headers], range_name="A1")

    return updated_headers


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.fullmatch(email))


def clear_rsvp_form_if_requested() -> None:
    if st.session_state.pop("_clear_rsvp_form", False):
        for key in FORM_STATE_KEYS:
            st.session_state.pop(key, None)


def render_admin_login() -> bool:
    if st.session_state.get("admin_authenticated", False):
        return True

    try:
        expected_password = str(get_setting("admin_password"))
    except AppConfigurationError:
        st.info("Admin access has not been configured for this deployment.")
        return False

    password = st.text_input(
        "Admin password",
        type="password",
        key="admin_password_entry",
    )

    if st.button("Unlock Admin Tracker", type="primary"):
        if hmac.compare_digest(password, expected_password):
            st.session_state["admin_authenticated"] = True
            st.session_state.pop("admin_password_entry", None)
            st.rerun()
        else:
            st.error("The password was not recognized.")

    return False


st.markdown(
    """
    <style>
        div.stButton > button:first-child {
            background-color: #006E43 !important;
            color: white !important;
            border-radius: 6px !important;
            border: none !important;
            min-height: 45px !important;
        }
        .footer-text {
            color: #64748b;
            font-size: 12px;
            line-height: 1.5;
            margin: 2px 0;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if Path("logo.png").exists():
    st.image("logo.png", use_container_width=True)

st.title(EVENT_META["title"])
st.subheader(f"🗓️ {EVENT_META['date']}")
st.caption(f"📍 {EVENT_META['venue']} | ⏰ {EVENT_META['hours']}")
st.divider()

tab_agenda, tab_faqs, tab_rsvp, tab_dashboard = st.tabs(
    ["📋 Agenda", "❓ FAQs & Info", "📝 Attendee Check-In", "🔒 Admin Tracker"]
)

with tab_agenda:
    st.header("Event Schedule")
    st.info(
        f"**👔 Dress Code:** {EVENT_META['dress_code']} | "
        f"**🍽️ Catering by:** {EVENT_META['catering']}"
    )
    for item in AGENDA:
        with st.expander(f"**{item['time']}** — {item['title']}"):
            st.write(item["desc"])

with tab_faqs:
    st.header("Frequently Asked Questions")
    for faq in FAQS:
        st.markdown(f"**Q: {faq['question']}**")
        st.write(faq["answer"])

    st.divider()
    st.subheader("🏨 Overnight Accommodations")
    st.markdown(
        "- 🏨 **[Home2 Suites by Hilton Milwaukee Downtown]"
        "(https://www.hilton.com/en/hotels/mkesuht-home2-suites-milwaukee-downtown/)**"
    )
    st.markdown(
        "- 🏨 **[Aloft Milwaukee Downtown]"
        "(https://www.marriott.com/en-us/hotels/mkeal-aloft-milwaukee-downtown/overview/)**"
    )
    st.markdown(
        "- 🏨 **[The Westin Milwaukee]"
        "(https://www.marriott.com/en-us/hotels/mkeiw-the-westin-milwaukee/overview/)**"
    )
    st.warning(
        "⚠️ **Parking:** On-site garage space is limited. Carpooling is highly encouraged!"
    )

with tab_rsvp:
    clear_rsvp_form_if_requested()

    success_message = st.session_state.pop("_rsvp_success_message", None)
    if success_message:
        st.success(success_message)

    st.header("Confirm Your Attendance Details")
    st.caption("Fields marked with * are required.")

    with st.form("rsvp_form", clear_on_submit=False):
        name = st.text_input("Full Name *", key="rsvp_name", max_chars=100)
        email = st.text_input("Work Email *", key="rsvp_email", max_chars=150)
        department = st.selectbox(
            "Department",
            [
                "HR",
                "Finance",
                "Marketing",
                "Sales",
                "Operations",
                "IT",
                "R&D",
                "Customer Service",
                "Procurement",
                "S&OP",
                "Manufacturing",
                "Other",
            ],
            key="rsvp_department",
        )
        dietary = st.multiselect(
            "Dietary Restrictions",
            [
                "Vegetarian",
                "Vegan",
                "Gluten-Free",
                "Nut Allergy",
                "Dairy-Free",
                "Other Allergy or Restriction",
            ],
            key="rsvp_dietary",
            help="Leave blank when there are no dietary restrictions.",
        )
        notes = st.text_area(
            "Additional comments",
            key="rsvp_notes",
            max_chars=500,
        )
        question = st.text_area(
            "Please list one question you would like to ask about Growth, Collaboration or Innovation (or anything else).",
            key="rsvp_question",
            max_chars=500,
            help="Optional. Your question will be shared with the event planning team.",
        )

        submitted = st.form_submit_button(
            "Submit Confirmation",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            clean_name = name.strip()
            clean_email = email.strip().casefold()
            clean_notes = notes.strip()
            clean_question = question.strip()

            if not clean_name:
                st.error("Please enter your full name.")
            elif not is_valid_email(clean_email):
                st.error("Please enter a valid work email address.")
            else:
                try:
                    sheet = get_sheet()
                    headers = ensure_rsvp_headers(sheet)
                    email_column = headers.index("Work Email") + 1
                    existing_emails = {
                        value.strip().casefold()
                        for value in sheet.col_values(email_column)[1:]
                        if value.strip()
                    }

                    if clean_email in existing_emails:
                        st.warning(
                            "A registration already exists for this work email address."
                        )
                    else:
                        row_by_header = {
                            "Submitted At": datetime.now(CENTRAL_TIME).strftime(
                                "%Y-%m-%d %I:%M:%S %p %Z"
                            ),
                            "Full Name": clean_name,
                            "Department": department,
                            "Dietary Restrictions": ", ".join(dietary)
                            if dietary
                            else "None",
                            "Additional Comments": clean_notes or "None",
                            "Work Email": clean_email,
                            "Kickoff Question": clean_question or "None",
                        }
                        sheet.append_row(
                            [row_by_header.get(header, "") for header in headers],
                            value_input_option="USER_ENTERED",
                        )
                        st.session_state["_rsvp_success_message"] = (
                            f"Thank you, {clean_name}! Your attendance details were saved."
                        )
                        st.session_state["_clear_rsvp_form"] = True
                        st.rerun()
                except AppConfigurationError:
                    logger.exception("RSVP configuration error")
                    st.error(
                        "The RSVP connection is not configured correctly. "
                        "Please contact the event planning team."
                    )
                except Exception:
                    logger.exception("RSVP submission failed")
                    st.error(
                        "We could not save your confirmation. "
                        "Please try again or contact the event planning team."
                    )

with tab_dashboard:
    st.header("Admin Tracker")
    st.caption("Authorized event planners only.")

    if render_admin_login():
        logout_column, _ = st.columns([1, 3])
        with logout_column:
            if st.button("Sign Out"):
                st.session_state["admin_authenticated"] = False
                st.rerun()

        st.subheader("Live Registration Data")
        if st.button("Load / Refresh Live RSVP Data", type="primary"):
            try:
                records = get_sheet().get_all_records()
                if records:
                    dataframe = pd.DataFrame(records)
                    st.metric("Total Attendees", len(dataframe))
                    st.dataframe(
                        dataframe,
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.info("No confirmations have been submitted yet.")
            except AppConfigurationError:
                logger.exception("Admin tracker configuration error")
                st.error(
                    "The RSVP connection is not configured correctly. "
                    "Please review the deployment secrets."
                )
            except Exception:
                logger.exception("Admin tracker load failed")
                st.error("The registration data could not be loaded. Please try again.")

st.divider()
footer_path = Path("footer.png")
if footer_path.exists():
    footer_data = footer_path.read_bytes()
    if not footer_data.startswith(b"\x89PNG\r\n\x1a\n"):
        try:
            footer_data = base64.b64decode(footer_data, validate=True)
        except (ValueError, base64.binascii.Error):
            logger.exception("Footer image data could not be decoded")
            footer_data = b""
    if footer_data:
        st.image(footer_data, use_container_width=True)

st.markdown(
    '<p class="footer-text">Central Specialty Pet supports a family of brands.</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="footer-text">FY27 Corporate Kickoff | Innovation & Collaboration | '
    'Discovery World, Milwaukee</p>',
    unsafe_allow_html=True,
)
