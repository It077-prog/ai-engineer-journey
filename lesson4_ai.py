import ollama

MODEL = "llama3.2"


def format_budget(budget):
    if budget:
        return f"AED {budget:,}"
    return "not given"


def build_prompt(lead):
    return (
        f"Score this Dubai real estate lead from 1 to 10 and give one short reason.\n"
        f"Budget: {format_budget(lead.get('budget'))}\n"
        f"Area: {lead.get('area', 'unknown')}\n"
        f"Message: {lead.get('message', '')}"
    )


def score_lead(lead):
    prompt = build_prompt(lead)
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]


leads = [
    {"name": "Omar Khalid", "budget": 2500000, "area": "Dubai Marina", "message": "Cash buyer, viewing this week"},
    {"name": "Priya Nair", "budget": None, "area": "JLT", "message": "Just browsing"},
    {"name": "Sara Ahmed", "budget": 5000000, "area": "Arabian Ranches", "message": "Mortgage pre-approved"}
]

for lead in leads:
    result = score_lead(lead)
    print(f"{lead['name']}: {result}")
    print("-" * 40)

