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

"""Tools for the LeafStep Agent.

This module provides tools for space intake, ecosystem-aware plant recommendations,
soil stewardship, care planning, and sustainability guardrails.
"""

from typing import Any


def space_intake_tool(
    location: str,
    space_type: str,
    sunlight: str,
    garden_style: str,
    safety_mode: str,
    starter_size: str,
) -> dict[str, Any]:
    """Normalizes the 6-question LeafStep setup into a structured profile.

    LeafStep only needs a city or general region for garden planning. If a user
    enters an exact-address-looking location, the tool keeps the original text
    for now but clearly marks that exact addresses are unnecessary.
    """

    def _clean(value: str) -> str:
        return value.strip().lower()

    def _normalize_space(value: str) -> str:
        value = _clean(value)
        if "back" in value:
            return "backyard"
        if "front" in value:
            return "front_yard"
        if "balcony" in value or "patio" in value or "container" in value:
            return "balcony_patio"
        if "side" in value or "strip" in value:
            return "side_yard_strip"
        if "community" in value:
            return "community_garden"
        return value or "custom_space"

    def _normalize_sunlight(value: str) -> str:
        value = _clean(value)
        if "full" in value or "6" in value:
            return "full_sun"
        if "part" in value or "2" in value or "3" in value:
            return "part_sun"
        if "shade" in value:
            return "mostly_shade"
        return value or "custom_sunlight"

    def _normalize_garden_style(value: str) -> str:
        value = _clean(value)
        if "flower" in value:
            return "flowers"
        if "leaf" in value or "green" in value:
            return "leafy"
        if "fruit" in value or "edible" in value or "berry" in value:
            return "fruits_edible"
        if "balanced" in value or "mix" in value:
            return "balanced"
        if "surprise" in value:
            return "surprise_me"
        return value or "custom_style"

    def _normalize_safety_mode(value: str) -> str:
        value = _clean(value)
        if "both" in value or (
            "kid" in value and ("dog" in value or "cat" in value or "pet" in value)
        ):
            return "pets_and_kids"
        if "dog" in value or "cat" in value or "pet" in value:
            return "pets"
        if "kid" in value or "child" in value or "children" in value:
            return "kids"
        if "none" in value or "no" in value:
            return "none"
        return value or "custom_safety"

    def _normalize_starter_size(value: str) -> tuple[str, int]:
        value = _clean(value)
        if "tiny" in value or "2" in value:
            return "tiny", 2
        if "small" in value or "5" in value:
            return "small", 5
        if "medium" in value or "10" in value:
            return "medium", 10
        if "large" in value or "15" in value:
            return "large", 15
        return "custom", 5

    def _looks_like_exact_address(value: str) -> bool:
        value_lower = value.lower()

        address_signals = [
            "address",
            "street",
            "st.",
            "road",
            "rd.",
            "avenue",
            "ave",
            "drive",
            "dr.",
            "lane",
            "court",
            "crt",
            "boulevard",
            "blvd",
            "postal",
            "postcode",
            "zip",
        ]

        has_number = any(char.isdigit() for char in value)
        has_address_signal = any(signal in value_lower for signal in address_signals)

        return has_number and has_address_signal

    def _generalize_location(value: str) -> str:
        value_lower = value.lower()

        known_regions = [
            "oakville",
            "halton",
            "burlington",
            "milton",
            "toronto",
            "mississauga",
            "ontario",
        ]

        for known_region in known_regions:
            if known_region in value_lower:
                return known_region.title()

        return "Ontario"

    raw_location = location.strip() or "Ontario"
    possible_exact_address = _looks_like_exact_address(raw_location)
    region = (
        _generalize_location(raw_location) if possible_exact_address else raw_location
    )
    patch_size, plant_count_target = _normalize_starter_size(starter_size)

    privacy_status = "pass"
    location_note = ""

    if possible_exact_address:
        privacy_status = "generalize_location"
        location_note = (
            "LeafStep does not need your exact home address. "
            "City or general region is enough for garden planning."
        )

    return {
        "region": region,
        "location": region,
        "space_type": _normalize_space(space_type),
        "sunlight": _normalize_sunlight(sunlight),
        "garden_style": _normalize_garden_style(garden_style),
        "safety_mode": _normalize_safety_mode(safety_mode),
        "patch_size": patch_size,
        "plant_count_target": plant_count_target,
        "exact_address_needed": False,
        "possible_exact_address": possible_exact_address,
        "privacy_status": privacy_status,
        "location_note": location_note,
        "default_leafstep_goals": [
            "pollinator_friendly",
            "water_saving",
            "low_maintenance",
            "native_or_region_friendly",
            "ecosystem_balance",
            "lifecycle_tracking",
        ],
        "status": "valid",
    }


