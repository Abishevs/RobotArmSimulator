import logging
import os

class LoggerConfig:
    ERROR_LOGGER = 'error_logger'
    ACTION_LOGGER = 'action_logger'
    DEBUG_LOGGER = 'debug_logger'

    @staticmethod
    def setup_logging():
        # Set up Error Logger
        LoggerConfig._setup_file_logger(LoggerConfig.ERROR_LOGGER, 'errors.log', 
                                        logging.INFO, '%(asctime)s - %(levelname)s - %(message)s')

        # Set up Action Logger
        LoggerConfig._setup_file_logger(LoggerConfig.ACTION_LOGGER, 'actions.log', 
                                        logging.INFO, '%(asctime)s - %(message)s')

        # Set up Debug Logger
        if os.getenv('DEBUG_MODE') == '1':
            LoggerConfig._setup_console_debug_logger()

    @staticmethod
    def _setup_file_logger(name, file_name, level, format_str):
        logger = logging.getLogger(name)
        logger.setLevel(level)
        handler = logging.FileHandler(file_name)
        formatter = logging.Formatter(format_str)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    @staticmethod
    def _setup_console_debug_logger():
        debug_logger = logging.getLogger(LoggerConfig.DEBUG_LOGGER)
        debug_logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        debug_logger.addHandler(console_handler)

    @staticmethod
    def err(err):
        """Log an error message."""
        logger = logging.getLogger(LoggerConfig.ERROR_LOGGER)
        logger.error(err)

    @staticmethod
    def info(message):
        """Log an info message."""
        logger = logging.getLogger(LoggerConfig.ACTION_LOGGER)
        logger.info(message)

    @staticmethod
    def debug(message):
        """Log a debug message."""
        logger = logging.getLogger(LoggerConfig.DEBUG_LOGGER)
        logger.debug(message)
