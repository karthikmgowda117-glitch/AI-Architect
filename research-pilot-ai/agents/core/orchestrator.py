import asyncio
from agents.core.memory import AgentMemory
from agents.logic.planner_agent import PlannerAgent
from agents.logic.search_agent import SearchAgent
from agents.logic.analysis_agent import AnalysisAgent
from agents.logic.hypothesis_agent import HypothesisAgent
from agents.logic.synthesis_agent import SynthesisAgent

class ResearchOrchestrator:
    def __init__(self):
        self.memory = AgentMemory()
        self.planner = PlannerAgent()
        self.searcher = SearchAgent()
        self.analyzer = AnalysisAgent()
        self.hypothesizer = HypothesisAgent()
        self.synthesizer = SynthesisAgent()

    async def run_mission(self, topic: str):
        """
        Executes the multi-agent research mission.
        Yields status updates for the Frontend status cards.
        """
        # 1. Planning
        yield {"agent": "Planner", "status": "active", "msg": "Strategic planning initiated..."}
        plan = self.planner.generate_plan(topic)
        await asyncio.sleep(0.5)

        results = []
        # 2. Sequential Research Loop
        for query in plan:
            yield {"agent": "Search", "status": "active", "msg": f"Searching: {query}"}
            raw_data = self.searcher.execute_search(query)
            
            # Index the raw data for semantic retrieval (RAG)
            self.memory.add_fact(raw_data)
            
            yield {"agent": "Analysis", "status": "active", "msg": "Extracting insights..."}
            analysis = self.analyzer.analyze_results(query, raw_data)
            results.append(analysis)

        # 3. Hypothesis (Using FAISS Retrieval)
        yield {"agent": "Hypothesis", "status": "active", "msg": "Querying vector memory..."}
        # Get the top 3 most relevant facts from the whole mission
        context = "\n".join(self.memory.retrieve_relevant(topic, k=3))
        hypotheses = self.hypothesizer.generate_hypotheses(topic, context)

        # 4. Final Synthesis
        yield {"agent": "Synthesis", "status": "active", "msg": "Polishing final report..."}
        final_report = self.synthesizer.synthesize(topic, results + [hypotheses])

        # 5. Signal Completion
        yield {"type": "complete", "content": final_report}