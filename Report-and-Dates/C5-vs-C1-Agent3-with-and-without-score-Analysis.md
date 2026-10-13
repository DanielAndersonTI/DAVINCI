# Agent 3 With and Without the Reference Score — C5 Control Test (Gemini)

**Scope of this text:** comparative analysis of Agent 3 (consolidator) under two conditions — with access to the Precision/Recall/F1 scores calculated against the reference architecture (C1 configuration and *with-score* arm of C5) and without such access (*without-score* arm of C5). It addresses the question: **does Agent 3 deliver good results on its own, or can its results only be explained by access to the score?** All numbers come from artifacts stored on disk; none were manually recalculated.

> **Article text.** Sections 1 to 7 are written for inclusion in the manuscript. The final section is a note to the author and **must not be published**.

---

## 1. What C5 Is — and What It Is Not

Configurations C0 to C4 in the study vary the **pipeline composition**: which agents are included, in what order, and with what input material. Each configuration is a treatment, with repeated runs, and these are the configurations to which the article's contrast tests are applied.

C5 does not belong to this family. It does not introduce a new system configuration or propose a different way of generating architectures. It is a **paired control test on a single agent**, designed to close an interpretive gap: the gains observed in configurations with consolidation (C1 and C2) could be attributed to the work of Agent 3 or, alternatively, to the fact that Agent 3 makes its decision with the reference score available. Since the pipeline design provides this score, the main-study contrasts do not separate these two explanations.

C5 does. In the same run, Agents 1 and 2 (with Agent 4 refinement) generate Proposals A and B **once**; these two proposals are frozen and stored on disk (`entrada_a.txt` and `entrada_b.txt`); and Agent 3 is run **twice** on exactly the same candidates:

* **with-score arm** — the same Agent 3 used in C1, which receives the Precision, Recall, and F1 metrics of each proposal against the reference;
* **without-score arm** — a prompt variant of the same Agent 3, which makes its decision based only on the requirements, the content of the two proposals, and their coherence.

Because the candidates are identical in both arms, any difference in outcome between them can be attributed to the score rather than to generation variation. This is why C5 has **two rounds rather than three**: it is not a treatment arm whose mean needs to be estimated precisely; it is a control whose unit of inference is the **pair** (same candidates, two arms). Two rounds per system already produce 16 pairs, and the repetition exists so that a potential fallback in one arm for one system is not interpreted as a property of the experimental design. C5 also does not enter the family of contrasts in the main study: its results are reported descriptively, within the declared scope of a single model.

The scope is Gemini. The study selected a single model for this control because it is the model in which there is a positive effect to explain — the two significant contrasts in the study (C1 vs. C3 and C2 vs. C3, on the interaction axis) are from Gemini — and because, with DeepSeek, Agent 3 frequently failed and fell back, whereas with Claude the contrasts were negligible. There is no claim to defend for the other models, and executing them would incur costs without proportional scientific return. The result is therefore presented with the explicit qualification: **verified on Gemini, where the consolidation contrasts were significant.**

## 2. Unit of Analysis and What Is Measured

The unit is the **run**, rather than the system-level average. The reason is that C5 is paired within the run: the pair of arms shares candidates, requirements, and token budget, so the valid comparison is arm against arm within the same run, while aggregation by system would only add generation noise. Where a system-level view is useful, it is reported as a count of systems, never as an average.

For each output, **service F1** and **interaction F1** are measured against the reference, using the same evaluation function employed throughout the rest of the study. In addition, each output is compared byte-for-byte with Proposals A and B (SHA-256), allowing each arm's result to be classified into three categories: **copy of A**, **copy of B**, or **original output**. This classification is necessary because only it distinguishes *selection* from *synthesis*.

## 3. Baseline: Agent 3 in C1

Before C5, the behavior of Agent 3 with the score available was measured across the 24 C1 runs on Gemini (8 systems × 3 rounds).

**Agent 3 hardly synthesizes: it selects.** In 22 of the 24 runs, the consolidated architecture is **byte-identical** to one of the two proposals — a copy of Proposal A in 16 runs and Proposal B in 6. Only 2 runs produce original text.

