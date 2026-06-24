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

"""LeafStep Agent – Local No-LLM Demo.

Runs all five LeafStep tools directly (no Gemini / no ADK Runner) and prints
a fully-formatted green space report for an Oakville household scenario.

Usage:
    python demo.py

The ADK project structure (app/agent.py, app/tools.py, etc.) remains intact
and is unaffected by this demo mode.
"""

import importlib.util
import sys
import os

# ── Import tools directly from the source file ──────────────────────────────
# We load tools.py directly rather than via the `app` package so that
# app/__init__.py (which imports agent.py → google.adk) is never triggered.
# This keeps the demo completely dependency-free (no ADK, no Gemini).
_tools_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "tools.py")
_spec = importlib.util.spec_from_file_location("app.tools", _tools_path)
_tools = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_tools)

space_intake_tool = _tools.space_intake_tool
plant_recommendation_tool = _tools.plant_recommendation_tool
soil_stewardship_tool = _tools.soil_stewardship_tool
care_plan_tool = _tools.care_plan_tool
sustainability_guardrail_tool = _tools.sustainability_guardrail_tool

# ─────────────────────────────────────────────
# Scenario: Oakville household, Day 1 prototype
# ─────────────────────────────────────────────
SCENARIO = {
    "location": "Oakville, Ontario",
    "dimensions": "3x5 backyard patch",
    "sunlight": "full sun",
    "experience_level": "beginner",
    "wants_indoor_support": True,
}


def _banner(title: str) -> None:
    """Print a section banner."""
    width = 60
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def _section(title: str) -> None:
    """Print a sub-section header."""
    print(f"\n── {title} {'─' * max(0, 54 - len(title))}")


def run_demo() -> None:
    """Run the full LeafStep workflow and print a formatted report."""

    _banner("🌿  LeafStep Agent – Local Demo  (No-LLM Mode)")
    print(
        "\nThis demo calls every LeafStep tool directly — no Gemini API,\n"
        "no credentials, and no ADK Runner required.\n"
    )

    # ── Step 0: Mission summary ──────────────────────────────────────────
    _banner("MISSION SUMMARY")
    print(
        f"  Location  : {SCENARIO['location']}\n"
        f"  Space     : {SCENARIO['dimensions']}\n"
        f"  Sunlight  : {SCENARIO['sunlight']}\n"
        f"  Experience: {SCENARIO['experience_level']}\n"
        f"  Goal      : Pollinator-friendly · Low-maintenance · Soil-supporting\n"
        f"  Indoor    : {'Yes – starter indoor plants included' if SCENARIO['wants_indoor_support'] else 'No'}"
    )

    # ── Step 1: Space intake ─────────────────────────────────────────────
    _section("STEP 1 · Space Intake & Validation")
    profile = space_intake_tool(
        location=SCENARIO["location"],
        dimensions=SCENARIO["dimensions"],
        sunlight=SCENARIO["sunlight"],
        experience_level=SCENARIO["experience_level"],
        wants_indoor_support=SCENARIO["wants_indoor_support"],
    )
    print(f"  Status        : {profile['status'].upper()}")
    print(f"  Small space?  : {'✔ Yes' if profile['is_small_space'] else '✘ No'}")
    if profile["space_warning"]:
        print(f"  ⚠  {profile['space_warning']}")
    if profile["location_note"]:
        print(f"  ℹ  {profile['location_note']}")

    # ── Step 2: Plant recommendations ────────────────────────────────────
    _section("STEP 2 · Ecosystem-Aware Plant Recommendations")
    plants_data = plant_recommendation_tool(
        sunlight=profile["sunlight"],
        wants_indoor_support=profile["wants_indoor_support"],
    )

    outdoor_plants = plants_data["outdoor_plants"]
    print(f"\n  Sunlight profile: {plants_data['sunlight_profile']}")

    _banner("OUTDOOR PLANT RECOMMENDATIONS  (Ontario Natives)")
    for i, plant in enumerate(outdoor_plants, start=1):
        print(
            f"\n  {i}. {plant['common_name']} ({plant['scientific_name']})\n"
            f"     Benefits : {plant['benefits']}\n"
            f"     Care     : {plant['care']}"
        )

    indoor_plants = plants_data["indoor_plants"]
    _banner("INDOOR SUPPORT PLANTS")
    if indoor_plants:
        for i, plant in enumerate(indoor_plants, start=1):
            print(
                f"\n  {i}. {plant['common_name']} ({plant['scientific_name']})\n"
                f"     Benefits : {plant['benefits']}\n"
                f"     Care     : {plant['care']}"
            )
    else:
        print("  (No indoor plants requested)")

    # ── Step 3: Soil stewardship ─────────────────────────────────────────
    _banner("SOIL STEWARDSHIP PLAN")
    soil_data = soil_stewardship_tool(
        location=profile["location"],
        space_type="backyard patch",
    )
    print(f"\n  Soil profile  : {soil_data['soil_profile']}")
    print(f"  Space type    : {soil_data['space_type']}")
    print("\n  Preparation steps:")
    for i, step in enumerate(soil_data["preparation_steps"], start=1):
        print(f"    {i}. {step}")
    print("\n  Organic practices:")
    for practice in soil_data["organic_practices"]:
        print(f"    • {practice}")
    print(f"\n  💡 Tip: {soil_data['tips']}")

    # ── Step 4: 30-day care plan ─────────────────────────────────────────
    plant_names = [p["common_name"] for p in outdoor_plants]
    _banner("30-DAY ESTABLISHMENT CARE PLAN")
    care_data = care_plan_tool(
        plants=plant_names,
        experience_level=profile["experience_level"],
    )
    print(f"\n  Plants covered  : {', '.join(care_data['target_plants'])}")
    print(f"  Experience level: {care_data['experience_level']}\n")
    for period, instructions in care_data["schedule"].items():
        print(f"  [{period}]\n    {instructions}\n")
    print("  📝 Care tips:")
    for tip in care_data["tips"]:
        print(f"    • {tip}")

    # ── Step 5: Sustainability guardrail ─────────────────────────────────
    all_plant_names = plant_names + [p["common_name"] for p in indoor_plants]
    proposed_inputs = ["organic leaf compost", "shredded leaf mulch", "compost tea"]

    _banner("SUSTAINABILITY GUARDRAIL CHECK")
    guardrail = sustainability_guardrail_tool(
        proposed_plants=all_plant_names,
        proposed_inputs=proposed_inputs,
    )
    status_icon = "✅ PASS" if guardrail["status"] == "PASS" else "❌ FAIL"
    print(f"\n  Overall status: {status_icon}")
    if guardrail["violations"]:
        print("\n  Violations found:")
        for v in guardrail["violations"]:
            print(f"    ⛔ {v}")
    else:
        print("  Invasive species check : PASS  (no invasive plants detected)")
        print("  Chemical inputs check  : PASS  (no synthetic inputs detected)")
    print(f"\n  Recommendation: {guardrail['recommendation']}")

    # ── Final summary ────────────────────────────────────────────────────
    _banner("🌱  LEAFSTEP WORKFLOW COMPLETE")
    print(
        "\n  All five tools executed successfully with zero LLM calls.\n"
        "  Your Oakville green space plan is ready!\n\n"
        "  Next steps:\n"
        "    • Source Ontario-native plugs from a local native plant nursery.\n"
        "    • Pick up organic compost (2-3 bags for a 3x5 space).\n"
        "    • Follow the 30-day care schedule above.\n"
        "    • Run `agents-cli run` when ready to use the full AI-powered agent.\n"
    )
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_demo()
