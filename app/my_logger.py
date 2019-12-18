import logging
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    '''Loggers set up'''

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return(logger)

# User session logger
session_logger = setup_logger('session_logger', 'logs/session.log')
session_logger.info('User logged in')
