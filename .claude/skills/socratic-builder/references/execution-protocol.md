# Execution Protocol — Socratic AI Tutor Builder (21 Steps)

Detailed step-by-step execution protocol. Each step's attributes are defined below.

---

## Master Step Table

| Step | Name | Phase | Agent Type | Agent | Model | Pre-processing | Post-processing | Review | Translation | Output Path | Trace Markers |
|------|------|-------|-----------|-------|-------|---------------|----------------|--------|-------------|-------------|---------------|
| 1 | PRD & Design Deep Analysis | Research | Sub-agent | @prd-analyst | opus | `split_prd_sections.py` | `validate_counts.py` | none | none | `research/requirements-manifest.md` | — |
| 2 | Tech Feasibility Assessment | Research | Sub-agent | @tech-scout | sonnet | — | — | none | none | `research/tech-feasibility-report.md` | [trace:step-1] |
| 3 | Educational Pedagogy Verification | Research | Sub-agent | @edu-analyst | opus | `extract_edu_theories.py` | `cross_ref_pedagogy.py` | @fact-checker | none | `research/pedagogy-verification-report.md` | [trace:step-1] |
| 4 | Research Findings Approval | Research | (human) | — | — | — | — | — | — | `autopilot-logs/step-4-decision.md` | — |
| 5 | System Architecture Blueprint | Planning | Sub-agent | @architect | opus | `merge_architecture_inputs.py` | — | @reviewer | @translator | `planning/architecture-blueprint.md` | [trace:step-1][trace:step-2][trace:step-3] |
| 6 | Agent Persona Design | Planning | (team) | 3-designer team | opus | — | — | @reviewer | @translator | `planning/agent-personas.md` | [trace:step-5] |
| 7 | Data Architecture & JSON Schema | Planning | Sub-agent | @schema-designer | opus | `extract_field_inventory.py` | `validate_schema_chain.py` | @reviewer | none | `planning/json-schemas.md` | [trace:step-1][trace:step-5] |
| 8 | Command Interface Design | Planning | Sub-agent | @interface-designer | sonnet | — | — | none | @translator | `planning/command-interfaces.md` | [trace:step-1][trace:step-5] |
| 9 | Quality Framework Design | Planning | Sub-agent | @qa-designer | sonnet | — | — | none | none | `planning/quality-framework.md` | [trace:step-1][trace:step-3] |
| 10 | Architecture & Design Review | Planning | Sub-agent | @reviewer | opus | — | — | (self) | none | `planning/design-review-report.md` | [trace:step-5]~[trace:step-9] |
| 11 | Complete Design Approval | Planning | (human) | — | — | — | — | — | — | `autopilot-logs/step-11-decision.md` | — |
| 12 | Project Scaffolding & SOT Init | Impl | Sub-agent | @builder | sonnet | — | — | none | none | Project scaffolding (multi-file) | [trace:step-5][trace:step-7] |
| 13 | Sub-Agent Implementation | Impl | (team) | 3-implementer team | opus | — | — | @reviewer | none | 17 agent files (`.claude/agents/`) | [trace:step-6][trace:step-7] |
| 14 | Phase 0 Pipeline Implementation | Impl | Sub-agent | @pipeline-builder | opus | `extract_phase0_spec.py` | — | @reviewer | none | Phase 0 pipeline code | [trace:step-5][trace:step-7][trace:step-8] |
| 15 | Phase 1-3 Skill Implementation | Impl | Sub-agent | @skill-builder | opus | `extract_phase13_spec.py` | — | @reviewer | none | Socratic Tutor Skill | [trace:step-5][trace:step-6][trace:step-7] |
| 16 | Slash Command Implementation | Impl | Sub-agent | @command-builder | sonnet | — | — | none | none | 9 command files | [trace:step-8] |
| 17 | Hook & State Management | Impl | Sub-agent | @infra-builder | sonnet | — | — | none | none | State management infra | [trace:step-5][trace:step-7] |
| 18 | Integration Testing | Impl | Sub-agent | @tester | opus | `generate_test_fixtures.py` | — | none | none | `testing/integration-test-report.md` | [trace:step-12]~[trace:step-17] |
| 19 | Final System Review | Impl | Sub-agent | @reviewer | opus | — | — | (self) | none | `review/final-system-review.md` | All prior steps |
| 20 | System Acceptance | Impl | (human) | — | — | — | — | — | — | `autopilot-logs/step-20-decision.md` | — |
| 21 | User Documentation | Impl | Sub-agent | @documenter | sonnet | — | — | @reviewer | @translator | `SOCRATIC-TUTOR-USER-MANUAL.md` | [trace:step-8][trace:step-14][trace:step-15] |

