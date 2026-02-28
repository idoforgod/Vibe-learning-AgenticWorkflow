# Fallback Matrix — Socratic AI Tutor Builder

Comprehensive failure recovery strategy for the 21-step builder workflow. Each failure type has 3 tiers of escalation.

---

## Failure Type Reference Table

| # | Failure Type | Tier 1 (First Try) | Tier 2 (Second Try) | Tier 3 (Escalation) |
|---|---|---|---|---|
| F1 | Sub-agent timeout/error | Retry with error context + feedback | Retry with model upgrade (sonnet→opus) | User escalation with diagnostic |
| F2 | Teammate failure | SendMessage with specific feedback | Replace teammate (new spawn, higher model) | Dissolve team, user escalation |
| F3 | Verification FAIL | Abductive Diagnosis → targeted retry | Alternative approach (different methodology) | User escalation (retry budget exhausted) |
| F4 | pACS RED (< 50) | Pre-mortem weak dimension → targeted fix | Full rework with different approach | User escalation |
| F5 | Review FAIL | Address specific issues from review report | Rework + re-review cycle | User escalation |
| F6 | Context overflow | Context Preservation auto-restore | Split step into sub-steps | Manual context restoration |
| F7 | Pre-processing failure | Re-run with relaxed parsing | Skip preprocessing (agent reads raw input) | User escalation |
| F8 | Post-processing failure | Re-run with relaxed validation | Skip postprocessing (manual verification) | User escalation |
| F9 | SOT corruption | Restore from last known good state | Re-initialize SOT from last completed step | User escalation |
| F10 | Team coordination failure | Re-send task with clarified instructions | Reduce team size (sequential fallback) | User escalation |
| F11 | Translation failure | Retry with glossary context + specific feedback | Model upgrade (sonnet→opus) | User escalation (accept/skip/manual) |

---

## Detailed Recovery Procedures

### F1: Sub-agent Timeout/Error

**Symptoms**: Task tool returns error, agent fails to produce output, output is malformed.

**Tier 1 — Retry with error context + feedback**
```
1. Capture error message from failed Task invocation
2. Analyze error type:
   - Timeout → increase timeout, simplify prompt
   - Malformed output → add explicit format instructions
   - Tool error → check tool availability, provide alternative
3. Re-invoke Task with:
   - Error context appended to prompt: "Previous attempt failed: {error}"
   - Refined instructions addressing the specific failure
4. Validate output meets Verification criteria
```

**Tier 2 — Retry with model upgrade**
```
1. If Tier 1 failed with sonnet model → upgrade to opus
2. Re-invoke Task with opus model
3. Include all Tier 1 error context
4. If already using opus → increase prompt specificity:
   - Break complex task into smaller sub-tasks
   - Provide more explicit examples
   - Add chain-of-thought instructions
```

**Tier 3 — User escalation with diagnostic**
```
1. Compile diagnostic report:
   - Failure type and error messages
   - Number of retry attempts
   - Tier 1 and Tier 2 outcomes
   - Suspected root cause
2. Present to user with options:
   a. Manual fix + resume from current step
   b. Skip step (if non-critical) with documented gap
   c. Abort workflow
3. Log decision in autopilot-logs/step-N-escalation.md
```

---

### F2: Teammate Failure (Steps 6, 13)

**Symptoms**: Teammate produces incomplete output, fails quality gates, becomes unresponsive.

**Tier 1 — SendMessage with specific feedback**
```
1. Identify specific failure:
   - Missing sections in output
   - Quality gate failures (which criteria)
   - Inconsistency with other teammates' outputs
2. SendMessage to failed teammate:
   content: |
     Your output for {task} needs revision:
     - Issue 1: {specific problem}
     - Issue 2: {specific problem}
     Required: Re-execute with fixes. Verify against criteria before reporting.
3. Wait for revised output
4. Re-run quality gates
```

**Tier 2 — Replace teammate**
```
1. TaskUpdate → mark failed task as pending (remove owner)
2. If teammate is responsive → SendMessage shutdown_request
3. Spawn new teammate:
   - Same task description + previous error context
   - Model upgrade if applicable
   - Include failed output as "what NOT to do" reference
4. TaskUpdate → assign to new teammate
5. Monitor new teammate through checkpoints
```

**Tier 3 — Dissolve team + user escalation**
```
1. Collect all completed teammate outputs
2. SendMessage shutdown_request to all remaining teammates
3. TeamDelete
4. SOT update: active_team → null
5. Present to user:
   - Completed portions: {list}
   - Failed portions: {list}
   - Options: manual completion, re-run as sequential sub-agents, abort
6. If user chooses sequential: convert remaining team tasks to sub-agent calls
```

