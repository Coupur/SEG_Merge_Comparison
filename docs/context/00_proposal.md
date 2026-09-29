# Merge-Tool Evaluation Under Ecosystem Drift: Pilot Study Proposal

Sep 29, 2026 · @Sam

## Abstract

We propose to measure how the results of automated merge tools change with time and environment, instead of reporting one ranking from one snapshot. Published comparisons of merge tools use different datasets, metrics, language versions, and models, so a ranking mixes the quality of a tool with the conditions of its evaluation.

We treat every result as a function of a (tool, environment, data era) triple. We run a fixed set of tools over Java merge scenarios from several eras, in both their published and modernized environments, and log the effort needed to run and port each tool.

The outputs are per-tool decay curves, rank stability across eras, and an idea-survival comparison for LLM-based tools: the original tool, its idea ported to a modern LLM, and the plain modern LLM. The design commits to no expected result.

## 1. Background: merging

A merge combines two lines of development that started from a common ancestor. The ancestor is the *base*; the two versions are *parent 1* and *parent 2*. A three-way merge compares each parent to the base to find what each side changed, then combines the two sets of changes.

When the two sets of changes touch different places, the merge is automatic. When they touch the same place, a line-based tool such as Git reports a *conflict*, and a developer resolves it by hand.

Line-based merging fails in both directions:

- **Needless conflict.** Parent 1 renames a variable on a line and parent 2 changes that variable's starting value on the same line. The changes are independent, but Git reports a conflict.
- **Clean but wrong.** Parent 1 renames a method and parent 2 adds a call to the old name on a different line. Git merges without complaint, but the result no longer compiles.

Merge tools exist to reduce the first failure without causing the second.

## 2. How merge tools differ

Merge tools differ mainly in what they treat as the unit of change: a line, a syntax node, a program element, or a text pattern learned from history.

| Approach | Works on | Examples | Trade-off |
| --- | --- | --- | --- |
| Line-based | Lines of text | Git Merge (ort, recursive), diff3 | Fast and language-independent; conflicts on same-line edits; can merge cleanly but wrongly |
| Character-level | Characters | Hires-Merge | Resolves same-line edits; loses surrounding context |
| Structured (tree) | Syntax tree of one language | JDime, Spork, AutoMerge; generic: Mergiraf, LastMerge | Fewer conflicts, but more correct and more incorrect merges; slower; most are Java-only |
| Graph-based | Graph of classes, methods, fields | IntelliMerge | Handles renames and moves; rarely applicable in Schesch et al.'s data |
| Learned | Model trained on past resolutions | DeepMerge, MergeBERT (classifies merge patterns), MergeGen (generates code) | Tied to the training data and model of its era; often not public |
| LLM-prompted | Prompt with the conflict and examples | GMerge, ChatMerge | Tied to the model generation and per-call cost |

JDime first runs a fast line-based pass and falls back to slower tree-based merging only when needed. Its authors call this staged approach auto-tuning.

**Import statements.** These are the lines at the top of a Java file that name the libraries and classes the file uses. Many changes touch them, so they conflict often: about 93% of merges in Schesch et al.'s final dataset involve them.

**Ablation-style comparison.** Schesch et al. built Imports, a tool that runs Git Merge and then re-merges only import-line conflicts. Spork and IntelliMerge also handle imports, so the comparison separates the value of import handling from the value of the rest of each tool. Imports outperformed both, which suggests the remaining parts of those tools add little or subtract value.

The lesson for this study is that the value of a component, a tool, and an environment must be measured separately.

## 3. Measuring a merge

Every merge attempt ends in one of three outcomes:

- **Unhandled.** The tool reports conflicts, and a developer resolves them by hand with the conflict location and diff supplied.
- **Correct.** The tool reports no conflicts, and the result behaves as intended. In practice this means it builds and passes the project's tests.
- **Incorrect.** The tool reports no conflicts, but the result fails to compile or fails tests.

