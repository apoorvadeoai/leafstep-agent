# Workshop Concepts Used in LeafStep Agent

LeafStep Agent uses several core concepts from the Google 5-Day Gen AI / Vibe Coding workshop.

## 1. ADK Agent Architecture

LeafStep includes a Google ADK agent structure in `app/agent.py`. The agent defines `root_agent` and registers the LeafStep tools that support the household sustainability workflow.

## 2. Tool-Oriented Agent Design

LeafStep separates the conversation layer from deterministic tool logic. The local tools live in `app/tools.py` and cover:

- space intake
- plant recommendation
- soil stewardship
- establishment care plan
- sustainability guardrail

This keeps the core recommendation logic testable and less dependent on model creativity.

## 3. Guardrails

LeafStep includes a sustainability guardrail tool to review recommendations for unsafe, invasive, or non-sustainable advice. This helps keep the agent focused on safe, practical, local actions.

## 4. Skills

LeafStep includes project-specific development skills under `.agents/skills/`:

- `leafstep-code-review`
- `leafstep-submission-review`

These skills document repeatable review workflows for code quality, capstone readiness, safety, and final submission polish.

## 5. Cloud Deployment

LeafStep is deployed to Google Cloud Run. Because Gemini API quota was limited during final packaging, the deployed service uses the reliable local deterministic demo path while preserving the ADK/Gemini implementation in the repository.
