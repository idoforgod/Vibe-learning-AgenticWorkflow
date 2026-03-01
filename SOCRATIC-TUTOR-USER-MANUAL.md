# Socratic AI Tutor 사용자 매뉴얼

> **이 문서의 범위**: 이 매뉴얼은 **Socratic AI Tutor 시스템**을 사용하는 방법을 안내합니다.
> 부모 프레임워크(AgenticWorkflow) 자체의 사용법은 [`AGENTICWORKFLOW-USER-MANUAL.md`](AGENTICWORKFLOW-USER-MANUAL.md)를 참조하세요.

| 문서 | 대상 |
|------|------|
| **이 문서 (`SOCRATIC-TUTOR-USER-MANUAL.md`)** | Socratic AI Tutor 시스템의 사용법 — 학습자/교수자를 위한 안내 |
| **[`SOCRATIC-TUTOR-README.md`](SOCRATIC-TUTOR-README.md)** | 프로젝트 첫 소개 — 개요, 빠른 시작, 구조 |
| **[`SOCRATIC-TUTOR-ARCHITECTURE.md`](SOCRATIC-TUTOR-ARCHITECTURE.md)** | 설계 철학, 아키텍처, 에이전트 구조 — "왜 이렇게 설계했는가" |

---

## 1. 시작하기

### 1.1 사전 준비

| 항목 | 필수 여부 | 설명 |
|------|----------|------|
| [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) | 필수 | `npm install -g @anthropic-ai/claude-code` |
| Python 3.10+ | 필수 | Hook 스크립트 실행 (PyYAML 권장) |
| Git | 권장 | 저장소 clone |

### 1.2 설치 및 실행

```bash
# 저장소 클론
git clone https://github.com/idoforgod/Vibe-learning-AgenticWorkflow.git
cd Vibe-learning-AgenticWorkflow

# Claude Code 실행
claude
```

Claude Code가 실행되면 모든 설정(에이전트, 명령, Hook)이 자동으로 적용됩니다.

### 1.3 인프라 검증 (선택)

```
/install
```

Python 버전, Hook 스크립트 구문, 디렉터리 구조, SOT 쓰기 패턴 등 시스템 인프라의 건강 상태를 검증합니다.

---

## 2. 전체 학습 흐름

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  Step 1:  /teach blockchain consensus                    │
│           (키워드로 커리큘럼 자동 생성 — 완전 자동)         │
│                          │                               │
│                          ▼                               │
│  Step 2:  /start-learning                                │
│           (학습 세션 시작)                                 │
│                          │                               │
│                          ▼                               │
│  Step 3:  소크라테스 대화 (25-45분)                        │
│           ← 질문에 답하고, 유도 질문을 받으며 학습           │
│                          │                               │
│                          ▼                               │
│  Step 4:  /end-session 또는 "그만"                        │
│           (세션 종료 + 요약)                               │
│                          │                               │
│                          ▼                               │
│  Step 5:  다음 세션에서 /start-learning                   │
│           (이전 진행 상황 기반으로 이어서 학습)              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 3. 커리큘럼 생성 (Phase 0)

### 3.1 `/teach [키워드]` — 키워드 기반 커리큘럼 생성

```
/teach blockchain consensus
```

**동작**: 키워드를 입력하면 6개 에이전트가 순차·병렬로 작동하여 완전한 교수 커리큘럼을 자동 생성합니다.

```
Step 0: @content-analyzer — 사용자 자료 스캔 (Case A/B 판별)
Step 1: @topic-scout — 주제 범위 도출 + 난이도 스펙트럼
Step 2: @web-searcher — 실시간 웹 검색 (병렬)   ┐
Step 3: @deep-researcher — 심층 학술 리서치 (병렬)  ├ 동시 실행
Step 4: @content-curator — 결과 병합 + 품질 관리
Step 5: @curriculum-architect — 완전한 커리큘럼 설계
```

