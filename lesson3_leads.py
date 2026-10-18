import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

leads = [
    {"name": "Omar Khalid", "budget": "2.5M", "area": "Dubai Marina", "message": "Cash buyer, viewing this week"},
    {"name": "Priya Nair", "budget": "", "area": "JLT", "message": "Just browsing"},
    {"name": "Sara Ahmed", "budget": "5M", "area": "Arabian Ranches", "message": "Mortgage pre-approved, ready to buy"},
]

for lead in leads:
    prompt = (
        f"Score this real estate lead from 1 to 10 and give one short reason.\n"
        f"Budget: {lead['budget'] or 'not given'}\n"
        f"Area: {lead['area']}\n"
        f"Message: {lead['message']}"
    )
    response = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
    print(f"{lead['name']}: {response.text}")
    print("-" * 40)
