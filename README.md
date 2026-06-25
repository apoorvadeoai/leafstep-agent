# LeafStep Agent

LeafStep is an AI habitat coach that helps people take one small, practical step toward creating pollinator-friendly, water-saving, low-maintenance green spaces using native or region-friendly plants.

This project was built for the **Google 5-Day Gen AI / Vibe Coding Capstone** using the **Google Agent Development Kit (ADK)** and `agents-cli`.

LeafStep focuses on simple, action-oriented recommendations. Instead of giving long gardening reports, the agent guides the user through a short setup flow and returns a crisp 30-second plan: what to buy, what to avoid, what impact it creates, and what to do this week.

---

## Project Goal

LeafStep helps users improve everyday spaces such as:

* Backyards
* Front yards
* Balconies / patios
* Side yard strips
* Community gardens

The default LeafStep goal is always:

* Pollinator-friendly planting
* Lower water needs
* Lower maintenance
* Native or region-friendly plants
* Better ecosystem balance
* Lifecycle tracking for future biodiversity insights

---

## Day 1–3 Progress

### Day 1 — ADK Agent Foundation

Built the initial LeafStep ADK agent and local no-LLM demo.

Completed:

* Created the LeafStep agent structure.
* Added the first ecosystem tools.
* Built a local `demo.py` flow.
* Verified the project can run without needing Gemini/API calls for the demo path.
* Established the capstone direction: native/pollinator-friendly habitat planning.

### Day 2 — Guided Recommendations + Safety + Impact

Upgraded LeafStep from a basic demo into a more product-like workflow.

Completed:

* Replaced open-ended intake with a 6-question guided setup.
* Added richer plant recommendation logic.
* Added diverse plant metadata across flowers, leafy plants, grasses, and edible/fruiting plants.
* Added pet/kid safety filtering.
* Added “Plants to buy / Careful placement / Avoid” safety output.
* Replaced numeric habitat scores with easy impact badges.
* Updated the agent instruction to produce short, action-card style answers.

### Day 3 — Validation + Judge-Ready Demo

Improved reliability and demo readiness.

Completed:

* Added `validate_day3.py` to test core tool behavior.
* Validated guided setup normalization.
* Validated plant recommendations return useful results.
* Validated dangerous plants do not appear in the buy list.
* Validated impact badges use simple bands.
* Updated `demo.py` for the Day 2/Day 3 guided LeafStep workflow.

---

## Project Structure

```text
leafstep-agent/
├── app/
│   ├── __init__.py
│   ├── agent.py               # Main ADK agent definition and LeafStep coordinator instructions
│   ├── tools.py               # LeafStep tools for intake, recommendations, safety, impact, soil, care, and guardrails
│   └── app_utils/             # Scaffolding utilities
├── demo.py                    # Local no-LLM guided LeafStep demo
├── validate_day3.py           # Day 3 validation checks
├── requirements.txt           # Python dependency file
├── pyproject.toml             # Project config and dependencies
└── README.md                  # Project documentation
```

---

## LeafStep Input Flow

LeafStep uses a short 6-question setup.

### Q1/6 — Location

```text
A. Use my location
B. I’ll type my city
```

LeafStep does not need an exact address. City or general region is enough.

### Q2/6 — Space

```text
A. Backyard
B. Front yard
C. Balcony / patio
D. Side yard / small strip
E. Community garden
F. Other / I’ll type it
```

### Q3/6 — Sunlight

```text
A. Full sun — 6+ hours
B. Part sun — 2–3 hours
C. Mostly shade — little direct sun
D. Other / I’ll type it
```

### Q4/6 — Garden Style

```text
A. More flowers
B. More leafy green plants
C. More fruits / edible plants
D. Balanced mix
E. Surprise me
F. Other / I’ll type it
```

### Q5/6 — Safety

```text
A. Dogs / cats
B. Kids
C. Both pets and kids
D. None
E. Something else / I’ll type it
```

### Q6/6 — Starter Size

```text
A. Tiny — 2 small plants
B. Small — 5 small plants
C. Medium — about 10 plants
D. Large — 15+ plants
E. Other / I’ll type it
```

---

## LeafStep Tools

LeafStep uses tools instead of one free-form answer. This keeps the workflow structured, testable, and easier to improve.

### 1. `space_intake_tool`

Normalizes the 6-question setup into a structured profile.

It converts user choices into values such as:

* Region
* Space type
* Sunlight
* Garden style
* Safety mode
* Starter size
* Plant count target