---

### F3: Verification FAIL

**Symptoms**: L1 Verification Gate finds criteria not met after agent execution.

**Tier 1 — Abductive Diagnosis → targeted retry**
```
1. Run Abductive Diagnosis:
   python3 .claude/hooks/scripts/diagnose_context.py \
     --step N --gate verification --project-dir .

2. Check Fast-Path:
   - FP1 (missing file): regenerate specific missing file
   - FP2 (size < 100B): re-execute with "ensure comprehensive output"
   - FP3 (same failure 3x): → Tier 3 escalation

3. If no fast-path, run LLM diagnosis:
   - Read diagnosis evidence bundle
   - Identify which Verification criteria failed
   - Determine root cause (insufficient data, wrong approach, misunderstanding)

4. Generate diagnosis log:
   diagnosis-logs/step-N-verification-{timestamp}.md

5. Validate diagnosis:
   python3 .claude/hooks/scripts/validate_diagnosis.py \
     --step N --gate verification --project-dir .

6. Re-execute step with diagnosis-guided corrections:
   - Focus agent on failed criteria only
   - Provide failed output as context ("improve THIS section")
   - Add specific instructions for each failed criterion

7. Re-run Verification Gate
```

**Tier 2 — Alternative approach**
```
1. If Tier 1 failed 3+ times → change methodology:
   - Different prompt structure
   - Different data breakdown (Pattern A→B, B→C)
   - Split into sub-tasks if monolithic
   - Add explicit chain-of-thought for complex criteria
2. Re-execute with alternative approach
3. Re-run full quality gate chain (L0 → L1 → L1.5)
```

**Tier 3 — User escalation (retry budget exhausted)**
```
1. validate_retry_budget.py returns can_retry: false
2. Compile escalation report:
   - Which criteria failed persistently
   - All diagnosis logs from attempts
   - Suspected fundamental issue
3. Present options:
   a. User provides manual fix
   b. Relax specific criteria (with documented rationale)
   c. Abort workflow
```

---

### F4: pACS RED (< 50)

**Symptoms**: Pre-mortem Protocol reveals critical weakness, any F/C/L dimension < 50.

**Tier 1 — Weak dimension targeted fix**
```
1. Identify weak dimension from pACS log:
   - F (Faithfulness) < 50: output doesn't follow requirements
   - C (Completeness) < 50: output is missing critical sections
   - L (Lucidity) < 50: output is unclear or poorly structured

2. Targeted fix based on dimension:
   F-fix: Re-read requirements, re-execute with explicit requirement checklist
   C-fix: Identify missing sections, generate only missing parts
   L-fix: Restructure output with clearer headings, examples, diagrams

3. Re-run pACS scoring
4. If still RED → Tier 2
```

**Tier 2 — Full rework with different approach**
```
1. Discard current output
2. Re-analyze step requirements from scratch
3. Choose different approach:
   - Different output structure
   - Different decomposition of the task
   - Different model (if not already opus)
4. Full re-execution
5. Full quality gate chain (L0 → L1 → L1.5)
```

**Tier 3 — User escalation**
```
1. If retry budget exhausted
2. Present pACS history showing persistent weakness
3. User options:
   a. Accept with documented weakness (YELLOW override)
   b. Manual intervention
   c. Abort
```

---

### F5: Review FAIL

**Symptoms**: @reviewer or @fact-checker returns FAIL verdict with issue list.

**Tier 1 — Address specific issues**
```
1. Parse review report for issues:
   - Critical issues: must fix
   - Warnings: should fix
   - Suggestions: optional

2. For each Critical issue:
   - Identify affected section in output
   - Determine fix (re-generate section, correct data, restructure)
   - Apply fix

3. Re-run review
4. IMPORTANT: Do NOT proceed to Translation until Review PASS
```

**Tier 2 — Rework + re-review cycle**
```
1. If Tier 1 didn't resolve all Critical issues:
   - Re-execute the entire step with review feedback as input
   - Prompt: "Previous review found: {issues}. Avoid these issues."
2. Run full quality gate chain
3. Request re-review with:
   - Previous review report attached
   - Changelog of fixes applied
```

**Tier 3 — User escalation**
```
1. If review cycle repeats 3+ times (retry budget)
2. Present:
   - Persistent review issues
   - All review reports
   - Root cause analysis
3. User options:
   a. Accept with documented issues
   b. Manual fix
   c. Abort
```

---

### F6: Context Overflow

**Symptoms**: Claude Code compresses context, conversation becomes long, agent loses track of workflow state.

