# Socratic AI Tutor

**키워드 하나로 완전한 교육 커리큘럼을 자동 생성하고, 소크라테스 문답법으로 1:1 맞춤 튜터링을 제공하는 AI 교육 시스템.**

17개 전문 AI 에이전트가 협업하여 대학 대형 강의의 한계를 극복합니다.
학습자의 수준을 진단하고, 최적 학습 경로를 설계하며, 실시간 소크라테스식 대화로 깊은 이해를 이끌어냅니다.

> 이 시스템은 [AgenticWorkflow](AGENTICWORKFLOW-ARCHITECTURE-AND-PHILOSOPHY.md) 프레임워크("만능줄기세포")에서 분화된 자식 시스템입니다.
> 부모의 전체 DNA — 절대 기준, 4계층 품질 보장, 안전장치, 기억 체계 — 를 구조적으로 내장합니다.

---

## 핵심 특징

| 특징 | 설명 |
|------|------|
| **Zero-to-Curriculum** | 키워드 하나 입력 → Pre-trained 지식 + 실시간 검색 + 심층 리서치 결합 → 완전한 교수 커리큘럼 자동 생성 |
| **소크라테스 문답법** | 답을 알려주지 않고, 3단계 질문(L1 recall → L2 application → L3 synthesis)으로 사고를 이끌어냄 |
| **적응형 학습 경로** | ZPD(근접발달영역) 기반 — 학습자의 현재 수준에 최적화된 순서로 개념을 배치 |
| **오개념 탐지** | Chi(2005) 8유형 분류법으로 실시간 오개념 탐지 + 인지적 갈등 전략으로 교정 |
| **메타인지 코칭** | Flavell(1979) 프레임워크 기반 — 학습자가 "어떻게 배우는지"를 인식하도록 코칭 |
| **전이 학습 챌린지** | 같은 도메인 → 다른 도메인으로 지식 전이를 검증하는 도전 문제 |
| **세션 복구** | 예기치 않은 중단(컨텍스트 오버플로, 연결 끊김) 후 `/resume`으로 정확히 이어서 학습 |
| **자연어 인터랙션** | 슬래시 명령 없이 "배우자", "그만하자" 같은 자연어로도 시스템 제어 가능 |

---

## 빠른 시작

### 1. 커리큘럼 생성 (Phase 0)

```
/teach blockchain consensus
```

키워드를 입력하면 6개 에이전트가 순차·병렬로 작동하여 완전한 커리큘럼을 자동 생성합니다.
사용자 확인 없이 완전 자동으로 실행됩니다.

### 2. 학습 시작 (Phase 1-3)

```
/start-learning
```

또는 자연어로:

```
배우자
```

새로운 학습자는 적응형 진단 → 학습 경로 설계 → 소크라테스 대화 순서로 진행됩니다.
돌아온 학습자는 이전 세션의 진행 상황을 기반으로 경로를 갱신한 뒤 바로 대화에 진입합니다.

### 3. 학습 종료

```
/end-session
```

또는 자연어로:

```
오늘은 여기까지
```

개념 맵 갱신, 진척도 리포트 생성, 학습 경로 재최적화가 자동 수행됩니다.

---

## 사용자 명령 요약

| 명령 | 설명 | 자연어 트리거 |
|------|------|-------------|
| `/teach [키워드]` | 키워드로 커리큘럼 자동 생성 (Phase 0) | — |
| `/teach-from-file [파일경로]` | 파일 기반 커리큘럼 생성 (Case A) | — |
| `/upload-content [파일경로]` | 기존 커리큘럼에 보충 자료 추가 | — |
| `/start-learning [topic]` | 소크라테스 튜터링 세션 시작 | "배우자", "학습 시작", "teach me" |
| `/resume [session-id]` | 중단된 세션 복구 | "이어서 하자", "continue" |
| `/end-session` | 현재 세션 종료 + 요약 | "그만", "여기까지", "done for today" |
| `/my-progress` | 학습 진척도 리포트 | "진도율", "얼마나 배웠어?" |
| `/concept-map [topic]` | 개념 연결 맵 시각화 | "개념 맵", "배운 것 보여줘" |
| `/challenge [concept]` | 전이 학습 챌린지 | "테스트", "quiz me" |

---

## 프로젝트 구조