### 2. `plant_recommendation_tool`

Recommends native or region-friendly plants based on:

* Region
* Space type
* Sunlight
* Garden style
* Starter size

The plant catalog includes diverse options across:

* Flowers
* Leafy / texture plants
* Native grasses
* Edible / fruiting plants
* Shade-friendly plants
* Balcony/patio-friendly plants

### 3. `plant_safety_tool`

Applies pet/kid safety rules.

It separates recommendations into:

* `Plants to buy`
* `Careful placement`
* `Avoid`

Dangerous plants must never appear in the main buy list.

### 4. `impact_tracking_tool`

Creates simple impact badges instead of numeric scores.

LeafStep shows:

* Pollinator support: Low / Medium / High
* Water need: Low / Medium / High
* Maintenance: Low / Medium / High
* Native fit: Weak / Good / Strong
* Tracking action

### 5. `soil_stewardship_tool`

Provides soil-supporting actions such as:

* Mulching exposed soil
* Adding compost
* Avoiding synthetic chemicals
* Supporting soil structure and moisture retention

### 6. `care_plan_tool`

Generates simple next actions for getting plants established.

The final user output stays short unless the user asks for more detail.

### 7. `sustainability_guardrail_tool`

Checks recommendations against ecological safety rules.

It blocks:

* Known invasive species
* Synthetic pesticides
* Synthetic herbicides
* Non-organic soil inputs

---

## Example Output

```text
🌿 LeafStep Plan

Best next step:
Start a 5-plant flower patch in your backyard.

Plants to buy:
✅ Wild Bergamot
✅ Black-eyed Susan
✅ Purple Coneflower
✅ New England Aster
✅ Dense Blazing Star

Careful placement:
⚠️ Butterfly Milkweed — keep away from chewing or digging.

Avoid:
❌ Foxglove
❌ Lily of the Valley
❌ Daffodil bulbs

Impact:
🦋 Pollinator support: High ✅
💧 Water need: Low ✅
🧤 Maintenance: Low ✅
🌱 Native fit: Strong ✅

This week:
1. Pick one sunny patch
2. Place plants before digging
3. Add compost + mulch
4. Water deeply once

Track:
📸 Take a first photo and log first bloom or new growth later.
```

---

## Setup

### 1. Install dependencies

Recommended:

```bash
uv pip install -r requirements.txt
```

Alternative:

```bash
pip install -r requirements.txt
```

---

## Running the Local Demo

The local demo does not require Gemini/API calls.

Run:

```bash
uv run python demo.py
```

This prints the guided LeafStep setup and a short action-card recommendation.

---

## Running Validation

Run:

```bash
uv run python validate_day3.py
```

Expected result:

```text
✅ LeafStep Day 3 validation passed.
```

The validation script checks:

* Guided setup normalization
* Plant recommendation results
* Safety filtering
* Dangerous plants excluded from the buy list
* Impact badge values

---

## Running the ADK Playground

To test the interactive ADK agent:

```bash
agents-cli playground
```

This launches a browser-based UI to chat with LeafStep Agent locally.

---

## Credentials / API Key

The local demo and validation script do not require Gemini credentials.

To use the full ADK agent with an LLM backend, configure credentials.

### Option A: Google AI Studio API Key

```bash
export GEMINI_API_KEY="your_api_key_here"
```

### Option B: Google Cloud / Vertex AI

```bash
gcloud auth login --update-adc
export GOOGLE_CLOUD_PROJECT="your_gcp_project_id"
```

---

## Core Workshop Concepts Used

LeafStep demonstrates:

* ADK agent design
* Tool/function calling
* Structured input normalization
* Rich domain data inside tools
* Safety guardrails
* Prompt/output control
* Validation/testing
* Product-focused AI workflow design

---

## Safety and Privacy Rules

LeafStep avoids unnecessary personal information.

It should not ask for:

* Exact address
* Phone number
* Private family details
* Unneeded personal data

If pets or kids are selected, safety filtering must run before the final recommendation.

Dangerous plants should be shown under `Avoid`, not in the buy list.

---

## Future Vision

LeafStep can grow into a social plant community where users track:

* Plant lifecycle
* First bloom
* First fruit
* Pollinator visits
* Plant survival
* Regional biodiversity trends
* Watering frequency
* Maintenance effort

Over time, these observations could help communities understand which native or region-friendly plants thrive in their area and how small green spaces contribute to biodiversity recovery.
