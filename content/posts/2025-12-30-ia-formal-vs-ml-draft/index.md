---
og_image: og-image-1200x630.png
image: "og-image.svg"
tags:
title: "Computational cost and truth affinity: formal languages ​​vs ML (Draft)"
date: 2025-12-30T10:00:00+01:00
draft: true
layout: post
  - ia
---
- formal-methods
  - machine learning
  -research---
This article compares, in draft mode, the computational cost and truth-friendliness of two approaches to building AI systems: methods based on formal languages (specification, verification, synthesis) and the currently dominant machine learning (ML) approaches.

Introduction
---
-------
In the next generations we will see two paradigms compete and complement each other: formal methods (logical modeling, verification, synthesis by specification) and current statistical approaches (neural networks, transformers). Here I compare its expected short- and medium-term computational cost, its scalability, and what I call "truth affinity": the system's propensity to produce correct, justifiable, and verifiable outputs.

Quick definitions
---
-----------------
- Formal languages: systems built on mathematical logic, grammars and automata; They include model checking, formal testing, and programmatic synthesis.
- Machine learning (ML): statistical models that approximate functions from data; its guarantees are probabilistic.

Computational cost according to time horizon
---
----------------------------------------
We use three axes: initial development cost, computational cost for training/compiling/verification, and maintenance/adaptation cost.

- Short term (1–3 years): ML masters language/vision tasks; Formal methods remain in critical niches.
- Medium term (3–7 years): improvements in synthesis and verification will reduce costs in structured domains; ML improves efficiency (distillation, sparsity, dedicated hardware).
- Long term (>7 years): hybrids appear (specifications that guide ML; ML that suggests formal invariants); The cost/benefit ratio will depend a lot on the hardware available.

Guidance estimates (summary)
---
-------------------------------

- Formal methods: high human cost to specify; Verification can be intensive (from 10^2 to 10^4 core-seconds for non-trivial modules, depending on abstraction and tool). Efficient maintenance if there is good modularity.
- ML: Modern large model training can use 10^6–10^9 GPU-seconds at full scale; Optimized inference lowers the cost per request.

Factors that change the cost ratio
---
----------------------------------

- Specialized hardware (TPU, NPU, SMT accelerators) and algorithmic advances can reduce costs on both sides.
- Data vs. specifications: obtaining labeled data is expensive; formally specifying properties is also important.

Affinity to truth (definition and comparison)
---
-----------------------------------------

We define "truth affinity" as the ability of the system to produce outputs that correspond to verifiable facts, invariants, or requirements, and to justify why the output is correct.

- Formal languages: high affinity for truth when the specification is correct and complete; verification provides evidence within the formal model. Risk: If the specification is poor, the warranties are misleading (GIGO).
- ML: probabilistic affinity dependent on data quality and coverage; may hallucinate or show biases; Limited explainability except using XAI techniques.

Hybrids
---
-----

Hybrid approaches (ML suggesting candidates, formal methods verifying) offer a balance: search space reduction thanks to ML and correctness guarantee provided by verification. In many domains this pattern offers better cost/truth than either approach alone.

Applications by domain
---
---------------------

- Critical (medical, aerospace): formal preferred; higher cost but the affinity to truth and traceability justify the investment.
- Creative NLP and generation: ML dominates; expensive and difficult formal guarantees.
- Mixed systems (business+rules): practical combination: formal rules + ML for ranking.

Practical economics
---
--------------

- Critical formal project: higher human cost and tools; high amortization if the failure has a high cost.
- Large ML project: infrastructure (GPU/TPU), data and operation costs; Scalability reduces cost per user.

Conclusion (DRAFT — review pending)
---
--------------------------------------

WARNING: This conclusion is left as a draft at the author's request. The balance between computational cost and truth affinity is not a binary choice; However, the claim that "convergence will be the norm" requires nuance: it depends heavily on the domain, the social cost of error, and improvements in formal and ML techniques.

Open points (to review):

- What weight should be given to probabilistic verification compared to classical verification in mixed systems?
- How to correctly quantify the human cost of specifying complex systems versus the cost of obtaining and curating data? (required for real ROI)
- What is the realistic horizon for ML-guided synthesis to reduce the verification cost in practice?

Tell me how you want to modify the conclusion and I will update it. The post is marked `draft: true` and I will not upload it to git unless you tell me to.