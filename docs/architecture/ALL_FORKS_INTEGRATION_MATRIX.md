# Complete Fork Integration Matrix

This document accounts for every confirmed fork in the connected GitHub account inventory at the time of review. The target platform is not counted as a fork. Forks are not discarded merely because they are not coding agents: each receives a concrete product, engineering, evaluation, knowledge, or enablement role.

## Inventory and planned use

| # | Fork | Upstream | Required platform use | Integration class | Boundary / validation |
|---:|---|---|---|---|---|
| 1 | `dusssi/agent-desktop` | `vercel-labs/agent-desktop` | Optional computer-use and desktop automation capability for user-opted-in local workflows | Separate desktop capability | Device-side consent, visible actions, strict app/window scope; later milestone |
| 2 | `dusssi/aider` | `Aider-AI/aider` | Git-aware patch/edit engine, repo map, lint/test feedback | Coding engine adapter | Task worktree only; normalize edits and git operations through platform policy |
| 3 | `dusssi/awesome-prompts` | `ai-boost/awesome-prompts` | Curated prompt/context-engineering/evaluation patterns for platform agent profiles | Prompt and eval knowledge base | License/provenance, deduplicate, evaluate; prompts never grant permissions |
| 4 | `dusssi/claude-code-from-source-bucky` | `alejandrobalderas/claude-code-from-source` | Agent-loop, tool, context, subagent and permission architecture reference | Architecture research corpus | Extract concepts and tests; do not depend on undocumented/private internals |
| 5 | `dusssi/claw-code-bucky` | `ultraworkers/claw-code-parity` | Rust/Python harness experiments, runtime/session/permission parity patterns | Experimental runtime reference | Compare against platform contracts; promote only tested and licensed components |
| 6 | `dusssi/codex` | `openai/codex` | Coding engine adapter; session/turn events, approvals, sandbox and exec-server patterns | Coding engine adapter + reference | Pin commit/protocol, worker isolation, approval round-trip, no direct platform DB access |
| 7 | `dusssi/Complete-Data-Science-With-Machine-Learning-And-NLP-2024` | `krishnaik06/Complete-Data-Science-With-Machine-Learning-And-NLP-2024` | Internal learning/reference corpus for ML/NLP tasks, examples and evaluation exercises | Knowledge and enablement corpus | Check license, select relevant materials; not copied into production runtime |
| 8 | `dusssi/Complete-Python-Bootcamp` | `krishnaik06/Complete-Python-Bootcamp` | Python onboarding, worker SDK examples and contributor learning path | Developer enablement corpus | Curate only relevant material; license and attribution checks |
| 9 | `dusssi/ECC` | `affaan-m/ECC` | Agent harness skills, instincts, memory, security and research-first workflow patterns | Harness/skills subsystem reference | Translate into versioned skills and evals; sandbox tools; inspect every skill before enabling |
| 10 | `dusssi/gemini-cli` | `google-gemini/gemini-cli` | Coding engine adapter; tool registry, hooks, event and confirmation patterns | Coding engine adapter | Structured headless protocol, scoped tools, normalize confirmation and cancellation |
| 11 | `dusssi/opencode` | `anomalyco/opencode` | Primary broad coding-engine adapter candidate; provider/model routing, sessions and tool streaming | Coding engine adapter | Use supported CLI/server API; pin version; platform tool gateway owns side effects |
| 12 | `dusssi/openfilm` | `openfilm/openfilm` | Video-generation/editing workflow for demo/release artifacts and optional coding-agent-produced video assets | Media workflow adapter | Separate media worker, storage/rights checks, no access to source-code worker secrets |
| 13 | `dusssi/OpenHands` | `OpenHands/OpenHands` | Isolated software-engineering runtime and agent-server/workspace/event architecture | Worker/runtime integration | Separate deployment; tenant isolation, network egress policy, resource quotas and security review |
| 14 | `dusssi/pipeshub-ai` | `pipeshub-ai/pipeshub-ai` | Enterprise context/data connector layer for authorized docs, knowledge and retrieval grounding | Context and connector subsystem | Connector-level ACL propagation, source citations, tenant isolation, prompt-injection defense |
| 15 | `dusssi/public-apis` | `public-apis/public-apis` | Catalog seed for a governed integration directory (discover candidate public APIs) | Integration catalog data | Verify live API, license, terms, auth, privacy and security before listing/connecting; catalog is not an allowlist |
| 16 | `dusssi/system_prompts_leaks-bucky` | `asgeirtj/system_prompts_leaks` | Red-team/evaluation corpus to study prompt-injection resistance and compare instruction-following behavior | Security evaluation corpus | Treat all content as untrusted test data; no leaked prompt is used as a system prompt or trusted policy |
| 17 | `dusssi/Unstop-POTD` | `Jatin87660/Unstop-POTD` | Coding-challenge ingestion and regression benchmark candidates for problem-solving agents | Benchmark/evaluation corpus | Verify source rights, correctness, provenance and test cases; use only licensed/permitted problems |

## How all 17 contribute to the product

The product uses forks across the full lifecycle rather than pretending every repository is a code execution engine:

- **Build and edit:** OpenCode, Codex, Gemini CLI, Aider.
- **Runtime and desktop action:** OpenHands, agent-desktop, Claw Code experiments.
- **Agent harness, skills and orchestration:** ECC, Claude Code architecture research.
- **Context and integration discovery:** PipesHub AI, public-apis.
- **Prompt quality and safety evaluation:** Awesome Prompts, system-prompts-leaks.
- **Media artifacts:** OpenFilm.
- **Agent capability evaluation and learning:** Unstop-POTD, Python Bootcamp, Data Science/ML/NLP course corpus.

## Platform-owned architecture

Every production integration must be behind a BuckLabs-owned interface. Forks do not get direct authority over tenancy, identity, task state, approvals, secrets, or audit records.

Proposed internal subsystems:

1. `engine_adapters` — OpenCode, Codex, Gemini CLI, Aider.
2. `worker_runtimes` — isolated OpenHands runtime; future local/remote workers.
3. `desktop_capabilities` — explicit opt-in desktop sessions.
4. `agent_harness` — skill registry, context policy, memory and workflow profiles informed by ECC and architecture research.
5. `context_connectors` — PipesHub-inspired authorized connector and retrieval boundary.
6. `integration_catalog` — vetted API catalog seeded from public-apis.
7. `prompt_eval` — versioned prompt patterns, adversarial test cases and red-team suite.
8. `media_jobs` — isolated OpenFilm media generation/editing jobs.
9. `agent_benchmarks` — coding challenge and ML/NLP evaluation corpora.
10. `developer_enablement` — curated Python and ML/NLP learning paths and examples.

## Required audit record per fork

Before importing code or enabling a connector, record:

- Exact upstream and fork commit SHAs.
- License, notices, provenance and redistribution obligations.
- Repository structure and major execution/data-flow paths.
- Reusable modules, interfaces, dependencies and transitive risks.
- Security review: execution, filesystem, network, secrets, auth, tenant boundaries.
- Component-to-platform mapping and whether reuse is code, protocol, concept, dataset or workflow.
- Adaptation plan, tests, ownership and upgrade strategy.

## Non-negotiable rule

"Use all forks" means every fork must have a real, documented role in the product ecosystem and be assessed for usable assets. It does not mean blindly copying every file or shipping unrelated code in the API. A component is promoted into production only after license, architecture, security and test gates pass. Where code is unsuitable, its useful data, patterns, benchmarks or enablement material is still evaluated for governed use.
