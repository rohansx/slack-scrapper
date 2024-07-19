# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SLACK_URL = os.getenv('SLACK_URL')
COOKIES = {
    'b': os.getenv('COOKIE_B'),
}
CHANNEL_ID = os.getenv('CHANNEL_ID')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Content-Type': 'application/json;charset=utf-8'
}
