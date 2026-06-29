# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0

"""Run the LeafStep demo with both ADK/Gemini and deterministic tool chaining.

This script is intentionally separate from demo.py.

- demo.py runs the original deterministic no-LLM local demo.
- run_agent_demo.py shows:
  1. A real ADK/Gemini tool-calling trace.
  2. A deterministic full LeafStep tool chain for judges.

Before running with a Gemini API key, set:

    export GEMINI_API_KEY="your_api_key_here"
    export GOOGLE_GENAI_USE_ENTERPRISE=FALSE

Then run:

    uv run python run_agent_demo.py
"""

from typing import Any

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import root_agent
from app.tools import (
    care_plan_tool,
    impact_tracking_tool,
    plant_recommendation_tool,
    plant_safety_tool,
    soil_stewardship_tool,
    space_intake_tool,
    sustainability_guardrail_tool,
)

APP_NAME = "leafstep_agent_demo"
USER_ID = "demo_user"


DEMO_PROMPT = """
Plan a first LeafStep for this household.

Use these exact intake details:
- Location: 123 Maple Street, Oakville
- Space type: backyard patch
- Sunlight: part sun
- Garden style: flowers
- Safety mode: pets and kids
- Starter size: small

Please call the LeafStep tools to:
1. Normalize the intake.
2. Recommend plants.
3. Apply the pet/kid safety filter.
4. Create impact tracking badges.
5. Create soil stewardship guidance.
6. Create a 30-day care plan.
7. Run the sustainability guardrail check.

Then give a short final summary for a beginner.
"""


def _print_section(title: str) -> None:
    """Print a readable demo section header."""

    print(f"\n{title}")
    print("=" * len(title))


def _print_dict(title: str, data: dict[str, Any]) -> None:
    """Print compact dictionary output for demo readability."""

    print(f"\n{title}")
    print("-" * len(title))
    print(data)


def run_real_adk_demo() -> None:
    """Run one real ADK/Gemini demo conversation and print text/tool events."""

    session_service = InMemorySessionService()
    session = session_service.create_session_sync(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=DEMO_PROMPT)],
    )

    _print_section("LeafStep ADK/Gemini Tool Trace")
    print("\nUser prompt:")
    print(DEMO_PROMPT.strip())
    print("\nAgent response / tool trace:")
    print("-" * 40)

    events = runner.run(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    )

    printed_any_output = False

    for event in events:
        if not event.content or not event.content.parts:
            continue

        for part in event.content.parts:
            if part.text:
                printed_any_output = True
                print(part.text)

            if part.function_call:
                printed_any_output = True
                print(f"\nTool call: {part.function_call.name}")
                print(part.function_call.args)

            if part.function_response:
                printed_any_output = True
                print(f"\nTool response: {part.function_response.name}")
                print(part.function_response.response)

    if not printed_any_output:
        print(
            "No text, tool call, or tool response was returned. "
            "Check Gemini credentials and ADK agent configuration."
        )


def run_full_tool_chain_demo() -> None:
    """Run the complete LeafStep workflow deterministically using project tools."""

    _print_section("LeafStep Full Tool Chain Demo")

    intake = space_intake_tool(
        location="123 Maple Street, Oakville",
        space_type="backyard patch",
        sunlight="part sun",
        garden_style="flowers",
        safety_mode="pets and kids",
        starter_size="small",
    )
    _print_dict("1. Intake + privacy guardrail", intake)

    recommendations = plant_recommendation_tool(
        region=intake["region"],
        space_type=intake["space_type"],
        sunlight=intake["sunlight"],
        garden_style=intake["garden_style"],
        plant_count_target=intake["plant_count_target"],
    )
    _print_dict("2. Plant recommendations", recommendations)

    safety = plant_safety_tool(
        recommended_plants=recommendations["recommended_plants"],
        safety_mode=intake["safety_mode"],
        plant_count_target=intake["plant_count_target"],
    )
    _print_dict("3. Pet/kid safety filter", safety)

    impact = impact_tracking_tool(
        buy_list=safety["buy_list"],
        careful_placement_list=safety["careful_placement_list"],
    )
    _print_dict("4. Impact tracking badges", impact)

    soil = soil_stewardship_tool(
        location=intake["region"],
        space_type=intake["space_type"],
    )
    _print_dict("5. Soil stewardship guidance", soil)

    plant_names = [plant["common_name"] for plant in safety["buy_list"]]
    care = care_plan_tool(
        plants=plant_names,
        experience_level="beginner",
    )
    _print_dict("6. 30-day care plan", care)

    guardrail = sustainability_guardrail_tool(
        proposed_plants=plant_names,
        proposed_inputs=["leaf compost", "shredded leaves"],
    )
    _print_dict("7. Sustainability guardrail", guardrail)

    print("\nBeginner summary")
    print("----------------")
    print(
        "LeafStep converted an exact-address input into a general Oakville region, "
        "recommended five part-sun pollinator-friendly plants, applied pet/kid "
        "safety filtering, added impact badges, and produced soil and 30-day care "
        "guidance without needing private address details."
    )


def main() -> None:
    """Run both the real ADK trace and the deterministic full tool chain."""

    run_real_adk_demo()
    run_full_tool_chain_demo()


if __name__ == "__main__":
    main()
