from typing import List, Final, Any
from dataclasses import dataclass, field

MAX_WINDOW_TOKENS: Final[int] = 4096
COMPRESSION_RATIO: Final[float] = 0.5

@dataclass(slots=True)
class ContextWindow:
    """
    Stateful manager for the active attention window.
    """
    active_tokens: int = 0
    buffer: List[dict] = field(default_factory=list)


class TemporalSlidingWindow:
    """
    Score-In-Score-Out dynamic pruning
    """

    def __init__(self, token_limit: int = MAX_WINDOW_TOKENS):
        self.token_limit = token_limit
        self.current_window = ContextWindow()

    def sync_window(self, new_scored_nodes: List[Any]):
        """
        Integrates new nodes and prunes stale ones
        """

        incoming_buffer = [
            {
                "id": n.node_id,
                "text": n.content,
                "tokens": len(n.content.split()),
                "score": n.fused_score,
            }
            for n in new_scored_nodes
        ]

        full_context = sorted(
            self.current_window.buffer + incoming_buffer,
            key=lambda x: x["score"],
            reverse=True,
        )

        running_total = 0
        optimized_buffer = []

        for node in full_context:
            if running_total + node["tokens"] <= self.token_limit:
                optimized_buffer.append(node)
                running_total += node["tokens"]
            else:
                break

        self.current_window.buffer = optimized_buffer
        self.current_window.active_tokens = running_total

        return "\n---\n".join(n["text"] for n in optimized_buffer)

    def get_stats(self):
        print("--- [Temporal-RAG] Window Metrics ---")
        print(f"Window Density: {self.current_window.active_tokens}/{self.token_limit} tokens")
        print(f"Active Context Fragments: {len(self.current_window.buffer)}")



if __name__ == "__main__":
    window_manager = TemporalSlidingWindow(token_limit=100)

    class MockNode:
        def __init__(self, nid, content, score):
            self.node_id = nid
            self.content = content
            self.fused_score = score

    nodes = [
        MockNode("A", "Critical fresh info...", 0.95),
        MockNode("B", "Secondary context...", 0.45),
        MockNode("C", "Deeply stale background...", 0.12),
    ]

    final_prompt = window_manager.sync_window(nodes)

    print("\n--- Final Prompt ---\n")
    print(final_prompt)

    window_manager.get_stats()
