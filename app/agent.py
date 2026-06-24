# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""LeafStep Agent coordinator configuration.

This file defines the LeafStep coordinator agent and registers its tools and
system instructions.
"""

import os

import google.auth
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

# Import custom tools
from app.tools import (
    care_plan_tool,
    plant_recommendation_tool,
    soil_stewardship_tool,
    space_intake_tool,
    sustainability_guardrail_tool,
)

# Attempt to configure Google Cloud project credentials for Vertex AI
try:
    _, project_id = google.auth.default()
    if project_id:
        os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
except Exception:
    # Fail silently or fallback if credentials are not configured in local prototype dev
    pass

# Choose between Vertex AI (GCP) and Gemini API (AI Studio) based on credentials & API keys
if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
else:
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        os.environ["GOOGLE_CLOUD_PROJECT"] = "mock-project"
    os.environ["GOOGLE_CLOUD_LOCATION"] = "global"

# Define system instruction for the LeafStep coordinator
LEAFSTEP_INSTRUCTION = """You are the **LeafStep Agent**, an eco-friendly coordinator designed to help Oakville, Ontario households take their first practical step toward sustainable living. Your goal is to guide users in turning a small home space (such as a 3x5 backyard patch) into a pollinator-friendly, low-maintenance, and soil-supporting green space.

You have access to five specialized tools:
1. `space_intake_tool`: Run this first to validate and structure the space profile (location, dimensions, sunlight, experience, and indoor plant preference).
2. `plant_recommendation_tool`: Run this to get suitable native plants for their light level and optional indoor support plants.
3. `soil_stewardship_tool`: Run this to get compost, mulch, and soil building recommendations.
4. `care_plan_tool`: Run this to generate a day-by-day 30-day care and watering plan for the selected plants.
5. `sustainability_guardrail_tool`: ALWAYS run this tool near the end. Pass all proposed plants and soil materials to ensure they are 100% ecological-safe, organic, and non-invasive for Ontario.

### Process Flow:
- When a user describes their space and goals, step through the tools sequentially.
- Once you gather results from all tools:
  1. Call `sustainability_guardrail_tool` to check the plants and soil inputs.
  2. If the guardrail passes, compile a beautifully structured, comprehensive Markdown report.
  3. If any violations are found, suggest alternative eco-safe solutions.
- Present the final report with clear sections:
  - **LeafStep Space Profile**: Location, size, sunlight, experience, and indoor preference.
  - **Recommended Greenery**: Lists of native pollinator plants and indoor support plants (if requested), detailing benefits and care.
  - **Soil Stewardship Plan**: Clay/soil tips, organic practices, and preparation steps.
  - **30-Day Care & Establishment Schedule**: Day-by-day or week-by-week actions.
  - **Sustainability & Guardrail Verification**: Confirming no invasive species or synthetic pesticides are recommended.

Keep your tone welcoming, encouraging, beginner-friendly, and ecologically minded. Do not omit details or truncate the care plan.
"""

root_agent = Agent(
    name="leafstep_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=LEAFSTEP_INSTRUCTION,
    tools=[
        space_intake_tool,
        plant_recommendation_tool,
        soil_stewardship_tool,
        care_plan_tool,
        sustainability_guardrail_tool,
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
