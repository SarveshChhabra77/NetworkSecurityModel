import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message=error_message
        _,_,exc_tb=error_details.exc_info()
        
        self.filename=exc_tb.tb_frame.f_code.co_filename
        self.fileline=exc_tb.tb_lineno
        
        
    def __str__(self):
            return 'Error occured in the python script name [{0}], line number [{1}], error message [{2}] '.format(self.filename,self.fileline,str(self.error_message))    
        
        

    
    
        