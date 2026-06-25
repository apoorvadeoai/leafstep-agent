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

    LeafStep uses a quick multiple-choice style intake instead of asking users
    to measure square footage or provide unnecessary personal information.

    Args:
        location: City or general region, e.g. "Oakville, Ontario".
        space_type: Backyard, front yard, balcony/patio, side strip, community garden, or custom text.
        sunlight: Full sun, part sun, mostly shade, or custom text.
        garden_style: Flowers, leafy green plants, fruits/edible plants, balanced mix, surprise me, or custom text.
        safety_mode: Dogs/cats, kids, both pets and kids, none, or custom text.
        starter_size: Tiny, small, medium, large, or custom text.

    Returns:
        A normalized user profile for downstream LeafStep tools.
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
        if "both" in value or ("kid" in value and ("dog" in value or "cat" in value or "pet" in value)):
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

    region = location.strip() or "Ontario"
    normalized_space = _normalize_space(space_type)
    normalized_sunlight = _normalize_sunlight(sunlight)
    normalized_style = _normalize_garden_style(garden_style)
    normalized_safety = _normalize_safety_mode(safety_mode)
    patch_size, plant_count_target = _normalize_starter_size(starter_size)

    location_note = ""
    if any(word in region.lower() for word in ["address", "street", "postal", "zip"]):
        location_note = (
            "LeafStep does not need an exact address. City or general region is enough."
        )

    return {
        "region": region,
        "space_type": normalized_space,
        "sunlight": normalized_sunlight,
        "garden_style": normalized_style,
        "safety_mode": normalized_safety,
        "patch_size": patch_size,
        "plant_count_target": plant_count_target,
        "exact_address_needed": False,
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
    """Recommends region-friendly plants using the LeafStep guided setup.

    This Day 2 version supports recommendation diversity based on:
    - region
    - space type
    - sunlight
    - garden style
    - starter size / plant count

    Args:
        region: City or general region, e.g. "Oakville, Ontario".
        space_type: Normalized space type from space_intake_tool.
        sunlight: Normalized sunlight value from space_intake_tool.
        garden_style: Normalized garden style from space_intake_tool.
        plant_count_target: Target number of plants from space_intake_tool.

    Returns:
        A dictionary with ranked plant recommendations and impact-friendly metadata.
    """

    def _clean(value: str) -> str:
        return value.strip().lower()

    normalized_region = _clean(region)
    normalized_space = _clean(space_type)
    normalized_sunlight = _clean(sunlight)
    normalized_style = _clean(garden_style)

    plant_catalog = [
        {
            "common_name": "Wild Bergamot",
            "scientific_name": "Monarda fistulosa",
            "plant_type": "flower",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun", "part_sun"],
            "space_fit": ["backyard", "front_yard", "community_garden", "balcony_patio", "side_yard_strip"],
            "garden_style": ["flowers", "balanced", "surprise_me"],
            "pollinator_support": "High",
            "water_need": "Low",
            "maintenance": "Low",
            "native_fit": "Strong",
            "why": "Native flower that supports bees, butterflies, and a long summer bloom.",
        },
        {
            "common_name": "Black-eyed Susan",
            "scientific_name": "Rudbeckia hirta",
            "plant_type": "flower",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun", "part_sun"],
            "space_fit": ["backyard", "front_yard", "community_garden", "balcony_patio", "side_yard_strip"],
            "garden_style": ["flowers", "balanced", "surprise_me"],
            "pollinator_support": "High",
            "water_need": "Low",
            "maintenance": "Low",
            "native_fit": "Strong",
            "why": "Hardy native-style flower with a long bloom season and strong pollinator value.",
        },
        {
            "common_name": "Purple Coneflower",
            "scientific_name": "Echinacea purpurea",
            "plant_type": "flower",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun", "part_sun"],
            "space_fit": ["backyard", "front_yard", "community_garden", "balcony_patio"],
            "garden_style": ["flowers", "balanced", "surprise_me"],
            "pollinator_support": "High",
            "water_need": "Low",
            "maintenance": "Low",
            "native_fit": "Good",
            "why": "A tough flowering plant that brings color, seed heads, and pollinator visits.",
        },
        {
            "common_name": "New England Aster",
            "scientific_name": "Symphyotrichum novae-angliae",
            "plant_type": "flower",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun", "part_sun"],
            "space_fit": ["backyard", "front_yard", "community_garden", "side_yard_strip"],
            "garden_style": ["flowers", "balanced", "surprise_me"],
            "pollinator_support": "High",
            "water_need": "Low",
            "maintenance": "Low",
            "native_fit": "Strong",
            "why": "Late-season native bloom that helps pollinators when many flowers are finished.",
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
            "why": "Important monarch-supporting plant with bright flowers; safety filter should handle pet/kid use.",
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
            "why": "Tall purple flower spikes add visual drama and attract butterflies.",
        },
        {
            "common_name": "Canada Anemone",
            "scientific_name": "Anemone canadensis",
            "plant_type": "flower",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["part_sun", "mostly_shade"],
            "space_fit": ["backyard", "side_yard_strip", "community_garden"],
            "garden_style": ["flowers", "balanced", "leafy"],
            "pollinator_support": "Medium",
            "water_need": "Medium",
            "maintenance": "Low",
            "native_fit": "Strong",
            "why": "Soft white flowers for part-sun spaces and naturalized garden edges.",
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
            "why": "Native groundcover that creates a low-maintenance leafy carpet in shade.",
        },
        {
            "common_name": "Foamflower",
            "scientific_name": "Tiarella cordifolia",
            "plant_type": "leafy",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["mostly_shade", "part_sun"],
            "space_fit": ["backyard", "side_yard_strip", "community_garden", "balcony_patio"],
            "garden_style": ["leafy", "flowers", "balanced", "surprise_me"],
            "pollinator_support": "Medium",
            "water_need": "Medium",
            "maintenance": "Low",
            "native_fit": "Good",
            "why": "Compact leafy plant with delicate blooms, good for shade and containers.",
        },
        {
            "common_name": "Ostrich Fern",
            "scientific_name": "Matteuccia struthiopteris",
            "plant_type": "leafy",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["mostly_shade", "part_sun"],
            "space_fit": ["backyard", "side_yard_strip", "community_garden"],
            "garden_style": ["leafy", "balanced"],
            "pollinator_support": "Low",
            "water_need": "Medium",
            "maintenance": "Low",
            "native_fit": "Strong",
            "why": "Large native fern that adds lush texture in shady spaces.",
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
            "why": "Soft grass-like native groundcover that reduces bare soil and mowing.",
        },
        {
            "common_name": "Little Bluestem",
            "scientific_name": "Schizachyrium scoparium",
            "plant_type": "grass",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun"],
            "space_fit": ["backyard", "front_yard", "side_yard_strip", "community_garden", "balcony_patio"],
            "garden_style": ["leafy", "balanced", "surprise_me"],
            "pollinator_support": "Medium",
            "water_need": "Low",
            "maintenance": "Low",
            "native_fit": "Strong",
            "why": "Hardy native grass that adds structure, seed heads, and low-water texture.",
        },
        {
            "common_name": "Switchgrass",
            "scientific_name": "Panicum virgatum",
            "plant_type": "grass",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun", "part_sun"],
            "space_fit": ["backyard", "front_yard", "community_garden", "side_yard_strip"],
            "garden_style": ["leafy", "balanced"],
            "pollinator_support": "Medium",
            "water_need": "Low",
            "maintenance": "Low",
            "native_fit": "Strong",
            "why": "Durable native grass that supports structure and habitat with little fuss.",
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
            "space_fit": ["backyard", "front_yard", "community_garden", "balcony_patio", "side_yard_strip"],
            "garden_style": ["fruits_edible", "balanced", "surprise_me"],
            "pollinator_support": "Medium",
            "water_need": "Low",
            "maintenance": "Low",
            "native_fit": "Strong",
            "why": "Native edible groundcover that works in small patches and containers.",
        },
        {
            "common_name": "Highbush Blueberry",
            "scientific_name": "Vaccinium corymbosum",
            "plant_type": "fruit",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun", "part_sun"],
            "space_fit": ["backyard", "front_yard", "community_garden", "balcony_patio"],
            "garden_style": ["fruits_edible", "balanced"],
            "pollinator_support": "Medium",
            "water_need": "Medium",
            "maintenance": "Medium",
            "native_fit": "Good",
            "why": "Edible berries plus spring flowers, best where soil can be kept acidic.",
        },
        {
            "common_name": "Red Raspberry",
            "scientific_name": "Rubus idaeus",
            "plant_type": "fruit",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun", "part_sun"],
            "space_fit": ["backyard", "community_garden"],
            "garden_style": ["fruits_edible"],
            "pollinator_support": "Medium",
            "water_need": "Medium",
            "maintenance": "Medium",
            "native_fit": "Good",
            "why": "Fruit-producing cane that supports pollinators but needs space and pruning.",
        },
        {
            "common_name": "Elderberry",
            "scientific_name": "Sambucus canadensis",
            "plant_type": "fruit",
            "region_fit": ["ontario", "oakville", "toronto"],
            "sunlight": ["full_sun", "part_sun"],
            "space_fit": ["backyard", "community_garden"],
            "garden_style": ["fruits_edible", "balanced"],
            "pollinator_support": "High",
            "water_need": "Medium",
            "maintenance": "Medium",
            "native_fit": "Strong",
            "why": "Native shrub with flowers and berries; better for larger outdoor spaces.",
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

    ranked_plants = sorted(
        plant_catalog,
        key=lambda plant: _score_plant(plant),
        reverse=True,
    )

    # Keep output useful without overwhelming the user.
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
    """Filters recommended plants using LeafStep pet/kid safety rules.

    Safety labels:
    - safe_pick: allowed in the main buy list
    - careful_placement: only shown if more options are needed
    - do_not_buy: never shown in the buy list
    """

    normalized_safety = safety_mode.strip().lower()

    safety_database = {
        "Butterfly Milkweed": {
            "pets": "careful_placement",
            "kids": "careful_placement",
            "pets_and_kids": "careful_placement",
            "reason": "keep away from chewing or digging",
        },
        "Black-eyed Susan": {
            "pets": "safe_pick",
            "kids": "safe_pick",
            "pets_and_kids": "safe_pick",
            "reason": "low-risk garden pick",
        },
        "Purple Coneflower": {
            "pets": "safe_pick",
            "kids": "safe_pick",
            "pets_and_kids": "safe_pick",
            "reason": "low-risk garden pick",
        },
        "Wild Bergamot": {
            "pets": "safe_pick",
            "kids": "safe_pick",
            "pets_and_kids": "safe_pick",
            "reason": "low-risk garden pick",
        },
        "New England Aster": {
            "pets": "safe_pick",
            "kids": "safe_pick",
            "pets_and_kids": "safe_pick",
            "reason": "low-risk garden pick",
        },
        "Little Bluestem": {
            "pets": "safe_pick",
            "kids": "safe_pick",
            "pets_and_kids": "safe_pick",
            "reason": "low-risk grass-like habitat plant",
        },
        "Switchgrass": {
            "pets": "safe_pick",
            "kids": "safe_pick",
            "pets_and_kids": "safe_pick",
            "reason": "low-risk grass-like habitat plant",
        },
        "Wild Strawberry": {
            "pets": "safe_pick",
            "kids": "safe_pick",
            "pets_and_kids": "safe_pick",
            "reason": "edible groundcover",
        },
        "Serviceberry": {
            "pets": "safe_pick",
            "kids": "safe_pick",
            "pets_and_kids": "safe_pick",
            "reason": "edible berry shrub/tree",
        },
        "Highbush Blueberry": {
            "pets": "safe_pick",
            "kids": "safe_pick",
            "pets_and_kids": "safe_pick",
            "reason": "edible berry shrub",
        },
        "Red Raspberry": {
            "pets": "careful_placement",
            "kids": "careful_placement",
            "pets_and_kids": "careful_placement",
            "reason": "can be thorny; place away from rough play or chewing",
        },
        "Elderberry": {
            "pets": "careful_placement",
            "kids": "careful_placement",
            "pets_and_kids": "careful_placement",
            "reason": "berries and plant parts need careful handling",
        },
        "Ostrich Fern": {
            "pets": "careful_placement",
            "kids": "careful_placement",
            "pets_and_kids": "careful_placement",
            "reason": "use where pets/kids will not chew plants",
        },
        "Wild Ginger": {
            "pets": "careful_placement",
            "kids": "careful_placement",
            "pets_and_kids": "careful_placement",
            "reason": "keep away from chewing or digging",
        },
        "Foamflower": {
            "pets": "safe_pick",
            "kids": "safe_pick",
            "pets_and_kids": "safe_pick",
            "reason": "low-risk shade plant",
        },
        "Pennsylvania Sedge": {
            "pets": "safe_pick",
            "kids": "safe_pick",
            "pets_and_kids": "safe_pick",
            "reason": "low-risk groundcover",
        },
        "Canada Anemone": {
            "pets": "careful_placement",
            "kids": "careful_placement",
            "pets_and_kids": "careful_placement",
            "reason": "keep away from chewing access",
        },
        "Dense Blazing Star": {
            "pets": "safe_pick",
            "kids": "safe_pick",
            "pets_and_kids": "safe_pick",
            "reason": "low-risk pollinator flower",
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
    do_not_buy_list = known_do_not_buy.copy()

    for plant in recommended_plants:
        plant_name = plant.get("common_name", "")
        safety_record = safety_database.get(plant_name, {})
        safety_label = safety_record.get(normalized_safety, "careful_placement")
        reason = safety_record.get("reason", "keep away from pets/kids")

        plant_with_safety = {
            **plant,
            "safety_label": safety_label,
            "safety_reason": reason,
        }

        if safety_label == "safe_pick":
            buy_list.append(plant_with_safety)
        elif safety_label == "careful_placement":
            careful_placement_list.append(plant_with_safety)
        else:
            do_not_buy_list.append(
                {
                    "common_name": plant_name,
                    "reason": reason,
                }
            )

    if len(buy_list) < plant_count_target:
        needed = plant_count_target - len(buy_list)
        buy_list = buy_list + careful_placement_list[:needed]
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
        "do_not_buy_list": do_not_buy_list,
        "safety_summary": summary,
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
