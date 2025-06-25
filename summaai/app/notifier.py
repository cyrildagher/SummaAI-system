import requests

# Notification threshold
NOTIFY_THRESHOLD = 5

# Example: Slack webhook URL should be set in config or .env
try:
    from summaai.config.config import Config
    SLACK_WEBHOOK = Config().SLACK_WEBHOOK
except Exception:
    SLACK_WEBHOOK = None

def send_notification(email: dict, threshold: int = NOTIFY_THRESHOLD) -> bool:
    """
    Send a notification if the email's importance_score exceeds the threshold.
    Supports Slack webhook notifications. Simulates/prints if no webhook is set.
    Returns True if notification sent, False otherwise.
    """
    score = email.get('importance_score', 0)
    if score < threshold:
        return False
    # Prepare notification message
    message = f"New Important Email!\nSubject: {email.get('subject')}\nFrom: {email.get('sender')}\nScore: {score}\nSummary: {email.get('summary')}"
    # Slack notification
    if SLACK_WEBHOOK:
        try:
            resp = requests.post(SLACK_WEBHOOK, json={"text": message})
            if resp.status_code == 200:
                print("Slack notification sent.")
                return True
            else:
                print(f"Slack notification failed: {resp.text}")
        except Exception as e:
            print(f"Slack notification error: {e}")
    # Simulate/print notification if no webhook
    print("[Simulated Notification]\n" + message)
    # Optional: Add email or push notification logic here
    return True

class Notifier:
    def __init__(self, config):
        self.config = config

    def send_notification(self, message):
        # TODO: Send notification via Slack/email
        pass 