---

## Detailed Step Definitions

### Step 1: PRD & Design Document Deep Analysis

**Agent**: `@prd-analyst` (Sub-agent, model: opus)

**Pre-processing Script**: `temp/scripts/split_prd_sections.py`
- Input: `coding-resource/PRD.md` (full document)
- Action: Split PRD into logical sections (Problem Statement, Architecture, Agent Specs, User Stories, etc.)
- Output: `temp/prd-sections/` directory with individual section files
- Purpose: Reduce noise per analysis pass (Design Principle P1)

**Agent Task Prompt** (English-First):
```
You are a requirements analyst. Deep-analyze two documents:
1. PRD.md — requirements specification
2. socratic-ai-tutor-workflow.md — original design document

Extract a complete requirements manifest covering:
- All 17 agents: roles, triggers, inputs, outputs
- All 9 slash commands: args, actions, outputs
- All 7 MCP servers: purpose, integration points
- Phase 0-3 execution flow: data dependency graph
- JSON schema field inventory (pipeline order)
- Dual SOT schema: state.yaml + learner-state.yaml
- User-Resource Priority Policy (Case A/B)
- Quality metrics: 6 curriculum + 7 educational
```

**Verification Criteria**:
1. 17 agents fully documented (role, trigger, input, output) — zero omission
2. 9 slash commands fully defined (args, action, output)
3. 7 MCP servers documented (purpose, target agent)
4. Phase 0-3 data dependency graph included
5. JSON schema field inventory in pipeline order
6. Dual SOT schema defined

**Post-processing Script**: `temp/scripts/validate_counts.py`
- Validates: agent count ≥ 17, command count ≥ 9, MCP count ≥ 7
- Output: PASS/FAIL with counts

**Output**: `research/requirements-manifest.md`

---

### Step 2: Technology Feasibility Assessment

**Agent**: `@tech-scout` (Sub-agent, model: sonnet)

**Agent Task Prompt**:
```
You are a technology feasibility analyst. Assess the Claude Code environment
for building a Socratic AI Tutor system.

Evaluate:
1. MCP server availability for: web-search, deep-research, scholar-search,
   mooc-connector, adaptive-test, graph-renderer, analytics
2. Context Injection patterns: classify each agent's input size → Pattern A/B/C
3. File-based architecture constraints and workarounds
4. Model selection: opus vs sonnet per agent (cost/performance tradeoff)
5. Top 5 technical risks + mitigation strategies
6. Deep Research API accessibility
7. Session management in CLI environment (no persistent server)

Reference: Step 1 requirements manifest at research/requirements-manifest.md
```

**Verification Criteria**:
1. 7 MCP servers analyzed with availability/alternative assessment
2. Context Injection pattern mapping table (per agent)
3. File-based architecture constraints + workaround strategies
4. Model selection rationale table (agent × model)
5. Top 5 risks with mitigation strategies

**Output**: `research/tech-feasibility-report.md`

---

### Step 3: Educational Pedagogy Verification

**Agent**: `@edu-analyst` (Sub-agent, model: opus)

**Pre-processing Script**: `temp/scripts/extract_edu_theories.py`
- Input: `coding-resource/PRD.md`
- Action: Extract all educational theory references (Bloom, ZPD, Socratic method, spaced repetition, metacognition, transfer learning)
- Output: `temp/edu-theories.json`

