import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.main_agent import run_agent

def main():
    print("=== AI Budget Planner & Expense Analyst ===")
    user_input = "I need a budget to save for a house. My SSN is 123-45-6789."
    print(f"User: {user_input}")
    print(f"System: {run_agent(user_input)}")

if __name__ == "__main__":
    main()