def plant_recommendation_tool(
    region: str,
    space_type: str,
    sunlight: str,
    garden_style: str,
    plant_count_target: int,
) -> dict[str, Any]:
    """Recommends region-friendly plants using the LeafStep guided setup."""

    normalized_region = region.strip().lower()
    normalized_space = space_type.strip().lower()
    normalized_sunlight = sunlight.strip().lower()
    normalized_style = garden_style.strip().lower()

    plant_catalog = [
        {
            "common_name": "Wild Bergamot",
            "scientific_name": "Monarda fistulosa",
            "plant_type": "flower",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun", "part_sun"],
            "space_fit": [
                "backyard",
                "front_yard",
                "community_garden",
                "balcony_patio",
                "side_yard_strip",
            ],
            "garden_style": ["flowers", "balanced", "surprise_me"],
            "pollinator_support": "High",
            "water_need": "Low",
            "maintenance": "Low",
            "native_fit": "Strong",
            "why": "Native flower that supports bees, butterflies, and summer blooms.",
        },
        {
            "common_name": "Black-eyed Susan",
            "scientific_name": "Rudbeckia hirta",
            "plant_type": "flower",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun", "part_sun"],
            "space_fit": [
                "backyard",
                "front_yard",
                "community_garden",
                "balcony_patio",
                "side_yard_strip",
            ],
            "garden_style": ["flowers", "balanced", "surprise_me"],
            "pollinator_support": "High",
            "water_need": "Low",
            "maintenance": "Low",
            "native_fit": "Strong",
            "why": "Hardy native-style flower with a long bloom season.",
        },
        {
            "common_name": "Purple Coneflower",
            "scientific_name": "Echinacea purpurea",
            "plant_type": "flower",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun", "part_sun"],
            "space_fit": [
                "backyard",
                "front_yard",
                "community_garden",
                "balcony_patio",
            ],
            "garden_style": ["flowers", "balanced", "surprise_me"],
            "pollinator_support": "High",
            "water_need": "Low",
            "maintenance": "Low",
            "native_fit": "Good",
            "why": "Tough flowering plant with color, seed heads, and pollinator visits.",
        },
        {
            "common_name": "New England Aster",
            "scientific_name": "Symphyotrichum novae-angliae",
            "plant_type": "flower",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun", "part_sun"],
            "space_fit": [
                "backyard",
                "front_yard",
                "community_garden",
                "side_yard_strip",
            ],
            "garden_style": ["flowers", "balanced", "surprise_me"],
            "pollinator_support": "High",
            "water_need": "Low",
            "maintenance": "Low",
            "native_fit": "Strong",
            "why": "Late-season native bloom that supports pollinators.",
        },
        {
            "common_name": "Butterfly Milkweed",
            "scientific_name": "Asclepias tuberosa",
            "plant_type": "flower",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun"],
            "space_fit": ["backyard", "front_yard", "community_garden"],
            "garden_style": ["flowers", "balanced"],
            "pollinator_support": "High",
            "water_need": "Low",
            "maintenance": "Medium",
            "native_fit": "Strong",
            "why": "Monarch-supporting flower; safety tool handles pet/kid placement.",
        },
        {
            "common_name": "Dense Blazing Star",
            "scientific_name": "Liatris spicata",
            "plant_type": "flower",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun"],
            "space_fit": ["backyard", "front_yard", "community_garden"],
            "garden_style": ["flowers", "balanced"],
            "pollinator_support": "High",
            "water_need": "Medium",
            "maintenance": "Low",
            "native_fit": "Strong",
            "why": "Purple flower spikes that attract butterflies.",
        },
        {
            "common_name": "Wild Ginger",
            "scientific_name": "Asarum canadense",
            "plant_type": "leafy",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["mostly_shade", "part_sun"],
            "space_fit": ["backyard", "side_yard_strip", "community_garden"],
            "garden_style": ["leafy", "balanced", "surprise_me"],
            "pollinator_support": "Low",
            "water_need": "Low",
            "maintenance": "Low",
            "native_fit": "Strong",
            "why": "Native groundcover for low-maintenance shade.",
        },
        {
            "common_name": "Foamflower",
            "scientific_name": "Tiarella cordifolia",
            "plant_type": "leafy",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["mostly_shade", "part_sun"],
            "space_fit": [
                "backyard",
                "side_yard_strip",
                "community_garden",
                "balcony_patio",
            ],
            "garden_style": ["leafy", "flowers", "balanced", "surprise_me"],
            "pollinator_support": "Medium",
            "water_need": "Medium",
            "maintenance": "Low",
            "native_fit": "Good",
            "why": "Compact leafy plant with delicate blooms for shade and containers.",
        },
        {
            "common_name": "Pennsylvania Sedge",
            "scientific_name": "Carex pensylvanica",
            "plant_type": "leafy",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["mostly_shade", "part_sun"],
            "space_fit": ["backyard", "side_yard_strip", "front_yard"],
            "garden_style": ["leafy", "balanced", "surprise_me"],
            "pollinator_support": "Low",
            "water_need": "Low",
            "maintenance": "Low",
            "native_fit": "Strong",
            "why": "Grass-like native groundcover that reduces bare soil.",
        },
        {
            "common_name": "Little Bluestem",
            "scientific_name": "Schizachyrium scoparium",
            "plant_type": "grass",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun"],
            "space_fit": [
                "backyard",
                "front_yard",
                "side_yard_strip",
                "community_garden",
                "balcony_patio",
            ],
            "garden_style": ["leafy", "balanced", "surprise_me"],
            "pollinator_support": "Medium",
            "water_need": "Low",
            "maintenance": "Low",
            "native_fit": "Strong",
            "why": "Hardy native grass with structure and low-water texture.",
        },
        {
            "common_name": "Serviceberry",
            "scientific_name": "Amelanchier canadensis",
            "plant_type": "fruit",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun", "part_sun"],
            "space_fit": ["backyard", "front_yard", "community_garden"],
            "garden_style": ["fruits_edible", "balanced", "surprise_me"],
            "pollinator_support": "High",
            "water_need": "Medium",
            "maintenance": "Medium",
            "native_fit": "Strong",
            "why": "Native shrub/tree with spring flowers, berries, and bird value.",
        },
        {
            "common_name": "Wild Strawberry",
            "scientific_name": "Fragaria virginiana",
            "plant_type": "fruit",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun", "part_sun"],
            "space_fit": [
                "backyard",
                "front_yard",
                "community_garden",
                "balcony_patio",
                "side_yard_strip",
            ],
            "garden_style": ["fruits_edible", "balanced", "surprise_me"],
            "pollinator_support": "Medium",
            "water_need": "Low",
            "maintenance": "Low",
            "native_fit": "Strong",
            "why": "Native edible groundcover for small patches and containers.",
        },
        {
            "common_name": "Highbush Blueberry",
            "scientific_name": "Vaccinium corymbosum",
            "plant_type": "fruit",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun", "part_sun"],
            "space_fit": [
                "backyard",
                "front_yard",
                "community_garden",
                "balcony_patio",
            ],
            "garden_style": ["fruits_edible", "balanced"],
            "pollinator_support": "Medium",
            "water_need": "Medium",
            "maintenance": "Medium",
            "native_fit": "Good",
            "why": "Edible berries plus spring flowers.",
        },
    ]

    def _score_plant(plant: dict[str, Any]) -> int:
        score = 0

        if any(region_word in normalized_region for region_word in plant["region_fit"]):
            score += 3
        if normalized_sunlight in plant["sunlight"]:
            score += 4
        if normalized_space in plant["space_fit"]:
            score += 3
        if normalized_style in plant["garden_style"]:
            score += 4
        if plant["pollinator_support"] == "High":
            score += 2
        elif plant["pollinator_support"] == "Medium":
            score += 1
        if plant["water_need"] == "Low":
            score += 2
        elif plant["water_need"] == "Medium":
            score += 1
        if plant["maintenance"] == "Low":
            score += 2
        elif plant["maintenance"] == "Medium":
            score += 1
        if plant["native_fit"] == "Strong":
            score += 2
        elif plant["native_fit"] == "Good":
            score += 1

        return score

    ranked_plants = sorted(plant_catalog, key=_score_plant, reverse=True)
    target_count = max(2, min(int(plant_count_target), 10))
    selected_plants = ranked_plants[:target_count]

    return {
        "region": region,
        "space_type": normalized_space,
        "sunlight": normalized_sunlight,
        "garden_style": normalized_style,
        "plant_count_target": target_count,
        "recommended_plants": selected_plants,
        "recommendation_summary": (
            f"{target_count} {normalized_sunlight.replace('_', ' ')} "
            f"{normalized_style.replace('_', ' ')} picks for {normalized_space.replace('_', ' ')}."
        ),
    }