**Agent Task Prompt**:
```
You are an educational psychology researcher. Verify the pedagogical claims
in the PRD against current academic consensus.

Verify each theory:
1. Bloom's 2-Sigma Problem (1984) — verify correction to d=0.79
2. Zone of Proximal Development (Vygotsky) — AI applicability
3. Socratic Method — 3-level questioning (confirm/explore/refute) evidence
4. Spaced Repetition — algorithm selection for AI tutoring
5. Metacognition Training — effectiveness in AI-mediated learning
6. Transfer Learning — same-field vs far-transfer challenge design

For each: academic source, current consensus, limitations, AI-specific risks.
Provide ≥ 3 design improvement recommendations.
```

**Post-processing Script**: `temp/scripts/cross_ref_pedagogy.py`
- Cross-reference educational theories against each other
- Verify no contradictory recommendations

**Verification Criteria**:
1. All 6 theories verified with academic sources
2. Bloom 2-Sigma correction (d=0.79) confirmed
3. Socratic 3-level academic basis confirmed
4. ≥ 3 AI-specific pedagogical risks identified
5. Design improvement recommendations included

**Review**: `@fact-checker` — verify academic source accuracy

**Output**: `research/pedagogy-verification-report.md`

---

### Step 4: (human) Research Findings Approval

**Slash Command**: `/review-research`

**Autopilot Behavior**: Auto-approve with quality-maximizing defaults. Decision log records:
- Summary of all 3 research outputs
- Approval rationale (Absolute Criterion 1)
- Any noted risks or concerns

**Output**: `autopilot-logs/step-4-decision.md`

---

### Step 5: System Architecture Blueprint

**Agent**: `@architect` (Sub-agent, model: opus)

**Pre-processing Script**: `temp/scripts/merge_architecture_inputs.py`
- Merge Step 1-3 outputs into single architecture input
- Extract: agent list, data flows, constraints, risks

**Verification Criteria**:
1. 17-agent call-graph Mermaid diagram
2. Dual SOT schema fully defined
3. File system directory tree (`data/socratic/` complete)
4. Phase 0 data pipeline flowchart (6 agents + parallel section)
5. Phase 1-3 Skill state machine diagram
6. Context Injection pattern mapping (per agent)
7. Agent data contracts (input→output mapping)

**Review**: `@reviewer`
**Translation**: `@translator`
**Output**: `planning/architecture-blueprint.md`

**Translation Protocol** (executed AFTER Review PASS):
1. Pre-condition: `review-logs/step-5-review.md` exists with verdict = PASS
2. Invoke `@translator` sub-agent:
   - Source: `planning/architecture-blueprint.md` (English original)
   - Glossary: `translations/glossary.yaml`
   - Output: `planning/architecture-blueprint.ko.md`
3. Trace marker rule: All `[trace:step-N]` markers preserved verbatim (never translated)
4. Translation pACS: Ft/Ct/Nt scored → `pacs-logs/step-5-translation-pacs.md`
5. P1 Validation: `python3 .claude/hooks/scripts/validate_translation.py --step 5 --project-dir . --check-pacs --check-sequence`
6. SOT: Record `outputs.step-5-ko: "planning/architecture-blueprint.ko.md"`

---

### Step 6: (team) Agent Persona Design

**Team**: `step-6-agent-design`

| Teammate | Assignment | Agent Count |
|----------|-----------|-------------|
| `@agent-designer-alpha` | Phase 0: @content-analyzer, @topic-scout, @web-searcher, @deep-researcher, @content-curator, @curriculum-architect | 6 |
| `@agent-designer-beta` | Phase 1-2: @orchestrator, @learner-profiler, @knowledge-researcher, @path-optimizer, @session-planner, @session-logger | 6 |
| `@agent-designer-gamma` | Phase 3: @socratic-tutor, @misconception-detector, @metacog-coach, @concept-mapper, @progress-tracker | 5 |

**Dense Checkpoints**:
- **CP-1**: Each agent's role definition + trigger conditions complete → cross-team review
- **CP-2**: System prompts + tool access designed → integration check
- **CP-3**: Cross-consistency validated → final sign-off

**Verification Criteria**:
1. All 17 agent persona definitions present
2. System prompt drafts for each agent
3. Tool access permission matrix (agent × tool)
4. Sub-agent call relationships documented
5. Cross-team consistency validated

