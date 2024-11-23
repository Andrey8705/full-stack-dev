from dotenv import load_dotenv
import os

load_dotenv()
api = os.environ.get('API_KEY')
debug_status = os.environ.get('DEBUG_MODE')
print(api)
print(debug_status)