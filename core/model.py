import asyncio
import time
from dataclasses import dataclass, field
from typing import List, Final, Dict

SUMMARY_THRESHOLD: Final[int] = 5
COMPRESSION_MODEL: Final[str] = "gpt-4o-mini"

@dataclass(slots=True)
class MemoryNode:
    node_id: str
    content: str
    timestamp: int
    is_summary: bool = False

class TemporalSummarizer:
    """
    Converts a stream of 'Raw Experience' into 'Condensed Wisdom'.
    """
    def __init__(self):
        self.raw_buffer: List[MemoryNode] = []
        self.archived_summaries: List[MemoryNode] = []

    async def _call_llm_summarizer(self, text_to_condense: str):

        await asyncio.sleep(0.5)
        return f"[RECURSIVE SUMMARY]: Optimized synthesis of {len(text_to_condense.split())} words into a core semantic anchor."

    async def process_new_node(self, node: MemoryNode):
        self.raw_buffer.append(node)

        if len(self.raw_buffer) >= SUMMARY_THRESHOLD:
            print(f"\n[Agent] Buffer limit reached ({SUMMARY_THRESHOLD}). Triggering Recursive Summarization...")
            await self.summarize_yesterday()

    async def summarize_yesterday(self):
        """
        The Core Logic:
        1. Takes all raw nodes in the buffer.
        2. Merges them into a single high-density string.
        3. Calls LLM to generate a 'Memory Node'.
        4. Flushes the buffer and saves the summary.
        """
        start_time = time.perf_counter()

        combined_text = " | ".join([n.content for n in self.raw_buffer])

        condensed_wisdom = await self._call_llm_summarizer(combined_text)

        summary_node = MemoryNode(
            node_id=f"sum_{int(time.time())}",
            content=condensed_wisdom,
            timestamp=int(time.time()),
            is_summary=True
        )

        self.archived_summaries.append(summary_node)
        self.raw_buffer.clear()

        duration = (time.perf_counter() - start_time) * 1000
        print(f"[Agent] Compression Success. Latency: {duration:.2f}ms | Buffer Flushed.")

async def main():
    agent = TemporalSummarizer()
    print("--- [Temporal-Alpha] Recursive Memory Agent Demo ---")

    for i in range(6):
        print(f"[System] Ingesting Node {i}...")
        new_node = MemoryNode(
            node_id=f"raw_{i}",
            content=f"Detailed observation number {i} regarding ARMv8 thermal state...",
            timestamp=int(time.time())
        )
        await agent.process_new_node(new_node)
        await asyncio.sleep(0.1)

    print(f"\nFinal State:")
    print(f"Raw Buffer Count: {len(agent.raw_buffer)}")
    print(f"Archived Summaries: {len(agent.archived_summaries)}")
    print(f"Latest Memory: {agent.archived_summaries[0].content}")

if __name__ == "__main__":
    asyncio.run(main())
