from pathlib import Path

ROOT = Path(__file__).parent

required_paths = [
    "main.py",
    "Dockerfile",
    "requirements.txt",
    "demo.py",
    "README.md",
    "app/agent.py",
    "app/tools.py",
    "docs/skill_usage.md",
    "docs/workshop_concepts.md",
    ".agents/skills/leafstep-code-review/SKILL.md",
    ".agents/skills/leafstep-submission-review/SKILL.md",
]

checks = {}

for path in required_paths:
    checks[f"{path} exists"] = (ROOT / path).exists()

main_text = (ROOT / "main.py").read_text() if (ROOT / "main.py").exists() else ""
docker_text = (ROOT / "Dockerfile").read_text() if (ROOT / "Dockerfile").exists() else ""
req_text = (ROOT / "requirements.txt").read_text() if (ROOT / "requirements.txt").exists() else ""
agent_text = (ROOT / "app" / "agent.py").read_text() if (ROOT / "app" / "agent.py").exists() else ""
tools_text = (ROOT / "app" / "tools.py").read_text() if (ROOT / "app" / "tools.py").exists() else ""

checks.update({
    "FastAPI app defined": "FastAPI" in main_text,
    "Demo endpoint defined": "/demo" in main_text,
    "Health endpoint defined": "/health" in main_text,
    "Dockerfile runs uvicorn": "uvicorn main:app" in docker_text,
    "requirements include fastapi": "fastapi" in req_text.lower(),
    "requirements include uvicorn": "uvicorn" in req_text.lower(),
    "ADK root_agent preserved": "root_agent" in agent_text,
    "space intake tool present": "space_intake_tool" in tools_text,
    "plant recommendation tool present": "plant_recommendation_tool" in tools_text,
    "soil stewardship tool present": "soil_stewardship_tool" in tools_text,
    "care plan tool present": "care_plan_tool" in tools_text,
    "sustainability guardrail tool present": "sustainability_guardrail_tool" in tools_text,
})

failed = [name for name, passed in checks.items() if not passed]

for name, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'} - {name}")

if failed:
    raise SystemExit(f"\nDay 5 validation failed: {', '.join(failed)}")

print("\nDay 5 validation passed. LeafStep is ready for Cloud Run deployment.")
