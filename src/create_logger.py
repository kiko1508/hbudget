import logging


def create_logger(log_file):
    """
    create logger with 'application'
    """
    logger = logging.getLogger( 'main' )
    logger.setLevel( logging.DEBUG )
    # create file handler which logs even debug messages
    fh = logging.FileHandler(log_file)
    fh.setLevel( logging.DEBUG )
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel( logging.INFO )
    # create formatter and add it to the handlers
    formatter = logging.Formatter( '%(asctime)s - %(name)s - %(levelname)s - %(message)s' )
    fh.setFormatter( formatter )
    ch.setFormatter( formatter )
    # add the handlers to the logger
    logger.addHandler( fh )
    logger.addHandler( ch )

    return logger