import numpy as np
import time
import logging
from typing import List,Dict,Optional

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger("TemporalRag")

class TemporalRAGCore:
    def __init__(self,dimension: int=384,alpha: float=0.05):

        self.dim = dimension
        self.alpha = alpha

        # Stream A: Ephemeral Buffer("The Working Memory")

        self._temp_vectors: List[np.ndarray] = []
        self.e_matrix: Optional[np.ndarray] = None
        self.e_metadata: List[Dict] = []

        # Stream B: Persistent store("The Crystallized Knowledge")

        self.p_matrix: Optional[np.ndarray] = None
        self.p_metadata: List[Dict] = []

    def _rebuild_index(self):
        """Synchronizes the list buffer into a searchable Numpy matrix"""

        if self._temp_vectors:
            self.e_matrix = np.vstack(self._temp_vectors)
            logger.info(f"Synchronized Ephemeral Index:{self.e_matrix.shape[0]} vectors.")

    def add_to_ephemeral(self,vector: np.ndarray,text:str,importance:float = 1.0):
        """Adds vector with safety checks and recursive potential."""

        try:
            norm = np.linalg.norm(vector)
            norm_vec = vector/(norm+1e-9)

            self._temp_vectors.append(norm_vec)
            self.e_metadata.append({
                   "ts" : time.time(),
                   "text" : text,
                   "hits" : 0,
                   "base_importance" : importance
            })

            #Batch rebuild for effficiency

            if len(self._temp_vectors)%50==0:
                self._rebuild_index()

        except Exception as e:
            logger.error(f"Ingestion Error: {e}")

    def get_decay_weights(self):
        """Calculates e^ (-alpha*∆t) for all ephemeral items"""

        now = time.time()
        deltas = np.array([(now-m["ts"])/60 for m in self.e_metadata])

        return np.exp(-self.alpha*deltas)

    def query(self,query_vec:np.ndarray,k: int=5):
        """Hybrid Search : Semamtic Similarity × Temporal Freshness."""

        if self.e_matrix is None and self._temp_vectors:
            self._rebuild_index()

        if self.e_matrix is None:
            return[]

        query_vec = query_vec/(np.lingalg.norm(query_vec) + 1e-9)

        semantic_sim = np.dot(self.e_matrix, query_vec)

        temporal_weights = self.get_decay_weights()

        final_scores = semantic_sim*temporal_weights

        top_k = np.argsort(final_scores)[::-1][:k]

        return[(self.e_metadata[i], final_scores[i]) for i in top_k]

if __name__ == "__main__":

    engine = TemporalRAGCore()
    print(f"Engine logic is ready")

