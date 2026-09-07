# Kisan Dost 🌾 — Farmer's Friend


## Live Demo
🔗 https://kisan-project.fastapicloud.dev

An AI agronomy agent that helps Pakistani farmers decide what to grow, how to protect it, and when to sell — built with the OpenAI Agents SDK (running on Groq's free API).

## What It Does

Kisan Dost is a terminal-based (with an optional web UI) AI advisory system for farmers. A farmer types a question in plain Urdu-English (Roman Urdu) and gets a genuinely useful, structured answer back.

## Tools / Capabilities

| Tool | What it does |
|---|---|
| **Fertilizer Calculator** | Computes Urea/DAP bags needed per acre for a crop, with total cost in PKR |
| **Crop Advisor** | Recommends the best crop based on season (Rabi/Kharif), water availability, and land size |
| **Pest & Disease Doctor** | Identifies likely pest/disease from symptoms and gives safe treatment dosage |
| **Mandi Price Lookup** | Returns current wholesale mandi price for a crop and selling advice |

## Architecture

- **Triage Agent** — routes each farmer question to the right specialist
- **Agronomy Agent** — handles fertilizer + crop recommendation
- **Pest Doctor Agent** — handles pest/disease diagnosis
- **Market Agent** — handles mandi price lookups
- **Input Guardrail** — rejects off-topic or human-medical questions

Built using: `Agent`, `Runner`, `function_tool`, Pydantic structured outputs, and multi-agent `handoffs` from the OpenAI Agents SDK.

## Tech Stack

- **Framework:** OpenAI Agents SDK (`openai-agents`)
- **Model provider:** Groq (free, OpenAI-compatible endpoint)
- **Structured outputs:** Pydantic models
- **Optional web UI:** FastAPI + HTML/JS frontend

## Setup & How to Run

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd kisaaan-project
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_key_here
```
Get a free key at [console.groq.com](https://console.groq.com).

### 5. Run the terminal agent
```bash
python main.py
```

### 6. (Optional) Run the web version
```bash
python web_app.py
```
Then open `http://localhost:8000` in your browser.

## Example Questions to Try

```
Cotton ke liye 5 acre pe kitni fertilizer chahiye?
Kharif season hai, paani kam hai, 3 acre zameen hai, kya lagaun?
Cotton ke pattay peeli ho rahay hain, chitay keeray dikh rahay hain
Cotton ka mandi rate kya hai?
```

## Safety

- Input guardrail rejects non-farming and human-medical questions
- Pesticide dosages are capped to safe, hardcoded limits

## Project Structure

```
kisaaan-project/
├── main.py                  # Entry point — triage agent + specialists
├── agents_setup/
│   ├── agents.py             # Groq model configuration
│   └── guardrails.py         # Input guardrail (off-topic/medical rejection)
├── tools/
│   ├── fertilizer.py
│   ├── crop_advisor.py
│   ├── pest_doctor.py
│   └── mandi_price.py
├── web_app.py                # FastAPI backend (optional bonus)
├── frontend/
│   └── index.html            # Web chat UI (optional bonus)
└── requirements.txt
```

## Data Sources

Currently uses realistic hardcoded lookup tables for crop yields, fertilizer rates, pest/disease treatments, and mandi prices. Can be extended with:
- [Open-Meteo API](https://open-meteo.com/) for real weather data
- [AMIS Punjab](http://www.amis.pk/) for live mandi rates
- [Crop Recommendation Dataset (Kaggle)](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)

## Built For

Kisan Dost Agentic AI Hackathon — Terminal Agent Challenge



## Live Demo
🔗 https://kisan-project.fastapicloud.dev
