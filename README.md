# FY27 Corporate Kickoff Site

Streamlit site for the Central Specialty Pet FY27 Corporate Kickoff. The attendee-facing pages provide the event agenda, FAQs, accommodations, and RSVP form. RSVP records are stored in a restricted Google Sheet.

## Security and data handling

- Never commit `.streamlit/secrets.toml`, service-account credentials, passwords, RSVP exports, or employee information.
- The Admin Tracker requires a password stored in Streamlit Secrets.
- Internal planning deadlines and financial details are intentionally not stored in this public repository.
- The Google service account should receive access only to the RSVP spreadsheet it needs.
- Review the Streamlit Community Cloud sharing settings so the application is available only to the intended audience.

## Required Streamlit Secrets

Configure these values in the Streamlit Community Cloud app settings under **Secrets**:

```toml
google_sheet_id = "YOUR_GOOGLE_SHEET_ID"
admin_password = "USE_A_LONG_UNIQUE_PASSWORD"

google_credentials = """
{
  "type": "service_account",
  "project_id": "YOUR_PROJECT_ID",
  "private_key_id": "YOUR_PRIVATE_KEY_ID",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "YOUR_SERVICE_ACCOUNT@YOUR_PROJECT.iam.gserviceaccount.com",
  "client_id": "YOUR_CLIENT_ID",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "YOUR_CLIENT_CERT_URL"
}
"""
```

Share the RSVP Google Sheet with the service account's `client_email`. The app requests only the Google Sheets API scope.

The worksheet's first row is used as the header row. The app adds any missing headers from this set without moving existing columns:

- Submitted At
- Full Name
- Department
- Dietary Restrictions
- Additional Comments
- Work Email

Existing RSVP rows without an email remain unchanged. New duplicate checks use Work Email.

## Local development

1. Create a virtual environment.
2. Install the pinned dependencies.
3. Create `.streamlit/secrets.toml` using the template above.
4. Start Streamlit.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```

Codespaces also installs the requirements and starts the app on port 8501 without disabling Streamlit's CORS or XSRF protections.

## Keep-awake workflow

`.github/workflows/keep_awake.yml` opens the deployed application with Chromium every four hours. It validates that the expected event page rendered and uploads a short-lived screenshot only when the check fails. The workflow can also be started manually from the GitHub Actions page.
