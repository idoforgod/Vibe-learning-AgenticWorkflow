---
description: "Planning Phase 설계 산출물 승인 (Step 11)"
---

## Planning Phase Approval — Step 11 Human Checkpoint

워크플로우 Step 11: Planning Phase(Step 5-10)의 설계 산출물을 사용자에게 제시하고 최종 승인을 받습니다.
승인 후 Implementation Phase로 진입합니다.

### 승인 프로토콜:

**1단계 — SOT 상태 확인:**
`.claude/state.yaml`을 Read tool로 읽어 `current_step`이 11인지 확인하세요.
- `current_step < 11`: "아직 Planning Phase가 완료되지 않았습니다. Step {current_step}을 먼저 완료하세요."
- `current_step > 11`: "Design Approval은 이미 완료되었습니다. 현재 Step {current_step}입니다."
- `current_step == 11`: 승인 진행

**2단계 — 6개 설계 산출물 읽기 및 요약:**
SOT의 `outputs`에서 Step 5-10 산출물 경로를 확인하고, 각 파일을 Read tool로 읽으세요.

**산출물 1 — Architecture Blueprint** (Step 5):
- 전체 시스템 아키텍처 다이어그램 제시
- 검토 포인트:
  - 컴포넌트 간 데이터 흐름이 명확한가?
  - SOT 구조가 절대 기준 2를 준수하는가?
  - 확장성과 유지보수성이 고려되었는가?

**산출물 2 — 17 Agent Personas** (Step 6):
- 각 에이전트의 역할·도구·제약 요약 테이블 제시
- 검토 포인트:
  - 17개 에이전트가 모두 정의되었는가?
  - 역할 중복이나 공백이 없는가?
  - 각 에이전트의 도구 접근 권한이 적절한가?

**산출물 3 — Data Schemas** (Step 7):
- 스키마 목록 및 관계 다이어그램 제시
- 검토 포인트:
  - 15개 이상 스키마가 정의되었는가?
  - 스키마 간 참조 무결성이 보장되는가?
  - 학습 진행 상태 추적에 충분한가?

**산출물 4 — Command Interface Design** (Step 8):
- 9개 커맨드 인터페이스 목록 제시
- 검토 포인트:
  - 모든 커맨드의 입력/출력이 명확한가?
  - 사용자 경험(UX) 흐름이 자연스러운가?
  - 에러 처리가 정의되었는가?

**산출물 5 — Quality Framework** (Step 9):
- 품질 보증 프레임워크 요약 제시
- 검토 포인트:
  - 테스트 전략이 포괄적인가?
  - 품질 게이트 기준이 명확한가?
  - 교육적 효과 측정 방법이 정의되었는가?

**산출물 6 — Reviewer Report** (Step 10):
- `@reviewer` 교차 검증 결과 요약 제시
- 검토 포인트:
  - 식별된 이슈가 모두 해결되었는가?
  - Critical 이슈가 남아있지 않은가?
  - pACS Delta 분석 결과가 적정한가?

**3단계 — 종합 설계 요약 제시:**
```
## Planning Phase 설계 요약

### 시스템 구성
- 에이전트: 17개 정의
- 커맨드: 9개 정의
- 데이터 스키마: N개 정의
- MCP 서버: 7개 통합 설계

### 품질 상태
| Step | 산출물 | pACS | Review |
|------|--------|------|--------|
| 5 | Architecture Blueprint | N | - |
| 6 | Agent Personas | N | - |
| 7 | Data Schemas | N | - |
| 8 | Command Interface | N | - |
| 9 | Quality Framework | N | - |
| 10 | Reviewer Report | N | PASS/FAIL |

### 주요 설계 결정
- [아키텍처에서 내린 핵심 결정 요약]
- [에이전트 설계에서 내린 핵심 결정 요약]
```

**4단계 — 사용자 결정 요청:**
AskUserQuestion tool로 사용자에게 결정을 요청하세요:

질문: "Planning Phase 설계를 승인하고 Implementation Phase로 진행하시겠습니까?"
선택지:
1. **승인 — Implementation Phase 진행** (Recommended): 설계 품질이 충분하여 Step 12로 진행
2. **부분 수정 요청**: 특정 산출물에 대한 수정 사항을 지정하여 해당 단계만 재작업
3. **전면 재설계**: Planning Phase 전체를 처음부터 다시 수행

**5단계 — 결과 처리:**

| 사용자 선택 | 동작 |
|-----------|------|
| 승인 | SOT `current_step` → 12, `auto_approved_steps`에 step-11 추가, `autopilot-logs/step-11-decision.md` 생성 |
| 부분 수정 | 사용자 피드백을 반영하여 해당 산출물만 재생성 → Step 10 Reviewer 재검증 → 다시 승인 요청 |
| 전면 재설계 | SOT `current_step` → 5로 재설정, 이전 산출물 백업 후 재시작 |
