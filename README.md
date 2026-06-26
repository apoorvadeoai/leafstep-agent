# LeafStep Agent

LeafStep is an AI habitat coach for Oakville, Ontario households.

It helps people take one small, practical first step toward creating pollinator-friendly, low-maintenance, soil-supporting green spaces using native or region-friendly plants.

This project was built for the **Google 5-Day Gen AI / Vibe Coding Capstone** using the **Google Agent Development Kit (ADK)**, `agents-cli`, local tools, project skills, validation scripts, and a Cloud Run deployment.

LeafStep is intentionally scoped. It does not try to be a generic global gardening app. The current recommendations are optimized for **Oakville / Ontario conditions**.

---

## Project Goal

LeafStep helps users improve everyday spaces such as:

* Small backyard patches
* Front yard patches
* Balconies / patios
* Side yard strips
* Container gardens
* Small community garden plots

The default LeafStep goal is always:

* Support pollinators
* Reduce exposed soil
* Encourage native or region-friendly plants
* Lower maintenance burden
* Reduce synthetic chemical use
* Help households take one realistic first step

Instead of producing long gardening reports, LeafStep guides the user toward a concise starter plan: what to plant, what to avoid, what safety checks apply, what impact it creates, and what to do this week.

---

## Current Demo Scope

The public Cloud Run demo is a lightweight, interactive version of LeafStep that works without live Gemini API credits.

It asks only the inputs that matter for the current demo:

1. Location — fixed as **Oakville, Ontario**
2. Space size/type
3. Sunlight
4. Whether pets or small children are present

The deployed demo uses LeafStep’s deterministic local tools so reviewers can test the product flow without depending on API quota.

The full ADK/Gemini agent is available in `app/agent.py` and can be run locally with a Gemini API key.

---

## Day 1–5 Progress

### Day 1 — ADK Agent Foundation

Completed:

* Created the LeafStep ADK agent structure.
* Added the first ecosystem tools.
* Built a local `demo.py` flow.
* Verified the project can run without Gemini/API calls for the deterministic demo path.
* Established the capstone direction: practical native/pollinator-friendly habitat planning.

### Day 2 — Guided Recommendations, Safety, and Impact

Completed:

* Replaced open-ended responses with a structured recommendation workflow.
* Added richer plant recommendation logic.
* Added plant metadata across flowers, leafy plants, grasses, and edible/fruiting plants.
* Added pet/kid plant safety filtering through `plant_safety_tool`.
* Added “Plants to buy / Careful placement / Avoid” safety output.
* Replaced numeric habitat scores with simple impact badges.
* Updated the agent instruction to produce short, action-card style answers.

### Day 3 — Validation and Judge-Ready Demo

Completed:

* Added `validate_day3.py` to test core tool behavior.
* Validated setup normalization.
* Validated plant recommendations return useful results.
* Validated dangerous plants do not appear in the buy list.
* Validated impact badges use simple bands.
* Updated `demo.py` for the guided LeafStep workflow.

### Day 4 — LLM-backed ADK Flow and Skills

Completed:

* Tested LeafStep in ADK Web with a Gemini-backed prompt flow.
* Confirmed the agent accepts user input and returns a practical first-step plan.
* Reduced token usage in the agent instruction.
* Added project-specific skills:

  * `.agents/skills/leafstep-code-review/`
  * `.agents/skills/leafstep-submission-review/`
* Added `docs/skill_usage.md`.
* Added `docs/workshop_concepts.md`.
* Added `validate_day4.py`.

### Day 5 — Cloud Run Deployment and Final Capstone Package

Completed:

* Added `main.py` as a lightweight FastAPI Cloud Run demo.
* Added `requirements-cloudrun.txt`.
* Updated `Dockerfile` for Cloud Run deployment.
* Added `validate_day5.py`.
* Added deployment-ready documentation.
* Preserved the full ADK/Gemini agent in `app/agent.py`.
* Created a public demo path that can run without consuming Gemini credits.