**Review**: `@reviewer`
**Translation**: `@translator`
**Output**: `planning/agent-personas.md`

**Translation Protocol** (executed AFTER Review PASS):
1. Pre-condition: `review-logs/step-6-review.md` exists with verdict = PASS
2. Invoke `@translator` sub-agent:
   - Source: `planning/agent-personas.md` (English original — merged from 3 teammates)
   - Glossary: `translations/glossary.yaml`
   - Output: `planning/agent-personas.ko.md`
3. Trace marker rule: All `[trace:step-N]` markers preserved verbatim (never translated)
4. Translation pACS: Ft/Ct/Nt scored → `pacs-logs/step-6-translation-pacs.md`
5. P1 Validation: `python3 .claude/hooks/scripts/validate_translation.py --step 6 --project-dir . --check-pacs --check-sequence`
6. SOT: Record `outputs.step-6-ko: "planning/agent-personas.ko.md"`

---

### Step 7: Data Architecture & JSON Schema Design

**Agent**: `@schema-designer` (Sub-agent, model: opus)

**Pre-processing**: `temp/scripts/extract_field_inventory.py`

**Post-processing**: `temp/scripts/validate_schema_chain.py`
- Verify upstream→downstream field reference integrity

**Verification Criteria**:
1. Phase 0 schemas: user-resource-scan, topic-scope, web-search-results, deep-research-results, curated-content, auto-curriculum (all 6)
2. learner-state.yaml schema complete
3. Session log schema (session_info, current_position, conversation_context, recovery_checkpoint)
4. Schema chain integrity — all downstream references resolvable (source: Step 5)
5. Required/optional/default values specified

**Review**: `@reviewer`
**Output**: `planning/json-schemas.md`

---

### Step 8: Command Interface Design

**Agent**: `@interface-designer` (Sub-agent, model: sonnet)

**Verification Criteria**:
1. All 9 commands fully defined (/teach, /teach-from-file, /start-learning, /upload-content, /my-progress, /concept-map, /challenge, /end-session, /resume)
2. Argument types/defaults/required for each
3. Agent call sequence diagrams per command
4. Progress display format unified
5. Error message standard format
6. Cross-command interaction mapping

**Translation**: `@translator`
**Output**: `planning/command-interfaces.md`

**Translation Protocol** (executed after step completion — no Review gate for this step):
1. Pre-condition: Verification Gate PASS (no Review required for Step 8)
2. Invoke `@translator` sub-agent:
   - Source: `planning/command-interfaces.md` (English original)
   - Glossary: `translations/glossary.yaml`
   - Output: `planning/command-interfaces.ko.md`
3. Trace marker rule: All `[trace:step-N]` markers preserved verbatim (never translated)
4. Translation pACS: Ft/Ct/Nt scored → `pacs-logs/step-8-translation-pacs.md`
5. P1 Validation: `python3 .claude/hooks/scripts/validate_translation.py --step 8 --project-dir . --check-pacs`
6. SOT: Record `outputs.step-8-ko: "planning/command-interfaces.ko.md"`

---

### Step 9: Quality Framework Design

**Agent**: `@qa-designer` (Sub-agent, model: sonnet)

**Verification Criteria**:
1. 6 curriculum quality metrics defined with measurement methods
2. 7 educational effectiveness metrics defined with targets
3. Automated quality verification logic
4. Quality data collection/storage/reporting design

**Output**: `planning/quality-framework.md`

---

### Step 10: Architecture & Design Review

**Agent**: `@reviewer` (Sub-agent, model: opus)

**Input**: All Step 5-9 outputs

**Verification Criteria**:
1. Issue list per Planning deliverable (Steps 5-9)
2. Zero Critical issues
3. Agent data flow completeness confirmed
4. Dual SOT consistency verified
5. Explicit PASS/FAIL verdict

**Output**: `planning/design-review-report.md`

---

### Step 11: (human) Complete Design Approval

**Slash Command**: `/approve-design`

**Autopilot Behavior**: Auto-approve with quality-maximizing defaults.

**Output**: `autopilot-logs/step-11-decision.md`

