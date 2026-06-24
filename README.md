# LeafStep Agent

LeafStep Agent is a capstone agent designed to help Oakville, Ontario households take their first practical step toward sustainable living. It focuses on turning a small 3x5 home space (e.g. backyard patch, garden bed, container) into a pollinator-friendly, low-maintenance, and soil-supporting green space.

This project is built using the **Google Agent Development Kit (ADK)** and the `agents-cli` framework.

## Project Structure

```
leafstep-agent/
├── app/
│   ├── __init__.py
│   ├── agent.py               # Main agent definition & LeafStep coordinator instructions
│   ├── tools.py               # The 5 custom ecosystem tools
│   └── app_utils/             # Scaffolding utilities
├── demo.py                    # Runs the Oakville household scenario demo
├── requirements.txt           # Python dependency file
├── pyproject.toml             # Project config & dependencies
└── README.md                  # This documentation
```

## The 5 Ecosystem Tools

LeafStep Agent orchestrates five local tools:
1.  **Space Intake Tool (`space_intake_tool`)**: Validates and structures the input space information (location, dimensions, sunlight, experience, and indoor support plant flag).
2.  **Ecosystem-Aware Plant Recommendation Tool (`plant_recommendation_tool`)**: Recommends Oakville-native/pollinator-friendly plants (e.g. Butterfly Milkweed, Wild Bergamot) and beginner-friendly indoor support plants (e.g. Spider Plant).
3.  **Soil Stewardship Tool (`soil_stewardship_tool`)**: Recommends organic soil preparation and amendments specific to Halton Region clay soil (e.g. compost top-dressing, leaf mulch, avoiding synthetic fertilizers).
4.  **30-Day Establishment Care Plan Tool (`care_plan_tool`)**: Generates a day-by-day 30-day care and watering plan for the selected plants.
5.  **Sustainability Guardrail Tool (`sustainability_guardrail_tool`)**: Audits proposed plants and materials against Ontario Invasive Species lists and organic stewardship rules (blocking invasive species like Garlic Mustard or chemicals like Glyphosate).

---

## Setup & Running the Demo

### 1. Installation
Install the project dependencies using `uv` (recommended):

```bash
uv pip install -r requirements.txt
```

Alternatively, using standard `pip`:

```bash
pip install -r requirements.txt
```

### 2. Configure Credentials / API Key
To execute the LLM backend of the agent, you need credentials.

#### Option A: Google AI Studio API Key (Recommended for fast local testing)
Set your Gemini API key:
```bash
export GEMINI_API_KEY="your_api_key_here"
```
*(The agent automatically detects the API key and routes requests through Google AI Studio rather than Vertex AI).*

#### Option B: Google Cloud Application Default Credentials (Vertex AI)
Ensure you are authenticated with your Google Cloud account:
```bash
gcloud auth login --update-adc
export GOOGLE_CLOUD_PROJECT="your_gcp_project_id"
```

### 3. Run the Demo
Execute the demo script to run the LeafStep Oakville Beginner backyard scenario:

```bash
uv run python demo.py
```

Or:

```bash
python demo.py
```

### 4. Interactive Testing (Playground)
You can also run the interactive web playground:

```bash
agents-cli playground
```
This launches a browser-based UI to chat with LeafStep Agent locally.
