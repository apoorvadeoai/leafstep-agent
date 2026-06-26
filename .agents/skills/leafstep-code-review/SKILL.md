---
name: leafstep-code-review
description: Review LeafStep Agent code, tools, tests, README updates, demo output, and submission materials for Google ADK structure, tool orchestration clarity, sustainability guardrails, beginner-friendly UX, token efficiency, and capstone readiness.
---

# LeafStep Code Review

Use this review checklist when changing LeafStep Agent code or documentation.

Check:

1. `app/agent.py` keeps `root_agent` as the ADK entrypoint.
2. The agent uses a lightweight Gemini model for local demo cost control.
3. The agent instruction clearly explains the LeafStep flow.
4. The agent uses the registered LeafStep tools instead of giving generic gardening advice.
5. `sustainability_guardrail_tool` is used before final recommendations when safety or sustainability concerns appear.
6. `app/tools.py` keeps tools deterministic, small, and easy to test.
7. The demo remains beginner-friendly for an Oakville household.
8. README changes clearly explain what was built and how to run it.
9. No API keys, secrets, or local `.env` files are committed.
10. The project story stays focused on a small first step, not a huge gardening transformation.

Return:

- Pass/fail
- Issues found
- Suggested fixes