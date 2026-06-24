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

"""Demo script running a LeafStep Agent scenario.

This script executes one Oakville household scenario using LeafStep Agent.
If no Google Cloud credentials or Gemini API key are found in the environment,
it automatically injects a mock model callback to simulate the ReAct tool-use loop
and print the resulting green space report successfully.
"""

import asyncio
import os
import sys

# Ensure the root leafstep-agent directory is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import google.auth
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import root_agent


async def mock_llm_callback(callback_context, llm_request) -> LlmResponse | None:
    """Interceptors to simulate the model tool call loop when running offline."""
    if not llm_request.contents:
        return None

    last_content = llm_request.contents[-1]
    last_part = last_content.parts[-1] if last_content.parts else None

    # Step 1: Check if the last part is a function response from a tool execution
    if last_part and last_part.function_response:
        resp = last_part.function_response
        name = resp.name

        if name == "space_intake_tool":
            print("[Mock LLM] Space verified. Calling plant_recommendation_tool...")
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[
                        types.Part(
                            function_call=types.FunctionCall(
                                name="plant_recommendation_tool",
                                args={
                                    "sunlight": "full sun",
                                    "wants_indoor_support": True,
                                },
                            )
                        )
                    ],
                ),
                partial=False,
            )

        elif name == "plant_recommendation_tool":
            print("[Mock LLM] Plants recommended. Calling soil_stewardship_tool...")
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[
                        types.Part(
                            function_call=types.FunctionCall(
                                name="soil_stewardship_tool",
                                args={
                                    "location": "Oakville, Ontario",
                                    "space_type": "backyard patch",
                                },
                            )
                        )
                    ],
                ),
                partial=False,
            )

        elif name == "soil_stewardship_tool":
            print("[Mock LLM] Soil guidelines generated. Calling care_plan_tool...")
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[
                        types.Part(
                            function_call=types.FunctionCall(
                                name="care_plan_tool",
                                args={
                                    "plants": [
                                        "Butterfly Milkweed",
                                        "Wild Bergamot",
                                        "Black-eyed Susan",
                                    ],
                                    "experience_level": "beginner",
                                },
                            )
                        )
                    ],
                ),
                partial=False,
            )

        elif name == "care_plan_tool":
            print(
                "[Mock LLM] Care plan generated. Calling sustainability_guardrail_tool..."
            )
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[
                        types.Part(
                            function_call=types.FunctionCall(
                                name="sustainability_guardrail_tool",
                                args={
                                    "proposed_plants": [
                                        "Butterfly Milkweed",
                                        "Wild Bergamot",
                                        "Black-eyed Susan",
                                        "Spider Plant",
                                        "Golden Pothos",
                                    ],
                                    "proposed_inputs": [
                                        "organic leaf compost",
                                        "shredded leaf mulch",
                                    ],
                                },
                            )
                        )
                    ],
                ),
                partial=False,
            )

        elif name == "sustainability_guardrail_tool":
            print(
                "[Mock LLM] Sustainability guardrail passed. Compiling final report..."
            )
            report = """# LeafStep Agent: Oakville Green Space Transition Report

## LeafStep Space Profile
- **Location**: Oakville, Ontario (Zone 6b)
- **Dimensions**: 3x5 backyard patch (Small, manageable starter space)
- **Sunlight**: Full Sun
- **Experience Level**: Beginner
- **Indoor Support Plants**: Yes (Requested)

---

## Recommended Greenery

### Ontario-Native Pollinator Plants (Full Sun)
1. **Butterfly Milkweed** (*Asclepias tuberosa*)
   - *Benefits*: Essential host plant for Monarch butterflies; bright orange blossoms.
   - *Care*: Needs well-drained soil, highly drought-tolerant once established.
2. **Wild Bergamot** (*Monarda fistulosa*)
   - *Benefits*: Attracts bumblebees and butterflies; lavender-colored, fragrant flowers.
   - *Care*: Easy-care, spreads gently to fill out a 3x5 space.
3. **Black-eyed Susan** (*Rudbeckia hirta*)
   - *Benefits*: Resilient nectar source for local bees and butterflies.
   - *Care*: Handles dry soils and heat very well.

### Indoor Support Plants (Starter Greenery)
- **Spider Plant** (*Chlorophytum comosum*)
  - *Benefits*: Beginner-friendly, air-purifying, pet-safe.
  - *Care*: Indirect light, water when top soil feels dry.
- **Golden Pothos** (*Epipremnum aureum*)
  - *Benefits*: Extremely hardy, beautiful trailing foliage.
  - *Care*: Low-light tolerant, low watering needs.

---

## Soil Stewardship Plan
- **Soil Type**: Halton Clay Loam (Typical of Oakville/Halton Region)
- **Preparation Steps**:
  1. *Aerate Gently*: Use a garden fork to loosen soil. Avoid deep tilling.
  2. *Top-dress Compost*: Add 2-3 bags (approx. 2-3 inches) of organic compost to improve drainage and add soil life.
  3. *Mulching*: Cover with shredded leaf mulch to retain moisture and suppress weeds.
- **Organic Practices**: Avoid synthetic fertilizers and chemical weed killers to protect local ground water and earthworms.

---

## 30-Day Care & Establishment Schedule
- **Days 1-3**: Plant plugs, water thoroughly immediately. Keep soil damp.
- **Days 4-7**: Water once every morning. Ensure mulch is kept away from plant stems.
- **Days 8-14**: Water every 2 days if no rain. Hand-weed gently to avoid root disturbance.
- **Days 15-21**: Water twice a week. Spend 5 minutes observing any insect activity.
- **Days 22-30**: Water only during extreme heat. Plants are establishing self-sufficiency.

---

## Sustainability & Guardrail Verification
- **Invasive Species Check**: PASS (None of the proposed plants are invasive in Ontario).
- **Chemical Inputs Check**: PASS (No synthetic fertilizers or toxic pesticides were requested/recommended).
- **Status**: **VERIFIED ECOLOGICALLY SAFE**
"""
            return LlmResponse(
                content=types.Content(role="model", parts=[types.Part(text=report)]),
                partial=False,
            )

    # Step 2: User prompt received (initial model call)
    if last_content.role == "user":
        print("[Mock LLM] Processing user request. Calling space_intake_tool...")
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[
                    types.Part(
                        function_call=types.FunctionCall(
                            name="space_intake_tool",
                            args={
                                "location": "Oakville, Ontario",
                                "dimensions": "3x5 backyard patch",
                                "sunlight": "full sun",
                                "experience_level": "beginner",
                                "wants_indoor_support": True,
                            },
                        )
                    )
                ],
            ),
            partial=False,
        )

    return None