**산출물**: `data/socratic/curriculum/auto-curriculum.json`
- 모듈 → 레슨 → 개념 계층 구조
- 개념별 소크라테스 질문 (L1/L2/L3)
- 개념 의존성 그래프 (DAG)
- 전이 학습 챌린지
- 메타인지 체크포인트

**사용자 개입**: 없음 (완전 자동). 키워드 입력 후 최종 결과만 확인하면 됩니다.

### 3.2 `/teach-from-file [파일경로]` — 파일 기반 커리큘럼 생성 (Case A)

```
/teach-from-file coding-resource/my-textbook.pdf
```

사용자가 제공한 자료(PDF, 텍스트 등)를 분석하여 커리큘럼을 생성합니다.
자료의 구조와 내용을 우선하고, 웹 검색/심층 리서치로 보충합니다.

### 3.3 `/upload-content [파일경로]` — 보충 자료 추가

```
/upload-content lecture-notes/week3.pdf
```

이미 생성된 커리큘럼에 추가 자료를 보충합니다. 커리큘럼이 이미 존재해야 합니다.

---

## 4. 학습 세션 (Phase 1-3)

### 4.1 `/start-learning [topic]` — 세션 시작

```
/start-learning
```

또는 자연어:

```
배우자
공부하자
teach me
```

**신규 학습자** (첫 세션):
1. **진단** (Phase 1): 적응형 질문 5-7개로 현재 수준 파악
2. **경로 설계** (Phase 2): ZPD 기반 최적 학습 순서 결정
3. **대화 시작** (Phase 3): 소크라테스 문답법으로 학습

**돌아온 학습자** (2회차 이후):
1. **경로 갱신**: 이전 세션의 진행 상황 + 시간 경과에 따른 망각 반영
2. **대화 시작**: 이전에 멈춘 지점부터 이어서 학습

### 4.2 소크라테스 대화 방식

대화 세션 중 시스템은 **절대로 직접 답을 알려주지 않습니다**. 대신:

1. **유도 질문**: 학습자가 스스로 답에 도달하도록 단서를 제공
2. **비유와 예시**: 추상적 개념을 구체적 상황에 연결
3. **인지적 갈등**: 오개념 발견 시, 기존 생각과 모순되는 상황을 제시하여 자기 교정 유도

```
예시 대화:

AI: "블록체인에서 '합의'란 무엇이라고 생각하시나요?"

학습자: "모든 컴퓨터가 같은 데이터를 가지는 것?"

AI: "좋은 출발점이에요. 그런데 '같은 데이터를 가진다'는 것과
    '같은 데이터에 동의한다'는 것 사이에 차이가 있을까요?
    예를 들어, 내 컴퓨터에 복사된 파일과 계약서에 서명하는 것의
    차이를 생각해보면..."

학습자: "아, 단순 복제가 아니라 검증과 동의 과정이 있다는 건가요?"

AI: "바로 그 방향이에요! 그렇다면 그 '검증과 동의'를
    중앙 서버 없이 어떻게 달성할 수 있을까요?"
```

### 4.3 대화 중 사용 가능한 상호작용

| 행동 | 방법 | 설명 |
|------|------|------|
| **일반 응답** | 자연어로 답하기 | 소크라테스 대화 계속 |
| **모르겠다고 말하기** | "모르겠어요" | 시스템이 더 기본적인 수준(L1)으로 돌아가 힌트 제공 |
| **개념 맵 보기** | "개념 맵" 또는 `/concept-map` | 현재까지 배운 개념 관계도 표시 |
| **진도 확인** | "얼마나 배웠어?" 또는 `/my-progress` | 경량 진행 요약 표시 |
| **도전 요청** | "테스트" 또는 `/challenge` | 전이 학습 챌린지 시작 |
| **세션 종료** | "그만" 또는 `/end-session` | 세션 종료 + 요약 |

---

## 5. 세션 관리

### 5.1 `/end-session` — 세션 종료

```
/end-session
```

또는 자연어:

```
그만
여기까지
오늘은 여기까지
done for today
```

