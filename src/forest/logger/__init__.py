import os
import logging
from from_root import from_root
from datetime import datetime   

# Setup logging

LOG_FILE_NAME = f"{datetime.now().strftime('%m/%d/%Y_%M%H%S')}.log"
LOG_DIR = 'logs'
os.makedirs(LOG_DIR,exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)


logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='[%(asctime)s - %(lineno)d - %(levelname)s %(message)s]')