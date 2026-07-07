from dotenv import load_dotenv
import os

load_dotenv()

CHATWOOT_URL = os.getenv("CHATWOOT_URL")
CHATWOOT_API_TOKEN = os.getenv("CHATWOOT_API_TOKEN")
CHATWOOT_ACCOUNT_ID = os.getenv("CHATWOOT_ACCOUNT_ID")