**종료 시 자동 수행되는 작업**:
1. 세션 트랜스크립트 저장
2. 개념 맵 갱신 (`@concept-mapper`)
3. 진척도 리포트 생성 (`@progress-tracker`)
4. 오개념 데이터 통합
5. 학습 경로 재최적화 (`@path-optimizer`)
6. 세션 요약 표시

### 5.2 `/resume [session-id]` — 중단된 세션 복구

```
/resume
```

또는 자연어:

```
이어서 하자
continue
```

세션이 예기치 않게 중단된 경우(컨텍스트 오버플로, 연결 끊김 등), 마지막 상태에서 복구합니다.

**복구 대상**:
- 보류 중이던 질문 (정확 복원)
- 현재 모듈/레슨 위치 (정확 복원)
- 마스터리 점수 (±1 상호작용)
- 대화 맥락 (요약 수준)

**여러 세션이 중단된 경우**: 목록에서 선택하거나 `session-id`를 직접 지정

```
/resume SES_20260228_a3f7b2
```

### 5.3 자동 저장

세션 중 데이터는 **자동으로 저장**됩니다:
- **매 응답 후**: Stop Hook이 세션 스냅샷을 `data/socratic/sessions/snapshots/`에 저장
- **매 상호작용 후**: @orchestrator가 `learner-state.yaml`을 갱신
- **활동 추적**: PostToolUse Hook이 마지막 활동 시간을 기록

수동 저장이 필요 없습니다. 예기치 않은 중단 시 `/resume`으로 복구할 수 있습니다.

---

## 6. 진척도 추적

### 6.1 `/my-progress` — 진척도 리포트

```
/my-progress
```

또는 자연어:

```
진도율
얼마나 배웠어?
how far along
```

**리포트 내용**:
- 전체 학습 진행률 (%)
- 개념별 마스터리 수준 (0.0 ~ 1.0)
- 세션 히스토리 (총 세션 수, 총 학습 시간)
- 오개념 교정 현황
- 전이 챌린지 통과 현황
- 학습 속도 트렌드 (improving / stable / declining)
- Bloom 효과 크기 추정치 (3회 이상 세션 후)

### 6.2 마스터리 수준 해석

| 마스터리 | 의미 | 다음 단계 |
|---------|------|----------|
| 0.0 ~ 0.3 | 기초 부족 | L1(기억/이해) 수준 질문으로 기초 강화 |
| 0.3 ~ 0.5 | 기본 이해 | ZPD 타겟 — L2(적용/분석) 질문 도전 |
| 0.5 ~ 0.7 | 적용 가능 | L3(종합/평가) 질문으로 깊은 이해 유도 |
| 0.7 ~ 0.8 | 숙달 근접 | 전이 챌린지 준비. 0.7 이상은 전이 검증 없이는 상승 불가 |
| 0.8 ~ 1.0 | 전이 검증 완료 | 간격 반복으로 유지. 다음 개념으로 진행 |

### 6.3 마스터리 감소 (망각 곡선)

시간이 지나면 마스터리가 자연적으로 감소합니다 (Ebbinghaus 망각 곡선):

```
effective_mastery = mastery × max(0.3, 1.0 - days_since_review × 0.02)
```

- 30일 미복습: 마스터리 약 40% 감소
- 돌아온 학습자의 경로에 자동으로 복습 일정이 반영됩니다

---

## 7. 개념 맵

### 7.1 `/concept-map [topic]` — 개념 연결 맵 시각화

```
/concept-map
/concept-map blockchain
```

또는 자연어:

```
개념 맵
배운 것 보여줘
concept map
```

**표시 내용**:
- 학습한 개념들의 관계 그래프 (Mermaid 다이어그램)
- 개념별 마스터리 수준 (색상으로 표시)
- 학습자가 직접 표현한 관계 (세션 대화에서 추출)
- 커리큘럼의 정규 관계 (auto-curriculum.json에서 파생)

**`topic` 옵션**: 특정 주제/모듈만 필터링하여 표시

