from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from typing import Optional, Dict, List
import threading
import re
from datetime import datetime

# Global cache for the summarizer pipeline
_summarizer_pipeline = None
_summarizer_lock = threading.Lock()

# Model and tokenizer names
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
MAX_TOKENS = 1024  # Model's max input length


def get_summarizer_pipeline():
    """
    Load and cache the summarization pipeline for efficiency.
    Uses a thread lock to ensure only one instance is loaded.
    """
    global _summarizer_pipeline
    if _summarizer_pipeline is None:
        with _summarizer_lock:
            if _summarizer_pipeline is None:
                tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
                model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
                _summarizer_pipeline = pipeline(
                    "summarization",
                    model=model,
                    tokenizer=tokenizer,
                    framework="pt"
                )
    return _summarizer_pipeline


def summarize_email(body: str) -> str:
    """
    Summarize an email body using a local Hugging Face model.
    - Truncates/preprocesses input to ~1024 tokens.
    - Returns a 2–4 sentence summary as plain text.
    - Loads the model only once for efficiency.
    """
    summarizer = get_summarizer_pipeline()
    # Truncate input to model's max token length
    tokenizer = summarizer.tokenizer
    inputs = tokenizer(
        body,
        max_length=MAX_TOKENS,
        truncation=True,
        return_tensors="pt"
    )
    input_text = tokenizer.decode(inputs['input_ids'][0], skip_special_tokens=True)
    # Generate summary (2-4 sentences)
    summary_list = summarizer(
        input_text,
        max_length=130,  # ~2-4 sentences
        min_length=40,
        do_sample=False
    )
    summary = summary_list[0]['summary_text'].strip()
    return summary


def score_email_importance(body: str, keyword_weights: Optional[Dict[str, int]] = None) -> int:
    """
    Score the importance of an email based on keyword occurrences and weights.
    - body: The full email text to scan.
    - keyword_weights: Dict mapping keywords (case-insensitive) to integer weights.
      If not provided, uses a default set of common keywords.
    Returns the total importance score as an integer.
    """
    if keyword_weights is None:
        # Fallback default keywords and weights
        keyword_weights = {
            "urgent": 5,
            "asap": 4,
            "important": 3,
            "invoice": 3,
            "payment": 2,
            "alert": 2,
            "action required": 4,
            "deadline": 3,
            "security": 2,
            "meeting": 1
        }
    score = 0
    body_lower = body.lower()
    for keyword, weight in keyword_weights.items():
        # Use word boundaries for single words, substring for phrases
        if ' ' in keyword:
            # Phrase match (case-insensitive)
            count = len(re.findall(re.escape(keyword.lower()), body_lower))
        else:
            # Whole word match (case-insensitive)
            count = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', body_lower))
        score += count * weight
    return score


def generate_daily_digest(emails: List[Dict]) -> str:
    """
    Generate a plain-text daily digest for the top 3-5 emails, sorted by importance_score (descending).
    Each email dict should have: subject, sender, summary, importance_score.
    Returns a formatted string suitable for display or notification.
    """
    if not emails:
        return "No important emails today."
    # Sort emails by importance_score descending
    sorted_emails = sorted(emails, key=lambda e: e.get('importance_score', 0), reverse=True)
    top_emails = sorted_emails[:5]
    today_str = datetime.now().strftime('%B %d')
    digest_lines = [f"\U0001F4EC SummaAI Daily Digest – {today_str}\n"]
    for idx, email in enumerate(top_emails, 1):
        subject = email.get('subject', 'No Subject')
        sender = email.get('sender', 'Unknown Sender')
        summary = email.get('summary', 'No summary available.')
        digest_lines.append(f"{idx}. {subject} – {sender}\n   {summary}\n")
    return '\n'.join(digest_lines)

# Example usage:
# digest = generate_daily_digest(list_of_email_dicts)

class Summarizer:
    def __init__(self, model_name='facebook/bart-large-cnn'):
        self.model_name = model_name
        # TODO: Load Hugging Face model

    def summarize(self, text):
        # TODO: Summarize the input text
        return 'Summary placeholder' 