An incorrect merge costs more than an unhandled one because nothing signals the defect. A developer must find it later, through a failing test or in production.

Let U be the number of unhandled merges, I the number of incorrect merges, N the total, and k the cost of an incorrect merge relative to an unhandled one. The developer cost and the effort reduction against resolving everything by hand are:

```latex
\mathrm{Cost}(T) = (U + k\,I)\cdot c_U
\qquad
\mathrm{ER}_k(T) = 1 - \frac{U + k\,I}{N}
```

Here c\_U is the average cost of one unhandled merge. A tool that only produces correct merges scores 1; a tool that only produces unhandled merges scores 0; a score below 0 is worse than no tool.

**Worked example.** Per 100 merges, Spork gives about 54 correct, 35 unhandled, 11 incorrect; Git Merge (ort) gives about 46, 51, 3 (rounded from Schesch et al.). The table shows cost in units of one unhandled merge; lower is better.

| k | Spork | Git Merge (ort) | Resolve all by hand |
| --- | --- | --- | --- |
| 1 | 46 | 54 | 100 |
| 2 | 57 | 57 | 100 |
| 4 | 79 | 63 | 100 |
| 6 | 101 | 69 | 100 |
| 8 | 123 | 75 | 100 |

Spork resolves more merges but makes more mistakes, so its rank depends on k. In the full evaluation it is the best tool at k = 1 and the worst except IntelliMerge by k of about 2. Schesch et al. made k an explicit parameter of the ranking; this study makes data era and environment explicit parameters in the same way.

The previous study reports cost at k = 1, 2, 4, 8 and also classifies each merge as better, comparable, unresolved, or worse than the human resolution. Which taxonomy to use is an open decision (Section 10).

## 4. The problem: rankings depend on conditions that are rarely reported

A published ranking describes one tool, in one environment, on one dataset, yet it is read as a property of the tool. Merge-tool papers differ in all three.

| Work | Data | Success metric | Comparison |
| --- | --- | --- | --- |
| Spork (Larsén et al., 2023) | 890 merge scenarios (1,740 file merges) from open-source Java projects | Conflicts, run time, formatting preservation | JDime and AutoMergePTM run by the authors; IntelliMerge and Git Merge excluded |
| IntelliMerge (Shen et al., 2019) | Only merges with refactoring-related conflicts that Git Merge could not merge cleanly | Reduction in conflict blocks and conflicting lines | Git Merge, default configuration |
| GMerge (arXiv 2111.11904) | 379 semantic conflicts from the Edge browser, Aug 2020 to Apr 2021 | Developer's fix is a prefix of the model output | Heuristic and string-based baselines; tool not public |
| MergeBERT (Svyatkovskiy et al., 2022) | About 54,000 historical conflicts with recorded resolutions | Accuracy against the recorded resolution; user study with 25 developers on 122 conflicts | Structured, semi-structured, and neural tools; tool not public |
| Schesch et al. (2024) | 6,045 merges from 1,120 Java repositories, including non-main branches | Project tests plus cost factor k | Ten tools and configurations, including Git Merge variants |
| LastMerge (Duarte et al., 2025) | Replayed merge scenarios from a large dataset | Run time, behavioral divergence, merge accuracy | jDime, Spork, and their generic counterparts LastMerge and Mergiraf |

Rows other than Schesch et al. rest on excerpts of the papers and on Schesch et al.'s account of them. Each is to be verified against the full paper in the claim table (Section 10). Merge-Bench (2026) adds a further protocol: a test-free evaluation, because test-based evaluation can be gamed.

**Problems documented by Schesch et al.**

- **Correctness is not checked.** Many studies count every clean merge as correct, or compare with the resolution in the commit history, which rewards Git Merge even when its clean merge was wrong.
- **Merges are unrepresentative.** Studies use synthetic merges, main-branch merges only, or only the scenarios a tool was designed for.
- **The state of the art is missing.** Git Merge is compared only in its default configuration, and rival tools are omitted.