---

## 8. 전이 학습 챌린지

### 8.1 `/challenge [concept]` — 전이 챌린지 실행

```
/challenge
/challenge blockchain_consensus
```

또는 자연어 (세션 중):

```
테스트
quiz me
실력 확인
```

**전제 조건**: 해당 개념의 마스터리 ≥ 0.7

**챌린지 유형**:
1. **Same-field Transfer**: 같은 도메인 내에서 다른 상황에 적용
2. **Far Transfer**: 완전히 다른 도메인에 개념을 적용

**결과**:
- PASS → `transfer_validated: true` → 마스터리 0.7 상한 해제 (최대 1.0까지)
- FAIL → 구체적 피드백 + 해당 개념 학습 경로에 재배치

---

## 9. 자연어 인터랙션

슬래시 명령을 외우지 않아도 자연어로 시스템을 제어할 수 있습니다.

### 9.1 세션 밖에서 (Pre-Session)

| 의도 | 한국어 예시 | 영어 예시 | 실행 |
|------|-----------|----------|------|
| 학습 시작 | "배우자", "공부하자", "시작하자" | "teach me", "let's learn" | /start-learning |
| 세션 복구 | "이어서 하자", "계속하자" | "continue", "resume" | /resume |
| 진도 확인 | "진도율", "얼마나 배웠어?" | "my progress" | /my-progress |
| 개념 맵 | "개념 맵", "배운 것 보여줘" | "concept map" | /concept-map |

### 9.2 세션 중 (In-Session)

| 의도 | 한국어 예시 | 영어 예시 | 실행 |
|------|-----------|----------|------|
| 세션 종료 | "그만", "여기까지", "끝내자" | "stop", "quit", "done for today" | /end-session |
| 챌린지 | "테스트", "실력 확인" | "test me", "quiz me" | /challenge |
| 개념 맵 | "개념 맵" | "concept map" | @concept-mapper (비차단) |
| 진도 확인 | "진도율" | "how am I doing" | 경량 요약 |

### 9.3 모호한 입력 처리

시스템이 의도를 확실히 판단하지 못하면, 확인 질문을 합니다:

```
학습자: "다시 해볼까?"

AI: "이전 세션을 이어서 하시겠어요, 아니면 새로 시작하시겠어요?"
```

학습 내용에 포함된 키워드(예: "이 개념은 여기까지 이해했어")는 의도로 분류하지 않습니다.

---

## 10. 선택적 MCP 강화

기본 설치만으로도 모든 기능이 작동합니다. 아래 MCP 서버는 **선택적 강화**입니다:

### 10.1 Brave Search (고품질 검색)

```json
// .mcp.json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": { "BRAVE_API_KEY": "<your-key>" }
    }
  }
}
```

Fallback: 내장 WebSearch (항상 사용 가능)

### 10.2 Perplexity Deep Research (심층 학술 리서치)

```json
// .mcp.json
{
  "mcpServers": {
    "perplexity": {
      "command": "npx",
      "args": ["-y", "@anthropic/perplexity-mcp"],
      "env": { "PERPLEXITY_API_KEY": "<your-key>" }
    }
  }
}
```

Fallback: 다단계 WebSearch + WebFetch 패턴

### 10.3 Mermaid PNG 내보내기 (개념 맵 이미지)

```json
// .mcp.json
{
  "mcpServers": {
    "mermaid": {
      "command": "npx",
      "args": ["-y", "mermaid-mcp-server"]
    }
  }
}
```

Fallback: Mermaid 텍스트 다이어그램 (인라인 렌더링)

---

## 11. 트러블슈팅

### 11.1 일반적 문제

