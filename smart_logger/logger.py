import logging
import inspect
import os
from datetime import datetime

from .db_manager import DBManager



class SmartLogger:
    def __init__(self, env, project_name, name, log_dir='logs'):
        self.project_name = project_name
        self.service_name = name
        self.env = env
        frame = inspect.currentframe().f_back
        frame_info = inspect.getframeinfo(frame)
        filename = os.path.basename(frame_info.filename)
        self.filename = os.path.splitext(os.path.basename(filename))[0]
        self.execute_query = DBManager()

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
            '%(asctime)s - %(name)s - %(levelname)s - [%(file_name)s:%(line_nos)s - %(func_name)s - %(message)s]'
        )
        ch.setFormatter(formatter)

        # Add the handler to the logger

        file_handler.setFormatter(formatter)
        ch.setFormatter(formatter)
        

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(ch)



    def fetch_create_project(self):
        """
        fetching project does exist or not.
        Description - 
            not exists - create new project and return project id
            exists - return project id
        """
        query = f"""select id, name from core_project where name = '{self.project_name}'"""
        record = self.execute_query.fetchone(query)
        if not record:
            insert_query = f"""
                insert into core_project (name, created_at, updated_at) values ('{self.project_name}', now(), now()) RETURNING id
            """
            record = self.execute_query.insert(insert_query)
        return record['id']
    
    
    def insert_log(self, **kwargs):
        """
        inserting log into logger tables
        """
        insert_query = f"""
            INSERT INTO public.core_logger(
                created_at, updated_at, environment, logger_type, service_name, log, project_id
            )
            VALUES (
                now(), now(), '{self.env.upper()}', 
                '{kwargs['log_type']}', '{self.service_name}',
                '{kwargs['log']}',
                {kwargs['project_id']}
            ) returning id;
        """
        self.execute_query.insert(insert_query)
        


    def log(self, level, message, extra=None, log_type='INFO'):
        """Log a message at a given level with optional extra information."""
        if not extra:
            extra = {}
        
        project_id = self.fetch_create_project()
  
        self.logger.log(level, message, extra=extra)
        asctime = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime('%Y-%m-%d %H:%M:%S')


        log_message = f"{self.env.upper()} - {asctime} - {self.service_name} - {log_type} - [{extra.get('file_name')}:{extra.get('line_nos')} - {extra.get('func_name')} - {message}]"


        self.insert_log(**{
            "project_id": project_id, 
            "log_type"  : log_type, 
            "log"       : log_message
        })

    def info(self, message, extra=None):
        """Log an info message."""
        self.log(logging.INFO, message, extra, log_type='INFO')

    def warning(self, message, extra=None):
        """Log a warning message."""
        self.log(logging.WARNING, message, extra, log_type='WARNING')

    def error(self, message, extra=None):
        """Log an error message."""
        self.log(logging.ERROR, message, extra, log_type='ERROR')

    def debug(self, message, extra=None):
        """Log a debug message."""
        self.log(logging.DEBUG, message, extra, log_type='DEBUG')



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
