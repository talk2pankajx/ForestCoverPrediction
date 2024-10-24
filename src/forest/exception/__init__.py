import os,sys

class CustomException(Exception):
    def __init__(self,error_message:Exception,error_message_detail: sys):
        super().__init__(error_message)
        self.error_message = CustomException.prepare_error_message(error_message,error_message_detail)
    
    @staticmethod
    def prepare_error_message(error_message: Exception, error_message_detail: sys):
        _,_,exc_tb = error_message_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_no =exc_tb.tb_lineno
        err_message = f'Error occurred in file: [{file_name}], line number: {line_no} and error message: {error_message}'
        return err_message
    
    def __repr__(self):
        return  self.error_message
    
    def __str__(self):
        return self.error_message
        