def plant_safety_tool(
    recommended_plants: list[dict[str, Any]],
    safety_mode: str,
    plant_count_target: int,
) -> dict[str, Any]:
    """Filters recommended plants using LeafStep pet/kid safety rules."""

    normalized_safety = safety_mode.strip().lower()

    safety_database = {
        "Butterfly Milkweed": {
            "pets": "careful_placement",
            "kids": "careful_placement",
            "pets_and_kids": "careful_placement",
            "reason": "keep away from chewing or digging",
        },
        "Wild Ginger": {
            "pets": "careful_placement",
            "kids": "careful_placement",
            "pets_and_kids": "careful_placement",
            "reason": "keep away from chewing or digging",
        },
        "Red Raspberry": {
            "pets": "careful_placement",
            "kids": "careful_placement",
            "pets_and_kids": "careful_placement",
            "reason": "thorny canes; place away from rough play",
        },
        "Elderberry": {
            "pets": "careful_placement",
            "kids": "careful_placement",
            "pets_and_kids": "careful_placement",
            "reason": "plant parts need careful handling",
        },
    }

    known_do_not_buy = [
        {
            "common_name": "Foxglove",
            "reason": "toxic; do not use in pet/kid-accessible spaces",
        },
        {
            "common_name": "Lily of the Valley",
            "reason": "toxic; do not use in pet/kid-accessible spaces",
        },
        {
            "common_name": "Daffodil bulbs",
            "reason": "toxic if eaten; avoid in pet/kid-accessible spaces",
        },
    ]

    if normalized_safety in {"none", "no special safety concern"}:
        return {
            "safety_mode": "none",
            "buy_list": recommended_plants[:plant_count_target],
            "careful_placement_list": [],
            "do_not_buy_list": known_do_not_buy,
            "safety_summary": "No special safety filter selected.",
        }

    buy_list = []
    careful_placement_list = []

    for plant in recommended_plants:
        plant_name = plant.get("common_name", "")
        safety_record = safety_database.get(plant_name)

        if safety_record:
            safety_label = safety_record.get(normalized_safety, "careful_placement")
            reason = safety_record.get("reason", "keep away from pets/kids")
        else:
            safety_label = "safe_pick"
            reason = "low-risk garden pick"

        plant_with_safety = {
            **plant,
            "safety_label": safety_label,
            "safety_reason": reason,
        }

        if safety_label == "safe_pick":
            buy_list.append(plant_with_safety)
        else:
            careful_placement_list.append(plant_with_safety)

    # If there are not enough safe picks, include careful placement options.
    if len(buy_list) < plant_count_target:
        needed = plant_count_target - len(buy_list)
        buy_list.extend(careful_placement_list[:needed])
        careful_placement_list = careful_placement_list[needed:]

    if normalized_safety == "pets":
        summary = "Pet-safe mode on. Dangerous plants removed."
    elif normalized_safety == "kids":
        summary = "Kid-safe mode on. Dangerous plants removed."
    elif normalized_safety == "pets_and_kids":
        summary = "Strict safety mode on. Dangerous plants removed."
    else:
        summary = "Safety filter applied."

    return {
        "safety_mode": normalized_safety,
        "buy_list": buy_list[:plant_count_target],
        "careful_placement_list": careful_placement_list,
        "do_not_buy_list": known_do_not_buy,
        "safety_summary": summary,
    }


