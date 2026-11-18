from dotenv import load_dotenv
load_dotenv()
import os
from google import genai

print("key set:", bool(os.environ.get("GEMINI_API_KEY")))
c = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
print(c.models.generate_content(model="gemini-3.5-flash-lite", contents="Say hi in 3 words").text)