**Tier 1 — Context Preservation auto-restore**
```
1. Context Preservation System automatically:
   - PreCompact hook saves snapshot
   - SessionStart hook restores context
   - SOT state.yaml provides ground truth for current_step

2. After auto-restore:
   - Read state.yaml to determine current position
   - Read latest snapshot for work context
   - Continue from current_step
```

**Tier 2 — Split step into sub-steps**
```
1. If a single step exceeds context capacity:
   - Break step into 2-3 sub-steps
   - Each sub-step produces intermediate output
   - Chain sub-steps through files (not context)

2. Example: Step 13 (17 agents) → sub-steps:
   - 13a: Phase 0 agents (6)
   - 13b: Phase 1-2 agents (6)
   - 13c: Phase 3 agents (5)

3. SOT tracks sub-step progress via active_team
```

**Tier 3 — Manual context restoration**
```
1. User intervention:
   - Review .claude/context-snapshots/latest.md
   - Manually confirm current state
   - Provide context summary for next agent
2. Resume from confirmed state
```

---

### F7: Pre-processing Script Failure

**Symptoms**: Python pre-processing script fails (syntax error, missing input, parsing failure).

**Tier 1 — Re-run with relaxed parsing**
```
1. Identify failure cause:
   - Missing input file → verify previous step output exists
   - Parsing error → fix script or adjust input format
   - Python error → debug and fix script

2. Re-run with relaxed mode (if available):
   - Skip non-critical parsing sections
   - Use broader regex patterns
   - Accept partial results
```

**Tier 2 — Skip preprocessing**
```
1. Agent reads raw input instead of pre-processed input
2. Adjust agent prompt to handle noise:
   "Input has not been pre-processed. Extract relevant information
    from the full document. Focus on: {specific sections}"
3. Accept slightly lower precision (Design Principle P1 degradation)
4. Log skip in Decision Log with rationale
```

**Tier 3 — User escalation**
```
1. If raw input is too large/noisy for agent to handle
2. Present:
   - Pre-processing failure details
   - Input characteristics (size, format)
   - Options: fix script, provide pre-processed input, skip step
```

---

### F8: Post-processing Script Failure

**Symptoms**: Python post-processing/validation script fails after agent output.

**Tier 1 — Re-run with relaxed validation**
```
1. Identify failure:
   - Schema validation failure → check output format, re-run agent
   - Count mismatch → verify if output is correct but format differs
   - Script error → fix script

2. Re-run with relaxed thresholds if available
```

**Tier 2 — Skip post-processing**
```
1. Skip automated validation
2. Perform manual verification:
   - Read output file
   - Check key criteria manually
   - Log manual verification in Decision Log
3. Proceed to L1 Verification Gate (which covers similar checks)
```

**Tier 3 — User escalation**
```
1. Present validation failure details
2. User reviews output and decides: accept, fix, re-execute
```

---

### F9: SOT Corruption

**Symptoms**: `state.yaml` has invalid content, missing fields, or inconsistent state.

**Tier 1 — Restore from last known good state**
```
1. Check .claude/context-snapshots/latest.md for last known SOT state
2. Reconstruct state.yaml from:
   - Snapshot SOT section
   - Existing output files (verify which steps completed)
   - Git history (if available)
3. Validate reconstructed SOT:
   python3 .claude/hooks/scripts/validate_pacs.py --check-sot --project-dir .
```

**Tier 2 — Re-initialize from last completed step**
```
1. Scan output directories to determine last completed step:
   - Check research/ → Steps 1-3
   - Check planning/ → Steps 5-10
   - Check .claude/agents/ → Step 13
   - etc.
2. Re-initialize state.yaml:
   current_step: {last_completed + 1}
   outputs: {rebuild from existing files}
   workflow_status: "in_progress"
3. Resume from determined step
```

**Tier 3 — User escalation**
```
1. Present:
   - What was lost
   - What can be recovered
   - Options: manual SOT edit, restart from specific step, full restart
```

---

### F10: Team Coordination Failure (Steps 6, 13)

**Symptoms**: Teammates produce inconsistent outputs, deadlock, or fail to communicate.

**Tier 1 — Re-send with clarified instructions**
```
1. Identify inconsistency:
   - Cross-reference teammate outputs
   - Find conflicting definitions, formats, or assumptions
2. SendMessage to all teammates:
   content: |
     Cross-consistency issue found:
     {specific inconsistency}
     Reference standard: {authoritative source}
     Please align your output to this standard.
3. Wait for revised outputs
4. Re-run cross-consistency check
```

