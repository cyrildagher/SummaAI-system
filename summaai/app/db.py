import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, config):
        self.config = config
        self.conn = None
        self.connect()

    def connect(self):
        """
        Establish a connection to the MySQL database.
        """
        try:
            self.conn = mysql.connector.connect(
                host=self.config.MYSQL_HOST,
                user=self.config.MYSQL_USER,
                password=self.config.MYSQL_PASSWORD,
                database=self.config.MYSQL_DB
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.conn = None

    def store_email(self, sender, subject, body, summary, importance_score, timestamp, notified=False):
        """
        Store an email in the database, avoiding duplicates (subject+timestamp).
        Fields: sender, subject, body, summary, importance_score, timestamp, notified.
        """
        if not self.conn:
            self.connect()
        try:
            cursor = self.conn.cursor()
            # Create table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS emails (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    sender VARCHAR(255),
                    subject VARCHAR(255),
                    body TEXT,
                    summary TEXT,
                    importance_score INT,
                    timestamp DATETIME,
                    notified BOOLEAN DEFAULT FALSE,
                    UNIQUE KEY unique_email (subject, timestamp)
                )
            ''')
            # Check for duplicate
            cursor.execute(
                "SELECT id FROM emails WHERE subject=%s AND timestamp=%s",
                (subject, timestamp)
            )
            if cursor.fetchone():
                # Duplicate found, skip insert
                return False
            # Insert new email
            cursor.execute(
                """
                INSERT INTO emails (sender, subject, body, summary, importance_score, timestamp, notified)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (sender, subject, body, summary, importance_score, timestamp, notified)
            )
            self.conn.commit()
            return True
        except Error as e:
            print(f"Error storing email: {e}")
            return False

    def insert_email(self, email_data):
        # TODO: Insert parsed email into database
        pass 