**The service axis never discriminates.** The service F1 of Proposals A and B is identical in all 24 runs. All observable decision-making by Agent 3 occurs on the interaction axis.

**On the interaction axis, the score discriminates in 10 of the 24 runs.** In these 10 cases, Agent 3's output was equal to or better than the best of the two proposals in **9**, and worse in **1** (Cargo Tracker, third round: 0.7273 versus 0.8421 for Proposal B). In one run (7ep, second round), the original output outperformed both proposals (1.0000 versus 0.9524 and 0.7500). Comparing the consolidated output with the best of the two proposals: **22 ties, 1 improvement, 1 deterioration.**

Taken together: with the score, Agent 3 returns one of the existing proposals and chooses the better one when the two diverge. The gain attributed to consolidation, on Gemini, is therefore a gain in **selection**, not in the fusion of complementary interactions. This interpretation directly motivates C5: if Agent 3's role is to choose, the question becomes whether it chooses well **without** the score.

## 4. Main Result: The Two C5 Arms

C5 produced 16 pairs (8 systems × 2 rounds). The result is **equality between the arms**.

| Measure                                   | With-score arm    | Without-score arm |
| ----------------------------------------- | ----------------- | ----------------- |
| Fallback to Proposal A                    | 4/16              | 2/16              |
| Copy of A or B                            | 15/16 (13 A, 2 B) | 13/16 (9 A, 4 B)  |
| Original output (not identical to A or B) | 1/16              | 3/16              |
| Interaction F1 identical to the other arm | 14/16             | 14/16             |

**The interaction F1 of the two arms is identical in 14 of the 16 runs.** The two divergences are:

| Run                   | With score            | Without score         | Cause of difference               |
| --------------------- | --------------------- | --------------------- | --------------------------------- |
| Cargo Tracker, Test-1 | 0.0000 (fallback → A) | 0.6087 (selected B)   | fallback in the with-score arm    |
| TNTConcept, Test-2    | 0.7761 (selected B)   | 0.7647 (fallback → A) | fallback in the without-score arm |

The two divergences have opposite signs — one favors each arm — and **both are caused by a fallback on one side, not by a different selection**. When both arms returned a valid CSV, the result was the same, with one textual exception (DayTrader7, Test-2), where the texts differ but the F1 is identical.

In the **4 cases where the proposals actually diverge** on the interaction axis, performance is symmetric: the with-score arm gets 2 right and 2 wrong; the without-score arm gets 2 right and 2 wrong. All four errors are fallbacks — two on each side. In other words, **neither arm made an incorrect selection: both failed because they were unable to produce a valid response.** When the without-score arm actually responded in a decisive case, it selected the better proposal both times this occurred (Cargo Tracker Test-1 → Proposal B; 7ep Test-2 → Proposal A).

The service axis reinforces this interpretation. Proposals A and B have different service F1 in only 1 of the 16 runs (Cargo Tracker, Test-1: 0.9091 versus 0.7692), and in that case the with-score arm obtained the better service score not through a decision, but because the fallback returned Proposal A.

**Interpretation.** On Gemini, the reference score does not alter Agent 3's outcome. This does not mean that dispensing with the reference is harmless in general; it means that, **in this corpus**, the cases in which the two proposals diverge are easy enough for a coherence-based judgment to reach the same conclusion as the score. The clearest evidence is Cargo Tracker: Proposal A has an interaction F1 of zero because its dependencies are not service names, but text fragments ("destination", "load", "last-known-location"). An agent examining the two proposals can recognize this without any metric; the score and coherence agree because the defect is obvious. In the only case where the with-score arm outperformed the without-score arm, the margin was 0.0114 F1 (TNTConcept, Test-2) — and the without-score arm did not make the wrong selection; it fell back.

The consequence for the article text is one of precision, not a weakening of the finding. Consolidation gains on Gemini should be described as gains in **selection** — placing one of the already-generated proposals in the output by choosing the better one — rather than as synthesis. Regarding dependence on the score, the control does not support the claim that the reference-free variant is inferior: it is statistically indistinguishable from the reference-based variant in this corpus. What the control does support, and what constitutes the specific finding of C5, is that **the difference between the two variants is dominated by the validity of Agent 3's response, rather than by the information it receives.**

