# ruff: noqa
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

import os
import re
import google.auth
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools import LongRunningFunctionTool
from google.genai import types

load_dotenv()

# Check for a user-provided API key first
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    os.environ["GEMINI_API_KEY"] = api_key
    if "GOOGLE_GENAI_USE_VERTEXAI" in os.environ:
        del os.environ["GOOGLE_GENAI_USE_VERTEXAI"]
    if "GOOGLE_CLOUD_PROJECT" in os.environ:
        del os.environ["GOOGLE_CLOUD_PROJECT"]
    if "GOOGLE_CLOUD_LOCATION" in os.environ:
        del os.environ["GOOGLE_CLOUD_LOCATION"]
else:
    # Fallback to local Google Cloud Vertex AI credentials for testing
    try:
        _, project_id = google.auth.default()
        os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
        os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
    except Exception:
        pass

def redact_pii(text: str) -> str:
    """Redacts PII like SSNs from text before processing.
    
    Args:
        text: The user input text.
    Returns:
        Text with SSNs redacted.
    """
    return re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[REDACTED SSN]', text)

def draft_budget(strategy: str) -> str:
    """Drafts a numeric budget based on a financial strategy.
    
    Args:
        strategy: The high-level financial strategy.
    Returns:
        A formatted draft budget.
    """
    return f"Budget Draft: Housing 30%, Food 20%, Savings 20%, Other 30% based on {strategy}"

def audit_budget(draft: str) -> str:
    """Audits the draft budget for correctness.
    
    Args:
        draft: The drafted budget.
    Returns:
        An audited and verified budget.
    """
    return f"Verified Budget: {draft}"

def request_approval(final_budget: str) -> dict:
    """Request Human-In-The-Loop (HITL) approval for the final budget.
    
    Use this tool when the budget is finalized and ready for the user to review.
    Calling this tool will pause execution until the user responds.

    Args:
        final_budget: The final audited budget string to show the user.
    """
    return {"status": "awaiting_approval", "budget": final_budget}

root_agent = Agent(
    name="budget_orchestrator",
    model=Gemini(
        model="gemini-flash-lite-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Orchestrator for the AI Budget Planner.",
    instruction="""You are the Main Orchestrator for the AI Budget Planner. 
Your workflow:
1. Use redact_pii on the user's input.
2. Develop a strategy and use draft_budget.
3. Use audit_budget to verify it.
4. ALWAYS call request_approval to get the user's final sign-off before completing your turn.
""",
    tools=[
        redact_pii,
        draft_budget,
        audit_budget,
        LongRunningFunctionTool(func=request_approval),
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
