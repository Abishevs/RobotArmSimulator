import logging
import os

def setup_logging(base_dir=None):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))  

    log_dir = os.path.join(base_dir, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    app_env = os.getenv('APP_ENV', 'dev')
    debug_mode = os.getenv('DEBUG_MODE') == '1'
    print(f"Debug mode: {debug_mode}, app_env: {app_env}")
    
    log_level = logging.DEBUG if debug_mode else logging.INFO
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Clear existing handlers
    logging.getLogger().handlers.clear()

    # Set up file handlers
    error_handler = logging.FileHandler(os.path.join(log_dir, 'error.log'))
    error_handler.setLevel(logging.ERROR)  # Only log ERROR and above to error.log
    error_handler.setFormatter(logging.Formatter(log_format))

    action_handler = logging.FileHandler(os.path.join(log_dir, 'action.log'))
    action_handler.setLevel(log_level)  # Action logs respect the log_level
    action_handler.setFormatter(logging.Formatter(log_format))

    debug_handler = logging.FileHandler(os.path.join(log_dir, 'debug.log'))
    debug_handler.setLevel(logging.DEBUG)  # Always log DEBUG and above to debug.log
    debug_handler.setFormatter(logging.Formatter(log_format))

    handlers = [error_handler, action_handler, debug_handler]

    if app_env == 'dev':
        # Add console handler in development environment
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(console_handler)

    # Configure the root logger
    logging.basicConfig(level=log_level, format=log_format, handlers=handlers)

class LoggerConfig:
    ERROR_LOGGER = 'error_logger'
    ACTION_LOGGER = 'action_logger'
    DEBUG_LOGGER = 'debug_logger'
    LOG_DIR = 'logs'

    @staticmethod
    def setup_logging():
        if not os.path.exists(LoggerConfig.LOG_DIR):
            os.makedirs(LoggerConfig.LOG_DIR)

        # Set up Error Logger
        LoggerConfig._setup_file_logger(LoggerConfig.ERROR_LOGGER, 
                                        os.path.join(LoggerConfig.LOG_DIR, 'errors.log'), 
                                        logging.INFO, '%(asctime)s - %(levelname)s - %(message)s')

        # Set up Action Logger
        LoggerConfig._setup_file_logger(LoggerConfig.ACTION_LOGGER,
                                        os.path.join(LoggerConfig.LOG_DIR, 'actions.log'), 
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
