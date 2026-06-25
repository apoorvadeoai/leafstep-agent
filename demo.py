# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0

"""LeafStep Agent – Day 2 Local No-LLM Demo.

Runs the Day 2 LeafStep workflow directly:
1. Guided 6-question intake
2. Rich plant recommendations
3. Pet/kid safety filtering
4. Impact badges
5. Short action-card output

Usage:
    uv run python demo.py
"""

import importlib.util
import os

# Import tools.py directly so app/__init__.py and google.adk are not triggered.
_tools_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "tools.py")
_spec = importlib.util.spec_from_file_location("app.tools", _tools_path)
_tools = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_tools)

space_intake_tool = _tools.space_intake_tool
plant_recommendation_tool = _tools.plant_recommendation_tool
plant_safety_tool = _tools.plant_safety_tool
impact_tracking_tool = _tools.impact_tracking_tool
soil_stewardship_tool = _tools.soil_stewardship_tool
care_plan_tool = _tools.care_plan_tool
sustainability_guardrail_tool = _tools.sustainability_guardrail_tool


SCENARIOS = [
    {
        "name": "Backyard flower patch with pets",
        "location": "Oakville, Ontario",
        "space_type": "Backyard",
        "sunlight": "Full sun — 6+ hours",
        "garden_style": "More flowers",
        "safety_mode": "Dogs / cats",
        "starter_size": "Small — 5 small plants",
    },
    {
        "name": "Shady leafy side strip with kids",
        "location": "Oakville, Ontario",
        "space_type": "Side yard / small strip",
        "sunlight": "Mostly shade — little direct sun",
        "garden_style": "More leafy green plants",
        "safety_mode": "Kids",
        "starter_size": "Tiny — 2 small plants",
    },
    {
        "name": "Balcony edible starter",
        "location": "Toronto, Ontario",
        "space_type": "Balcony / patio",
        "sunlight": "Part sun — 2–3 hours",
        "garden_style": "More fruits / edible plants",
        "safety_mode": "None",
        "starter_size": "Tiny — 2 small plants",
    },
]


def _print_setup(scenario: dict) -> None:
    print("\n🌿 LeafStep Setup\n")
    print("Q1/6 — Where should LeafStep plan for?")
    print("A. Use my location")
    print("B. I’ll type my city")
    print(f"> B — {scenario['location']}\n")

    print("Q2/6 — Where do you want more green?")
    print("A. Backyard")
    print("B. Front yard")
    print("C. Balcony / patio")
    print("D. Side yard / small strip")
    print("E. Community garden")
    print("F. Other / I’ll type it")
    print(f"> A — {scenario['space_type']}\n")

    print("Q3/6 — How much direct sun does it get?")
    print("A. Full sun — 6+ hours")
    print("B. Part sun — 2–3 hours")
    print("C. Mostly shade — little direct sun")
    print("D. Other / I’ll type it")
    print(f"> A — {scenario['sunlight']}\n")

    print("Q4/6 — What look do you want?")
    print("A. More flowers")
    print("B. More leafy green plants")
    print("C. More fruits / edible plants")
    print("D. Balanced mix")
    print("E. Surprise me")
    print("F. Other / I’ll type it")
    print(f"> A — {scenario['garden_style']}\n")

    print("Q5/6 — Should LeafStep avoid plants risky for anyone?")
    print("A. Dogs / cats")
    print("B. Kids")
    print("C. Both pets and kids")
    print("D. None")
    print("E. Something else / I’ll type it")
    print(f"> A — {scenario['safety_mode']}\n")

    print("Q6/6 — How big should your first LeafStep be?")
    print("A. Tiny — 2 small plants")
    print("B. Small — 5 small plants")
    print("C. Medium — about 10 plants")
    print("D. Large — 15+ plants")
    print("E. Other / I’ll type it")
    print(f"> B — {scenario['starter_size']}\n")


