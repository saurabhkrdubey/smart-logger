import logging
import inspect
import os



class SmartLogger:
    def __init__(self, name='smart-logger'):
        # Create a custom logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Create and set a standard formatter that includes the filename and function name
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(file_name)s:%(line_nos)s - %(func_name)s - %(message)s]'
        )
        ch.setFormatter(formatter)

        # Add the handler to the logger
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
