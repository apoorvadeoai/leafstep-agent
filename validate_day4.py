from pathlib import Path

ROOT = Path(__file__).parent

agent_path = ROOT / "app" / "agent.py"
tools_path = ROOT / "app" / "tools.py"

agent_text = agent_path.read_text() if agent_path.exists() else ""
tools_text = tools_path.read_text() if tools_path.exists() else ""

checks = {
    "app/agent.py exists": agent_path.exists(),
    "app/tools.py exists": tools_path.exists(),
    "root_agent defined": "root_agent" in agent_text,
    "Gemini model configured": "gemini" in agent_text.lower(),
    "lightweight model configured": "flash-lite" in agent_text.lower(),
    "space intake tool registered": "space_intake_tool" in agent_text,
    "plant recommendation tool registered": "plant_recommendation_tool" in agent_text,
    "soil stewardship tool registered": "soil_stewardship_tool" in agent_text,
    "care plan tool registered": "care_plan_tool" in agent_text,
    "sustainability guardrail registered": "sustainability_guardrail_tool"
    in agent_text,
    "guardrail tool defined": "def sustainability_guardrail_tool" in tools_text,
    "code review skill exists": (
        ROOT / ".agents" / "skills" / "leafstep-code-review" / "SKILL.md"
    ).exists(),
    "submission review skill exists": (
        ROOT / ".agents" / "skills" / "leafstep-submission-review" / "SKILL.md"
    ).exists(),
    "skill usage doc exists": (ROOT / "docs" / "skill_usage.md").exists(),
}

failed = [name for name, passed in checks.items() if not passed]

for name, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'} - {name}")

if failed:
    raise SystemExit(f"\nDay 4 validation failed: {', '.join(failed)}")

print("\nDay 4 validation passed.")
