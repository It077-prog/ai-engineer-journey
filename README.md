# AI Engineer Journey

My hands-on path from operations and project coordination into AI engineering, learning Python by building real AI features for a Dubai real estate use case.

## What's inside

| Lesson | File | What I built | Key skills |
|---|---|---|---|
| 1 | — | Dev environment | Python, PyCharm, virtual environments, Git |
| 2 | `Lesson2_hello_ai.py` | First LLM call | Google Gemini API, API keys in `.env` |
| 3 | `lesson3_leads.py` | Batch lead scoring | Lists, dictionaries, loops, f-strings, data cleaning |
| 4 | `lesson4_ai.py` | Reusable scoring functions + local LLM | Functions, `return`, swapping cloud API for Ollama |
| 5 | `lesson5_structured.py` | Rule-based lead scorer with JSON output | System prompts, few-shot examples, `format="json"`, temperature 0 |

## Result so far

A 3B-parameter model (Llama 3.2) running **locally** scores real estate leads against business rules and returns structured JSON:

```
Omar Khalid: 10/10 (hot) - Cash buyer viewing this week in Dubai Marina
   🔥 Hot lead: call now
Priya Nair: 2/10 (cold) - Just browsing with no budget, no urgency
Sara Ahmed: 9/10 (hot) - Mortgage pre-approved buyer in Arabian Ranches
   🔥 Hot lead: call now
```

3/3 test leads scored correctly, using a structured prompt with explicit rules and few-shot examples (kept separate from test data to avoid leakage).

## How to run

1. Install [Ollama](https://ollama.com) and pull the model: `ollama pull llama3.2`
2. Create a virtual environment and install packages:
```
   python3 -m venv .venv
   source .venv/bin/activate
   pip install ollama google-genai python-dotenv
```
3. For the Gemini lessons, copy `.env.example` to `.env` and add your API key.
4. Run a lesson: `python lesson5_structured.py`

## Next

Evaluation on a larger test set, error handling and retries, reading leads from CSV, then RAG and AI agents.

---
**Author:** Anil Kumar Gunda · Dubai, UAE
