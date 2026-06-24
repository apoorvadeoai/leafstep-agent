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
    dimensions: str,
    sunlight: str,
    experience_level: str,
    wants_indoor_support: bool,
) -> dict[str, Any]:
    """Validates and structures the input space information for LeafStep.

    Args:
        location: The household location (e.g. 'Oakville, Ontario').
        dimensions: The size and type of the space (e.g. '3x5 backyard patch').
        sunlight: Sunlight levels ('full sun', 'partial shade', 'shade').
        experience_level: Gardening experience level ('beginner', 'intermediate', 'advanced').
        wants_indoor_support: Whether the user wants indoor support plants.

    Returns:
        A dictionary containing the validated and structured space profile.
    """
    # Standardize input values slightly
    loc_clean = location.strip()
    dim_clean = dimensions.strip()
    sun_clean = sunlight.lower().strip()
    exp_clean = experience_level.lower().strip()

    # Simple size validation check (checking for a small scale space, e.g. 3x5)
    is_small_space = any(
        x in dim_clean for x in ["3x5", "3 x 5", "15 sq", "small", "patch", "container"]
    )

    # We encourage small spaces for the first step
    space_warning = ""
    if not is_small_space:
        space_warning = "LeafStep focuses on small, manageable spaces (like 3x5 ft) for your first step. Proceeding with caution for larger spaces."

    is_oakville = "oakville" in loc_clean.lower()
    location_note = ""
    if not is_oakville:
        location_note = "LeafStep is optimized for Oakville, Ontario. Planting lists will default to Ontario Zone 6b native options."

    return {
        "location": loc_clean,
        "dimensions": dim_clean,
        "sunlight": sun_clean,
        "experience_level": exp_clean,
        "wants_indoor_support": wants_indoor_support,
        "is_small_space": is_small_space,
        "space_warning": space_warning,
        "location_note": location_note,
        "status": "valid",
    }


def plant_recommendation_tool(
    sunlight: str, wants_indoor_support: bool
) -> dict[str, Any]:
    """Recommends Oakville-native, pollinator-friendly plants and optional indoor support plants based on sunlight.

    Args:
        sunlight: Sunlight level ('full sun', 'partial shade', 'shade').
        wants_indoor_support: If True, includes starter indoor support plants.

    Returns:
        A dictionary with recommended native outdoor plants and indoor support plants.
    """
    sun_lower = sunlight.lower().strip()

    # Curated Oakville / Ontario native plants dataset matching light profiles
    native_database = {
        "full sun": [
            {
                "common_name": "Butterfly Milkweed",
                "scientific_name": "Asclepias tuberosa",
                "benefits": "Essential host plant for Monarch butterflies; beautiful orange blossoms.",
                "care": "Drought tolerant once established; requires well-drained soil.",
            },
            {
                "common_name": "Wild Bergamot",
                "scientific_name": "Monarda fistulosa",
                "benefits": "Attracts native bees, bumblebees, and butterflies; fragrant lavender flowers.",
                "care": "Low maintenance; spreads gently by rhizomes.",
            },
            {
                "common_name": "Black-eyed Susan",
                "scientific_name": "Rudbeckia hirta",
                "benefits": "Highly attractive to butterflies and bees; long bloom season.",
                "care": "Extremely hardy; handles dry soil well.",
            },
        ],
        "partial shade": [
            {
                "common_name": "Wild Columbine",
                "scientific_name": "Aquilegia canadensis",
                "benefits": "Nectar source for early-season hummingbirds and bees.",
                "care": "Prefers moist, well-drained soils; self-seeds readily.",
            },
            {
                "common_name": "Wild Geranium",
                "scientific_name": "Geranium maculatum",
                "benefits": "Supports specialized native bees; soft pink-lavender flowers.",
                "care": "Easy to grow; tolerates clay soil.",
            },
        ],
        "shade": [
            {
                "common_name": "Wild Columbine",
                "scientific_name": "Aquilegia canadensis",
                "benefits": "Thrives in shade; attractive red/yellow flowers for pollinators.",
                "care": "Low-maintenance; handles tree root competition.",
            },
            {
                "common_name": "Blue Wood Aster",
                "scientific_name": "Symphyotrichum cordifolium",
                "benefits": "Late fall nectar source for migrating butterflies and bees.",
                "care": "Thrives in dry shade; very resilient.",
            },
        ],
    }

    # Select outdoor plants based on sunlight
    outdoor_recs = native_database.get(sun_lower, native_database["partial shade"])

    # Select indoor support plants (for beginner-friendly indoor green addition)
    indoor_recs = []
    if wants_indoor_support:
        indoor_recs = [
            {
                "common_name": "Spider Plant",
                "scientific_name": "Chlorophytum comosum",
                "benefits": "Excellent air purifier, pet-friendly, produces 'pups' that are easy to propagate.",
                "care": "Indirect light; water when top inch of soil is dry.",
            },
            {
                "common_name": "Golden Pothos",
                "scientific_name": "Epipremnum aureum",
                "benefits": "Extremely resilient green vine; thrives in low-light indoor spaces.",
                "care": "Water occasionally; tolerates neglect.",
            },
        ]

    return {
        "sunlight_profile": sun_lower,
        "outdoor_plants": outdoor_recs,
        "indoor_plants": indoor_recs,
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