---

## Project Structure

```text
leafstep-agent/
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── tools.py
│   └── app_utils/
├── .agents/
│   └── skills/
│       ├── leafstep-code-review/
│       └── leafstep-submission-review/
├── docs/
│   ├── skill_usage.md
│   └── workshop_concepts.md
├── demo.py
├── main.py
├── validate_day3.py
├── validate_day4.py
├── validate_day5.py
├── Dockerfile
├── requirements.txt
├── requirements-cloudrun.txt
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## LeafStep Tools

LeafStep uses tools instead of relying on one free-form answer. This keeps the workflow structured, testable, and easier to improve.

### 1. `space_intake_tool`

Normalizes the user’s space information into a structured profile.

It handles:

* Location
* Space type or dimensions
* Sunlight
* Experience level when needed
* Indoor support preference when needed

For the current Cloud Run demo, location is fixed to **Oakville, Ontario**, experience defaults to `beginner`, and indoor support defaults to `False`.

### 2. `plant_recommendation_tool`

Recommends suitable plants based on sunlight and user context.

The plant catalog includes options across:

* Native / region-friendly flowers
* Leafy or texture plants
* Native grasses
* Edible / fruiting plants
* Shade-friendly plants
* Balcony or patio-friendly plants

### 3. `plant_safety_tool`

Applies pet and child safety rules.

It separates recommendations into:

* Plants to buy
* Careful placement
* Avoid

Dangerous or higher-risk plants should not appear in the main buy list when pets or children are present.

### 4. `impact_tracking_tool`

Creates simple impact badges instead of numeric scores.

LeafStep can summarize:

* Pollinator support
* Water need
* Maintenance level
* Native fit
* Tracking action

This helps users understand the value of a small first step without overwhelming them.

### 5. `soil_stewardship_tool`

Provides soil-supporting actions such as:

* Adding compost
* Mulching exposed soil
* Avoiding synthetic chemicals
* Supporting moisture retention
* Improving soil structure over time

### 6. `care_plan_tool`

Generates simple care guidance for selected plants.

By default, LeafStep summarizes the first-week care steps. It should only provide a full 30-day plan if the user explicitly asks.

### 7. `sustainability_guardrail_tool`

Checks recommendations against ecological safety rules.

It blocks or flags:

* Known invasive species
* Synthetic pesticides
* Synthetic herbicides
* Non-organic soil inputs

This guardrail should run before final recommendations are presented.

---

## Example Output

```text
🌿 LeafStep Starter Plan

Space:
Oakville, Ontario
Small sunny backyard patch
Pets or small children: Yes

Best next step:
Start a small pollinator patch with beginner-friendly outdoor plants.

Plants to buy:
✅ Wild Bergamot
✅ Black-eyed Susan
✅ Purple Coneflower
✅ New England Aster
✅ Dense Blazing Star

Plant safety:
✅ No high-risk plants detected in the main buy list.
⚠️ Keep all new plants, tags, soil amendments, and mulch away from chewing pets or small children.

Soil step:
Add compost lightly and mulch exposed soil with shredded leaves or natural mulch.

This week:
1. Pick one sunny patch.
2. Remove weeds.
3. Place plants before digging.
4. Add compost and mulch.
5. Water deeply after planting.

Impact:
🦋 Pollinator support: High
💧 Water need: Low
🧤 Maintenance: Low
🌱 Native fit: Strong

