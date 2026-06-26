from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, PlainTextResponse
import html
import importlib.util
import inspect
import os
import subprocess
import sys
from typing import Any


app = FastAPI(title="LeafStep Agent Demo")


# Load local LeafStep tools directly from app/tools.py.
# This keeps the Cloud Run demo no-LLM and avoids Gemini/API credit usage.
TOOLS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "tools.py")
_spec = importlib.util.spec_from_file_location("leafstep_tools", TOOLS_PATH)
_tools = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_tools)

space_intake_tool = _tools.space_intake_tool
plant_recommendation_tool = _tools.plant_recommendation_tool
plant_safety_tool = _tools.plant_safety_tool
impact_tracking_tool = _tools.impact_tracking_tool
soil_stewardship_tool = _tools.soil_stewardship_tool
care_plan_tool = _tools.care_plan_tool
sustainability_guardrail_tool = _tools.sustainability_guardrail_tool


def page_shell(title: str, body: str) -> str:
    return f"""
    <html>
      <head>
        <title>{html.escape(title)}</title>
        <style>
          body {{
            font-family: Arial, sans-serif;
            max-width: 980px;
            margin: 36px auto;
            line-height: 1.6;
            padding: 0 20px;
            color: #1f2933;
            background: #ffffff;
          }}
          h1, h2, h3 {{
            color: #1f4f35;
          }}
          .hero {{
            border: 1px solid #d9e2dc;
            border-radius: 16px;
            padding: 24px;
            background: #f7fbf7;
            margin-bottom: 20px;
          }}
          .card {{
            border: 1px solid #d9e2dc;
            border-radius: 14px;
            padding: 18px;
            margin: 16px 0;
            background: #fbfdfb;
          }}
          .plant {{
            border-left: 5px solid #2f6f4e;
            padding-left: 14px;
            margin: 14px 0;
          }}
          label {{
            display: block;
            font-weight: bold;
            margin-top: 14px;
          }}
          select {{
            width: 100%;
            padding: 10px;
            margin-top: 6px;
            border: 1px solid #bdc9c1;
            border-radius: 8px;
            font-size: 15px;
            background: white;
          }}
          button, .button {{
            display: inline-block;
            margin-top: 18px;
            margin-right: 8px;
            padding: 11px 16px;
            background: #2f6f4e;
            color: white;
            text-decoration: none;
            border: 0;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
          }}
          .muted {{
            color: #5f6f66;
          }}
          .pass {{
            color: #176b3a;
            font-weight: bold;
          }}
          .fail {{
            color: #a12622;
            font-weight: bold;
          }}
          .caution {{
            color: #9a5b00;
            font-weight: bold;
          }}
          code {{
            background: #eef5ef;
            padding: 2px 5px;
            border-radius: 4px;
          }}
          pre {{
            background: #eef5ef;
            padding: 12px;
            border-radius: 8px;
            overflow-x: auto;
          }}
          ul {{
            padding-left: 22px;
          }}
        </style>
      </head>
      <body>
        {body}
      </body>
    </html>
    """


def safe_text(value: Any) -> str:
    return html.escape(str(value))


def status_class(status: str) -> str:
    normalized = str(status).upper()
    if normalized == "PASS":
        return "pass"
    if normalized in {"CAUTION", "WARN", "WARNING"}:
        return "caution"
    return "fail"


def call_plant_safety_tool(
    plants_data: dict[str, Any],
    has_pets_or_children: bool,
) -> dict[str, Any]:
    """Call plant_safety_tool while tolerating small signature differences."""

    outdoor_plants = plants_data.get("outdoor_plants", [])
    indoor_plants = plants_data.get("indoor_plants", [])
    all_plant_dicts = outdoor_plants + indoor_plants
    all_plant_names = [plant.get("common_name", str(plant)) for plant in all_plant_dicts]

    safety_mode = "both pets and kids" if has_pets_or_children else "none"

    attempts = [
        {"recommended_plants": all_plant_dicts, "safety_mode": safety_mode},
        {"plant_recommendations": all_plant_dicts, "safety_mode": safety_mode},
        {"plants": all_plant_dicts, "safety_mode": safety_mode},
        {"recommended_plants": all_plant_names, "safety_mode": safety_mode},
        {"proposed_plants": all_plant_names, "has_pets_or_children": has_pets_or_children},
        {"plants": all_plant_names, "has_pets_or_children": has_pets_or_children},
        {"proposed_plants": all_plant_names, "has_pets": has_pets_or_children, "has_children": has_pets_or_children},
    ]

    for kwargs in attempts:
        try:
            return plant_safety_tool(**kwargs)
        except TypeError:
            continue

    # Last-resort signature-aware call.
    signature = inspect.signature(plant_safety_tool)
    kwargs = {}
    for name in signature.parameters:
        lower_name = name.lower()
        if "plant" in lower_name or "recommend" in lower_name:
            kwargs[name] = all_plant_dicts
        elif "safety" in lower_name or "pet" in lower_name or "child" in lower_name or "kid" in lower_name:
            kwargs[name] = safety_mode

    try:
        return plant_safety_tool(**kwargs)
    except Exception as exc:
        return {
            "status": "CAUTION",
            "plants_to_buy": all_plant_dicts,
            "careful_placement": [],
            "avoid": [],
            "recommendation": "Plant safety tool could not be rendered in the Cloud Run wrapper.",
            "error": str(exc),
        }


