# SummaAI

SummaAI is a Streamlit-powered smart email assistant that parses incoming emails, detects important ones using keywords, summarizes them using NLP, and sends notifications. It uses a MySQL database for storage.

## Features
- Email integration (IMAP/Gmail)
- Keyword-based importance detection
- Summarization using Hugging Face models
- Notification system (Slack/email)
- Streamlit dashboard
- MySQL storage

## Project Structure
```
summaai/
├── app/
│   ├── main.py              # Streamlit UI
│   ├── email_parser.py      # Email fetching via IMAP
│   ├── summarizer.py        # Summarization logic
│   ├── notifier.py          # Notification system
│   └── db.py                # MySQL connection and helpers
├── config/
│   └── config.py            # Reads .env variables
├── .env                     # Stores credentials securely
├── requirements.txt         # Dependencies
├── plan.txt                 # Build roadmap
└── README.md
```

## Setup
1. Clone the repo and navigate to the project directory.
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Mac/Linux
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env` template and fill in your credentials.
5. Run the Streamlit app:
   ```
   streamlit run summaai/app/main.py
   ```

## Configuration
Edit the `.env` file with your email, MySQL, and Slack credentials.

## Roadmap
See `plan.txt` for the build plan and features.

---
