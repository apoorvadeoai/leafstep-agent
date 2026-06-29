"""Day 3 validation checks for LeafStep.

Usage:
    uv run python validate_day3.py
"""

import importlib.util
import os

_tools_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "app", "tools.py"
)
_spec = importlib.util.spec_from_file_location("app.tools", _tools_path)
_tools = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_tools)


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run_validation() -> None:
    profile = _tools.space_intake_tool(
        location="Oakville, Ontario",
        space_type="Backyard",
        sunlight="Full sun — 6+ hours",
        garden_style="More flowers",
        safety_mode="Dogs / cats",
        starter_size="Small — 5 small plants",
    )

    assert_true(
        profile["space_type"] == "backyard", "space_type should normalize to backyard"
    )
    assert_true(
        profile["sunlight"] == "full_sun", "sunlight should normalize to full_sun"
    )
    assert_true(
        profile["garden_style"] == "flowers", "garden_style should normalize to flowers"
    )
    assert_true(
        profile["safety_mode"] == "pets", "safety_mode should normalize to pets"
    )
    assert_true(profile["plant_count_target"] == 5, "plant_count_target should be 5")

    recommendations = _tools.plant_recommendation_tool(
        region=profile["region"],
        space_type=profile["space_type"],
        sunlight=profile["sunlight"],
        garden_style=profile["garden_style"],
        plant_count_target=profile["plant_count_target"],
    )

    assert_true(
        len(recommendations["recommended_plants"]) >= 5,
        "recommendations should return at least 5 plants",
    )

    safety = _tools.plant_safety_tool(
        recommended_plants=recommendations["recommended_plants"],
        safety_mode=profile["safety_mode"],
        plant_count_target=profile["plant_count_target"],
    )

    buy_names = {plant["common_name"] for plant in safety["buy_list"]}
    avoid_names = {plant["common_name"] for plant in safety["do_not_buy_list"]}

    assert_true("Foxglove" not in buy_names, "Foxglove must not be in buy list")
    assert_true(
        "Lily of the Valley" not in buy_names,
        "Lily of the Valley must not be in buy list",
    )
    assert_true("Foxglove" in avoid_names, "Foxglove should appear in avoid list")

    impact = _tools.impact_tracking_tool(
        buy_list=safety["buy_list"],
        careful_placement_list=safety["careful_placement_list"],
    )

    allowed_pollinator = {"Low", "Medium", "High"}
    allowed_water = {"Low", "Medium", "High"}
    allowed_maintenance = {"Low", "Medium", "High"}
    allowed_native = {"Weak", "Good", "Strong"}

    assert_true(
        impact["pollinator_support"] in allowed_pollinator, "invalid pollinator band"
    )
    assert_true(impact["water_need"] in allowed_water, "invalid water band")
    assert_true(
        impact["maintenance"] in allowed_maintenance, "invalid maintenance band"
    )
    assert_true(impact["native_fit"] in allowed_native, "invalid native fit band")

    print("✅ LeafStep Day 3 validation passed.")


if __name__ == "__main__":
    run_validation()
