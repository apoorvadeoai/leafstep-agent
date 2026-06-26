# Skill Usage

LeafStep uses skills as development-time support for building, reviewing, and preparing the capstone submission.

## Skills added

### `leafstep-code-review`

A project-specific code review skill for checking ADK structure, tool orchestration, guardrail usage, tests, README quality, token efficiency, and secret safety.

### `leafstep-submission-review`

A project-specific submission review skill for checking the final capstone story, judging clarity, demo strength, ADK/Gemini usage, skills usage, sustainability impact, safety guardrails, and limitations.

## Why these are development-time skills

LeafStep's runtime behavior is handled by:

- `app/agent.py`
- `app/tools.py`
- Gemini through Google ADK
- The registered LeafStep tools, including `sustainability_guardrail_tool`

The `.agents/skills/` files document repeatable review workflows used while building and preparing the capstone.