import streamlit as st
from summaai.app.email_parser import EmailParser, generate_dummy_emails
from summaai.app.summarizer import summarize_email, score_email_importance, generate_daily_digest
from summaai.app.db import Database
from summaai.app.notifier import send_notification
from summaai.config.config import Config
from datetime import datetime

st.title('SummaAI – Smart Email Summarizer')
st.write('Welcome to SummaAI! This dashboard will display important email summaries and allow you to manage settings.')

# Sidebar toggle for dummy data
use_dummy_data = st.sidebar.checkbox('Use dummy email data (for demo/testing)', value=True)

# Initialize the email parser, config, and database
parser = EmailParser()
config = Config()
db = Database(config)

# Store fetched emails in session state for digest generation
if 'fetched_emails' not in st.session_state:
    st.session_state['fetched_emails'] = []

# Streamlit button to fetch emails
if st.button('Fetch Emails'):
    with st.spinner('Fetching emails...'):
        try:
            if use_dummy_data:
                emails = generate_dummy_emails()
            else:
                emails = parser.fetch_emails()
            st.session_state['fetched_emails'] = []  # Reset
            if not emails:
                st.info('No emails found.')
            else:
                for idx, email_obj in enumerate(emails, 1):
                    # Score importance and summarize
                    importance_score = score_email_importance(email_obj['body'])
                    summary = summarize_email(email_obj['body'])
                    # Store in DB (avoid duplicates)
                    timestamp = email_obj['timestamp']
                    if isinstance(timestamp, datetime):
                        timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        timestamp_str = str(timestamp)
                    stored = db.store_email(
                        sender=email_obj['sender'],
                        subject=email_obj['subject'],
                        body=email_obj['body'],
                        summary=summary,
                        importance_score=importance_score,
                        timestamp=timestamp_str,
                        notified=False
                    )
                    # Prepare email dict for notification and digest
                    email_data = {
                        'sender': email_obj['sender'],
                        'subject': email_obj['subject'],
                        'body': email_obj['body'],
                        'summary': summary,
                        'importance_score': importance_score,
                        'timestamp': timestamp_str,
                        'notified': False
                    }
                    st.session_state['fetched_emails'].append(email_data)
                    # Send notification if not notified and score exceeds threshold
                    if not email_data['notified'] and importance_score > 5:
                        notified = send_notification(email_data)
                        if notified:
                            # Update DB to mark as notified
                            try:
                                cursor = db.conn.cursor()
                                cursor.execute(
                                    "UPDATE emails SET notified=TRUE WHERE subject=%s AND timestamp=%s",
                                    (email_obj['subject'], timestamp_str)
                                )
                                db.conn.commit()
                            except Exception as e:
                                st.warning(f"Failed to update notification status: {e}")
                    with st.expander(f"Email #{idx}: {email_obj['subject']}"):
                        st.markdown(f"**Sender:** {email_obj['sender']}")
                        st.subheader(email_obj['subject'])
                        st.caption(f"Timestamp: {timestamp_str}")
                        st.text_area('Body', email_obj['body'], height=200)
                        st.markdown(f"**Summary:** {summary}")
                        st.markdown(f"**Importance Score:** {importance_score}")
                        if stored:
                            st.success("Email stored in database.")
                        else:
                            st.info("Duplicate email (subject + timestamp) not stored.")
        except Exception as e:
            st.error(f"Error fetching emails: {e}")

# Button to generate and display the daily digest
if st.button('Generate Digest'):
    emails_for_digest = st.session_state.get('fetched_emails', [])
    if not emails_for_digest:
        st.info('No emails available. Please fetch emails first.')
    else:
        digest = generate_daily_digest(emails_for_digest)
        st.code(digest, language=None)

# Helpful Streamlit comments:
# - Use the sidebar to toggle between dummy and live email data.
# - Use the button above to fetch emails.
# - Use 'Generate Digest' to create a daily summary of the top emails.
# - Each email is shown in an expandable section for easy browsing.
# - Sender, subject, timestamp, summary, importance score, and body are displayed for each email.
# - Emails are stored in the database unless a duplicate is detected.
# - Notifications are sent for important emails and DB is updated.
# - Errors are shown if fetching, storing, or notifying fails. 