## 5. The Fallbacks

Fallbacks are included in the analysis, but not as results: they are counted, reported, and **excluded from what is interpreted as an Agent 3 decision**. What is evaluated is the consolidation outcome — the selection — in the two arms; a fallback is not a selection, but the absence of one. For this reason, the C5 instrumentation records, for each arm, the `fallback_proposta_a` flag, which C1 did not record (there, fallback is silent and indistinguishable from "selected Proposal A"). This is a relevant methodological difference between the two measurements and must be stated in the text: in C1, some of the 16 copies of Proposal A may be fallbacks rather than decisions, and the artifact does not allow the two cases to be separated.

There is, however, an indication that this masking is limited in C1. If Agent 3 in C1 fell back at the frequency observed in C5 (4 out of 16), one would expect, among the 10 runs in which the score discriminates, to see some copy of Proposal A precisely where Proposal B was better. This never occurs: the copies of A in the decisive runs of C1 are all cases in which A was the better proposal. The indication is weak by construction (n = 10) and should not be presented as an estimate; it merely shows that the finding in Section 3 is not an artifact of the silent fallback.

In C5, the fallback rate was 25% in the with-score arm (4/16) and 12.5% in the without-score arm (2/16). Two points deserve mention. First, **the score did not reduce failure**: the arm receiving it fell back twice as often. Second, the fallbacks are not concentrated in a single system: with score, they occurred in Cargo Tracker (two rounds), Jokul (Test-2), and TNTConcept (Test-1); without score, in Cargo Tracker (Test-2) and TNTConcept (Test-2). Since the failure is the inability to produce a valid architecture CSV, it is essentially a model event rather than an experimental-design event — reinforcing that the comparison between arms should be interpreted over pairs in which both arms responded.

## 6. Agent 3 Token Cost

The cost of Agent 3 is practically the same under both conditions, both per invocation and in the accumulated cost per arm.

|                                                         | With score | Without score |
| ------------------------------------------------------- | ---------- | ------------- |
| Tokens per invocation (median)                          | ≈ 6,470    | ≈ 6,418       |
| Tokens per arm, when it runs once (median)              | 7,004      | 6,439         |
| Runs in which the arm required more than one invocation | 3/15       | 1/15          |

The interpretation is straightforward: **adding the score to the prompt does not make consolidation perceptibly more expensive.** Both conditions consume roughly the same amount per invocation, and differences in total cost arise from occasional reinvocations rather than prompt size. For reference, Agent 3 in C1 consumes a median of 6,431 tokens per run, approximately 17% of the total run cost (median of 53,068 tokens) — a value that is consistent with both C5 conditions. The total cost of a C5 run ranges from 518,000 to 541,000 tokens, in the same order of magnitude as C1, confirming that removing the score does not make the pipeline cheaper: it only removes the information without reducing the agent's workload.

Two observability caveats should be noted in the limitations: the tracker still records `prompt_tokens` as zero (input cost is obtained as `total − completion`), and, for each Agent 3 run, there is one call that the tracker cannot attribute to any role (≈ 3,700 tokens). This call was excluded from the per-agent number and occurs equally in both arms, so it does not affect the comparison.

## 7. Limitations

1. **The corpus provides little discrimination.** In 12 of the 16 C5 runs (and 14 of the 24 C1 runs), the two proposals have the same interaction F1, so no selection is possible. All inference therefore rests on 4 runs in C5 and 10 in C1.
2. **The divergence, when it exists, is coarse.** The decisive cases involve obvious defects (dependencies that are not service names), making coherence-based judgment easy and reducing the control's power to detect the value of the score in subtle cases.
3. **Single model.** The result applies to Gemini. There is no basis for extending it to DeepSeek — where Agent 3 frequently failed — or to Claude, where the contrasts were negligible.
4. **Silent fallback in C1.** The fallback flag exists only in C5; in C1, "selected Proposal A" and "fell back" are indistinguishable in the artifact. Section 5 presents evidence that this does not distort the interpretation, but does not quantify it.

## 8. Synthesis

