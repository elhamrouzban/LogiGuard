# Risk Register

**Project:** LogiGuard AI — AI Logistics Exception Management & Operations Copilot  
**Purpose:** Track project risks that could affect correctness, delivery, demo reliability, or technical credibility.  
**Rule:** A risk is not a task. Mitigation actions should also appear in `BACKLOG.md` when implementation work is required.

---

## Risk Scoring

Use qualitative ratings:

- **Probability:** Low / Medium / High / Certain
- **Impact:** Low / Medium / High / Critical
- **Status:** Open / Monitoring / Mitigated / Closed

Do not lower a risk rating merely because a mitigation is planned. Change the status only when evidence shows that the risk has been reduced.

---

# Active Risks

| ID | Risk | Probability | Impact | Status | Current Mitigation / Control | Trigger / Evidence to Watch |
|---|---|---|---|---|---|---|
| RISK-001 | Target leakage from post-outcome fields | High if not controlled | Critical | Open | Define prediction timestamp; audit every feature; exclude post-outcome fields; add automated leakage tests | Unexpectedly high model score; use of fields unavailable at prediction time |
| RISK-002 | Same order/entity appears across train/test splits | Medium | High | Open | Identify grouping keys; inspect duplicate/repeated entities; prefer group-aware or chronological evaluation where justified | Shared order/entity IDs across split boundaries |
| RISK-003 | DataCo target semantics differ from assumptions | Medium | Critical | Open | Verify `Late_delivery_risk` using the official description file before modeling | Ambiguous or contradictory source description |
| RISK-004 | Leakage-safe model performance is materially lower than leakage-heavy results | Medium | Medium | Open | Compare against trivial baseline; prioritize valid evaluation over inflated performance; perform error analysis | Large score drop after leakage removal |
| RISK-005 | Historical DataCo domain does not represent a real Hamburg freight company's production distribution | High | Medium | Open | Frame model as a capstone trained on open historical supply-chain data; use Hamburg data only for contextual demo enrichment | Temptation to claim real Hamburg production validity |
| RISK-006 | Dataset age limits direct real-world generalization | Certain | Medium | Monitoring | Document limitation; avoid production-performance claims; focus on engineering methodology | Questions about current operational validity |
| RISK-007 | Hamburg traffic service is unavailable or changes | Medium | Low | Open | Keep traffic optional; fail gracefully; mock in CI; core `/predict` must work offline | API timeout, schema change, endpoint unavailable |
| RISK-008 | Hamburg traffic forecast demo service is unstable | Medium | Low | Open | Keep it P3/optional and out of the core path | Forecast endpoint unavailable during development/demo |
| RISK-009 | DWD weather enrichment consumes time without improving core project value | Medium | Low | Open | Keep weather optional; implement only after P1 core is on schedule | Week 3 P1 work incomplete |
| RISK-010 | HVCC access is commercial/uncertain | Medium/High | High | Mitigated | Explicitly exclude HVCC from MVP dependency | Any proposal to make HVCC required |
| RISK-011 | Paid LLM API becomes a hidden dependency | Medium | High | Open | Select a no-cost/local/free approach before agent implementation; keep provider replaceable; deterministic fallback | Credit requirement, paid key, free-tier instability |
| RISK-012 | Agent hallucinates risk values, traffic, weather, or causal explanations | Medium | High | Open | Read-only allow-list; structured outputs; tool-grounded evidence; deterministic validator | Output contains values absent from tool results |
| RISK-013 | Agent action space expands into unsafe or untestable behavior | Medium | High | Open | No write actions; no customer/carrier contact; no data mutation; no tool creation; no autonomous dispatch | New tool proposal outside allow-list |
| RISK-014 | Scope overload threatens the four-week deadline | High | Critical | Open | P0/P1 before P2/P3; explicit non-goals; no new major technology without ADR; Week 4 no new architecture | P1 work slipping while optional features are being built |
| RISK-015 | Solo execution capacity is insufficient for ML + MLOps + agent + UI | Medium/High | High | Open | Keep Streamlit minimal; optionalize weather/forecast/LLM reviewer; simplify presentation layer; seek collaborators if available | Week 2 exit criteria not met on time |
| RISK-016 | UI work consumes disproportionate time | Medium | Medium | Open | One Streamlit workflow only; no auth/multi-tenancy/admin; call API rather than duplicate logic | Significant time spent on visual polish before P1 backend completion |
| RISK-017 | CI becomes fragile because of live external API calls | Medium | Medium | Open | Mock external APIs in automated CI; use manual smoke tests separately | CI failures caused by network/service availability |
| RISK-018 | Monitoring is over-engineered relative to capstone requirements | Medium | Medium | Open | Monitor golden signals only; Evidently reference/current batch; one demonstrable alert | Multiple dashboards/alerts added before one end-to-end demo works |
| RISK-019 | Drift demo is presented as real production drift without evidence | Medium | High | Open | Clearly label simulated/production-like comparison batch; document construction method | Presentation language implying real production observations |
| RISK-020 | Data/model artifacts are handled inconsistently between Git, DVC, and MLflow | Medium | Medium | Open | Define ownership: Git for code/metadata, DVC for large data artifacts, MLflow for experiment/model lifecycle | Duplicate or conflicting artifact sources |
| RISK-021 | Prediction logic is duplicated in Streamlit and FastAPI | Medium | Medium | Open | Make FastAPI the application/model service boundary; Streamlit consumes the service | UI code loads/trains model independently |
| RISK-022 | Risk-level thresholds (Low/Medium/High) are chosen arbitrarily | Medium | Medium | Open | Treat probability as primary model output; define UI thresholds only after evaluation/business reasoning | Hard-coded thresholds introduced before model analysis |
| RISK-023 | Model/data quality gate is set arbitrarily | Medium | Medium | Open | Establish gate after leakage-safe baseline and documented metric behavior | Quality threshold chosen before baseline results |
| RISK-024 | Project documentation diverges from implementation | Medium | High | Open | Update `PROJECT_STATUS.md`, backlog, decision log, and relevant technical docs after meaningful changes | Code behavior contradicts blueprint/status |
| RISK-025 | Coding agent expands scope or introduces unfamiliar technology | Medium | High | Open | Require agent to read Blueprint, Status, Expectations, Backlog, Decision Log, Risk Register, and Handoff first; no undocumented architectural changes | New dependency/architecture appears without corresponding decision |
| RISK-026 | Secrets or credentials are committed to Git | Low/Medium | High | Open | Environment-based config; `.env` ignored; GitHub secrets for CI where needed; no hard-coded API keys | Credential appears in tracked files or logs |

---

# Risk Ownership Rules

Until specific team roles are assigned:

- **Project owner** owns scope, data validity, modeling validity, and final acceptance.
- **Coding agents** may implement mitigations but may not silently close a risk.
- A risk can be marked **Mitigated** only after the corresponding control exists and has been checked.
- A risk can be marked **Closed** only when it is no longer applicable to the project.

---

# Immediate Risk Priorities

Before application engineering begins, resolve or materially reduce these first:

1. `RISK-001` — target leakage.
2. `RISK-002` — split/entity leakage.
3. `RISK-003` — target semantics.
4. `RISK-014` — scope overload.
5. `RISK-025` — coding-agent scope expansion.

The first three are part of the pre-start data gate. The project should not proceed to product engineering if the ML problem cannot be defined in a leakage-safe and defensible way.

---

# Update Rule

Review this file:

- at the end of each project week;
- after discovering a major data/model limitation;
- before adding a major dependency;
- after a failed exit gate;
- before the final demo.

Do not duplicate implementation tasks here. Link the risk to backlog work when necessary.
