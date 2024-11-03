import sys


class ForestException(Exception):
    
    def __init__(self,error_message,error_detail:sys):
        super().__init__()
        self.error_message = ForestException.prepare_error_message(error_message,error_detail)
    
    @staticmethod
    def prepare_error_message(error_message,error_detail:sys)->str:
        _,_,exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        error_message = f"error Occured file_name : [{file_name}] line_number: [{line_number}] and error_message : [{error_message}]"
        return error_message
    
    def __repr__(self) :
        return self.error_message
    
    def __str__(self):
        return self.error_message
     
