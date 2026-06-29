# LeafStep Agent

**LeafStep Agent** is an AI agent that helps households turn a small outdoor space into a safe, low-maintenance, pollinator-friendly microhabitat.

The project was built for the **Google x Kaggle 5-Day AI Agents: Intensive Vibe Coding Capstone**. It demonstrates how an agent can guide a beginner from vague gardening intent to a practical first action plan using structured intake, tool orchestration, safety guardrails, and deployment-ready architecture.

---

## Problem

Many households want to do something positive for the environment but do not know where to start.

Gardening advice can be overwhelming:

* Which plants work in my region?
* What fits a small backyard, balcony, or side strip?
* What is safe if I have pets or kids?
* What should I do in the first 30 days?
* How do I avoid invasive plants or chemical-heavy shortcuts?

LeafStep focuses on a small, realistic starting point: **one tiny household patch**.

Instead of telling users to redesign their whole yard, LeafStep helps them take one practical first step.

---

## Solution

LeafStep Agent collects a simple 6-question intake and turns it into a beginner-friendly microhabitat plan.

The agent can:

* Normalize the user's space, sunlight, safety needs, and starter size
* Recommend region-friendly plants for Oakville / Ontario-style conditions
* Apply pet/kid safety filtering
* Avoid unnecessary exact address collection
* Provide simple impact badges
* Suggest organic soil stewardship actions
* Generate a 30-day beginner care plan
* Run sustainability guardrails against invasive plants and synthetic inputs

---

## Why Agents?

LeafStep is more than a static plant list.

An agent is useful here because the user’s needs are contextual:

* A backyard is different from a balcony
* Full sun is different from shade
* A dog/kid household needs extra safety checks
* A beginner needs a simpler plan than an experienced gardener
* A privacy-aware assistant should not require an exact home address

LeafStep uses tools to break the workflow into reliable steps instead of asking the LLM to invent everything from scratch.

---

## Architecture

```mermaid
flowchart TD
    User[User] --> Agent[LeafStep ADK Agent]

    Agent --> Intake[space_intake_tool]
    Agent --> Recommend[plant_recommendation_tool]
    Agent --> Safety[plant_safety_tool]
    Agent --> Impact[impact_tracking_tool]
    Agent --> Soil[soil_stewardship_tool]
    Agent --> Care[care_plan_tool]
    Agent --> Guardrail[sustainability_guardrail_tool]

    Intake --> Privacy[Privacy Guardrail]
    Recommend --> Plants[Region-Friendly Plant Catalog]
    Safety --> Household[Pet/Kid Safety Rules]
    Guardrail --> Eco[Invasive Plant + Chemical Input Checks]
```

---

## Core Tools

### `space_intake_tool`

Normalizes the 6-question setup:

* Location
* Space type
* Sunlight
* Garden style
* Safety mode
* Starter size

It also includes a privacy guardrail. If a user enters an exact-address-looking location, LeafStep generalizes it to a city/region.

Example:

```text
Input: 123 Maple Street, Oakville
Output region: Oakville
privacy_status: generalize_location
```

### `plant_recommendation_tool`

Recommends plants based on:

* Region
* Space type
* Sunlight
* Garden style
* Starter size

### `plant_safety_tool`

Applies pet/kid safety rules and returns:

* Safe buy list
* Careful placement list
* Do-not-buy list

### `impact_tracking_tool`

Creates simple impact badges:

* Pollinator support
* Water need
* Maintenance
* Native fit
* Biodiversity value
* Tracking action

### `soil_stewardship_tool`

Provides organic soil preparation guidance, including compost, mulch, and low-disturbance soil practices.

### `care_plan_tool`

Creates a beginner-friendly 30-day care plan.

### `sustainability_guardrail_tool`

Checks proposed plants and inputs against ecological safety rules.

It can block:

* Invasive plants such as English ivy
* Synthetic inputs such as Roundup, glyphosate, and chemical pesticides

---

## Safety and Guardrails

LeafStep includes three practical guardrail themes.

### 1. Privacy Guardrail

LeafStep does not need a user’s exact home address.

If a user enters something like:

```text
123 Maple Street, Oakville
```

the tool generalizes the location to:

```text
Oakville
```

and returns a privacy note.

### 2. Household Safety Guardrail

If the user has pets or kids, LeafStep applies safety filtering.

It separates plants into:

* Safe picks
* Careful placement options
* Do-not-buy plants

### 3. Sustainability Guardrail

LeafStep checks against invasive plants and synthetic chemical inputs.

This keeps the agent aligned with the project goal: helping users create small ecological improvements without causing accidental harm.

---

## Course Concepts Demonstrated

This project demonstrates multiple concepts from the Google/Kaggle AI Agents course.

| Concept                | Where it appears                                                          |
| ---------------------- | ------------------------------------------------------------------------- |
| ADK agent              | `app/agent.py`                                                            |
| Tool orchestration     | `app/tools.py`                                                            |
| Gemini / real LLM demo | `run_agent_demo.py`                                                       |
| Guardrails / safety    | `space_intake_tool`, `plant_safety_tool`, `sustainability_guardrail_tool` |
| Agents CLI skills      | `.agents/skills/`                                                         |
| Deployability          | `Dockerfile`, `main.py`, Cloud Run-ready app structure                    |
| Testing                | `tests/unit/test_tools.py`                                                |

