---
description: "최종 시스템 인수 검사 (Step 20)"
---

## Final System Acceptance — Step 20 Human Checkpoint

워크플로우 Step 20: Implementation Phase(Step 12-19)의 완성된 시스템을 사용자에게 제시하고 최종 인수를 받습니다.
인수 후 Step 21(문서화)을 수행하고 워크플로우를 완료합니다.

### 인수 프로토콜:

**1단계 — SOT 상태 확인:**
`.claude/state.yaml`을 Read tool로 읽어 `current_step`이 20인지 확인하세요.
- `current_step < 20`: "아직 Implementation Phase가 완료되지 않았습니다. Step {current_step}을 먼저 완료하세요."
- `current_step > 20`: "System Acceptance는 이미 완료되었습니다. 현재 Step {current_step}입니다."
- `current_step == 20`: 인수 검사 진행

**2단계 — 시스템 완성도 검사:**
SOT의 `outputs`에서 Step 12-19 산출물 경로를 모두 확인하고, 각 핵심 파일의 존재와 크기를 검증하세요.

**검사 항목 1 — 시스템 완성도:**
```
## 시스템 구성 요소 완성도

### 에이전트 (17개)
| # | 에이전트 | 파일 | 상태 |
|---|---------|------|------|
| 1 | [에이전트명] | [파일 경로] | ✅/❌ |
| ... | ... | ... | ... |
| 17 | [에이전트명] | [파일 경로] | ✅/❌ |

### 커맨드 (9개)
| # | 커맨드 | 파일 | 상태 |
|---|--------|------|------|
| 1 | [커맨드명] | [파일 경로] | ✅/❌ |
| ... | ... | ... | ... |
| 9 | [커맨드명] | [파일 경로] | ✅/❌ |

### 인프라
| 항목 | 상태 |
|------|------|
| MCP 서버 통합 | ✅/❌ (N/7) |
| 데이터 스키마 | ✅/❌ (N개) |
| Hook 시스템 | ✅/❌ |
| SOT 구조 | ✅/❌ |
| 설정 파일 | ✅/❌ |
```

**검사 항목 2 — 통합 테스트 결과:**
Step 18(Integration Testing) 산출물에서 테스트 시나리오 결과를 읽어 제시하세요.

```
## 통합 테스트 결과

| # | 테스트 시나리오 | 결과 | 비고 |
|---|---------------|------|------|
| 1 | [시나리오 설명] | PASS/FAIL | [비고] |
| 2 | [시나리오 설명] | PASS/FAIL | [비고] |
| 3 | [시나리오 설명] | PASS/FAIL | [비고] |
| 4 | [시나리오 설명] | PASS/FAIL | [비고] |
| 5 | [시나리오 설명] | PASS/FAIL | [비고] |

통과율: N/5 (N%)
```

**검사 항목 3 — Reviewer 보고서:**
Step 19(Final Review) 산출물에서 `@reviewer` 최종 검증 결과를 읽어 제시하세요.

```
## Reviewer 최종 보고서

- Verdict: PASS/FAIL
- Critical 이슈: N개 (모두 해결됨/N개 미해결)
- Warning: N개
- Suggestion: N개
- pACS 최종 점수: N
```

**3단계 — 체험 명령 안내:**
시스템을 직접 체험해볼 수 있는 명령을 안내하세요:

```
## 시스템 체험

다음 명령으로 Socratic AI Tutor를 직접 체험할 수 있습니다:

### Phase 0 — 주제 탐색
/teach [키워드]
예: /teach "recursion", /teach "machine learning"

### Phase 1-3 — 학습 세션
/start-learning
(Phase 0에서 생성된 학습 계획을 기반으로 Socratic 대화 시작)
```

**4단계 — 사용자 결정 요청:**
AskUserQuestion tool로 사용자에게 결정을 요청하세요:

질문: "Socratic AI Tutor 시스템을 인수하시겠습니까?"
선택지:
1. **인수 승인** (Recommended): 시스템 품질이 충분하여 Step 21(문서화)로 진행 후 완료
2. **수정 요청**: 특정 이슈에 대한 수정 사항을 지정하여 해당 부분만 재작업
3. **추가 테스트 요청**: 특정 시나리오에 대한 추가 통합 테스트 수행

**5단계 — 결과 처리:**

| 사용자 선택 | 동작 |
|-----------|------|
| 인수 승인 | SOT `current_step` → 21, `auto_approved_steps`에 step-20 추가, `autopilot-logs/step-20-decision.md` 생성. Step 21 실행 후 `workflow_status` → `completed` |
| 수정 요청 | 사용자 피드백을 반영하여 해당 부분 수정 → Step 19 Reviewer 재검증 → 다시 인수 요청 |
| 추가 테스트 | 지정된 시나리오 테스트 수행 → 결과 보고 → 다시 인수 요청 |