---

### Step 12: Project Scaffolding & SOT Init

**Agent**: `@builder` (Sub-agent, model: sonnet)

**Verification Criteria**:
1. Directory structure matches Step 5 architecture
2. `state.yaml` initialized
3. `data/socratic/learner-state.yaml` template created
4. 17 agent scaffolding files exist under `.claude/agents/`
5. 9 command scaffolding files exist under `.claude/commands/`
6. JSON schema files exist under `data/socratic/schemas/`
7. Scaffolding files contain header + placeholder (not empty)

**Output**: Project scaffolding (multi-file)

---

### Step 13: (team) Sub-Agent Implementation

**Team**: `step-13-agent-impl`

| Teammate | Assignment | Agent Count |
|----------|-----------|-------------|
| `@implementer-alpha` | Phase 0 agents | 6 |
| `@implementer-beta` | Phase 1-2 agents + @session-logger | 6 |
| `@implementer-gamma` | Phase 3 agents | 5 |

**Dense Checkpoints**:
- **CP-1**: System prompts complete → cross-check consistency
- **CP-2**: Tool access + I/O schemas implemented → integration check
- **CP-3**: Cross-testing complete → final validation

**Verification Criteria**:
1. 17 `.claude/agents/*.md` files exist, each ≥ 100 bytes
2. System prompts match Step 6 personas
3. Tool access matches Step 5 architecture
4. JSON I/O matches Step 7 schemas
5. @socratic-tutor includes 3-level questioning (confirm/explore/refute)
6. @misconception-detector includes severity classification (minor/moderate/critical)
7. @session-logger includes 5-second snapshot + recovery checkpoint
8. Cross-step traceability: [trace:step-6] markers present

**Review**: `@reviewer`
**Output**: 17 agent files

---

### Step 14: Phase 0 Pipeline Implementation

**Agent**: `@pipeline-builder` (Sub-agent, model: opus)

**Pre-processing**: `temp/scripts/extract_phase0_spec.py`

**Verification Criteria**:
1. `/teach` triggers Phase 0 pipeline
2. User-Resource Priority Policy (Case A/B) implemented
3. @web-searcher + @deep-researcher parallel execution
4. 6 JSON outputs generated in order
5. Progress display ([1/7]~[7/7]) implemented
6. Error retry logic included
7. auto-curriculum.json matches Step 7 schema

**Review**: `@reviewer`
**Output**: Phase 0 pipeline code

---

### Step 15: Phase 1-3 Skill Implementation

**Agent**: `@skill-builder` (Sub-agent, model: opus)

**Pre-processing**: `temp/scripts/extract_phase13_spec.py`

**Verification Criteria**:
1. `.claude/skills/socratic-tutor/SKILL.md` complete
2. Phase 1 agent call flow implemented
3. Phase 2 agent call flow implemented
4. Phase 3 agent call flow (with sub-agents) implemented
5. learner-state.yaml management logic
6. Session start/end/resume state machine
7. /start-learning, /end-session, /resume integration

**Review**: `@reviewer`
**Output**: Socratic Tutor Skill

---

### Step 16: Slash Command Implementation

**Agent**: `@command-builder` (Sub-agent, model: sonnet)

**Verification Criteria**:
1. 9 `.claude/commands/*.md` files exist, each ≥ 100 bytes
2. Arguments match Step 8 interface design
3. Agent call sequences match Step 8
4. /teach → /start-learning auto-connection
5. /resume session recovery logic
6. Progress display format matches Step 8

**Output**: 9 command files

---

### Step 17: Hook & State Management

**Agent**: `@infra-builder` (Sub-agent, model: sonnet)

**Verification Criteria**:
1. @session-logger snapshot mechanism (5-second interval)
2. Session recovery manager (active/ → completed/, interrupted/ scan)
3. learner-state.yaml update logic (mastery, session history)
4. Spaced repetition algorithm (review scheduling)
5. Quality metrics collection/storage
6. Directory structure: `data/socratic/sessions/{active,completed,interrupted}/`

**Output**: State management infrastructure code

---

### Step 18: Integration Testing

