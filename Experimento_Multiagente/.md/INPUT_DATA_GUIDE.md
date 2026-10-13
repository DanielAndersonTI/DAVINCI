# Input Data Guide

This document explains the role of each input required by the DAVINCI Microservice Architecture Workbench and how to collect it.

---

## Why These Inputs Are Used

### System Requirements

The textual requirements describe what the system must do. They are the **only input the generating agents receive** (Agents 1, 2 and 4); the consolidator (Agent 3) additionally receives the evaluation metrics of the two proposals, as described below. The LLM agents read the requirements to:

- identify distinct business capabilities;
- group related responsibilities into cohesive services;
- infer necessary communications between services.

Requirements must be as complete and precise as possible, because they are the sole source of evidence for the generated architecture.

### Reference Services

The reference services list represents the expected set of microservices for the system. Agents 1 and 2 (and the refiner, Agent 4) never see it: the proposals are generated from the requirements alone.

The reference has two uses:

- **Evaluation:** Precision, Recall and F1-score compare the proposed service names with this reference list, for the two proposals and for the final consolidated architecture.
- **Consolidation signal (C1, C2 and C4):** the same metrics of the two proposals are passed to Agent 3, which uses them to choose the strongest base and to combine complementary interactions. Agent 3 does not generate services; it consolidates what Agents 1 and 2 produced.

If the reference is not provided, the metrics are computed against an empty reference and come out zeroed.

### Reference Interactions

The reference interactions describe which pairs of services are expected to communicate. Each interaction is an unordered pair of service names, e.g., `order-service <-> payment-service`.

The same two uses apply: evaluation of the two proposals and of the final architecture, and — in C1, C2 and C4 — as part of the metrics passed to the consolidator (Agent 3). They allow the calculation of interaction-level metrics and help determine whether the pipeline identified the necessary dependencies.

### Name Normalization Map

Different agents may generate slightly different service names for the same concept (e.g., `api-gateway`, `gateway`, `apigateway`). The normalization map maps these variations to a canonical name.

This map is used **only during evaluation** to avoid penalizing valid services or interactions that use alternative names. It does not influence the generation process.

---

## How to Collect These Inputs

### System Requirements

Gather requirements from:

- product owners;
- domain experts;
- user stories;
- functional specification documents;
- existing documentation or legacy system analysis.

Write them as a numbered list of functional capabilities, including any explicit technical requirements (e.g., service discovery, centralized configuration, API gateway, monitoring) if they are part of the system specification.

Organize the requirements as clearly as possible, because the quality of the generated architecture depends heavily on the completeness and precision of this text.

### Reference Services

To build the reference service list:

1. Identify the major business capabilities of the system.
2. Apply Domain-Driven Design (DDD) or bounded-context analysis to group related responsibilities.
3. Name each resulting service using a clear, consistent convention.
4. Use this list as the ground truth for service evaluation.

If you do not have a predefined target architecture, you can derive it from the same business capabilities used during analysis.

### Reference Interactions

To build the reference interaction set:

1. Analyze the business workflows and processes described in the requirements.
2. Determine which services must exchange data or trigger actions to complete those workflows.
3. Record each required pair as an unordered interaction (e.g., `service-a <-> service-b`).
4. Include only interactions that are clearly necessary; avoid adding speculative links.

### Name Normalization Map

The normalization map can be built by anticipating common naming variations:

- synonyms (e.g., `customer` → `customer-service`);
- abbreviation or concatenation (e.g., `apigateway` → `api-gateway`);
- plural/singular differences;
- naming choices made by different architects.

Map each alternative to the canonical service name used in the reference list. This prevents valid services or interactions from being penalized only because of superficial differences in writing.

---

## Summary

| Input | Used by Agents 1/2/4 (generation and refinement)? | Used for evaluation? | Used by Agent 3 (consolidation)? |
|-------|----------------------|----------------------|----------------------|
| System Requirements | Yes | No | Yes — as context |
| Reference Services | No | Yes | Yes — metrics of the two proposals (C1, C2, C4) |
| Reference Interactions | No | Yes | Yes — metrics of the two proposals (C1, C2, C4) |
| Name Normalization Map | No | Yes | No |

The DAVINCI Workbench generates the candidate architectures from the requirements alone. The reference data and the normalization map are used to compute the evaluation metrics; in the configurations that run the consolidator (C1, C2 and C4), the metrics of the two proposals are also passed to Agent 3 as its selection signal — Agent 3 consolidates the proposals, it does not generate architecture.