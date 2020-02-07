import logging

logging.getLogger().setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s-%(levelname)s-%(message)s, datefmt="%d-%b-%y %H:%M:%S" ')


def log_debug_message(message: str):
    logging.debug(message)


def log_info_message(message: str):
    logging.info(message)


def log_error_message(message: str):
    logging.error(message)