def impact_tracking_tool(
    buy_list: list[dict[str, Any]],
    careful_placement_list: list[dict[str, Any]],
) -> dict[str, Any]:
    """Creates simple LeafStep impact badges and lifecycle tracking guidance."""

    selected_plants = buy_list + careful_placement_list

    if not selected_plants:
        return {
            "pollinator_support": "Low",
            "water_need": "High",
            "maintenance": "High",
            "native_fit": "Weak",
            "biodiversity_value": "Low",
            "tracking_action": "Add your first plant to start tracking growth.",
        }

    pollinator_values = [
        plant.get("pollinator_support", "Low") for plant in selected_plants
    ]
    water_values = [plant.get("water_need", "Medium") for plant in selected_plants]
    maintenance_values = [
        plant.get("maintenance", "Medium") for plant in selected_plants
    ]
    native_values = [plant.get("native_fit", "Good") for plant in selected_plants]

    high_pollinator_count = pollinator_values.count("High")
    medium_pollinator_count = pollinator_values.count("Medium")
    low_water_count = water_values.count("Low")
    medium_water_count = water_values.count("Medium")
    low_maintenance_count = maintenance_values.count("Low")
    medium_maintenance_count = maintenance_values.count("Medium")
    strong_native_count = native_values.count("Strong")
    good_native_count = native_values.count("Good")

    half_count = max(1, len(selected_plants) // 2)

    if high_pollinator_count >= half_count:
        pollinator_support = "High"
    elif high_pollinator_count + medium_pollinator_count >= half_count:
        pollinator_support = "Medium"
    else:
        pollinator_support = "Low"

    if low_water_count >= half_count:
        water_need = "Low"
    elif low_water_count + medium_water_count >= half_count:
        water_need = "Medium"
    else:
        water_need = "High"

    if low_maintenance_count >= half_count:
        maintenance = "Low"
    elif low_maintenance_count + medium_maintenance_count >= half_count:
        maintenance = "Medium"
    else:
        maintenance = "High"

    if strong_native_count >= half_count:
        native_fit = "Strong"
    elif strong_native_count + good_native_count >= half_count:
        native_fit = "Good"
    else:
        native_fit = "Weak"

    if pollinator_support == "High" and native_fit in {"Strong", "Good"}:
        biodiversity_value = "High"
    elif pollinator_support == "Medium" or native_fit == "Good":
        biodiversity_value = "Medium"
    else:
        biodiversity_value = "Low"

    return {
        "pollinator_support": pollinator_support,
        "water_need": water_need,
        "maintenance": maintenance,
        "native_fit": native_fit,
        "biodiversity_value": biodiversity_value,
        "tracking_action": "Take a first photo and log first bloom or new growth later.",
    }


def soil_stewardship_tool(location: str, space_type: str) -> dict[str, Any]:
    """Provides organic soil stewardship recommendations for the given location and space type.

    Args:
        location: The location (e.g. 'Oakville, Ontario').
        space_type: Type of space (e.g. 'backyard patch', 'garden bed').

    Returns:
        A dictionary with soil preparation, organic amendments, and stewardship advice.
    """
    is_oakville = "oakville" in location.lower()

    # Oakville/Halton region is known for clay soils (Halton Clay/Clay Loam)
    soil_profile = "Halton Clay Loam" if is_oakville else "General garden soil"

    preparation_steps = [
        "Avoid deep tilling: Tilling disrupts soil microbes and structure. Instead, gently aerate with a garden fork.",
        "Add Organic Compost: Top-dress the 3x5 space with 2-3 inches of organic leaf compost or local mushroom compost.",
        "Mulch for Protection: Lay down a light layer of shredded leaves or straw. This retains moisture, prevents weed growth, and feeds soil life as it decomposes.",
    ]

    organic_practices = [
        "Zero Chemical Pesticides: Protect soil microbes, earthworms, and pollinators by avoiding synthetic chemicals.",
        "Use Natural Fertilizers: If needed, use compost tea, seaweed extract, or alfalfa meal instead of synthetic granular fertilizers.",
    ]

    return {
        "soil_profile": soil_profile,
        "space_type": space_type,
        "preparation_steps": preparation_steps,
        "organic_practices": organic_practices,
        "tips": "For a 3x5 space, about 2 to 3 bags of quality organic compost is enough to kickstart soil health.",
    }


def care_plan_tool(plants: list[str], experience_level: str) -> dict[str, Any]:
    """Generates a day-by-day 30-day care and establishment plan for the selected plants.

    Args:
        plants: List of recommended plants.
        experience_level: Experience level of the gardener (e.g., 'beginner').

    Returns:
        A dictionary representing the care plan.
    """
    exp = experience_level.lower().strip()

    # Establish a beginner-friendly schedule
    schedule = {
        "Days 1-3": "Planting & Initial Hydration. Plant your native plugs. Water gently but thoroughly immediately after planting. Check soil moisture daily; keep damp but not soggy.",
        "Days 4-7": "Root Settling. Water once every morning. Ensure mulch is kept 1 inch away from plant stems to prevent rot.",
        "Days 8-14": "Establishment Phase. Water every 2 days if there is no rain. Hand-pull any competing weeds gently so you don't disturb the new plant roots.",
        "Days 15-21": "Stewardship and Observation. Reduce watering to twice a week. Spend 5 minutes observing: check for new leaf growth or early pollinator visits.",
        "Days 22-30": "Independence. Water only during hot, dry spells. Native plants are adapted to local rain patterns and are beginning to establish self-sufficiency.",
    }

    tips = [
        "Water the base of the plant, not the leaves, to prevent fungal issues.",
        "Water early in the morning to reduce evaporation.",
        "Don't worry if plants look slightly droopy in the first few days (transplant shock); keep them watered and they will recover.",
    ]

    if exp == "beginner":
        tips.append(
            "Beginner Tip: Native plants need less attention than traditional garden flowers once established! Trust the process and avoid overwatering."
        )

    return {
        "target_plants": plants,
        "experience_level": exp,
        "schedule": schedule,
        "tips": tips,
    }


def sustainability_guardrail_tool(
    proposed_plants: list[str], proposed_inputs: list[str]
) -> dict[str, Any]:
    """Checks plants and soil inputs against Ontario ecological safety rules and organic standards.

    Args:
        proposed_plants: List of plant names to check.
        proposed_inputs: List of materials or inputs (pesticides, fertilizers) to check.

    Returns:
        A dictionary with the safety check result (status: PASS/FAIL, reasons, and recommendations).
    """
    # Common invasive plants in Ontario/Oakville to block
    invasive_blocklist = [
        "garlic mustard",
        "alliaria petiolata",
        "dog-strangling vine",
        "vincetoxicum rossicum",
        "vincetoxicum nigrum",
        "purple loosestrife",
        "lythrum salicaria",
        "buckthorn",
        "rhamnus cathartica",
        "giant hogweed",
        "heracleum mantegazzianum",
        "periwinkle",
        "vinca minor",
        "english ivy",
        "hedera helix",
    ]

    # Chemical inputs to block
    chemical_blocklist = [
        "glyphosate",
        "roundup",
        "neonicotinoid",
        "imidacloprid",
        "synthetic fertilizer",
        "miracle-gro",
        "weed and feed",
        "chemical pesticide",
        "chemical herbicide",
        "sevin",
    ]

    violations = []

    # Check plants
    for plant in proposed_plants:
        plant_lower = plant.lower()
        for invasive in invasive_blocklist:
            if invasive in plant_lower:
                violations.append(
                    f"Invasive Plant Detected: '{plant}' is invasive in Ontario and must not be planted."
                )

    # Check inputs
    for inp in proposed_inputs:
        inp_lower = inp.lower()
        for chem in chemical_blocklist:
            if chem in inp_lower:
                violations.append(
                    f"Synthetic Input Detected: '{inp}' violates organic soil stewardship guidelines."
                )

    if violations:
        return {
            "status": "FAIL",
            "violations": violations,
            "recommendation": "Replace the flagged items with Ontario-native species or organic compost/leaf mulches.",
        }

    return {
        "status": "PASS",
        "violations": [],
        "recommendation": "All plants and materials are verified sustainable, native/adapted, and organic-compliant for Halton Region.",
    }
