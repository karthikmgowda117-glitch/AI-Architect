import json
from agents.core.llm_client import GroqClient
from dotenv import load_dotenv

load_dotenv()

class PlannerAgent:
    def __init__(self):
        self.llm = GroqClient()
        self.system_prompt = (
            "You are the Strategic Planner for ResearchPilot AI. "
            "Your job is to break down a complex research topic into 3 distinct, "
            "searchable sub-queries. Output ONLY a valid Python-style list of strings."
        )

    def generate_plan(self, topic: str):
        print(f"📋 PlannerAgent: Breaking down '{topic}' into sub-tasks...")
        
        prompt = (
            f"Topic: {topic}\n\n"
            "Create 3 specific search queries that cover different angles of this topic. "
            "Example: If topic is 'Electric Cars', queries could be 'EV battery tech 2026', "
            "'Global EV market share 2026', and 'EV charging infrastructure challenges'."
        )

        response = self.llm.generate(prompt, system_message=self.system_prompt)
        
        # Simple cleanup to ensure we get a list
        try:
            # This handles cases where the LLM adds markdown or extra text
            start = response.find('[')
            end = response.rfind(']') + 1
            plan = eval(response[start:end])
            return plan
        except:
            # Fallback if eval fails
            return [f"{topic} overview", f"{topic} latest developments", f"{topic} future outlook"]

if __name__ == "__main__":
    planner = PlannerAgent()
    print(planner.generate_plan("The impact of Agentic AI on Software Engineering"))