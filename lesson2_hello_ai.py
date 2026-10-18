import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

prompt1= "Score this lead from 1 to 10: cash buyer, 2BR in Dubai Marina, wants viewing this week in 2 lines"

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt1
)
print("Response from first generation is",response.text)
response2 = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt1
)
print("Response from first generation is",response2.text)


