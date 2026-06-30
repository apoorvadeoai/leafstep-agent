import html
import os
from typing import Any

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import root_agent

app = FastAPI(title="LeafStep Agent LLM Demo")

APP_NAME = "leafstep_agent_llm_web"
USER_ID = "cloud_run_demo_user"


def run_leafstep_agent(prompt: str) -> dict[str, Any]:
    session_service = InMemorySessionService()
    session = session_service.create_session_sync(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=prompt)],
    )

    output: dict[str, Any] = {
        "text": [],
        "tool_calls": [],
        "tool_responses": [],
        "error": None,
    }

    try:
        events = runner.run(
            user_id=USER_ID,
            session_id=session.id,
            new_message=message,
        )

        for event in events:
            if not event.content or not event.content.parts:
                continue

            for part in event.content.parts:
                if part.text:
                    output["text"].append(part.text)

                if part.function_call:
                    output["tool_calls"].append(
                        {
                            "name": part.function_call.name,
                            "args": dict(part.function_call.args),
                        }
                    )

                if part.function_response:
                    output["tool_responses"].append(
                        {
                            "name": part.function_response.name,
                            "response": part.function_response.response,
                        }
                    )

    except Exception as exc:
        output["error"] = str(exc)

    return output


def render_result(result: dict[str, Any]) -> str:
    if result.get("error"):
        return f"""
        <section class="card error">
          <h2>Gemini / ADK Error</h2>
          <p>{html.escape(result["error"])}</p>
          <p>This may happen if the Gemini model is temporarily overloaded. The no-LLM demo remains available as the stable public demo.</p>
        </section>
        """

    text_html = "".join(
        f"<pre>{html.escape(text)}</pre>" for text in result.get("text", [])
    )

    calls_html = "".join(
        f"<li><strong>{html.escape(call['name'])}</strong><pre>{html.escape(str(call['args']))}</pre></li>"
        for call in result.get("tool_calls", [])
    )

    responses_html = "".join(
        f"<li><strong>{html.escape(response['name'])}</strong><pre>{html.escape(str(response['response']))}</pre></li>"
        for response in result.get("tool_responses", [])
    )

    return f"""
    <section class="card">
      <h2>Agent Response</h2>
      {text_html or "<p>No final text returned.</p>"}
    </section>

    <section class="card">
      <h2>Tool Calls</h2>
      <ol>{calls_html or "<li>No tool calls returned.</li>"}</ol>
    </section>

    <section class="card">
      <h2>Tool Responses</h2>
      <ol>{responses_html or "<li>No tool responses returned.</li>"}</ol>
    </section>
    """


def page(body: str) -> str:
    return f"""
    <!doctype html>
    <html>
    <head>
      <title>LeafStep LLM Demo</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          max-width: 960px;
          margin: 40px auto;
          padding: 0 20px;
          background: #f5fbf4;
          color: #18351f;
        }}
        textarea {{
          width: 100%;
          min-height: 180px;
          padding: 12px;
          font-size: 16px;
        }}
        button {{
          background: #236b36;
          color: white;
          border: none;
          padding: 12px 18px;
          border-radius: 8px;
          font-size: 16px;
          cursor: pointer;
        }}
        .card {{
          background: white;
          border: 1px solid #d8ead8;
          border-radius: 12px;
          padding: 18px;
          margin: 18px 0;
        }}
        .error {{
          border-color: #f1b4b4;
          background: #fff7f7;
        }}
        pre {{
          white-space: pre-wrap;
          background: #f3f6f3;
          padding: 12px;
          border-radius: 8px;
          overflow-x: auto;
        }}
      </style>
    </head>
    <body>
      <h1>LeafStep Agent — LLM / ADK Demo</h1>
      <p>This version calls the ADK/Gemini LeafStep agent and shows tool calls plus tool responses.</p>
      {body}
    </body>
    </html>
    """


DEFAULT_PROMPT = """Plan a first LeafStep for this household.

Use these exact intake details:
- Location: 123 Maple Street, Oakville
- Space type: backyard patch
- Sunlight: part sun
- Garden style: flowers
- Safety mode: pets and kids
- Starter size: small

Please call the LeafStep tools to:
1. Normalize the intake.
2. Recommend plants.
3. Apply the pet/kid safety filter.
4. Create impact tracking badges.
5. Create soil stewardship guidance.
6. Create a 30-day care plan.
7. Run the sustainability guardrail check.

Then give a short final summary for a beginner.
"""


@app.get("/", response_class=HTMLResponse)
def home():
    body = f"""
    <form method="post">
      <textarea name="prompt">{html.escape(DEFAULT_PROMPT)}</textarea>
      <p><button type="submit">Run LeafStep LLM Agent</button></p>
    </form>
    """
    return page(body)


@app.post("/", response_class=HTMLResponse)
def run_prompt(prompt: str = Form(...)):
    result = run_leafstep_agent(prompt)
    body = f"""
    <form method="post">
      <textarea name="prompt">{html.escape(prompt)}</textarea>
      <p><button type="submit">Run LeafStep LLM Agent Again</button></p>
    </form>
    {render_result(result)}
    """
    return page(body)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "mode": "llm",
        "gemini_key_present": bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")),
    }
