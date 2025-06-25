import streamlit as st
from summaai.app.email_parser import EmailParser
from datetime import datetime

st.title('SummaAI – Smart Email Summarizer')
st.write('Welcome to SummaAI! This dashboard will display important email summaries and allow you to manage settings.')

# Initialize the email parser
parser = EmailParser()

# Streamlit button to fetch emails
if st.button('Fetch Emails'):
    with st.spinner('Fetching unread emails...'):
        try:
            emails = parser.fetch_emails()
            if not emails:
                st.info('No unread emails found.')
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
# - Use the button above to fetch the 10 most recent unread emails from your inbox.
# - Each email is shown in an expandable section for easy browsing.
# - Sender, subject, timestamp, and body are displayed for each email.
# - Errors are shown if fetching fails (e.g., bad credentials or network issues). 