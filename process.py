import os
import sys
import logme
import email

from imapclient import IMAPClient, exceptions
from settings import EMAIL_SERVER, EMAIL_USER, EMAIL_PASS, FOLDER_TO_SCAN

SERVER = None
module_logger = logme.log(scope="module")


@logme.log
def setup(logger=None):
    global SERVER

    if not all([EMAIL_USER, EMAIL_PASS, EMAIL_SERVER]):
        logger.error("Please provide all of the login information: email, password and host")
        sys.exit(1)

    logger.info(f"Connecting to {EMAIL_SERVER}")
    SERVER = IMAPClient(EMAIL_SERVER)

    logger.info(f"Logging in: {EMAIL_USER}")
    SERVER.login(EMAIL_USER, EMAIL_PASS)


@logme.log
def get_attachments(logger=None):
    try:
        logger.debug(f"Trying to get attachments from {FOLDER_TO_SCAN}")
        select_info = SERVER.select_folder(FOLDER_TO_SCAN)
        logger.debug(f"Total emails: {select_info.get(b'EXISTS')}")
        messages = SERVER.search("ALL")

        for uid, data in SERVER.fetch(messages, "RFC822").items():
            email_message = email.message_from_bytes(data[b"RFC822"])
            for part in email_message.walk():
                attachment_filename = part.get_filename()
                if attachment_filename is not None:
                    logger.warning(f"Downloading: {uid} - {attachment_filename}")
                    if not os.path.exists("attachments"):
                        os.mkdir("attachments")
                        logger.info("created attachments directory")
                    path = os.path.join(f"./attachments/{uid}_{attachment_filename}")
                    if not os.path.isfile(path):
                        with open(path, "wb") as f:
                            f.write(part.get_payload(decode=True))
                        logger.info(f"Wrote file: {path}")

    except exceptions.IMAPClientError as e:
        logger.error(e)


@logme.log
def teardown(logger=None):
    resp = SERVER.logout()
    logger.debug(resp)
    logger.info("Logged out")


@logme.log
def read_attachments():
    pass


@logme.log
def parse_smdr_data():
    pass


@logme.log
def save_to_db(parsed_smdr_line):
    pass


if __name__ == "__main__":
    try:
        setup()
        get_attachments()
    except Exception as e:
        module_logger.critical(f"Failed to get attachments: {e}")
    finally:

        teardown()