**Agent**: `@tester` (Sub-agent, model: opus)

**Pre-processing**: `temp/scripts/generate_test_fixtures.py`

**Verification Criteria**:
1. Phase 0: /teach keyword → auto-curriculum.json generated
2. Phase 1-3: /start-learning → Socratic dialogue starts
3. JSON schema conformance: all outputs match Step 7
4. Session recovery: /resume resumes interrupted session
5. Dual SOT: state.yaml + learner-state.yaml consistency
6. User-Resource Priority: Case A/B branching works
7. Error recovery: agent failure → retry works

**Output**: `testing/integration-test-report.md`

---

### Step 19: Final System Review

**Agent**: `@reviewer` (Sub-agent, model: opus)

**Verification Criteria**:
1. Issue list for entire system
2. Zero Critical issues
3. End-to-end connection verified (17 agents → 9 commands → Phase 0 → Phase 1-3)
4. Dual SOT integrity confirmed
5. Explicit PASS/FAIL verdict

**Output**: `review/final-system-review.md`

---

### Step 20: (human) System Acceptance

**Slash Command**: `/accept-system`

**Autopilot Behavior**: Auto-approve with quality-maximizing defaults.

**Output**: `autopilot-logs/step-20-decision.md`

---

### Step 21: User Documentation

**Agent**: `@documenter` (Sub-agent, model: sonnet)

**Verification Criteria**:
1. 9 commands documented with examples
2. Installation/setup guide (including MCP servers)
3. Phase 0 pipeline usage guide (Case A/B)
4. Phase 1-3 learning session guide
5. FAQ ≥ 10 items
6. Troubleshooting ≥ 5 scenarios

**Review**: `@reviewer`
**Translation**: `@translator`
**Output**: `SOCRATIC-TUTOR-USER-MANUAL.md`

**Translation Protocol** (executed AFTER Review PASS):
1. Pre-condition: `review-logs/step-21-review.md` exists with verdict = PASS
2. Invoke `@translator` sub-agent:
   - Source: `SOCRATIC-TUTOR-USER-MANUAL.md` (English original)
   - Glossary: `translations/glossary.yaml`
   - Output: `SOCRATIC-TUTOR-USER-MANUAL.ko.md`
3. Trace marker rule: All `[trace:step-N]` markers preserved verbatim (never translated)
4. Translation pACS: Ft/Ct/Nt scored → `pacs-logs/step-21-translation-pacs.md`
5. P1 Validation: `python3 .claude/hooks/scripts/validate_translation.py --step 21 --project-dir . --check-pacs --check-sequence`
6. SOT: Record `outputs.step-21-ko: "SOCRATIC-TUTOR-USER-MANUAL.ko.md"`

---

## P1 Validation Scripts

Each validation script is invoked by the Orchestrator after the corresponding quality gate.

| Script | Gate | Invocation |
|--------|------|-----------|
| `validate_pacs.py` | pACS | `python3 .claude/hooks/scripts/validate_pacs.py --step N --check-l0 --project-dir .` |
| `validate_verification.py` | Verification | `python3 .claude/hooks/scripts/validate_verification.py --step N --project-dir .` |
| `validate_review.py` | Adversarial Review | `python3 .claude/hooks/scripts/validate_review.py --step N --project-dir . --check-pacs-arithmetic` |
| `validate_translation.py` | Translation | `python3 .claude/hooks/scripts/validate_translation.py --step N --project-dir . --check-pacs [--check-sequence if Review step]` |
| `validate_traceability.py` | Cross-Step Traceability | `python3 .claude/hooks/scripts/validate_traceability.py --step N --project-dir .` |
| `validate_retry_budget.py` | Retry Budget | `python3 .claude/hooks/scripts/validate_retry_budget.py --step N --gate {gate} --project-dir . --check-and-increment` |
| `diagnose_context.py` | Abductive Diagnosis | `python3 .claude/hooks/scripts/diagnose_context.py --step N --gate {gate} --project-dir .` |
| `validate_diagnosis.py` | Diagnosis Validation | `python3 .claude/hooks/scripts/validate_diagnosis.py --step N --gate {gate} --project-dir .` |
