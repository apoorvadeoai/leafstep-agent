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

This file defines the LeafStep coordinator agent and registers one demo-safe
ADK web tool. The full planning workflow still runs through the underlying
LeafStep tools, but the LLM only sees one simple wrapper tool.
"""

import os

import google.auth
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.tools import leafstep_full_plan_tool


try:
    _, project_id = google.auth.default()
    if project_id:
        os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
except Exception:
    pass


if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
else:
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        os.environ["GOOGLE_CLOUD_PROJECT"] = "mock-project"
    os.environ["GOOGLE_CLOUD_LOCATION"] = "global"


LEAFSTEP_INSTRUCTION = """You are LeafStep Agent, a beginner-friendly garden planning assistant for Oakville, Ontario.

Use `leafstep_full_plan_tool` for planning requests. It runs the full workflow: intake, privacy generalization, plant recommendation, pet/kid safety, impact, soil guidance, care plan, and sustainability guardrail.

Do not call separate internal tools. Do not invent plant names. Use the tool result as the source of truth.

If the user gives an exact address, pass it to the tool, but do not repeat the exact address in the final answer.

Final answer format:
- Space Profile
- Recommended Plants
- Safety Check
- Soil Step
- First-Week Care
- Impact
- Sustainability Guardrail

Keep the answer short and practical.
"""


root_agent = Agent(
    name="leafstep_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=LEAFSTEP_INSTRUCTION,
    tools=[
        leafstep_full_plan_tool,
    ],
)


app = App(
    root_agent=root_agent,
    name="app",
)