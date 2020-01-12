import os
import sys
import logme
import email

from imapclient import IMAPClient, exceptions
from settings import EMAIL_SERVER, EMAIL_USER, EMAIL_PASS, FOLDER_TO_SCAN
from sylk_parser import SylkParser

SERVER = None
logger = logme.log(scope="module")


def setup():
    global SERVER

    if not all([EMAIL_USER, EMAIL_PASS, EMAIL_SERVER]):
        logger.error("Please provide all of the login information: email, password and host")
        sys.exit(1)

    logger.info(f"Connecting to {EMAIL_SERVER}")
    SERVER = IMAPClient(EMAIL_SERVER)

    logger.info(f"Logging in: {EMAIL_USER}")
    SERVER.login(EMAIL_USER, EMAIL_PASS)


def get_attachments():
    try:
        logger.debug(f"Trying to get attachments from {FOLDER_TO_SCAN}")
        select_info = SERVER.select_folder(FOLDER_TO_SCAN, readonly=True)
        logger.debug(f"Total emails: {select_info.get(b'EXISTS')}")
        latest_email_downloaded = get_latest_email_downloaded()
        logger.debug(f"Latest UID downloaded: {latest_email_downloaded}")

        # Get all messages after latest uid
        messages = SERVER.search(["UID", f"{latest_email_downloaded+1}:*"])
        all_messages = SERVER.fetch(messages, "RFC822").items()
        logger.debug(f"Fetched {len(all_messages)} new emails")

        for uid, data in all_messages:
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
                        update_latest_email_downloaded(uid)

    except exceptions.IMAPClientError as e:
        logger.error(e)


def get_latest_email_downloaded():
    with open("latest_email", "r") as f:
        uid = f.readline()
    logger.debug(f"retrieved latest uid: {uid}")
    return int(uid)


def update_latest_email_downloaded(uid):
    if uid and isinstance(uid, int):
        with open("latest_email", "w") as f:
            f.write(str(uid))
    else:
        logger.warning(f"[{uid}] is not a valid UID")


def teardown():
    resp = SERVER.logout()
    logger.debug(resp)
    logger.info("Logged out")


def unzip_attachments():
    path = "./attachments"
    # List all the items in the path directory, but keep only the files
    all_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for file in all_files:

        # If we are checking a gz make sure there isnot already a slk with the same name
        # which means we have already unzipped it
        if file.endswith("gz"):

            zipped_file_path = os.path.join(path, file)
            unzipped_file_path = os.path.join(path, file[:-3])

            logger.debug(f"Checking {file}")
            already_unzipped = os.path.isfile(unzipped_file_path)
            if already_unzipped:
                logger.debug(f"Skipping {file} - Already unzipped")
                continue

            unzipped_file = open(unzipped_file_path, "wb")
            with open(zipped_file_path, "rb") as f:
                bindata = f.read()
            unzipped_file.write(bindata)
            unzipped_file.close()


def parse_smdr_data():
    pass


def save_to_db(parsed_smdr_line):
    pass


if __name__ == "__main__":
    try:
        setup()
        get_attachments()
        unzip_attachments()
    except Exception as e:
        logger.critical(f"Failed to get SMDR Analytics: {e}")
    finally:

        teardown()
