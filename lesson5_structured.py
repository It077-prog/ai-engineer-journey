import json
import ollama

MODEL = "llama3.2"
SYSTEM_PROMPT = """You score real estate leads for a Dubai agency.
Follow these 4 steps in order.

STEP 1: Check each signal in the lead. Answer yes or no for each.
- CASH: the lead says "cash" or "cash buyer" or "paying cash".
- MORTGAGE: the lead says "pre-approved" or "mortgage approved".
- URGENT: the lead wants to view or buy soon, such as "this week", "today", "this month", "ASAP", "urgent".
- BUDGET: Budget is a number (not "not given").
- AREA: a specific area or community is named.
- BROWSING: the lead says "just browsing", "just looking", "maybe later" or "no rush".

STEP 2: Choose the category. Use the FIRST rule that matches.
1. CASH or MORTGAGE or URGENT is yes -> "hot"
2. BROWSING is yes -> "cold"
3. BUDGET and AREA are both yes -> "warm"
4. Anything else -> "cold"

STEP 3: Choose the score. It must be inside the category range.
- hot: 8 to 10. Give 10 if two or more of CASH, MORTGAGE, URGENT are yes. Otherwise give 9 if BUDGET is yes, else 8.
- warm: 5 to 7. Give 7 if the message shows a clear requirement (property type or bedrooms). Otherwise 6.
- cold: 1 to 4. Give 1 if the message is empty or spam. Give 4 if BUDGET is yes. Otherwise give 2 or 3.

STEP 4: Write a reason of 15 words or fewer. Mention the signals you found.
Use only facts from the lead. Never invent facts.

EXAMPLES
Lead:
Budget: AED 3,000,000
Area: Business Bay
Message: Paying cash, need to move next month
Answer: {"score": 10, "category": "hot", "reason": "Cash buyer who needs to move next month"}

Lead:
Budget: AED 1,200,000
Area: JVC
Message: Looking for a 1BR apartment
Answer: {"score": 7, "category": "warm", "reason": "Clear budget, area and property type, no urgency"}

Lead:
Budget: not given
Area: Downtown
Message: Just looking, maybe later
Answer: {"score": 2, "category": "cold", "reason": "Just looking with no budget"}

OUTPUT
Reply with one JSON object only. No other text.
{"score": <whole number 1-10>, "category": "hot" or "warm" or "cold", "reason": "<15 words max>"}"""


def format_budget(budget):
    if budget:
        return f"AED {budget:,}"
    return "not given"


def build_prompt(lead):
    return (
        f"Budget: {format_budget(lead.get('budget'))}\n"
        f"Area: {lead.get('area', 'unknown')}\n"
        f"Message: {lead.get('message', '')}"
    )


def score_lead(lead):
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(lead)},
        ],
        format="json",
        options={"temperature": 0},
    )
    return json.loads(response["message"]["content"])


leads = [
    {"name": "Omar Khalid", "budget": 2500000, "area": "Dubai Marina", "message": "Cash buyer, viewing this week"},
    {"name": "Priya Nair", "budget": None, "area": "JLT", "message": "Just browsing"},
    {"name": "Sara Ahmed", "budget": 5000000, "area": "Arabian Ranches", "message": "Mortgage pre-approved"},
]

for lead in leads:
    result = score_lead(lead)
    print(f"{lead['name']}: {result['score']}/10 ({result['category']}) - {result['reason']}")
    if result["score"] >= 8:
        print("   🔥 Hot lead: call now")