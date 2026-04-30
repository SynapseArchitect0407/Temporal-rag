# 🏗️ Temporal-Alpha: System Architecture

Temporal-Alpha is a **Recursive RAG Engine** designed to mitigate "Temporal Drift" in large-scale retrieval systems. It is optimized for high-velocity execution on **ARMv8-A (Mobile/Edge)** architectures, achieving benchmark speeds of over 300,000 nodes/sec.

---

## 🧠 The Veritas Swarm (Orchestration Layer)
The system operates through a tri-agent "Brain Trust" that ensures factual integrity through time-weighted validation.

* **Scout Agent**: Performs asynchronous vector stream diving to identify candidate shards based on raw semantic similarity.
* **Chronos Agent**: The temporal gatekeeper. It applies exponential decay kernels to verify the "freshness" of shards while protecting **Stability-Shielded** foundational data.
* **Architect Agent**: Synthesizes verified shards into a high-density executive summary, maintaining an optimal context-to-noise ratio.

---

## 📉 Mathematical Foundation: The Stability-Shielded Kernel
Standard RAG systems treat all information as static. Temporal-Alpha treats information as a decaying signal.

### **Temporal Decay Formula**
The primary scoring mechanism utilizes the following exponential decay function:
$$f(t) = \omega \cdot e^{-\lambda \Delta t}$$
*Where:*
* $\omega$: Raw semantic similarity.
* $\lambda$: Decay coefficient.
* $\Delta t$: Delta time (nanosecond precision).

### **The Stability Shield**
To prevent the erasure of **Long-Term Strategic Objectives**, we implement a bias-protection layer:
```text
Score = f(t) + (Similarity^2 * STABILITY_BIAS)
```

---

## 🛡️ Edge Optimizations (ARMv8 / Termux)
* **Entropy Gating**: Queries are routed through a Shannon-entropy filter. Low-complexity queries (Entropy < 0.7) stay local to save battery and compute cycles.
* **Thermal Guarding**: Ingestion batches include 10ms "cool-down" cycles to maintain SoC stability during high-load stress tests.
* **Memory Compression**: Recursive summarization flattens deep context into "Wisdom Nodes," enabling infinite-horizon memory on limited RAM.

---

## 🗺️ Future Roadmap
* **Phase 2**: Integration of Domain-specific weighting kernels for high-precision environments.
* **Phase 3**: Multi-device swarm synchronization via peer-to-peer protocols.

