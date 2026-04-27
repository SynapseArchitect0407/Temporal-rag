import math
import time
from dataclasses import dataclass
from typing import List,Final,Dict

DEFAULT_LAMBDA : Final[float] = 0.05
MIN_RELEVANCE_GATE : Final[float] = 0.1

@dataclass(slots=True)
class ScoredTemporalNode:
    node_id : str
    content : str
    similarity_score : float
    temporal_weight : float
    fused_score : float

class TemporalScoringKernel:
    """Mathematical kernel for time-weighted retrieval."""

    def __init__(self,decay_lambda : float = DEFAULT_LAMBDA):
        self.decay_lambda = decay_lambda
        self.reference_time = time.time_ns()

    def _calculate_weight(self,timestamp_ns :int):
        """Compute exponential decay weight based on time difference."""

        delta_t_sec = (self.reference_time-timestamp_ns)/1e9
        weight = math.exp(-self.decay_lambda*delta_t_sec)

        return weight if weight >= MIN_RELEVANCE_GATE else 0.0

    def rerank(self,base_results : List[Dict]):
        """Rerank results using temporal decay + semantic similarity."""

        self.reference_time = time.time_ns()
        scored_nodes : List[ScoredTemporalNode] = []

        get_weight = self._calculate_weight

        for node in base_results:
            omega = node.get("score",0.5)
            ts = node.get("timestamp",self.reference_time)

            temporal_w = get_weight(ts)
            fused_score = omega*temporal_w

            if fused_score>0:
                scored_nodes.append(
                  ScoredTemporalNode(
                   node_id = node["node_id"],
                   content = node["content"],
                   similarity_score = omega,
                   temporal_weight = temporal_w,
                   fused_score = fused_score,
              )
            )

        return sorted(scored_nodes,key=lambda x: x.fused_score,reverse=True)

if __name__ == "__main__":
    kernel = TemporalScoringKernel()
    now = time.time_ns()

    mock_results = [
      {
       "node_id" : "fresh_01",
       "content" : "Recent AI breakthrough",
       "score" : 0.8,
       "timestamp" : now,
      },
      {
       "node_id" : "stale_99",
       "content" : "Outdated 2021 tech",
       "score" : 0.9,
       "timestamp" : int(now-(86400*5*1e9)),
      },
    ]

    start = time.perf_counter()
    reranked = kernel.rerank(mock_results)
    end = time.perf_counter()

    print("---[Tempral-RAG] Scoring Kernel Results---")

    for node in reranked:
        print(f"ID : {node.node_id} | Final : {node.fused_score:.4f}"
              f"(TempW : {node.temporal_weight:.4f})")
        print(f"Kernel Latency: {(end-start)*1000:.4f}ms")


