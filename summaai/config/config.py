import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.IMAP_SERVER = os.getenv('IMAP_SERVER')
        self.IMAP_USER = os.getenv('IMAP_USER')
        self.IMAP_PASSWORD = os.getenv('IMAP_PASSWORD')
        self.MYSQL_HOST = os.getenv('MYSQL_HOST')
        self.MYSQL_USER = os.getenv('MYSQL_USER')
        self.MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
        self.MYSQL_DB = os.getenv('MYSQL_DB')
        self.SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK') 