| 증상 | 원인 | 해결 |
|------|------|------|
| `/start-learning` 실행 시 "No curriculum found" | 커리큘럼 미생성 | `/teach [키워드]`를 먼저 실행 |
| `/start-learning` 실행 시 "Active session already exists" | 이전 세션 미종료 | `/end-session` 후 재시작, 또는 `/resume` |
| `/resume` 실행 시 "No interrupted sessions found" | 중단된 세션 없음 | `/start-learning`으로 새 세션 시작 |
| 대화 중 응답이 느림 | @misconception-detector + @metacog-coach 동시 실행 | 정상 — 품질을 위한 다중 에이전트 분석 |
| `/teach` 실행 중 멈춤 | 웹 검색 타임아웃 | 자동 fallback 작동. 잠시 대기 후 재시도 |

### 11.2 인프라 검증

```
/install           # 전체 인프라 건강 검증
/maintenance       # 주기적 건강 검진 (stale data, 무결성)
```

### 11.3 데이터 위치

| 데이터 | 경로 | 설명 |
|--------|------|------|
| 커리큘럼 | `data/socratic/curriculum/auto-curriculum.json` | 자동 생성된 교수 커리큘럼 |
| 학습자 상태 | `data/socratic/learner-state.yaml` | 마스터리, 세션 기록, 학습 경로 |
| 세션 로그 | `data/socratic/sessions/active/` | 현재 세션 로그 |
| 세션 스냅샷 | `data/socratic/sessions/snapshots/` | 복구용 스냅샷 |
| 진척도 리포트 | `data/socratic/reports/` | 진행 상황 분석 |
| 개념 맵 | `data/socratic/` | concept-map.json |

### 11.4 학습 상태 초기화

모든 학습 진행 상황을 초기화하고 싶다면:

```bash
# 학습자 상태 초기화 (되돌릴 수 없음!)
rm data/socratic/learner-state.yaml
rm -rf data/socratic/sessions/active/*
rm -rf data/socratic/sessions/completed/*
rm -rf data/socratic/sessions/interrupted/*
rm -rf data/socratic/sessions/snapshots/*
```

커리큘럼은 유지하고 학습 진행만 초기화합니다.
커리큘럼도 재생성하려면 `data/socratic/curriculum/` 내 파일도 삭제 후 `/teach`를 다시 실행하세요.

---

## 12. 교수자를 위한 안내

### 12.1 커리큘럼 커스터마이징

`/teach` 명령으로 생성된 커리큘럼(`auto-curriculum.json`)은 자동 생성되지만,
교수자가 직접 편집하여 커스터마이징할 수 있습니다:

- **모듈/레슨 순서** 변경
- **소크라테스 질문** 추가/수정
- **전이 챌린지** 커스텀 문제 추가
- **메타인지 체크포인트** 위치 조정

### 12.2 학습자 진행 모니터링

`data/socratic/learner-state.yaml`의 주요 필드:

```yaml
knowledge_state:
  concept_001:
    mastery: 0.65        # 개념별 마스터리 수준
    confidence: 0.70     # 학습자 자기 보고 신뢰도
    transfer_validated: false  # 전이 챌린지 통과 여부

history:
  total_sessions: 5      # 총 세션 수
  total_study_time_minutes: 180  # 총 학습 시간
  transfer_challenges_passed: 2  # 전이 챌린지 통과 수

bloom_calibration:
  estimated_current_effect: 0.72  # 추정 효과 크기 (d값)
```

### 12.3 효과 측정

VanLehn(2011) 기준으로, 시스템은 **d=0.79** 효과 크기를 목표로 합니다.
3회 이상 세션 후 `bloom_calibration.estimated_current_effect`에 추정치가 계산됩니다.

---

## 13. 빌더 명령 (시스템 구축용)

이 명령들은 Socratic AI Tutor를 **처음 구축할 때** 사용된 빌더 워크플로우 명령입니다.
일반 사용자가 사용할 필요는 없습니다.

| 명령 | 설명 |
|------|------|
| `/build-socratic-tutor` | 21단계 빌더 워크플로우 시작 |
| `/review-research` | Research Phase 산출물 검토 |
| `/approve-design` | Planning Phase 설계 승인 |
| `/accept-system` | 최종 시스템 인수 검사 |
