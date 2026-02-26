import asyncio
import json
# Direct import to ensure AgentMemory is found
from agents.core.memory import AgentMemory

class ResearchOrchestrator:
    def __init__(self):
        print("--- Initializing ResearchOrchestrator ---")
        self.memory = AgentMemory()
        
        # Initialize your logic agents
        from agents.logic.planner_agent import PlannerAgent
        from agents.logic.search_agent import SearchAgent
        from agents.logic.analysis_agent import AnalysisAgent
        from agents.logic.hypothesis_agent import HypothesisAgent
        from agents.logic.synthesis_agent import SynthesisAgent
        
        self.planner = PlannerAgent()
        self.searcher = SearchAgent()
        self.analyzer = AnalysisAgent()
        self.hypothesizer = HypothesisAgent()
        self.synthesizer = SynthesisAgent()

    async def run_mission(self, topic: str):
        try:
            yield {"agent": "Planner", "status": "active", "msg": "Planning..."}
            plan = self.planner.generate_plan(topic)
            await asyncio.sleep(0.5)

            results = []
            for query in plan:
                yield {"agent": "Search", "status": "active", "msg": f"Searching: {query}"}
                raw_data = self.searcher.execute_search(query)
                self.memory.add_fact(raw_data)
                
                yield {"agent": "Analysis", "status": "active", "msg": "Analyzing..."}
                analysis = self.analyzer.analyze_results(query, raw_data)
                results.append(analysis)

            yield {"agent": "Hypothesis", "status": "active", "msg": "Generating Hypothesis..."}
            context = "\n".join(self.memory.retrieve_relevant(topic, k=3))
            hypotheses = self.hypothesizer.generate_hypotheses(topic, context)

            yield {"agent": "Synthesis", "status": "active", "msg": "Synthesizing..."}
            final_report = self.synthesizer.synthesize(topic, results + [hypotheses])

            yield {"type": "complete", "content": final_report}
        except Exception as e:
            yield {"type": "error", "msg": str(e)}