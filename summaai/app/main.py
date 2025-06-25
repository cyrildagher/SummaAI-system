import streamlit as st
from summaai.app.email_parser import EmailParser, generate_dummy_emails
from datetime import datetime

st.title('SummaAI – Smart Email Summarizer')
st.write('Welcome to SummaAI! This dashboard will display important email summaries and allow you to manage settings.')

# Sidebar toggle for dummy data
use_dummy_data = st.sidebar.checkbox('Use dummy email data (for demo/testing)', value=True)

# Initialize the email parser
parser = EmailParser()

# Streamlit button to fetch emails
if st.button('Fetch Emails'):
    with st.spinner('Fetching emails...'):
        try:
            if use_dummy_data:
                # Use dummy emails for demo/testing
                emails = generate_dummy_emails()
            else:
                # Use live Gmail/IMAP emails
                emails = parser.fetch_emails()
            if not emails:
                st.info('No emails found.')
            else:
                for idx, email_obj in enumerate(emails, 1):
                    with st.expander(f"Email #{idx}: {email_obj['subject']}"):
                        st.markdown(f"**Sender:** {email_obj['sender']}")
                        st.subheader(email_obj['subject'])
                        ts = email_obj['timestamp']
                        if isinstance(ts, datetime):
                            st.caption(f"Timestamp: {ts.strftime('%Y-%m-%d %H:%M:%S')}")
                        elif ts:
                            st.caption(f"Timestamp: {ts}")
                        else:
                            st.caption("Timestamp: Unknown")
                        st.text_area('Body', email_obj['body'], height=200)
        except Exception as e:
            st.error(f"Error fetching emails: {e}")

# Helpful Streamlit comments:
# - Use the sidebar to toggle between dummy and live email data.
# - Use the button above to fetch emails.
# - Each email is shown in an expandable section for easy browsing.
# - Sender, subject, timestamp, and body are displayed for each email.
# - Errors are shown if fetching fails (e.g., bad credentials or network issues). 