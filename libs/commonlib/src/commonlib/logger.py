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
