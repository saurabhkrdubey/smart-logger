import logging
import inspect
import os



import logging
import os

class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Adding a custom variable if needed
        record.custom_variable = "Custom Value"
        return super().format(record)

class SmartLogger:
    def __init__(self, name='smart-logger', log_dir='logs', log_file='app.log'):
        # Create a log directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create a custom logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Create a file handler to write logs to a file
        log_file_path = os.path.join(log_dir, log_file)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Use the CustomFormatter with both handlers
        formatter = CustomFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s - [Custom Variable: %(custom_variable)s]'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)





class SmartLogger:
    def __init__(self, name='smart-logger', log_dir='logs'):
        frame = inspect.currentframe().f_back
        frame_info = inspect.getframeinfo(frame)
        filename = os.path.basename(frame_info.filename)
        self.filename = os.path.splitext(os.path.basename(filename))[0]

        # Create a log directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)


        # Create a custom logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        log_file_path = os.path.join(log_dir,f'{self.filename}_log.log')
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)

        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Create and set a standard formatter that includes the filename and function name
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(file_name)s:%(line_nos)s - %(func_name)s - %(message)s]'
        )
        ch.setFormatter(formatter)

        # Add the handler to the logger

        file_handler.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(ch)


    def log(self, level, message, extra=None):
        """Log a message at a given level with optional extra information."""
        if not extra:
            extra = {}
        # extra.setdefault('filename', 'custom.py')
  
        self.logger.log(level, message, extra=extra)

    def info(self, message, extra=None):
        """Log an info message."""
        self.log(logging.INFO, message, extra)

    def warning(self, message, extra=None):
        """Log a warning message."""
        self.log(logging.WARNING, message, extra)

    def error(self, message, extra=None):
        """Log an error message."""
        self.log(logging.ERROR, message, extra)

    def debug(self, message, extra=None):
        """Log a debug message."""
        self.log(logging.DEBUG, message, extra)



def get_context():
    frame = inspect.currentframe().f_back
    frame_info = inspect.getframeinfo(frame)
    filename = os.path.basename(frame_info.filename)
    line_number = frame_info.lineno
    function_name = frame_info.function
    context = {
        "file_name": filename, 
        "line_nos": line_number, 
        "func_name": function_name
    }
    return context
