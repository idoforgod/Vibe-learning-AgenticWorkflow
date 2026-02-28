---
description: "Research Phase 산출물 검토 (Step 4)"
---

## Research Phase Review — Step 4 Human Checkpoint

워크플로우 Step 4: Research Phase(Step 1-3)의 산출물을 사용자에게 제시하고 검토를 받습니다.

### 검토 프로토콜:

**1단계 — SOT 상태 확인:**
`.claude/state.yaml`을 Read tool로 읽어 `current_step`이 4인지 확인하세요.
- `current_step < 4`: "아직 Research Phase가 완료되지 않았습니다. Step {current_step}을 먼저 완료하세요."
- `current_step > 4`: "Research Review는 이미 완료되었습니다. 현재 Step {current_step}입니다."
- `current_step == 4`: 검토 진행

**2단계 — 산출물 읽기 및 요약:**
SOT의 `outputs`에서 Step 1-3 산출물 경로를 확인하고, 각 파일을 Read tool로 읽으세요.

**산출물 1 — Requirements Manifest** (`research/requirements-manifest.md`):
- 내용 요약 제시
- 검토 포인트:
  - 17개 에이전트가 모두 식별되었는가?
  - 9개 커맨드가 모두 정의되었는가?
  - 7개 MCP 서버가 모두 매핑되었는가?
  - 15개 이상 데이터 스키마가 캡처되었는가?
- 통계 표시: `에이전트: N/17 | 커맨드: N/9 | MCP: N/7 | 스키마: N/15+`

**산출물 2 — Tech Feasibility Report** (`research/tech-feasibility-report.md`):
- 내용 요약 제시
- 검토 포인트:
  - MCP 서버별 fallback 계획이 수립되었는가?
  - 블로킹 제약 사항이 있는가?
  - Claude Code 기술 한계가 올바르게 식별되었는가?

**산출물 3 — Pedagogy Implementation Guide** (`research/pedagogy-implementation-guide.md`):
- 내용 요약 제시
- 검토 포인트:
  - 교육 프레임워크(Socratic Method, Bloom's Taxonomy 등)가 기술적으로 매핑되었는가?
  - 교육학적 엄밀성이 충분한가?
  - 적응형 학습 전략이 구체적인가?

**3단계 — 종합 통계 제시:**
```
## Research Phase 산출물 요약

| 항목 | 수량 | 상태 |
|------|------|------|
| 에이전트 | N/17 | ✅/⚠️ |
| 커맨드 | N/9 | ✅/⚠️ |
| MCP 서버 | N/7 | ✅/⚠️ |
| 데이터 스키마 | N/15+ | ✅/⚠️ |
| 기술 제약 | N개 식별 | ✅ |
| 교육 프레임워크 | N개 매핑 | ✅/⚠️ |
```

**4단계 — 사용자 결정 요청:**
AskUserQuestion tool로 사용자에게 결정을 요청하세요:

질문: "Research Phase 산출물을 승인하시겠습니까?"
선택지:
1. **승인 — Planning Phase 진행** (Recommended): 산출물 품질이 충분하여 Step 5로 진행
2. **수정 요청**: 특정 산출물에 대한 수정 사항을 지정하여 재작업
3. **전면 재작업**: Research Phase 전체를 처음부터 다시 수행

**5단계 — 결과 처리:**

| 사용자 선택 | 동작 |
|-----------|------|
| 승인 | SOT `current_step` → 5, `auto_approved_steps`에 step-4 추가, `autopilot-logs/step-4-decision.md` 생성 |
| 수정 요청 | 사용자 피드백을 반영하여 해당 산출물만 재생성 → 다시 검토 요청 |
| 전면 재작업 | SOT `current_step` → 1로 재설정, 이전 산출물 백업 후 재시작 |
