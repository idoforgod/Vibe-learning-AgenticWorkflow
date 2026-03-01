# Socratic AI Tutor — Powered by AgenticWorkflow

**키워드 하나로 완전한 교육 커리큘럼을 자동 생성하고, 소크라테스 문답법으로 1:1 맞춤 튜터링을 제공하는 AI 교육 시스템.**

17개 전문 AI 에이전트가 협업하여 대학 대형 강의의 한계를 극복합니다.
학습자의 수준을 진단하고, 최적 학습 경로를 설계하며, 실시간 소크라테스식 대화로 깊은 이해를 이끌어냅니다.

> 이 시스템은 [AgenticWorkflow](#부모-프레임워크-agenticworkflow) 프레임워크("만능줄기세포")에서 분화된 자식 시스템입니다.

---

## 빠른 시작

```bash
# 1. 설치
git clone https://github.com/idoforgod/Vibe-learning-AgenticWorkflow.git
cd Vibe-learning-AgenticWorkflow
claude

# 2. 커리큘럼 생성 (완전 자동)
/teach blockchain consensus

# 3. 학습 시작
/start-learning
```

## 핵심 명령

| 명령 | 설명 | 자연어로도 가능 |
|------|------|:---:|
| `/teach [키워드]` | 커리큘럼 자동 생성 | — |
| `/start-learning` | 소크라테스 대화 세션 시작 | "배우자", "teach me" |
| `/end-session` | 세션 종료 + 요약 | "그만", "done for today" |
| `/resume` | 중단된 세션 복구 | "이어서 하자", "continue" |
| `/my-progress` | 학습 진척도 확인 | "진도율", "how far along" |
| `/concept-map` | 개념 연결 맵 시각화 | "개념 맵", "배운 것 보여줘" |
| `/challenge` | 전이 학습 챌린지 | "테스트", "quiz me" |

---

## 문서 안내

### 부모-자식 문서 분리

이 프로젝트는 **만능줄기세포(AgenticWorkflow)**와 그로부터 분화된 **자식 시스템(Socratic AI Tutor)**을 구분합니다.
부모 문서는 방법론/프레임워크를, 자식 문서는 도메인 고유 아키텍처를 기술합니다.

#### 자식 시스템 (Socratic AI Tutor) 문서

| 순서 | 문서 | 목적 |
|------|------|------|
| 1 | [`SOCRATIC-TUTOR-README.md`](SOCRATIC-TUTOR-README.md) | Socratic AI Tutor 소개, 구조, 에이전트 목록 |
| 2 | [`SOCRATIC-TUTOR-ARCHITECTURE.md`](SOCRATIC-TUTOR-ARCHITECTURE.md) | 3-Phase 아키텍처, 17개 에이전트, 상태 관리, 교육학 이론 매핑 |
| 3 | [`SOCRATIC-TUTOR-USER-MANUAL.md`](SOCRATIC-TUTOR-USER-MANUAL.md) | 모든 명령 상세 사용법, 학습 흐름, 트러블슈팅 |

#### 부모 프레임워크 (AgenticWorkflow) 문서

| 순서 | 문서 | 목적 |
|------|------|------|
| 1 | [`soul.md`](soul.md) | 프로젝트 영혼 — DNA 유전 철학, 규칙 아래의 이유 |
| 2 | [`AGENTICWORKFLOW-ARCHITECTURE-AND-PHILOSOPHY.md`](AGENTICWORKFLOW-ARCHITECTURE-AND-PHILOSOPHY.md) | 부모 프레임워크의 설계 철학, 아키텍처 전체 조감도 |
| 3 | [`AGENTICWORKFLOW-USER-MANUAL.md`](AGENTICWORKFLOW-USER-MANUAL.md) | 부모 프레임워크 자체의 사용법 (워크플로우 설계·구현 도구) |
| 4 | [`DECISION-LOG.md`](DECISION-LOG.md) | 모든 설계 결정의 맥락과 근거 추적 (ADR) |
| 5 | `AGENTS.md` / `CLAUDE.md` | AI 도구별 지시서 |

---

## 프로젝트 구조

```
Vibe-learning-AgenticWorkflow/
│
├── ★ 자식 시스템 (Socratic AI Tutor) ─────────────────────────────
│
├── SOCRATIC-TUTOR-README.md              # 자식: 프로젝트 소개
├── SOCRATIC-TUTOR-ARCHITECTURE.md        # 자식: 설계 철학 및 아키텍처
├── SOCRATIC-TUTOR-USER-MANUAL.md         # 자식: 사용자 매뉴얼
│
├── .claude/
│   ├── agents/                           # 17개 전문 에이전트
│   │   ├── AGENT-MANIFEST.md             # 에이전트 레지스트리
│   │   ├── orchestrator.md               # 8-상태 세션 라이프사이클 관리
│   │   ├── socratic-tutor.md             # 소크라테스 문답 (Phase 3 핵심)
│   │   └── ... (15개 전문 에이전트)
│   │
│   ├── commands/                         # 9개 사용자 명령 + 4개 빌더 명령
│   │   ├── teach.md                      # /teach — 커리큘럼 생성
│   │   ├── start-learning.md             # /start-learning — 세션 시작
│   │   └── ... (11개 추가 명령)
│   │
│   ├── skills/
│   │   └── socratic-tutor/               # 소크라테스 튜터링 스킬
│   │       ├── SKILL.md                  # Phase 1-3 전체 세션 라이프사이클
│   │       └── hooks-and-state.md        # Hook + 상태 관리 인프라
│   │
│   └── hooks/scripts/                    # 자식 전용 Hook 3개
│       ├── guard_learner_state.py        # SOT 쓰기 보호
│       ├── track_session_activity.py     # 세션 활동 추적
│       └── save_session_snapshot.py      # 세션 스냅샷 저장
│
├── data/socratic/                        # 런타임 데이터
│   ├── state.yaml                        # Phase 0 워크플로우 SOT
│   ├── learner-state.yaml                # 학습자 SOT (영구 지속)
│   ├── curriculum/                       # 자동 생성 커리큘럼
│   ├── schemas/                          # 33개 JSON 스키마
│   └── sessions/                         # 세션 로그 + 스냅샷
│
├── coding-resource/
│   └── socratic-ai-tutor-workflow.md     # 원본 워크플로우 설계서
│
├── ★ 부모 프레임워크 (AgenticWorkflow — 만능줄기세포) ──────────────
│
├── CLAUDE.md                             # Claude Code 전용 지시서
├── AGENTS.md                             # 모든 AI 에이전트 공통 지시서
├── AGENTICWORKFLOW-ARCHITECTURE-AND-PHILOSOPHY.md  # 부모: 설계 철학
├── AGENTICWORKFLOW-USER-MANUAL.md        # 부모: 사용법
├── DECISION-LOG.md                       # 설계 결정 로그 (ADR)
├── soul.md                               # 프로젝트 영혼 (DNA 유전 철학)
├── COPYRIGHT.md                          # 저작권
│
├── .claude/
│   ├── settings.json                     # Hook 설정 (부모 + 자식 통합)
│   ├── hooks/scripts/                    # 부모 Hook 스크립트 (21개)
│   │   ├── context_guard.py              # Hook 통합 디스패처
│   │   ├── save_context.py               # 컨텍스트 저장
│   │   ├── restore_context.py            # 컨텍스트 복원
│   │   ├── block_destructive_commands.py # 위험 명령 차단
│   │   └── ... (17개 추가 스크립트)
│   ├── context-snapshots/                # 런타임 스냅샷 (gitignored)
│   └── skills/
│       ├── workflow-generator/           # 워크플로우 설계·생성 스킬
│       ├── doctoral-writing/             # 박사급 학술 글쓰기 스킬
│       └── socratic-builder/             # Socratic AI Tutor 빌더 스킬
│
├── translations/glossary.yaml            # 번역 용어 사전
└── prompt/                               # 프롬프트 자료
```

---

## 부모 프레임워크: AgenticWorkflow

이 시스템의 토대인 **AgenticWorkflow**는 어떤 에이전트 워크플로우로든 분화할 수 있는 만능줄기세포(Pluripotent Stem Cell) 프레임워크입니다.

### 핵심 개념

- **워크플로우 설계 → 구현**: `workflow.md`(설계도) → 실제 동작하는 시스템(최종 산출물)
- **3단계 구조**: Research → Planning → Implementation
- **DNA 유전**: 분화된 모든 자식 시스템은 부모의 전체 게놈(절대 기준, 품질 보장, 안전장치, 기억 체계)을 구조적으로 내장

### 절대 기준

1. **품질 최우선** — 속도, 비용, 작업량보다 최종 결과물의 품질이 유일한 기준
2. **단일 파일 SOT** — Single Source of Truth + 계층적 메모리 구조
3. **코드 변경 프로토콜 (CCP)** — 의도 파악 → 영향 범위 분석 → 변경 설계
4. **품질 > SOT, CCP** — 충돌 시 품질이 우선

### 4계층 품질 보장

| 계층 | 이름 | 검증 대상 |
|------|------|---------|
| **L0** | Anti-Skip Guard | 파일 존재 + 최소 크기 |
| **L1** | Verification Gate | 기능적 목표 100% 달성 |
| **L1.5** | pACS Self-Rating | F/C/L 3차원 신뢰도 |
| **L2** | Adversarial Review | 적대적 검토 |

### Context Preservation System

컨텍스트 토큰 초과·`/clear`·압축 시 작업 내역 상실을 방지하는 자동 저장·복원 시스템.
Hook 스크립트가 작업 내역을 자동 저장하고, 세션 시작 시 RLM 패턴으로 복원합니다.

상세: [`AGENTICWORKFLOW-ARCHITECTURE-AND-PHILOSOPHY.md`](AGENTICWORKFLOW-ARCHITECTURE-AND-PHILOSOPHY.md)

### 부모 스킬

| 스킬 | 설명 |
|------|------|
| **workflow-generator** | Research → Planning → Implementation 3단계 `workflow.md` 설계·생성 |
| **doctoral-writing** | 박사급 학위 논문 학술 글쓰기 지원 |
| **socratic-builder** | Socratic AI Tutor 21단계 빌더 워크플로우 |

### AI 도구 호환성

Hub-and-Spoke 패턴으로 Claude Code, Gemini CLI, Codex CLI, Copilot CLI, Cursor에서 동일 방법론이 자동 적용됩니다.

---

## 이론적 기반

| 이론 | 적용 |
|------|------|
| VanLehn(2011) — 1:1 튜터링 효과 (d=0.79) | 시스템 효과 목표 |
| Chi(2005) — 오개념 8유형 분류 | @misconception-detector |
| Flavell(1979) — 메타인지 프레임워크 | @metacog-coach |
| Vygotsky — ZPD(근접발달영역) | @path-optimizer |
| Ebbinghaus — 망각 곡선 | 간격 반복 + 마스터리 감소 |
| Recursive Language Models (논문) | 장기기억 구현 이론 |

상세: [`SOCRATIC-TUTOR-ARCHITECTURE.md`](SOCRATIC-TUTOR-ARCHITECTURE.md)
