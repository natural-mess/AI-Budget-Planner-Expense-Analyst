# AI Budget Planner & Expense Analyst

An intelligent, multi-agent system designed for the Kaggle Capstone Project. This application acts as a personal financial advisor by ingesting user inputs, automatically categorizing expenses, and generating a personalized, actionable budget plan using an advanced Agent Development Kit (ADK) architecture.

## Features

- **Multi-Agent Architecture (ADK):** Powered by a custom lightweight Agent Development Kit standardizing context injection and logging across specialized agents (`Planner`, `Worker`, `Evaluator`).
- **Modular Agent Skills:** Agents dynamically equip skills like the `CalculatorSkill` to perform deterministic mathematical operations without relying on LLM hallucinations.
- **Security Features:**
  - **PII Redaction:** Intercepts user input and automatically masks sensitive data (like SSNs) via the `PIIRedactorSkill` before it reaches agent memory.
  - **Human-In-The-Loop (HITL):** A security gate that halts execution to request explicit user approval if any finalized budget category exceeds a defined threshold (e.g., $1000).

## Project Structure

```text
├── project/
│   ├── adk/                 # Agent Development Kit (BaseAgent, SecurityManager, A2A Protocol)
│   ├── agents/              # Planner, Worker, Evaluator Agents
│   ├── memory/              # Session memory management
│   ├── skills/              # Modular agent skills (Calculator, PII Redactor)
│   ├── app.py               # Main application entry point
│   ├── main_agent.py        # Central workflow orchestrator
│   ├── requirements.txt     # Python dependencies
│   └── run_demo.py          # Quick automated test script
```

## Getting Started

1. **Clone the repository.**
2. **Install dependencies:**
   ```bash
   pip install -r project/requirements.txt
   ```
3. **Run the Interactive App:**
   ```bash
   python project/app.py
   ```
4. **Run the Automated Demo:**
   ```bash
   python project/run_demo.py
   ```
