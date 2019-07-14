import os

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_SERVER = os.getenv("EMAIL_SERVER", "outlook.office365.com")
FOLDER_TO_SCAN = os.getenv("EMAIL_FOLDER", "INBOX")