Sustainability guardrail:
✅ No invasive plants or synthetic inputs recommended.
```

---

## Setup

### Install dependencies

Recommended:

```bash
uv pip install -r requirements.txt
```

Alternative:

```bash
pip install -r requirements.txt
```

---

## Running the Local No-LLM Demo

The local deterministic demo does not require Gemini/API calls.

Run:

```bash
uv run python demo.py
```

This prints a guided LeafStep recommendation using local tools.

---

## Running Validations

Run:

```bash
uv run python validate_day3.py
uv run python validate_day4.py
uv run python validate_day5.py
```

Expected result:

```text
✅ validation passed
```

The validation scripts check:

* Tool behavior
* Plant recommendation output
* Safety filtering
* Impact badge output
* Demo readiness
* Cloud Run wrapper readiness

---

## Running the ADK/Gemini Agent Locally

The real ADK agent lives in:

```text
app/agent.py
```

To run it with Gemini:

```bash
export GEMINI_API_KEY="your_api_key_here"
export GOOGLE_GENAI_USE_VERTEXAI=FALSE
uv run adk web --port 8000
```

Example prompt:

```text
I live in Oakville. I have a small sunny 3x5 backyard patch and pets. Give me one simple first-week pollinator plan.
```

Note: entering prompts in ADK Web uses Gemini/API quota.

---

## Running the Cloud Run Demo Locally

The Cloud Run demo uses FastAPI and local tools.

Run:

```bash
uv run uvicorn main:app --reload --port 8080
```

Open:

```text
http://localhost:8080
```

Useful endpoints:

```text
/
Interactive demo page

/demo
Text version of the local demo

/health
Health check endpoint
```

---

## Deploying to Cloud Run

Deploy from Google Cloud Shell or a terminal with `gcloud` configured:

```bash
gcloud run deploy leafstep-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

The deployed Cloud Run demo is intentionally lightweight and does not require Gemini credits.

---

## Credentials / API Key

The local deterministic demo, validation scripts, and Cloud Run demo do not require Gemini credentials.

To use the full ADK/Gemini agent, configure credentials.

### Option A: Google AI Studio API Key

```bash
export GEMINI_API_KEY="your_api_key_here"
export GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

### Option B: Google Cloud / Vertex AI

```bash
gcloud auth application-default login
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT="your_gcp_project_id"
export GOOGLE_CLOUD_LOCATION="us-central1"
```

Do not commit `.env` or API keys.

---

## Core Workshop Concepts Used

LeafStep demonstrates:

* Google ADK agent design
* Tool/function calling
* Structured input normalization
* Local deterministic tools
* LLM-backed ADK flow
* Safety guardrails
* Pet/child-aware plant safety filtering
* Sustainability guardrails
* Skills
* Validation scripts
* Cloud Run deployment
* Product-focused AI workflow design

---

## Project Skills

LeafStep includes two project-specific skills:

```text
.agents/skills/leafstep-code-review/
.agents/skills/leafstep-submission-review/
```

These skills support:

* Reviewing code changes
* Checking capstone readiness
* Verifying docs, tools, validation, and demo flow
* Keeping the project aligned with its Oakville sustainability scope

See:

```text
docs/skill_usage.md
```

---

## Safety and Privacy Rules

LeafStep avoids unnecessary personal information.

It should not ask for:

* Exact address
* Phone number
* Private family details
* Unneeded personal data

If pets or small children are present, plant safety filtering should run before the final recommendation.

Dangerous plants should be shown under `Avoid`, not in the main buy list.

LeafStep gives beginner gardening guidance. It does not provide veterinary, medical, or poison-control advice.

---

## Current Limitations

LeafStep is currently optimized for Oakville / Ontario conditions.

The Cloud Run demo uses deterministic local tools to avoid Gemini quota dependency.

The ADK/Gemini version requires a valid Gemini API key or Vertex AI setup.

Plant safety rules are educational and should not replace professional advice for pet poisoning, child ingestion, allergies, or medical emergencies.

---

## Future Vision

LeafStep can grow into a community plant-tracking product where users log:

* Plant survival
* First bloom
* First fruit
* Pollinator visits
* Watering frequency
* Maintenance effort
* Soil coverage
* Regional biodiversity patterns

Over time, these observations could help communities understand which native or region-friendly plants thrive locally and how small household spaces contribute to biodiversity recovery.
