from agents.core.llm_client import GroqClient
from dotenv import load_dotenv

load_dotenv()

class SynthesisAgent:
    def __init__(self):
        self.llm = GroqClient()
        self.system_prompt = (
            "You are the Lead Research Synthesizer for ResearchPilot AI. "
            "You will be given several sub-analyses on a topic. Your job is to: \n"
            "1. Merge them into one comprehensive, logical document.\n"
            "2. Remove any redundant information.\n"
            "3. Ensure a professional tone and clear executive summary at the top.\n"
            "4. Retain all source URLs as citations."
        )

    def synthesize(self, main_topic: str, all_analyses: list[str]):
        print(f"✍️ SynthesisAgent: Compiling final report for '{main_topic}'...")
        
        combined_text = "\n\n".join(all_analyses)
        prompt = (
            f"Main Topic: {main_topic}\n\n"
            f"Individual Analyses:\n{combined_text}\n\n"
            "Synthesize this into a single, cohesive research report."
        )

        try:
            return self.llm.generate(prompt, system_message=self.system_prompt)
        except Exception as e:
            return f"Error during synthesis: {str(e)}"