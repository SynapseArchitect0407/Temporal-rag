import math
import random
from typing import Final

ENTROPY_THRESHOLD: Final[float] = 0.7 

class EntropyGatedOrchestrator:
    """
    We're adding a 'brain' to our retrieval trigger.
    """

    def calculate_query_entropy(self, query: str) -> float:
        """
        Measuring the 'complexity density' of the request.
        """
        words = query.lower().split()
        if not words: return 0.0

        word_counts = {w: words.count(w) for w in set(words)}
        probs = [count / len(words) for count in word_counts.values()]

        entropy = -sum(p * math.log2(p) for p in probs)

        normalized_entropy = min(entropy / 4.0, 1.0)
        return normalized_entropy

    def should_trigger_swarm(self, query: str) -> bool:
        """
        The gatekeeper. We only pull from the vector stream if 
        the query's uncertainty exceeds our threshold.
        """
        uncertainty_level = self.calculate_query_entropy(query)

        print(f"[Gatekeeper] Query Uncertainty: {uncertainty_level:.2f}")

        if uncertainty_level > ENTROPY_THRESHOLD:
            print("[Gatekeeper] Entropy High. Engaging Veritas Swarm...")
            return True

        print("[Gatekeeper] Entropy Low. Processing via local weights only.")
        return False

if __name__ == "__main__":
    gate = EntropyGatedOrchestrator()

    # Test 1: Simple/Low Entropy
    print("\n--- Testing Simple Query ---")
    gate.should_trigger_swarm("Hello there.")

    # Test 2: Complex/High Entropy
    print("\n--- Testing Complex Query ---")
    gate.should_trigger_swarm("Integrate the ARMv8 thermal telmetry")