**Tier 2 — Reduce to sequential execution**
```
1. If team coordination is fundamentally broken:
   - Dissolve team (TeamDelete)
   - Convert to sequential sub-agent calls:
     a. First sub-agent produces output
     b. Second sub-agent receives first's output as context
     c. Third sub-agent receives both as context
   - Sequential ensures consistency through shared context
2. Trade-off: slower but more consistent
```

**Tier 3 — User escalation**
```
1. If sequential also fails
2. Present completed portions + gaps
3. User decides: manual completion, alternative approach, abort
```

---

## Escalation Decision Tree

```
Quality Gate FAIL
       │
       ▼
  Check Retry Budget
  (validate_retry_budget.py)
       │
  ┌────┴────┐
  │         │
can_retry  cannot_retry
  │         │
  ▼         ▼
Tier 1    Tier 3
(Diagnosis  (User
+ retry)   escalation)
  │
  ├─ Success → Continue
  │
  └─ Fail → Tier 2
            │
            ├─ Success → Continue
            │
            └─ Fail → re-check budget
                       │
                  ┌────┴────┐
                  │         │
                can_retry  cannot_retry
                  │         │
                  ▼         ▼
                Tier 1    Tier 3
                (different (User
                approach)  escalation)
```

---

## Budget Limits Summary

| Gate | Default Max Retries | ULW Max Retries | Counter File |
|------|-------------------|-----------------|--------------|
| Verification | 10 | 15 | `verification-logs/.step-N-retry-count` |
| pACS | 10 | 15 | `pacs-logs/.step-N-retry-count` |
| Review | 10 | 15 | `review-logs/.step-N-retry-count` |

**Budget Check Command**:
```bash
python3 .claude/hooks/scripts/validate_retry_budget.py \
  --step N --gate {verification|pacs|review} \
  --project-dir . --check-and-increment
```

Returns: `{ "can_retry": true/false, "retries_used": N, "max_retries": M }`

---

## F11: Translation Failure

**Applicable Steps**: 5, 6, 8, 21 (steps with `Translation: @translator`)

**Symptoms**: @translator output missing or empty, Translation pACS RED (Ft/Ct/Nt < 50), `validate_translation.py` FAIL (T1-T9), glossary inconsistency, trace marker corruption.

### Tier 1 — Retry with glossary context + specific feedback

```
1. Capture failure details from validate_translation.py output:
   - T1/T2 (file missing/too small): translator did not write output
   - T4 (wrong extension): output path incorrect
   - T5 (empty): translator produced blank output
   - T6 (heading mismatch): partial translation — sections omitted
   - T7 (code block mismatch): code blocks were incorrectly translated
   - T8 (glossary stale): glossary not updated after translation
   - Translation pACS RED: meaning distortion or omissions

2. Re-invoke @translator sub-agent with specific feedback:
   - Append failure context: "Previous translation failed validation: {T-code}: {description}"
   - For T6/T7: "Ensure EVERY section is translated. Compare heading count."
   - For pACS RED: "Focus on {weak dimension}: {specific passages flagged}"
   - For T8: "You MUST update translations/glossary.yaml with new terms"

3. Re-run validate_translation.py to confirm fix:
   python3 .claude/hooks/scripts/validate_translation.py \
     --step N --project-dir . --check-pacs [--check-sequence if Review step]
```

### Tier 2 — Model upgrade (sonnet → opus)

```
1. If Tier 1 failed with sonnet model:
   - Re-invoke @translator with model: opus
   - Include all Tier 1 failure context
   - Add explicit quality anchors:
     "The English original has {N} headings, {M} code blocks.
      Your translation MUST have the same structure."

2. If already using opus:
   - Break translation into sections (chunked approach)
   - Translate each major section independently
   - Merge sections into final .ko.md
   - Re-validate merged output
```

### Tier 3 — User escalation

```
1. Compile translation diagnostic:
   - validate_translation.py results (T1-T9)
   - Translation pACS scores (Ft/Ct/Nt) from both attempts
   - Specific sections with persistent issues
   - Glossary state (new terms found vs. registered)

2. Save diagnostic: diagnosis-logs/step-N-translation-diagnosis.md

3. Present options to user:
   a) Accept translation with documented quality gaps
   b) Skip translation for this step (proceed without .ko.md)
   c) Manual translation (user provides .ko.md)

4. Record decision in autopilot-logs/step-N-translation-decision.md
```

### Trace Marker Preservation

If translation passes T1-T9 but trace markers `[trace:step-N]` are corrupted:
1. Post-process: regex scan for `\[trace:step-\d+\]` in .ko.md vs original
2. If markers missing or modified: patch .ko.md by reinserting original markers
3. This is NOT a translation failure — it's a post-processing fix