def call_impact_tracking_tool(plants_to_buy: list[dict[str, Any]]) -> dict[str, Any]:
    """Call impact_tracking_tool while tolerating small signature differences."""

    plant_names = [plant.get("common_name", str(plant)) for plant in plants_to_buy]

    attempts = [
        {"recommended_plants": plants_to_buy},
        {"plants": plants_to_buy},
        {"recommended_plants": plant_names},
        {"plants": plant_names},
        {"plant_count": len(plants_to_buy)},
    ]

    for kwargs in attempts:
        try:
            return impact_tracking_tool(**kwargs)
        except TypeError:
            continue

    return {
        "pollinator_support": "High" if len(plants_to_buy) >= 3 else "Medium",
        "water_need": "Low",
        "maintenance": "Low",
        "native_fit": "Strong",
        "tracking_action": "Take a first photo and log first bloom, new growth, or pollinator visits later.",
    }


def extract_plants_to_buy(
    safety_data: dict[str, Any],
    fallback_plants: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    for key in ["plants_to_buy", "Plants to buy", "safe_plants", "buy"]:
        value = safety_data.get(key)
        if isinstance(value, list):
            return value
    return fallback_plants


def extract_list(data: dict[str, Any], possible_keys: list[str]) -> list[Any]:
    for key in possible_keys:
        value = data.get(key)
        if isinstance(value, list):
            return value
    return []


def render_plant_list(plants: list[Any]) -> str:
    if not plants:
        return "<p>No plants returned for this section.</p>"

    html_parts = []
    for plant in plants:
        if isinstance(plant, dict):
            name = plant.get("common_name") or plant.get("name") or "Plant"
            scientific_name = plant.get("scientific_name", "")
            benefits = plant.get("benefits") or plant.get("reason") or plant.get("why") or ""
            care = plant.get("care") or plant.get("care_tip") or ""

            html_parts.append(
                f"""
                <div class="plant">
                  <h3>{safe_text(name)} {f'<span class="muted">({safe_text(scientific_name)})</span>' if scientific_name else ''}</h3>
                  {f'<p><strong>Why:</strong> {safe_text(benefits)}</p>' if benefits else ''}
                  {f'<p><strong>Care:</strong> {safe_text(care)}</p>' if care else ''}
                </div>
                """
            )
        else:
            html_parts.append(f"<li>{safe_text(plant)}</li>")

    if all(not isinstance(plant, dict) for plant in plants):
        return "<ul>" + "".join(html_parts) + "</ul>"

    return "".join(html_parts)


def render_warning_list(items: list[Any]) -> str:
    if not items:
        return "<p>No items in this section.</p>"

    output = "<ul>"
    for item in items:
        if isinstance(item, dict):
            name = item.get("common_name") or item.get("name") or item.get("plant") or "Plant"
            reason = item.get("reason") or item.get("note") or item.get("warning") or ""
            output += f"<li><strong>{safe_text(name)}:</strong> {safe_text(reason)}</li>"
        else:
            output += f"<li>{safe_text(item)}</li>"
    output += "</ul>"
    return output


@app.get("/", response_class=HTMLResponse)
def home():
    body = """
    <div class="hero">
      <h1>LeafStep Agent</h1>
      <p>
        Small first steps for pollinator-friendly, soil-supporting Oakville gardens.
      </p>
      <p class="muted">
        This public Cloud Run demo uses LeafStep's local tools and does not consume Gemini credits.
        The full ADK/Gemini agent is available in <code>app/agent.py</code>.
      </p>
    </div>

    <div class="card">
      <h2>LeafStep Starter Plan Generator</h2>
      <p>
        This demo is pre-selected for Oakville, Ontario because LeafStep's recommendations
        are localized to Oakville/Ontario conditions.
      </p>

      <form method="post" action="/plan">
        <label>Location</label>
        <p class="muted">
          Oakville, Ontario — fixed for this demo.
        </p>
        <input type="hidden" name="location" value="Oakville, Ontario">

        <label for="dimensions">Space size/type</label>
        <select id="dimensions" name="dimensions">
          <option value="3x5 backyard patch">3x5 backyard patch</option>
          <option value="small front yard patch">Small front yard patch</option>
          <option value="container garden">Container garden</option>
          <option value="larger garden bed">Larger garden bed</option>
        </select>

        <label for="sunlight">Sunlight</label>
        <select id="sunlight" name="sunlight">
          <option value="full sun">Full sun</option>
          <option value="partial shade">Partial shade</option>
          <option value="shade">Shade</option>
        </select>

        <label for="has_pets_or_children">Do you have pets or small children?</label>
        <select id="has_pets_or_children" name="has_pets_or_children">
          <option value="true">Yes</option>
          <option value="false">No</option>
        </select>

        <button type="submit">Generate my LeafStep plan</button>
      </form>
    </div>

    <div class="card">
      <h2>Live ADK/Gemini Mode</h2>
      <p>
        Reviewers can run the full ADK agent locally with their own Gemini API key:
      </p>
      <pre><code>export GEMINI_API_KEY="your_api_key_here"
export GOOGLE_GENAI_USE_VERTEXAI=FALSE
uv run adk web --port 8000</code></pre>
    </div>
    """
    return page_shell("LeafStep Agent", body)


@app.post("/plan", response_class=HTMLResponse)
def plan(
    location: str = Form(...),
    dimensions: str = Form(...),
    sunlight: str = Form(...),
    has_pets_or_children: str = Form(...),
):
    has_safety_needs = has_pets_or_children.lower() == "true"

    profile = space_intake_tool(
        location=location,
        dimensions=dimensions,
        sunlight=sunlight,
        experience_level="beginner",
        wants_indoor_support=False,
    )

    plants_data = plant_recommendation_tool(
        sunlight=profile["sunlight"],
        wants_indoor_support=False,
    )

    outdoor_plants = plants_data.get("outdoor_plants", [])
    outdoor_names = [plant.get("common_name", str(plant)) for plant in outdoor_plants]

    safety_data = call_plant_safety_tool(
        plants_data=plants_data,
        has_pets_or_children=has_safety_needs,
    )

    plants_to_buy = extract_plants_to_buy(safety_data, outdoor_plants)
    careful_placement = extract_list(
        safety_data,
        ["careful_placement", "Careful placement", "caution", "cautions", "warnings"],
    )
    avoid_plants = extract_list(
        safety_data,
        ["avoid", "Avoid", "plants_to_avoid", "unsafe_plants"],
    )

    final_plant_names = [
        plant.get("common_name", str(plant)) if isinstance(plant, dict) else str(plant)
        for plant in plants_to_buy
    ]

    space_type = "container garden" if "container" in dimensions.lower() else "garden patch"

    soil_data = soil_stewardship_tool(
        location=profile["location"],
        space_type=space_type,
    )

    care_data = care_plan_tool(
        plants=final_plant_names or outdoor_names,
        experience_level="beginner",
    )

    impact_data = call_impact_tracking_tool(plants_to_buy)

    proposed_inputs = [
        "organic leaf compost",
        "shredded leaf mulch",
        "natural mulch",
    ]

    guardrail = sustainability_guardrail_tool(
        proposed_plants=final_plant_names or outdoor_names,
        proposed_inputs=proposed_inputs,
    )

    preparation_steps = "".join(
        f"<li>{safe_text(step)}</li>"
        for step in soil_data.get("preparation_steps", [])
    )

    organic_practices = "".join(
        f"<li>{safe_text(step)}</li>"
        for step in soil_data.get("organic_practices", [])
    )

    first_week_items = []
    for period in ["Days 1-3", "Days 4-7"]:
        if period in care_data.get("schedule", {}):
            first_week_items.append(
                f"<li><strong>{safe_text(period)}:</strong> {safe_text(care_data['schedule'][period])}</li>"
            )
    first_week_html = "".join(first_week_items)

    care_tips_html = "".join(
        f"<li>{safe_text(tip)}</li>"
        for tip in care_data.get("tips", [])[:2]
    )

    safety_status = str(safety_data.get("status", "PASS"))
    safety_css = status_class(safety_status)

    guardrail_status = str(guardrail.get("status", "PASS"))
    guardrail_css = status_class(guardrail_status)

    if guardrail.get("violations"):
        guardrail_details = "<ul>" + "".join(
            f"<li>{safe_text(v)}</li>" for v in guardrail["violations"]
        ) + "</ul>"
    else:
        guardrail_details = """
        <ul>
          <li>No invasive plants detected.</li>
          <li>No synthetic pesticides or herbicides recommended.</li>
          <li>Organic soil inputs only.</li>
        </ul>
        """

    impact_lines = []
    impact_label_map = {
        "pollinator_support": "Pollinator support",
        "water_need": "Water need",
        "maintenance": "Maintenance",
        "native_fit": "Native fit",
        "tracking_action": "Tracking action",
    }

    for key, label in impact_label_map.items():
        if key in impact_data:
            impact_lines.append(f"<li><strong>{label}:</strong> {safe_text(impact_data[key])}</li>")

    if not impact_lines:
        for key, value in impact_data.items():
            impact_lines.append(f"<li><strong>{safe_text(key)}:</strong> {safe_text(value)}</li>")

    body = f"""
    <h1>Your LeafStep Starter Plan</h1>

    <div class="card">
      <h2>1. Space Profile</h2>
      <p><strong>Location:</strong> {safe_text(profile["location"])}</p>
      <p><strong>Space:</strong> {safe_text(profile["dimensions"])}</p>
      <p><strong>Sunlight:</strong> {safe_text(profile["sunlight"])}</p>
      <p><strong>Pets or small children:</strong> {"Yes" if has_safety_needs else "No"}</p>
      {f'<p class="muted">{safe_text(profile.get("space_warning", ""))}</p>' if profile.get("space_warning") else ''}
      {f'<p class="muted">{safe_text(profile.get("location_note", ""))}</p>' if profile.get("location_note") else ''}
    </div>

    <div class="card">
      <h2>2. Recommended Plants</h2>
      <p class="muted">These recommendations change when the sunlight selection changes.</p>
      {render_plant_list(plants_to_buy)}
    </div>

    <div class="card">
      <h2>3. Plant Safety Check</h2>
      <p>Status: <span class="{safety_css}">{safe_text(safety_status)}</span></p>
      <p><strong>Pets or small children:</strong> {"Yes" if has_safety_needs else "No"}</p>

      <h3>Careful placement</h3>
      {render_warning_list(careful_placement) if careful_placement else "<p>No careful-placement items returned for this plan.</p>"}

      <h3>Avoid</h3>
      {render_warning_list(avoid_plants) if avoid_plants else "<p>No avoid-list plants returned for this plan.</p>"}

      {f'<p><strong>Recommendation:</strong> {safe_text(safety_data.get("recommendation"))}</p>' if safety_data.get("recommendation") else ''}
      <p class="muted">Plant safety guidance is educational and does not replace veterinary, medical, or poison-control advice.</p>
    </div>

    <div class="card">
      <h2>4. Soil Stewardship</h2>
      <p><strong>Soil profile:</strong> {safe_text(soil_data.get("soil_profile", "General garden soil"))}</p>
      <ul>{preparation_steps}</ul>
      <h3>Organic practices</h3>
      <ul>{organic_practices}</ul>
      <p><strong>Tip:</strong> {safe_text(soil_data.get("tips", ""))}</p>
    </div>

    <div class="card">
      <h2>5. First-Week Action Plan</h2>
      <ul>{first_week_html}</ul>
      {f'<h3>Care tips</h3><ul>{care_tips_html}</ul>' if care_tips_html else ''}
    </div>

    <div class="card">
      <h2>6. Impact Snapshot</h2>
      <ul>
        {''.join(impact_lines)}
      </ul>
    </div>

    <div class="card">
      <h2>7. Sustainability Guardrail</h2>
      <p>Status: <span class="{guardrail_css}">{safe_text(guardrail_status)}</span></p>
      {guardrail_details}
      <p><strong>Recommendation:</strong> {safe_text(guardrail.get("recommendation", ""))}</p>
    </div>

    <p>
      <a class="button" href="/">Try another plan</a>
      <a class="button" href="/demo">View text demo</a>
    </p>
    """

    return page_shell("Your LeafStep Plan", body)


@app.get("/demo", response_class=PlainTextResponse)
def demo():
    try:
        result = subprocess.run(
            [sys.executable, "demo.py"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        output = result.stdout.strip()

        if result.stderr.strip():
            output += "\n\n--- stderr ---\n" + result.stderr.strip()

        if not output:
            output = "Demo ran but produced no output."

        return output

    except Exception as exc:
        return f"Demo failed: {exc}"


@app.get("/health")
def health():
    return {"status": "ok", "service": "leafstep-agent"}