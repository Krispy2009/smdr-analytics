import logme

from imapclient import IMAPClient, exceptions
import settings

SERVER = None

@logme.log
def setup(logger=None):
    global SERVER
    logger.info(f"Connecting to {settings.EMAIL_SERVER}")
    SERVER = IMAPClient(settings.EMAIL_SERVER)
    
    logger.info(f"Logging in: {settings.EMAIL_USER}")
    SERVER.login(settings.EMAIL_USER, settings.EMAIL_PASS)

@logme.log
def get_attachments(logger=None):
    try: 
        logger.debug(f'Trying to get attachments from {settings.FOLDER_TO_SCAN}')
        select_info = SERVER.select_folder(settings.FOLDER_TO_SCAN)
        logger.debug(f"Total emails: {select_info.get(b'EXISTS')}")
        messages = SERVER.search('ALL')

        for uid, data in SERVER.fetch(messages, 'RFC822').items():
            logger.warning(data)

    except exceptions.IMAPClientError as e:
        logger.error(e)

def teardown(logger=None):
    resp = SERVER.logout()
    logger.info(resp)
    logger.info('Logged out')


def read_attachments():
    pass

def parse_smdr_data():
    pass

def save_to_db(parsed_smdr_line):
    pass


if __name__ == '__main__':

    setup()

    get_attachments()    