def _status_icon(value: str, lower_is_better: bool = False) -> str:
    if lower_is_better:
        if value == "Low":
            return "✅"
        if value == "Medium":
            return "🟡"
        return "❌"

    if value in {"High", "Strong"}:
        return "✅"
    if value in {"Medium", "Good"}:
        return "🟡"
    return "❌"


def run_demo() -> None:
    """Run the Day 2 LeafStep workflow and print a short product-style result."""

    _print_setup(SCENARIOS[0])

    profile = space_intake_tool(
        location=SCENARIOS[0]["location"],
        space_type=SCENARIOS[0]["space_type"],
        sunlight=SCENARIOS[0]["sunlight"],
        garden_style=SCENARIOS[0]["garden_style"],
        safety_mode=SCENARIOS[0]["safety_mode"],
        starter_size=SCENARIOS[0]["starter_size"],
    )

    recommendations = plant_recommendation_tool(
        region=profile["region"],
        space_type=profile["space_type"],
        sunlight=profile["sunlight"],
        garden_style=profile["garden_style"],
        plant_count_target=profile["plant_count_target"],
    )

    safety = plant_safety_tool(
        recommended_plants=recommendations["recommended_plants"],
        safety_mode=profile["safety_mode"],
        plant_count_target=profile["plant_count_target"],
    )

    impact = impact_tracking_tool(
        buy_list=safety["buy_list"],
        careful_placement_list=safety["careful_placement_list"],
    )

    plant_names = [plant["common_name"] for plant in safety["buy_list"]]
    careful_names = [plant["common_name"] for plant in safety["careful_placement_list"]]

    soil = soil_stewardship_tool(
        location=profile["region"],
        space_type=profile["space_type"],
    )

    care = care_plan_tool(
        plants=plant_names,
        experience_level="beginner",
    )

    guardrail = sustainability_guardrail_tool(
        proposed_plants=plant_names + careful_names,
        proposed_inputs=["organic compost", "shredded leaf mulch"],
    )

    print("🌿 LeafStep Plan\n")

    print("Best next step:")
    print(
        f"Start a {profile['plant_count_target']}-plant "
        f"{profile['garden_style'].replace('_', ' ')} patch in your "
        f"{profile['space_type'].replace('_', ' ')}.\n"
    )

    print("Plants to buy:")
    for plant in safety["buy_list"]:
        print(f"✅ {plant['common_name']}")

    if safety["careful_placement_list"]:
        print("\nCareful placement:")
        for plant in safety["careful_placement_list"][:2]:
            reason = plant.get("safety_reason", "keep away from pets/kids")
            print(f"⚠️ {plant['common_name']} — {reason}")

    print("\nAvoid:")
    for plant in safety["do_not_buy_list"][:3]:
        print(f"❌ {plant['common_name']}")

    print("\nImpact:")
    print(
        f"🦋 Pollinator support: {impact['pollinator_support']} "
        f"{_status_icon(impact['pollinator_support'])}"
    )
    print(
        f"💧 Water need: {impact['water_need']} "
        f"{_status_icon(impact['water_need'], lower_is_better=True)}"
    )
    print(
        f"🧤 Maintenance: {impact['maintenance']} "
        f"{_status_icon(impact['maintenance'], lower_is_better=True)}"
    )
    print(
        f"🌱 Native fit: {impact['native_fit']} "
        f"{_status_icon(impact['native_fit'])}"
    )

    print("\nThis week:")
    print("1. Pick one sunny patch")
    print("2. Place plants before digging")
    print("3. Add compost + mulch")
    print("4. Water deeply once")

    print("\nTrack:")
    print(f"📸 {impact['tracking_action']}")

    print("\nSafety:")
    print(f"{safety['safety_summary']}")
    if guardrail["status"] == "PASS":
        print("✅ Sustainability guardrail passed.")
    else:
        print("⚠️ Sustainability guardrail found issues.")

    print("\nSoil tip:")
    print(f"🌿 {soil['tips'] if 'tips' in soil else 'Mulch exposed soil.'}")

    print()


if __name__ == "__main__":
    run_demo()