```
AgenticWorkflow/                          ← 부모 프레임워크 (만능줄기세포)
├── CLAUDE.md                             ← 부모: Claude Code 전용 지시서
├── AGENTS.md                             ← 부모: 모든 AI 에이전트 공통 지시서
├── soul.md                               ← 부모: DNA 유전 철학
│
├── SOCRATIC-TUTOR-README.md              ← ★ 자식: 이 파일 (프로젝트 소개)
├── SOCRATIC-TUTOR-ARCHITECTURE.md        ← ★ 자식: 설계 철학 및 아키텍처
├── SOCRATIC-TUTOR-USER-MANUAL.md         ← ★ 자식: 사용자 매뉴얼
│
├── .claude/
│   ├── agents/                           ← ★ 17개 전문 에이전트 정의
│   │   ├── AGENT-MANIFEST.md             (에이전트 레지스트리)
│   │   ├── orchestrator.md               (8-상태 세션 라이프사이클 관리)
│   │   ├── socratic-tutor.md             (소크라테스 문답 + 오개념 탐지)
│   │   ├── content-analyzer.md           (콘텐츠 분석 — Phase 0 + Phase 1)
│   │   ├── topic-scout.md                (주제 범위 도출)
│   │   ├── web-searcher.md               (실시간 웹 검색)
│   │   ├── deep-researcher.md            (심층 학술 리서치)
│   │   ├── content-curator.md            (콘텐츠 큐레이션 + 품질 관리)
│   │   ├── curriculum-architect.md        (커리큘럼 설계)
│   │   ├── learner-profiler.md           (학습자 진단)
│   │   ├── knowledge-researcher.md       (보충 지식 검색)
│   │   ├── path-optimizer.md             (ZPD 기반 학습 경로 최적화)
│   │   ├── session-planner.md            (세션 구조 설계)
│   │   ├── session-logger.md             (세션 로깅 + 복구)
│   │   ├── misconception-detector.md     (오개념 탐지 — 8유형 분류)
│   │   ├── metacog-coach.md              (메타인지 코칭)
│   │   ├── concept-mapper.md             (개념 그래프 구축)
│   │   └── progress-tracker.md           (학습 분석 + 진척도 추적)
│   │
│   ├── commands/                         ← ★ 9개 사용자 명령 + 4개 빌더 명령
│   │   ├── teach.md                      (/teach — 키워드 → 커리큘럼)
│   │   ├── teach-from-file.md            (/teach-from-file — 파일 기반)
│   │   ├── upload-content.md             (/upload-content — 보충 자료)
│   │   ├── start-learning.md             (/start-learning — 세션 시작)
│   │   ├── resume.md                     (/resume — 세션 복구)
│   │   ├── end-session.md                (/end-session — 세션 종료)
│   │   ├── my-progress.md                (/my-progress — 진척도)
│   │   ├── concept-map.md                (/concept-map — 개념 맵)
│   │   └── challenge.md                  (/challenge — 전이 챌린지)
│   │
│   ├── skills/
│   │   └── socratic-tutor/               ← ★ 소크라테스 튜터링 스킬 정의
│   │       ├── SKILL.md                  (Phase 1-3 전체 세션 라이프사이클)
│   │       └── hooks-and-state.md        (Hook + 상태 관리 인프라)
│   │
│   └── hooks/scripts/                    ← 부모 + 자식 Hook 스크립트
│       ├── guard_learner_state.py        (★ 자식: SOT 쓰기 보호)
│       ├── track_session_activity.py     (★ 자식: 세션 활동 추적)
│       └── save_session_snapshot.py      (★ 자식: 세션 스냅샷 저장)
│
├── data/socratic/                        ← ★ 런타임 데이터 디렉터리
│   ├── state.yaml                        (Phase 0 워크플로우 SOT)
│   ├── learner-state.yaml                (학습자 SOT — 세션 간 지속)
│   ├── curriculum/                       (자동 생성 커리큘럼)
│   ├── analysis/                         (콘텐츠 분석 + 학습자 프로필)
│   ├── planning/                         (학습 경로 + 세션 계획)
│   ├── sessions/                         (active/ + completed/ + interrupted/ + snapshots/)
│   ├── schemas/                          (33개 JSON 스키마)
│   ├── reports/                          (진척도 리포트)
│   └── misconceptions/                   (오개념 라이브러리)
│
└── coding-resource/
    └── socratic-ai-tutor-workflow.md     ← 원본 워크플로우 설계서
```

---

## 문서 읽기 순서

| 순서 | 문서 | 목적 |
|------|------|------|
| 1 | **이 파일** (`SOCRATIC-TUTOR-README.md`) | 프로젝트 개요 + 빠른 시작 |
| 2 | [`SOCRATIC-TUTOR-ARCHITECTURE.md`](SOCRATIC-TUTOR-ARCHITECTURE.md) | 설계 철학, 3-Phase 아키텍처, 17개 에이전트 구조, 상태 관리 |
| 3 | [`SOCRATIC-TUTOR-USER-MANUAL.md`](SOCRATIC-TUTOR-USER-MANUAL.md) | 모든 명령의 상세 사용법, 학습 흐름, 트러블슈팅 |
| 4 | [`AGENTICWORKFLOW-ARCHITECTURE-AND-PHILOSOPHY.md`](AGENTICWORKFLOW-ARCHITECTURE-AND-PHILOSOPHY.md) | 부모 프레임워크의 설계 철학 (참조용) |

---

## 부모 DNA 유전

이 시스템은 AgenticWorkflow 프레임워크의 다음 DNA를 구조적으로 내장합니다:

| DNA | 자식 시스템에서의 발현 |
|-----|---------------------|
| **절대 기준 1 (품질)** | 모든 에이전트의 산출물 품질이 유일한 기준 |
| **절대 기준 2 (SOT)** | `state.yaml` + `learner-state.yaml` 이중 SOT — @orchestrator만 쓰기 |
| **4계층 품질 보장** | L0(Anti-Skip) → L1(Verification) → L1.5(pACS) → L2(Adversarial Review) |
| **Safety Hooks** | 부모 Hook(위험 명령 차단, TDD 보호, Predictive Debug) + 자식 Hook 3개 |
| **Context Preservation** | 부모 Hook 시스템이 세션 스냅샷·Knowledge Archive를 자동 관리 |
| **Adversarial Review** | `@reviewer` + `@fact-checker`가 빌더 단계에서 산출물 검증 |
| **Decision Log** | Autopilot 결정 사항 투명 기록 |

상세: [`soul.md`](soul.md)

---

## 기술 스택

| 구성 요소 | 기술 |
|----------|------|
| **런타임** | Claude Code CLI |
| **에이전트 프레임워크** | Claude Code Sub-agents (Task tool) |
| **모델** | Claude Opus 4.6 (핵심 3개) + Sonnet (9개) + Haiku (5개) |
| **상태 관리** | YAML SOT + JSON 스키마 |
| **검색** | WebSearch (내장) + Semantic Scholar API + arXiv API |
| **시각화** | Mermaid 다이어그램 (인라인) |
| **MCP (선택)** | Brave Search, Perplexity, Mermaid PNG 내보내기 |
| **언어** | Python 3.10+ (Hook 스크립트) |
