from app.tools import (
    plant_recommendation_tool,
    plant_safety_tool,
    space_intake_tool,
    sustainability_guardrail_tool,
)


def test_space_intake_generalizes_exact_address() -> None:
    result = space_intake_tool(
        location="123 Maple Street, Oakville",
        space_type="backyard",
        sunlight="part sun",
        garden_style="flowers",
        safety_mode="pets and kids",
        starter_size="small",
    )

    assert result["region"] == "Oakville"
    assert result["location"] == "Oakville"
    assert result["exact_address_needed"] is False
    assert result["possible_exact_address"] is True
    assert result["privacy_status"] == "generalize_location"
    assert "does not need your exact home address" in result["location_note"]


def test_plant_recommendation_returns_matching_oakville_plants() -> None:
    result = plant_recommendation_tool(
        region="Oakville",
        space_type="backyard",
        sunlight="part_sun",
        garden_style="flowers",
        plant_count_target=5,
    )

    assert result["region"] == "Oakville"
    assert result["plant_count_target"] == 5
    assert len(result["recommended_plants"]) == 5

    first_plant = result["recommended_plants"][0]
    assert "common_name" in first_plant
    assert "why" in first_plant
    assert "part_sun" in first_plant["sunlight"]
    assert "backyard" in first_plant["space_fit"]


def test_plant_safety_applies_pets_and_kids_filter() -> None:
    recommended_plants = [
        {
            "common_name": "Butterfly Milkweed",
            "pollinator_support": "High",
            "water_need": "Low",
            "maintenance": "Medium",
            "native_fit": "Strong",
        },
        {
            "common_name": "Black-eyed Susan",
            "pollinator_support": "High",
            "water_need": "Low",
            "maintenance": "Low",
            "native_fit": "Strong",
        },
    ]

    result = plant_safety_tool(
        recommended_plants=recommended_plants,
        safety_mode="pets_and_kids",
        plant_count_target=2,
    )

    assert result["safety_mode"] == "pets_and_kids"
    assert (
        result["safety_summary"] == "Strict safety mode on. Dangerous plants removed."
    )
    assert len(result["buy_list"]) == 2
    assert any(
        plant["common_name"] == "Butterfly Milkweed"
        and plant["safety_label"] == "careful_placement"
        for plant in result["buy_list"]
    )
    assert len(result["do_not_buy_list"]) > 0


def test_sustainability_guardrail_blocks_invasive_plant() -> None:
    result = sustainability_guardrail_tool(
        proposed_plants=["English ivy"],
        proposed_inputs=[],
    )

    assert result["status"] == "FAIL"
    assert any("Invasive Plant Detected" in item for item in result["violations"])


def test_sustainability_guardrail_blocks_synthetic_input() -> None:
    result = sustainability_guardrail_tool(
        proposed_plants=["Wild Bergamot"],
        proposed_inputs=["Roundup"],
    )

    assert result["status"] == "FAIL"
    assert any("Synthetic Input Detected" in item for item in result["violations"])


def test_sustainability_guardrail_passes_safe_native_plan() -> None:
    result = sustainability_guardrail_tool(
        proposed_plants=["Wild Bergamot", "Black-eyed Susan"],
        proposed_inputs=["leaf compost", "shredded leaves"],
    )

    assert result["status"] == "PASS"
    assert result["violations"] == []
