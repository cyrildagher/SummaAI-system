import imaplib
import email
from email.header import decode_header
from datetime import datetime
from summaai.config.config import Config

class EmailParser:
    def __init__(self, config=None):
        """
        Initialize the EmailParser with configuration loaded from .env via Config.
        """
        self.config = config or Config()
        self.imap_server = self.config.IMAP_SERVER
        self.imap_user = self.config.IMAP_USER
        self.imap_password = self.config.IMAP_PASSWORD
        self.mailbox = None

    def connect(self):
        """
        Connect to the IMAP server and login using credentials.
        """
        self.mailbox = imaplib.IMAP4_SSL(self.imap_server)
        self.mailbox.login(self.imap_user, self.imap_password)

    def fetch_emails(self, max_emails=10):
        """
        Fetch the most recent unread emails from the inbox.
        Returns a list of dictionaries with sender, subject, body, and timestamp.
        """
        if not self.mailbox:
            self.connect()
        self.mailbox.select("inbox")
        # Search for unread emails
        status, messages = self.mailbox.search(None, '(UNSEEN)')
        if status != 'OK':
            return []
        email_ids = messages[0].split()
        # Get the latest emails (from the end)
        latest_email_ids = email_ids[-max_emails:][::-1]
        emails = []
        for eid in latest_email_ids:
            status, msg_data = self.mailbox.fetch(eid, '(RFC822)')
            if status != 'OK':
                continue
            msg = email.message_from_bytes(msg_data[0][1])
            # Parse sender
            sender = msg.get('From', '')
            # Parse subject
            subject, encoding = decode_header(msg.get('Subject', ''))[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or 'utf-8', errors='ignore')
            # Parse date
            date_str = msg.get('Date', '')
            try:
                timestamp = email.utils.parsedate_to_datetime(date_str)
            except Exception:
                timestamp = None
            # Parse body (ignore attachments)
            body = ''
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get('Content-Disposition'))
                    if content_type == 'text/plain' and 'attachment' not in content_disposition:
                        charset = part.get_content_charset() or 'utf-8'
                        try:
                            body += part.get_payload(decode=True).decode(charset, errors='ignore')
                        except Exception:
                            continue
            else:
                charset = msg.get_content_charset() or 'utf-8'
                try:
                    body = msg.get_payload(decode=True).decode(charset, errors='ignore')
                except Exception:
                    body = msg.get_payload()
            email_dict = {
                'sender': sender,
                'subject': subject,
                'body': body.strip(),
                'timestamp': timestamp
            }
            emails.append(email_dict)
        return emails

    def logout(self):
        """
        Logout from the IMAP server.
        """
        if self.mailbox:
            self.mailbox.logout()
            self.mailbox = None

# --- Dummy email generator for testing/demo purposes ---
def generate_dummy_emails(limit=5):
    """
    Generate a list of dummy email dictionaries for testing or demo purposes.
    Each dictionary includes sender, subject, body, and timestamp.
    """
    now = datetime.now().isoformat()
    dummy_emails = [
        {
            'sender': 'boss@company.com',
            'subject': 'Quarterly Report Needed ASAP',
            'body': 'Hi,\n\nThis is URGENT. Please send the quarterly report by EOD.\nKeywords: urgent, report, deadline.\n\nThanks.',
            'timestamp': now
        },
        {
            'sender': 'hr@company.com',
            'subject': 'Team Building Event Invitation',
            'body': 'Hello!\n\nYou are invited to our annual team building event next Friday. RSVP soon!\nKeywords: invitation, event, RSVP.\n\nBest, HR',
            'timestamp': now
        },
        {
            'sender': 'alerts@bank.com',
            'subject': 'Suspicious Login Attempt Detected',
            'body': 'Dear Customer,\n\nWe detected a suspicious login attempt on your account. Please verify your identity.\nKeywords: security, alert, verify.\n\nBank Security Team',
            'timestamp': now
        },
        {
            'sender': 'colleague@company.com',
            'subject': 'Lunch Plans?',
            'body': 'Hey,\n\nAre you free for lunch today? Let me know!\nKeywords: lunch, meeting, casual.\n\nCheers.',
            'timestamp': now
        },
        {
            'sender': 'newsletter@news.com',
            'subject': 'Your Daily News Digest',
            'body': 'Good morning!\n\nHere are today's top stories.\nKeywords: news, digest, daily.\n\nStay informed!',
            'timestamp': now
        }
    ]
    return dummy_emails[:limit] 