"""
Logging Configuration
"""
import os
import sys
import logging
import re
from datetime import datetime


class NoEmojiFilter(logging.Filter):
    """Remove emojis from log messages for Windows compatibility"""
    def filter(self, record):
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"
                u"\U0001F300-\U0001F5FF"
                u"\U0001F680-\U0001F6FF"
                u"\U0001F1E0-\U0001F1FF"
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                "]+", flags=re.UNICODE)
            record.msg = emoji_pattern.sub('', record.msg)
        return True


def setup_logger(name: str = 'ai-compiler') -> logging.Logger:
    """Setup logger"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    
    # Create logs directory
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.addFilter(NoEmojiFilter())
    
    # File handler
    log_file = os.path.join(logs_dir, f'{datetime.now().strftime("%Y-%m-%d")}.log')
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.addFilter(NoEmojiFilter())
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


logger = setup_logger()