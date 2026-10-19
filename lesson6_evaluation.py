"""
Lesson 6: Evaluation, validation and retries
--------------------------------------------
Goal: test the lead scorer on 12 varied leads with known correct answers,
measure accuracy, and handle broken AI output safely.
"""

import json
import ollama
from lesson5_structured import SYSTEM_PROMPT, MODEL, build_prompt   # reuse Lesson 5
from lesson5_structured import SYSTEM_PROMPT, build_prompt

MODEL = "gemma4:31b-cloud"

VALID_CATEGORIES = {"hot", "warm", "cold"}
SCORE_RANGES = {"hot": (8, 10), "warm": (5, 7), "cold": (1, 4)}


def is_valid(result):
    """Return True only if the AI's answer has a real category and a score inside its range."""
    if result.get("category") not in VALID_CATEGORIES:
        return False
    score = result.get("score")
    if not isinstance(score, int):
        return False
    low, high = SCORE_RANGES[result["category"]]
    return low <= score <= high

def extract_json(raw):
    """Pull the JSON object out of the model's text, even if it's wrapped in ```json fences or extra words."""
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1:
        raise json.JSONDecodeError("No JSON object found", raw, 0)
    return json.loads(raw[start:end + 1])


def score_lead(lead, max_attempts=3):
    """Score one lead. Retry if the output is broken or invalid. Never crash."""
    for attempt in range(1, max_attempts + 1):
        raw = ""
        try:
            response = ollama.chat(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": build_prompt(lead)},
                ],
                format="json",
                options={"temperature": 0 if attempt == 1 else 0.5},
            )
            raw = response["message"]["content"]
            result = extract_json(raw)
            if is_valid(result):
                return result
            print(f"   ⚠️ attempt {attempt}: invalid answer {result}")
        except json.JSONDecodeError:
            print(f"   ⚠️ attempt {attempt}: broken JSON → {raw!r}")
    return {"score": None, "category": "error", "reason": "failed after retries"}



# --- Test set: 12 leads with the CORRECT answer decided by us (a human) ---
TEST_CASES = [
    {"lead": {"name": "Omar", "budget": 2500000, "area": "Dubai Marina", "message": "Cash buyer, viewing this week"}, "expected": "hot"},
    {"lead": {"name": "Priya", "budget": None, "area": "JLT", "message": "Just browsing"}, "expected": "cold"},
    {"lead": {"name": "Sara", "budget": 5000000, "area": "Arabian Ranches", "message": "Mortgage pre-approved"}, "expected": "hot"},
    {"lead": {"name": "Ravi", "budget": 1500000, "area": "JVC", "message": "Looking for a 2BR apartment"}, "expected": "warm"},
    {"lead": {"name": "Empty", "budget": None, "area": "", "message": ""}, "expected": "cold"},
    {"lead": {"name": "Ahmed", "budget": 3000000, "area": "Downtown", "message": "Relocating, need to buy ASAP"}, "expected": "hot"},
    {"lead": {"name": "Lina", "budget": 2000000, "area": "Palm Jumeirah", "message": "Just looking, maybe later"}, "expected": "cold"},
    {"lead": {"name": "Tom", "budget": 4000000, "area": "Damac Hills", "message": "Looking for a villa"}, "expected": "warm"},
    {"lead": {"name": "Typo", "budget": 1800000, "area": "JLT", "message": "csh buyer, want to see it tomorrow"}, "expected": "hot"},
    {"lead": {"name": "Investor", "budget": None, "area": "Business Bay", "message": "Interested in rental yield"}, "expected": "cold"},
    {"lead": {"name": "Spam", "budget": None, "area": "", "message": "Win a free iPhone, click here"}, "expected": "cold"},
    {"lead": {"name": "Mixed", "budget": 2200000, "area": "Dubai Hills", "message": "Mortgage pre-approved but no rush"}, "expected": "hot"},
]

# --- Run the evaluation ---
correct = 0
for case in TEST_CASES:
    lead = case["lead"]
    result = score_lead(lead)
    passed = result["category"] == case["expected"]
    if passed:
        correct += 1
    mark = "✅" if passed else "❌"
    print(f"{mark} {lead['name']:<9} expected -{case['expected']:<5} got- {result['category']:<5} ({result['score']})")

accuracy = correct / len(TEST_CASES) * 100
print(f"\nAccuracy: {correct}/{len(TEST_CASES)} = {accuracy:.0f}%")

