from src.forest.exception import CustomException
import os,sys

def test():
    try:
        s = 1/0
    except Exception as e:
        raise CustomException(e,sys)
    
if __name__ == '__main__':
    try:
        test()
    except CustomException as e:
        print(e)