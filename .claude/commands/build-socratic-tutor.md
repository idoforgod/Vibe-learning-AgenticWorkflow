---
description: "Socratic AI Tutor 21단계 빌더 워크플로우 실행"
---

## Socratic AI Tutor — Builder Workflow Orchestrator

이 명령은 Socratic AI Tutor 시스템의 21단계 빌더 워크플로우를 실행합니다.
Research (1-4) → Planning (5-11) → Implementation (12-21) 3단계 구조를 Autopilot 모드로 자동 실행합니다.

### 실행 프로토콜:

**1단계 — SOT 상태 확인:**
`.claude/state.yaml`을 Read tool로 읽어 현재 워크플로우 상태를 파악하세요.

| `workflow_status` 값 | 동작 |
|---------------------|------|
| `pending` | Step 1부터 워크플로우 시작 |
| `in_progress` | `current_step` 값에서 워크플로우 재개 |
| `completed` | 사용자에게 완료 상태 보고 — "워크플로우가 이미 완료되었습니다. 재실행하려면 state.yaml을 초기화하세요." |

**2단계 — 사전 조건 확인:**
- PRD 읽기: `coding-resource/PRD.md` — 프로젝트 요구사항 정의서
- 설계 문서 읽기: `coding-resource/socratic-ai-tutor-workflow.md` — 워크플로우 설계 명세
- 두 파일이 모두 존재하는지 확인. 없으면 사용자에게 안내 후 중단.

**3단계 — Orchestrator Skill 실행:**
`.claude/skills/socratic-builder/SKILL.md`를 읽고, 해당 스킬의 지시에 따라 단계별 실행을 시작하세요.

스킬이 정의하는 21단계:

| 단계 | Phase | 설명 |
|------|-------|------|
| 1-3 | Research | 요구사항 분석, 기술 타당성, 교육학 프레임워크 |
| 4 | Research (human) | 리서치 산출물 검토 → `/review-research` |
| 5-10 | Planning | 아키텍처, 에이전트 페르소나, 스키마, 커맨드, 품질, 리뷰 |
| 11 | Planning (human) | 설계 산출물 승인 → `/approve-design` |
| 12-19 | Implementation | 코어 구현, 에이전트, MCP, 스키마, 커맨드, 통합, 테스트 |
| 20 | Implementation (human) | 최종 시스템 인수 → `/accept-system` |
| 21 | Implementation | 문서화 + 최종 마무리 |

**4단계 — Autopilot Execution Checklist 준수:**
각 단계마다 CLAUDE.md에 정의된 Autopilot Execution Checklist를 **반드시** 수행하세요:

- **단계 시작 전**: SOT `current_step` 확인, 이전 산출물 존재 확인, Verification 기준 읽기
- **단계 실행 중**: 모든 작업을 완전히 실행 (축약 금지 — 절대 기준 1)
- **단계 완료 후**: 4계층 품질 게이트 통과
  1. **L0 Anti-Skip Guard** — 산출물 파일 존재 + 최소 크기(100 bytes)
  2. **L1 Verification Gate** — Verification 기준 100% 달성 자기 검증
  3. **L1.5 pACS** — Pre-mortem + F/C/L 3차원 채점
  4. **L2 Review** — `@reviewer`/`@fact-checker` 교차 검증 (해당 단계만)
- **SOT 갱신**: `outputs`에 산출물 경로 기록, `current_step` +1

**5단계 — `(human)` 단계 처리:**
`(human)` 단계(Step 4, 11, 20)에 도달하면:
- Autopilot 모드: 산출물을 최대 품질 기본값으로 자동 승인 → Decision Log 기록
- 수동 모드: 사용자에게 해당 Slash Command(`/review-research`, `/approve-design`, `/accept-system`) 사용을 안내

**6단계 — 에러 처리:**
- 품질 게이트 FAIL 시: Abductive Diagnosis → 재시도 (예산 내)
- 재시도 예산 소진 시: 사용자 에스컬레이션
- Hook exit code 2 차단: 피드백 대로 수정 후 재시도

### NEVER DO:
- `current_step`을 2 이상 한 번에 증가 금지
- 산출물 없이 다음 단계 진행 금지
- "자동이니까 간략하게" 금지 — 절대 기준 1 위반
- Verification 기준 FAIL인 채로 다음 단계 진행 금지
