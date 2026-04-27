import math
import time
from typing import List, Dict, Final

STABILITY_BIAS: Final[float] = 0.15
DRIFT_CORRECTION_FACTOR: Final[float] = 1.2

class DriftResistantKernel:
    """
    Look, standard decay is too aggressive for what we're building.
    If we only prioritize the 'now,' we lose the 'why.'
    This kernel protects our long-term mission data from fading out.
    """
    def __init__(self, decay_lambda: float = 0.05):
        self.decay_lambda = decay_lambda

        self.reference_time = time.time_ns()

    def calculate_drift_corrected_score(self, omega: float, timestamp_ns: int) -> float:
        """
        Here's the logic: We apply the standard exponential decay to the base, 
        but then we layer on a 'Stability Shield.'
        Formula: (Similarity * Decay) + (Similarity^2 * Stability)

        If a piece of info is highly relevant (ω > 0.8), the squared term 
        kicks in, essentially locking it into our 'active memory' 
        regardless of how old it is.
        """

        delta_t_sec = (self.reference_time - timestamp_ns) / 1e9

        temporal_decay = math.exp(-self.decay_lambda * delta_t_sec)

        stability_shield = (omega ** 2) * STABILITY_BIAS

        fused_score = (omega * temporal_decay) + stability_shield

        return min(fused_score, 1.0)

    def rerank_stream(self, stream_data: List[Dict]) -> List[Dict]:
        """
        Reranking the stream while fighting off vector drift.
        This ensures our LLM keeps its eyes on the prize.
        """
        self.reference_time = time.time_ns() # Refresh 'now' for this specific pass

        for node in stream_data:

            node['fused_score'] = self.calculate_drift_corrected_score(
                node['score'],
                node['timestamp']
            )

        return sorted(stream_data, key=lambda x: x['fused_score'], reverse=True)

if __name__ == "__main__":

    kernel = DriftResistantKernel()
    now = time.time_ns()

    one_week_ago = now - (86400 * 7 * 1e9)

    mock_nodes = [
        {
            "id": "relocation_strategy",
            "content": "Deep insightful networking with peers for collaborations.",
            "score": 0.95,
            "timestamp": one_week_ago
        },
        {
            "id": "temporary_debug_log",
            "content": "Checking if the terminal font-size is readable.",
            "score": 0.35,
            "timestamp": now - (60 * 1e9)
        }
    ]

    results = kernel.rerank_stream(mock_nodes)

    print(f"--- [Temporal-Alpha] Drift Correction: Success ---")
    for r in results:

        status = "SHIELDED" if r['score'] > 0.8 else "DECAYED"
        print(f"Node: {r['id']} | Result: {r['fused_score']:.4f} | Logic: {status}")