---

## Agents CLI Skills

LeafStep uses project-scoped skills as development-time quality gates.

### `leafstep-code-review`

Checks:

* ADK structure
* Tool orchestration
* Guardrail usage
* Tests
* README quality
* Token efficiency
* Secret safety

### `leafstep-submission-review`

Checks:

* Kaggle writeup clarity
* Demo strength
* Architecture explanation
* ADK/Gemini usage
* Skills usage
* Sustainability impact
* Safety guardrails
* Limitations

These skills do not run inside the user-facing product. They support repeatable review workflows while building and preparing the capstone submission.

---

## Demo Options

LeafStep has two demo paths.

### 1. Local deterministic demo

This runs the no-LLM version of the workflow.

```bash
uv run python demo.py
```

Use this when you want a predictable local demo without Gemini credentials.

### 2. Real ADK/Gemini demo

This runs a real ADK/Gemini tool-calling trace and then a deterministic full tool-chain demo.

Set your Gemini API key first:

```bash
export GEMINI_API_KEY="your_api_key_here"
export GOOGLE_GENAI_USE_ENTERPRISE=FALSE
```

Then run:

```bash
uv run python run_agent_demo.py
```

This demo shows:

* Real ADK/Gemini tool call
* Privacy guardrail
* Plant recommendations
* Pet/kid safety filtering
* Impact badges
* Soil guidance
* 30-day care plan
* Sustainability guardrail

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/apoorvadeoai/leafstep-agent.git
cd leafstep-agent
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Run formatting and lint checks

```bash
uv run ruff format .
uv run ruff check . --fix
```

### 4. Run unit tests

```bash
uv run pytest tests/unit
```

### 5. Run local demo

```bash
uv run python demo.py
```

### 6. Run ADK/Gemini demo

```bash
export GEMINI_API_KEY="your_api_key_here"
export GOOGLE_GENAI_USE_ENTERPRISE=FALSE
uv run python run_agent_demo.py
```

---

## Testing

Unit tests cover:

* Exact-address privacy guardrail
* Oakville plant recommendation flow
* Pet/kid safety filtering
* Invasive plant blocking
* Synthetic input blocking
* Safe native plan pass case

Run:

```bash
uv run pytest tests/unit
```

Note: Some integration tests require Google credentials because they call the real ADK/Gemini agent.

---

## Example Scenario

User input:

```text
I live at 123 Maple Street, Oakville.
I have a small backyard patch with part sun.
I have two kids and a dog.
I want low-maintenance pollinator-friendly flowers.
```

LeafStep output:

* Generalizes location to Oakville
* Recommends part-sun pollinator plants
* Applies pet/kid safety filtering
* Returns simple impact badges
* Suggests compost and mulch-based soil prep
* Creates a 30-day care plan

---

## Example Recommended Plants

For an Oakville backyard patch with part sun and flower preference, LeafStep may recommend:

* Wild Bergamot
* Black-eyed Susan
* New England Aster
* Purple Coneflower
* Foamflower

The final list depends on the intake profile and safety filtering.

---

## Deployment

LeafStep is designed to be deployable using a containerized app structure.

Relevant files:

* `Dockerfile`
* `main.py`
* `requirements-cloudrun.txt`
* `app/fast_api_app.py`

A Cloud Run deployment can be added using the Google Cloud project and Gemini configuration.

Important:

Do not commit API keys or secrets to the repository.

Use environment variables for credentials.

---

## Project Structure

```text
leafstep-agent/
├── app/
│   ├── agent.py
│   ├── tools.py
│   ├── fast_api_app.py
│   └── app_utils/
├── tests/
│   ├── unit/
│   │   └── test_tools.py
│   ├── integration/
│   └── eval/
├── .agents/
│   └── skills/
│       ├── leafstep-code-review/
│       └── leafstep-submission-review/
├── docs/
│   ├── skill_usage.md
│   └── workshop_concepts.md
├── demo.py
├── run_agent_demo.py
├── main.py
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## Limitations

LeafStep is a capstone prototype.

Current limitations:

* Plant catalog is intentionally small and focused on Oakville/Ontario-style examples
* Recommendations should be verified before planting
* The agent does not replace professional horticultural, ecological, medical, or veterinary advice
* Pet/kid safety is conservative but not exhaustive
* Local nursery inventory is not currently checked
* MCP is not included in the current version and is a possible future enhancement

---

## Future Improvements

Potential next steps:

* Add MCP server for local native plant and invasive species lookup
* Expand plant catalog with verified Ontario native species
* Add image-based plant identification
* Add local nursery availability
* Add seasonal planting windows
* Add user progress tracking
* Add before/after microhabitat logs
* Add Cloud Run public demo endpoint

---

## Capstone Positioning

**LeafStep Agent: Turning Tiny Yards into Safe Pollinator Microhabitats**

LeafStep helps beginners convert a small household green space into a native, low-maintenance, pet/kid-aware, pollinator-supporting patch using an ADK-powered agent, structured tools, practical guardrails, and deployment-ready design.