async def run_demo():
    print("====================================================")
    print("Starting LeafStep Agent Oakville Scenario Demo...")
    print("====================================================")

    # 1. Setup in-memory session service
    session_service = InMemorySessionService()
    user_id = "oakville_household_1"
    session_id = "leafstep_session_001"

    await session_service.create_session(
        app_name="app", user_id=user_id, session_id=session_id
    )

    # 2. Instantiate the ADK Runner
    runner = Runner(agent=root_agent, app_name="app", session_service=session_service)

    # Define the Oakville household scenario prompt
    prompt = (
        "I live in Oakville, Ontario and want to start my first green space. "
        "I have a 3x5 backyard patch with full sun. "
        "I am a beginner and want a pollinator-friendly, low-maintenance, "
        "and soil-supporting garden. I would also love to have indoor support plants."
    )

    print(f"\nUser Input:\n{prompt}\n")
    print(
        "Running LeafStep Agent (invoking tools, checking guardrails, generating report)..."
    )

    # 3. Execute the agent asynchronously
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=types.Content(
            role="user", parts=[types.Part.from_text(text=prompt)]
        ),
    ):
        # We print events as they progress to show the agent's actions/thinking
        if event.is_final_response():
            print("\n====================================================")
            print("LEAFSTEP AGENT FINAL REPORT:")
            print("====================================================\n")
            print(event.content.parts[0].text)
            print("\n====================================================")


if __name__ == "__main__":
    # Check if Vertex or Studio API keys are set, activate mock if missing
    has_creds = False
    if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
        has_creds = True
    else:
        try:
            _, project_id = google.auth.default()
            if project_id:
                has_creds = True
        except Exception:
            pass

    if not has_creds:
        print(
            "⚠️  No Google GenAI credentials or API keys found. "
            "Activating offline simulation/dry-run mode..."
        )
        root_agent.before_model_callback = mock_llm_callback
    else:
        print("💡 Credentials found. Running in online mode using Gemini models.")

    asyncio.run(run_demo())
