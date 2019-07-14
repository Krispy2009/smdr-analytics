import os
EMAIL_USER = os.getenv('EMAIL')
EMAIL_PASS=os.getenv('EMAIL_PASSWORD')
EMAIL_SERVER=os.getenv('HOST','outlook.office365.com')

FOLDER_TO_SCAN=os.getenv('EMAIL_FOLDER','INBOX/ACMA-SMDR')