On a representative set, IntelliMerge produced about 50% incorrect merges where Git Merge produced 3%, far from its reported gains.

**Environment and era effects already visible in the record**

- JDime does not handle the full Java 8 syntax (Java 8 was released in 2014). Schesch et al. could not use it because of unfixed bugs.
- Schesch et al. suggest that Spork's lead over JDime may partly reflect programs that used fewer Java 8 features. Their own data included code up to Java 17.
- Schesch et al. spent over one person-month trying to fix Spork's bugs and did not fix them all.
- AutoMerge, DeepMerge, MergeBERT, and GMerge are not public, so later work can only quote reported numbers or rebuild them.
- Git's default merge strategy changed in 2023, when ort replaced recursive.

To our knowledge, no evaluation treats data era or execution environment as a factor. A full literature search is pending.

## 5. Formal framing

Every merge-tool result is a function of three things: the tool, the environment it runs in, and the data it runs on.

- **Tool T:** a merge approach at a specific implementation version.
- **Environment E:** language and runtime versions (for example the JDK), dependencies, the Git version, and for LLM-based tools the model, its settings, and the compute and cost budget.
- **Data D\_t:** merge scenarios (base, parent 1, parent 2, developer resolution) whose merge commits date to era t.
- **Measure m:** outcome split (unhandled, correct, incorrect), effort reduction ER\_k at k = 1, 2, 4, 8, run time, and model-call cost.

A published claim that tool A beats tool B compares m(A, E\_A, D\_A) with m(B, E\_B, D\_B). It is a claim about the tools only if the environments, the data, and the measure match.

Three kinds of drift break that match:

- **Data drift.** D changes, through language features and project practices.
- **Environment drift.** E changes, through language version, dependencies, model generation, hardware, or price.
- **Protocol drift.** The measure or oracle changes, for example text match, project tests, or test-free comparison.

This study fixes the protocol and varies the other two. The four measures below are defined for a fixed k: decay, environment sensitivity, rank stability, and idea gain.

```latex
d_{T,k}(t) = \mathrm{ER}_k(T, E, D_t) \quad (E \text{ fixed})

\Delta_{T,k}(t) = \mathrm{ER}_k(T, E_{\text{modern}}, D_t) - \mathrm{ER}_k(T, E_{\text{published}}, D_t)

\tau = \frac{P_{\text{agree}} - P_{\text{flip}}}{n(n-1)/2}

 G_k(t) = \mathrm{ER}_k(T_{\text{ported}}, E_{\text{modern}}, D_t) - \mathrm{ER}_k(\text{LLM}_{\text{plain}}, E_{\text{modern}}, D_t)
```

In the rank-stability formula, n is the number of tools, and P\_agree and P\_flip count the tool pairs whose order agrees or flips between two rankings (two eras, or two values of k). Idea gain G applies to LLM-based tools: the tool's idea ported to a modern LLM against the plain modern LLM. Porting effort is recorded in person-hours and changed lines.

Git Merge does not depend on a language version, so it is measured in every era as a reference for merge difficulty. If every tool dips in one era, the data changed; if one tool dips, the tool decayed.

## 6. Study design

The study reruns a small, fixed set of merge tools over merges from several eras, in each tool's published environment and in a modernized one.

**Research questions**

- **RQ1, decay.** How do the outcome split, cost, and run time of each tool change across merge eras when the environment is held fixed?
- **RQ2, environment.** How do they change when the environment is modernized (a newer language version or a newer LLM), how much effort does the change take, and does an LLM-based tool's idea still beat a plain LLM?
- **RQ3, rank stability.** Does the ranking of tools change across eras and across k?

**Tool arms**

