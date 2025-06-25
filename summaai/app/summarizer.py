from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from typing import Optional
import threading

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

# Example usage:
# summary = summarize_email(long_email_body)

class Summarizer:
    def __init__(self, model_name='facebook/bart-large-cnn'):
        self.model_name = model_name
        # TODO: Load Hugging Face model

    def summarize(self, text):
        # TODO: Summarize the input text
        return 'Summary placeholder' 