On Gemini, Agent 3 does not construct a new architecture: it returns one of the two proposals it receives — an exact copy in 22 of the 24 C1 runs and in 15 of the 16 with-score C5 runs. Its value lies in choosing the better of the two, and it does so well: with the score, the output was equal to or better than the best proposal in 9 of the 10 runs in which the two diverged.

The control test shows that **this success does not depend on the score**. With frozen and identical candidates in both arms, Agent 3 with and without the reference metrics produces the same interaction F1 in 14 of the 16 runs; the two divergences are explained by fallback, one in favor of each arm; and neither arm made an incorrect selection when it actually made a selection. The factor separating the outcomes is not the information the agent receives, but whether it was able to produce a valid architecture.

For the article, this establishes two points. First, the nature of the gain: consolidation, on Gemini, is **selection**, and should be described as such. Second, the limit of the claim regarding the reference: the space in which the two variants differ is small in this corpus, and the observed difference is dominated by response validity rather than by the presence of the score. The safe claim, supported by the data, is that the consolidation gains are realized in the scenario in which the reference is available — the scenario assumed by the tool, since the interface provides the reference as an input — and that the reference-free variant was not shown to be inferior, because the divergent cases in the corpus are resolved equally by both approaches.

---

## Note to the Author — Do Not Publish

**1. Where the data and framing are in tension.** Emanuel's framing asks that the text state that the consolidation gains apply in the scenario in which the reference is available, which is true and is reflected in the synthesis. However, it also suggests that C5 would show the reference-free variant *performing worse*. **It does not.** Across the 16 paired runs, interaction F1 is identical in 14; the two divergences offset each other (one favors each arm), and both are fallbacks rather than selections. Writing that the score-free agent "fails to discriminate" would be contradicted by the artifact itself — and the review has the files. The formulation used in the text is stronger and more defensible: the control shows that the difference between the variants is dominated by **response validity**, rather than by the information received, and that the decisive cases in the corpus are too easy to distinguish between the two conditions. If a version more closely aligned with the original framing is preferred, the maximum supported by the data is:

*"C5 did not allow us to isolate an effect of the score because the divergent cases in the corpus can be resolved through coherence"*

— which still leaves the main claim standing.

**2. Correction of an error in the two existing drafts.** The files `Gemini/C5/C5-Gemini-Synthesize-two-three-tests.txt` and `Synthesize-two-three-tests-C5-Gemini.txt` (which I did not modify) treat C5 as if it had **only** the without-score arm — their wording states that "Agent 3 performs consolidation without access to reference-based Precision/Recall/F1." This is not what C5 is: each run executes both arms, and both are recorded. Worse, the drafts interpret fallbacks as selections. Two literal examples:

* Test-2, Cargo Tracker: the draft states *"A3 selected A ... the clearest failure of the reference-free configuration"*. The artifacts show `fallback_proposta_a: true` in **both** arms — there was no selection.
* Test-2, TNTConcept: the draft states *"A3 selected A, missing the slightly better proposal"*. The without-score arm **fell back**; meanwhile, in the same run, the with-score arm selected B (0.7761), which was the better proposal. The draft loses the entire contrast.

The drafts also ignore the 6 C5 fallbacks and the C1 baseline (22 exact copies in 24 runs), without which the comparison is not supported. I suggest not reusing them without revision.

**3. Necessary adjustment to the project memories.** The previous C1 measurement (`a3-seleciona-nao-consolida`) recorded "9 discriminative runs, 9 correct." The correct count is **10 discriminative runs** — DayTrader7 FS1 was missing (A = 0.9091, B = 0.0000). The number of correct selections remains 9, with 1 original output worse than the best proposal (Cargo Tracker FS3). I have already corrected the memory.

**4. Provenance.** Everything here comes from `result/<system>/c5_fewshot/run_<execution_id>/` (`sumario.json`, `c5_bracos.json`, the four CSVs by SHA-256) and from `Report-and-Dates/Gemini/C1/Test-{1,2,3}/execuion-metadados-C1-Gemini-FS{1,2,3}.json`. Both C5 arms use the same `max_tokens` (16,384), and the only difference between them is the prompt.