| Slot | Purpose | Candidate | Availability |
| --- | --- | --- | --- |
| Control | Reference for merge difficulty; independent of language version | Git Merge (ort), Git version pinned | Public |
| Version-bound | Tests whether a tool works within its language version and breaks outside it | Spork (Java 17, per Alex); JDime (Java 8) as the deliberately old tool | Spork public; JDime public but buggy per Schesch et al. |
| Model-bound | Tests idea survival: original, ported, plain LLM | GMerge (paper text describes GPT-3, Alex's note says GPT-J: confirm) or MergeGen (CodeT5-small, per Alex), plus a plain modern LLM | GMerge not public; MergeGen to verify |
| Scope-limited | Tests a tool against its own claim and against representative merges | IntelliMerge | Public; rarely applicable per Schesch et al. |
| Resource-bound | Tests limits that bound at publication time (RAM, time, cost) | To be identified | To verify |

Availability comes from Schesch et al. (2024) and Merge-Bench (2026) and must be re-checked.

**Data.** Java merge scenarios from open-source repositories, binned by merge-commit date into at least three eras (placeholders: 2015 to 2016, 2019 to 2020, 2023 to 2024). Each era is a sample of main-branch and non-main-branch merges, drawn with the infrastructure and data of Schesch et al. if they can be reused. A merge is kept only if both parents pass their tests, so the project's tests serve as the oracle. Each test suite runs five times to absorb flaky tests. Attrition at every filter stage is recorded per era.

**Procedure**

1. Build the era datasets and record attrition.
2. Get each tool running in its published environment and write its resurrection log.
3. Run every tool over every era in that environment (RQ1).
4. Modernize each tool's environment or port its idea, and write the porting log.
5. Rerun every tool over every era in the modern environment (RQ2).
6. For LLM-based tools, run three arms: original, idea ported, plain modern LLM.
7. Compute decay curves, environment sensitivity, idea gain, and rank stability (RQ3) at k = 1, 2, 4, 8.

&#91;embedded content: data era by environment · 4 cells, 2 shaded\]

Each run of a tool over an era falls in one cell. The shaded cells change only the environment or only the data, so the effect of each can be read separately.

## 7. Outputs

The study produces six artifacts, none of which presupposes a result.

| Output | Answers | Form |
| --- | --- | --- |
| Decay curves | RQ1 | One line per tool: ER\_k against era, one panel per k; tool publication dates marked on the time axis; outcome split and run time alongside |
| Environment sensitivity and porting effort | RQ2 | Per tool and era: difference between the published and modern environment; hours, changed lines, and blockers per port |
| Idea-survival comparison | RQ2 | For the LLM-based tool: three arms per era (original, ported, plain modern LLM) |
| Rank stability | RQ3 | Rank lines for all tools across eras and across k; Kendall's τ per pair of eras |
| Attrition table | Validity | Scenarios retained after each filter, per era |
| Dataset, wrappers, logs | Reuse | Era datasets, tool wrappers, resurrection, porting, and run logs |

Each pattern in these outputs has a reading. A flat curve means a tool's result was stable over the eras tested. A steady decline, or a cliff at a language-version boundary, means the published number described a moment. A rank flip means a champion depended on its conditions, and a newer tool appearing where an older curve falls shows what the newer tool replaced.

**Contribution.** A protocol for reporting merge-tool results as (tool, environment, data era) triples, and a pilot dataset and logs that demonstrate it.

## 8. Threats to validity and pitfalls to track

Each item below can change a result and is tracked from the first run.

- **Oracle.** Passing tests do not prove a merge correct, so incorrect merges are undercounted.
- **Survivorship.** Old merges are kept only if both parents still build and pass tests, so an era may reflect which code still compiles. Attrition is reported per era.
- **Difficulty versus decay.** Later merges may be harder or easier. Git Merge in every era separates a change in the data from a change in a tool.
- **Cost factor.** The true value of k is unknown. Results are reported at k = 1, 2, 4, 8, never as a single ranking.
- **Merge source.** Non-main-branch merges are harder in absolute terms than main-branch merges. Both are sampled.
- **Flaky tests.** Each test suite runs five times.
- **LLM variability and retirement.** Model version, date, settings, and prompt are pinned and recorded, along with cost per call.
- **Training-data overlap.** Older merges may appear in a modern LLM's training data. This is noted for the LLM arms.
- **Patched tools.** Any patch to a tool is recorded, and results are labeled as published or patched.
- **Version pinning.** Git version, JDK version, tool commit, operating system, and hardware are recorded for every run.
- **Protocol consistency.** One oracle and one outcome taxonomy apply to every tool, unlike prior papers.
- **Generality.** The pilot covers Java only.

## 9. Logging protocol

The effort of running and porting a tool is data, so three logs are kept from the first attempt.

| Log | One entry per | Fields |
| --- | --- | --- |
| Resurrection | Attempt to run a tool in its published environment | Date; hours spent; what broke; exact error; fix applied; whether the tool's own code was patched; final status (runs, runs with patches, does not run) |
| Porting | Attempt to move a tool or its idea to a modern environment | Components of the idea kept and replaced; hours; files and lines changed; model, version, settings, and date; prompt; blockers |
| Run | Execution of a tool over a data slice | Tool commit; Git, JDK, operating system, hardware; era and sample; per-merge outcome, run time, and cost |

Breakage is classified as one of: language or JDK version, dependency, build system, retired model or API, missing artifact, or plain bug. Time-to-port is reported alongside performance, because how hard it is to move an idea to current technology is itself a result.

## 10. Scope and open decisions

The short paper is a four-page ICSE NIER submission due Oct 23, 2026, so the pilot stays small.

**Scope**

- Java only.
- Five to eight tool arms covering the slots in Section 6.
- At least three eras, with a sample per cell instead of full datasets.
- One LLM-based idea with a plain-LLM baseline.

**Open decisions**

- [ ] Outcome taxonomy: unhandled, correct, incorrect (Schesch et al.) or better, comparable, unresolved, worse (previous study).
- [ ] Tool shortlist, including which tool fills the resource-bound slot.
- [ ] Whether the previous study's harness and the infrastructure of Schesch et al. can be reused directly.
- [ ] Era boundaries and sample size per cell.
- [ ] Which model GMerge used (GPT-3 or GPT-J), and how the previous study handled tools that are not public.
- [ ] Which modern LLM and prompt budget the plain-LLM arm uses.

**Before the meeting with Alex on Oct 2, 2026**

- [ ] Tool spreadsheet: year, paradigm, environment binding, artifact link, availability, slot.
- [ ] Claim table for three or four papers: claim, metric, dataset and years, environment, baselines (re-run or copied), artifact status.
- [ ] One or two resurrection attempts, with logs.
- [ ] Draft shortlist and design matrix.

## References

1. Schesch, Featherman, Yang, Roberts, Ernst. [Evaluation of Version Control Merge Tools](https://arxiv.org/pdf/2410.09934). ASE 2024.
2. Larsén, Falleri, Baudry, Monperrus. [Spork: Structured Merge for Java with Formatting Preservation](https://arxiv.org/pdf/2202.05329). IEEE TSE 49(1), 2023.
3. Shen, Zhang, Zhao, Liang, Jin, Wang. IntelliMerge: A Refactoring-Aware Software Merging Technique. OOPSLA 2019. Cited through Schesch et al.
4. Leßenich, Apel, Lengauer. Balancing precision and performance in structured merge (JDime). Automated Software Engineering 22(3), 2014. Cited through Schesch et al.
5. Svyatkovskiy et al. [Program Merge Conflict Resolution via Neural Transformers](https://arxiv.org/pdf/2109.00084). ESEC/FSE 2022.
6. [Can Pre-trained Language Models be Used to Resolve Textual and Semantic Merge Conflicts?](https://arxiv.org/pdf/2111.11904) arXiv:2111.11904 (GMerge).
7. Duarte, Borba, Cavalcanti. [LastMerge: A language-agnostic structured tool for code integration](https://arxiv.org/pdf/2507.19687). 2025.
8. [Merge-Bench: Resolve Merge Conflicts with Large Language Models](https://arxiv.org/pdf/2605.25890). ICPR 2026.
