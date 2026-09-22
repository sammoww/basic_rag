import os
from dotenv import load_dotenv
from google.genai import Client

load_dotenv()
client = Client(api_key=os.getenv("GOOGLE_API_KEY"))

for m in client.models.list():
    if 'embed' in m.name.lower():
        print(m.name, m.supported_actions)
