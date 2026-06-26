from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
import subprocess
import sys

app = FastAPI(title="LeafStep Agent Demo")


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <head>
        <title>LeafStep Agent</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            max-width: 850px;
            margin: 40px auto;
            line-height: 1.6;
            padding: 0 20px;
          }
          code {
            background: #f3f3f3;
            padding: 2px 5px;
            border-radius: 4px;
          }
          .button {
            display: inline-block;
            margin-top: 12px;
            padding: 10px 14px;
            background: #2f6f4e;
            color: white;
            text-decoration: none;
            border-radius: 6px;
          }
        </style>
      </head>
      <body>
        <h1>LeafStep Agent</h1>

        <p>
          LeafStep helps Oakville, Ontario households take one practical first step
          toward pollinator-friendly, soil-supporting, low-maintenance gardening.
        </p>

        <h2>Cloud Run Demo Mode</h2>
        <p>
          This deployed version uses the reliable local no-LLM demo so reviewers can
          view the project without requiring live Gemini API credits.
        </p>

        <p>
          The repository also includes a Google ADK/Gemini agent implementation with
          registered tools, guardrails, and project-specific skills.
        </p>

        <p>
          <a class="button" href="/demo">View LeafStep Demo Output</a>
        </p>

        <h2>Workshop Concepts Demonstrated</h2>
        <ul>
          <li>Google ADK agent architecture in <code>app/agent.py</code></li>
          <li>Tool-oriented design in <code>app/tools.py</code></li>
          <li>Sustainability guardrail tool</li>
          <li>Project-specific skills under <code>.agents/skills/</code></li>
          <li>Google Cloud Run deployment</li>
        </ul>

        <h2>Live ADK/Gemini Mode</h2>
        <p>
          Reviewers can run the live ADK Web version locally with their own Gemini API key:
        </p>

        <pre><code>export GEMINI_API_KEY="your_api_key_here"
uv run adk web --port 8000</code></pre>

        <p>
          This deployed Cloud Run app does not collect reviewer API keys.
        </p>
      </body>
    </html>
    """


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
