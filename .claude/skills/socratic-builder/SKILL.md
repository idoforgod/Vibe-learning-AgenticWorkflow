---
name: build-socratic-tutor
description: Socratic AI Tutor 21단계 빌더 워크플로우 Orchestrator. `/build-socratic-tutor` 또는 "빌드 시작"으로 호출. PRD.md + socratic-ai-tutor-workflow.md를 기반으로 17개 에이전트, 9개 슬래시 커맨드, 7개 MCP 통합, 이중 SOT 상태 관리를 갖춘 완전 자율형 개인화 교육 AI 시스템을 구축한다. `.claude/state.yaml`에서 시작/재개 지점을 결정한다.
---

# Socratic AI Tutor Builder

대학 대형 강의의 한계를 극복하는 완전 자율형 개인화 교육 AI 시스템을 21단계에 걸쳐 구축하는 빌더 Orchestrator 스킬.

## When to Invoke

- 사용자가 "build socratic tutor", "빌드 시작", `/build-socratic-tutor`를 요청할 때
- Entry point: `.claude/state.yaml`을 읽어 `current_step`에서 시작/재개

## Inputs

| 입력 | 경로 | 용도 |
|------|------|------|
| PRD | `coding-resource/PRD.md` | 요구사항 명세 — 17개 에이전트, 이중 SOT, 4-Phase 구조 |
| 설계 문서 | `coding-resource/socratic-ai-tutor-workflow.md` | 원본 설계 — 에이전트 역할, JSON 스키마, 실행 흐름 |
| Builder SOT | `.claude/state.yaml` | 빌더 워크플로우 진행 상태 |

## Outputs

| 산출물 | 위치 | 설명 |
|--------|------|------|
| Target Agent 정의 | `.claude/agents/` | 17개 에이전트 마크다운 파일 |
| Slash Commands | `.claude/commands/` | 9개 사용자 커맨드 |
| Phase 0 Pipeline | `data/socratic/` + `.claude/skills/socratic-tutor/` | 배치 파이프라인 구현 |
| Phase 1-3 Skill | `.claude/skills/socratic-tutor/` | 대화형 튜터링 Skill |
| JSON Schemas | `data/socratic/schemas/` | 에이전트 간 데이터 계약 |
| Hook/State Infra | `.claude/hooks/scripts/`, `data/socratic/` | 상태 관리 + 세션 로깅 |
| User Documentation | `SOCRATIC-TUTOR-USER-MANUAL.md` | 사용자 매뉴얼 |

---

## 절대 기준 (이 도메인에 맥락화)

### 절대 기준 1: 최종 결과물의 품질

> **속도, 토큰 비용, 작업량은 완전히 무시한다.**
> 모든 의사결정의 유일한 기준은 **최종 Socratic AI Tutor 시스템의 교육적 품질**이다.
> 에이전트 수를 줄여서 빠르게 만드는 것보다, 13+4개의 전문 에이전트를 모두 구현하여 교육 효과를 극대화한다.
> 소크라테스 문답법의 3단계(확인→탐구→논박) 깊이를 절대 축소하지 않는다.

### 절대 기준 2: 단일 파일 SOT + 이중 SOT 구조

> **빌더 SOT(`state.yaml`)와 타겟 SOT(`learner-state.yaml`)를 명확히 분리한다.**
> - `state.yaml`: 빌더 워크플로우 진행 상태 — Orchestrator만 쓰기 권한
> - `learner-state.yaml`: 학습자 상태 — `@orchestrator` 타겟 에이전트만 쓰기 권한
> - 빌더 에이전트는 `state.yaml` 읽기 전용, 산출물은 별도 파일 생성

### 절대 기준 3: 코드 변경 프로토콜 (CCP)

> **Implementation Phase(Steps 12-21)에서 코드를 작성·수정할 때, 반드시 의도 파악 → 영향 범위 분석 → 변경 설계 3단계를 수행한다.**
> 에이전트 간 의존 관계(예: `@misconception-detector`가 `@socratic-tutor`의 서브에이전트), JSON 스키마 체인(예: `topic-scope.json` → `web-search-results.json`), SOT 구조 변경의 파급 효과를 분석한다.

**코딩 기준점 (CAP):**
- **CAP-1**: 코드를 읽기 전에 수정 금지. 기존 에이전트/스키마를 먼저 이해
- **CAP-2**: 최소 코드. 추측성 기능·조기 추상화 금지. 13개 에이전트 = 13개 파일, 과도한 공통 추상화 불필요
- **CAP-3**: 성공 기준 먼저 정의 (Verification 기준), 구현 후 검증
- **CAP-4**: 요청받은 변경만. "더 나은 교육학적 설계" 임의 추가 금지

### 절대 기준 간 우선순위

> **절대 기준 1(교육적 품질) > (절대 기준 2, 절대 기준 3)**

### English-First Execution Principle

> **All builder agents work in English. All deliverables are produced in English first.**
> After each step's English original passes all quality gates (L0→L1→L1.5→L2),
> `@translator` sub-agent produces a Korean `.ko.md` translation pair.

**Rationale** (Absolute Criterion 1 — quality maximization):
1. **Token efficiency** — Korean consumes 2-3x more tokens for equivalent content
2. **Accuracy** — LLMs achieve highest precision in English, their primary training language
3. **Consistency** — English prompts have less interpretation ambiguity across agent handoffs

**Language Allocation**:

| Context | Language | Reason |
|---------|----------|--------|
| Agent task prompts & system instructions | **English** | AI performance maximization |
| Agent deliverables (outputs) | **English** (original) | Primary artifact |
| Korean translation pair | **Korean** (`.ko.md`) | User-facing deliverable |
| SOT records (paths, numbers) | Language-neutral | Structural data |
| User-facing messages (reports, questions) | **Korean** | User communication |
| Skill/Agent/Command definition files | **English** (internal directives) | AI execution quality |

**Translation Steps** (Steps 5, 6, 8, 21 only):
1. English original passes Review (if applicable) → Translation eligible
2. Invoke `@translator` with `translations/glossary.yaml` reference
3. Output: Insert `.ko` before final extension (e.g., `report.md` → `report.ko.md`)
4. Translation pACS: Ft/Ct/Nt scored → `pacs-logs/step-N-translation-pacs.md`
5. P1 Validation: `validate_translation.py --step N --check-pacs [--check-sequence if Review step]`
6. SOT: Record `outputs.step-N-ko: "{path}.ko.md"`
7. Trace markers (`[trace:step-N]`) preserved verbatim — never translated

**NEVER DO**:
- Translate before Review PASS — Review PASS is a prerequisite for Translation
- Translate code, schemas, or configuration files — only text deliverables (`.md`, `.txt`)
- Translate trace markers — `[trace:step-N:section-id]` must remain intact
- Skip glossary reference — terminology consistency is non-negotiable

---

## 21-Step Execution Protocol

### Phase: Research (Steps 1-4)

#### Step 1: PRD & Design Document Deep Analysis
- **Agent**: `@prd-analyst` (Sub-agent)
- **Pre-processing**: `temp/scripts/split_prd_sections.py` — PRD를 섹션별로 분할하여 에이전트 집중도 향상
- **Task**: PRD.md + socratic-ai-tutor-workflow.md 심층 분석. 17개 에이전트 역할, 9개 커맨드, 7개 MCP, JSON 스키마, 실행 흐름, 이중 SOT 구조, 4-Phase 아키텍처의 완전한 요구사항 매니페스트 생성
- **Verification**:
  - 17개 에이전트 전체 역할·트리거·입출력이 누락 없이 기록됨
  - 9개 슬래시 커맨드의 인자·동작·출력이 완전히 정의됨
  - 7개 MCP 서버의 용도·연동 대상이 명시됨
  - Phase 0-3 실행 흐름의 데이터 의존성 그래프가 포함됨
  - JSON 스키마 필드 인벤토리가 파이프라인 순서대로 정리됨
  - 이중 SOT(`state.yaml` + `learner-state.yaml`) 스키마가 정의됨
- **Post-processing**: `temp/scripts/validate_counts.py` — 에이전트/커맨드/MCP 수량 검증
- **Output**: `research/requirements-manifest.md`
- **Review**: none
- **Translation**: none

#### Step 2: Technology Feasibility Assessment
- **Agent**: `@tech-scout` (Sub-agent)
- **Task**: Claude Code 환경에서의 기술 실현 가능성 평가. MCP 서버 가용성, 에이전트 간 통신 패턴, 파일 기반 상태 관리 제약, Context Injection 패턴 선택, 모델 선택(opus/sonnet), Deep Research API 접근성 확인
- **Verification**:
  - 7개 MCP 서버 각각에 대한 가용성/대안 분석 포함
  - Context Injection 패턴(A/B/C) 매핑 테이블 포함
  - 파일 기반 아키텍처 제약과 회피 전략 명시
  - 모델 선택 근거(비용/성능 트레이드오프) 테이블 포함
  - 기술적 리스크 상위 5개 + 완화 전략 포함
- **Output**: `research/tech-feasibility-report.md`
- **Review**: none
- **Translation**: none

#### Step 3: Educational Pedagogy Verification
- **Agent**: `@edu-analyst` (Sub-agent)
- **Pre-processing**: `temp/scripts/extract_edu_theories.py` — PRD에서 교육학 이론 참조 추출
- **Task**: PRD의 교육학적 주장(Bloom 2-Sigma, ZPD, 소크라테스 문답법, 간격 반복, 메타인지, 전이 학습) 학술적 검증. 각 이론의 현재 학술 컨센서스, 한계, AI 적용 시 고려사항 평가
- **Verification**:
  - 6개 교육학 이론 각각에 대한 학술 근거 확인 (출처 포함)
  - Bloom 2-Sigma 후속 연구 보정값(d=0.79) 검증
  - 소크라테스 문답법 3단계(확인/탐구/논박) 학술적 근거 확인
  - AI 적용 시 교육학적 리스크/한계 최소 3개 식별
  - 설계 개선 권고사항 포함
- **Post-processing**: `temp/scripts/cross_ref_pedagogy.py` — 교육학 이론 간 교차 참조 검증
- **Output**: `research/pedagogy-verification-report.md`
- **Review**: `@fact-checker`
- **Translation**: none

#### Step 4: (human) Research Findings Approval
- **Slash Command**: `/review-research`
- **Task**: Step 1-3 산출물 종합 리뷰. 사용자에게 요구사항 매니페스트, 기술 실현 가능성, 교육학 검증 결과 제시 및 승인 요청
- **Autopilot Default**: 품질 극대화 기본값으로 승인 + Decision Log 기록

---

### Phase: Planning (Steps 5-11)

#### Step 5: System Architecture Blueprint
- **Agent**: `@architect` (Sub-agent)
- **Pre-processing**: `temp/scripts/merge_architecture_inputs.py` — Step 1-3 산출물을 단일 아키텍처 입력으로 병합
- **Task**: 전체 시스템 아키텍처 설계. 17개 에이전트 호출 그래프, 이중 SOT 스키마, 파일 시스템 레이아웃, Phase 0 파이프라인 흐름, Phase 1-3 Skill 구조, Hook 배치, MCP 연동 포인트, 에러 복구 전략
- **Verification**:
  - 17개 에이전트 간 호출 관계 Mermaid 다이어그램 포함
  - 이중 SOT 스키마 완전 정의 (state.yaml + learner-state.yaml)
  - 파일 시스템 디렉터리 트리 (data/socratic/ 하위 전체)
  - Phase 0 데이터 파이프라인 흐름도 (6개 에이전트 + 병렬 구간)
  - Phase 1-3 Skill 상태 머신 다이어그램
  - Context Injection 패턴 매핑 (각 에이전트별)
  - 에이전트 간 데이터 계약 (input→output 매핑)
- **Output**: `planning/architecture-blueprint.md`
- **Review**: `@reviewer`
- **Translation**: `@translator`

#### Step 6: (team) Agent Persona Design
- **Team**: `step-6-agent-design` (3명)
  - `@agent-designer-alpha`: Phase 0 에이전트 6개 (`@content-analyzer`, `@topic-scout`, `@web-searcher`, `@deep-researcher`, `@content-curator`, `@curriculum-architect`)
  - `@agent-designer-beta`: Phase 1-2 에이전트 5개 (`@orchestrator`, `@learner-profiler`, `@knowledge-researcher`, `@path-optimizer`, `@session-planner`) + `@session-logger`
  - `@agent-designer-gamma`: Phase 3 에이전트 5개 (`@socratic-tutor`, `@misconception-detector`, `@metacog-coach`, `@concept-mapper`, `@progress-tracker`)
- **Checkpoints**: Dense (CP-1: 각 에이전트 역할 정의 완료, CP-2: 프롬프트 설계 완료, CP-3: 교차 검증 완료)
- **Task**: 각 에이전트의 페르소나, 시스템 프롬프트, 도구 접근 권한, 입출력 스키마, 트리거 조건, 서브에이전트 호출 패턴 설계
- **Verification**:
  - 17개 에이전트 전체의 페르소나 정의서 포함
  - 각 에이전트에 시스템 프롬프트 초안 포함
  - 도구 접근 권한 매트릭스 (에이전트 × 도구)
  - 서브에이전트 호출 관계 (@socratic-tutor → @misconception-detector, @metacog-coach)
  - 에이전트 간 교차 일관성 검증 (팀 합류 후)
- **Output**: `planning/agent-personas.md`
- **Review**: `@reviewer`
- **Translation**: `@translator`

#### Step 7: Data Architecture & JSON Schema Design
- **Agent**: `@schema-designer` (Sub-agent)
- **Pre-processing**: `temp/scripts/extract_field_inventory.py` — 설계 문서에서 JSON 필드 인벤토리 추출
- **Task**: 모든 JSON 스키마 정의. Phase 0 파이프라인 6개 산출물 스키마, Phase 1-3 상태 스키마, `learner-state.yaml` 스키마, 세션 로그 스키마, 개념 그래프 스키마. 스키마 체인(upstream→downstream) 정합성 보장
- **Verification**:
  - Phase 0 산출물 6개 스키마 완전 정의 (user-resource-scan, topic-scope, web-search-results, deep-research-results, curated-content, auto-curriculum)
  - learner-state.yaml 스키마 (knowledge_state, learning_style, current_session, path, history)
  - 세션 로그 스키마 (session_info, current_position, conversation_context, recovery_checkpoint)
  - 스키마 체인 정합성 — 모든 downstream 스키마가 upstream 필드를 참조 가능 (source: Step 5)
  - 필수 필드 / 선택 필드 / 기본값 명시
- **Post-processing**: `temp/scripts/validate_schema_chain.py` — upstream→downstream 필드 참조 무결성 검증
- **Output**: `planning/json-schemas.md`
- **Review**: `@reviewer`
- **Translation**: none (기술 스키마)

#### Step 8: Command Interface Design
- **Agent**: `@interface-designer` (Sub-agent)
- **Task**: 9개 슬래시 커맨드의 완전한 인터페이스 설계. 각 커맨드의 인자, 동작 흐름, 에이전트 호출 순서, 출력 형식, 에러 처리. UX 일관성 보장
- **Verification**:
  - 9개 커맨드 전체 인터페이스 정의 (/teach, /teach-from-file, /start-learning, /upload-content, /my-progress, /concept-map, /challenge, /end-session, /resume)
  - 각 커맨드의 인자 타입/기본값/필수 여부 명시
  - 에이전트 호출 시퀀스 다이어그램 (각 커맨드별)
  - 진행 상태 표시 형식 통일 (Phase 0 파이프라인 진행 바)
  - 에러 메시지 표준 형식 정의
  - 커맨드 간 상호작용 매핑 (/teach → /start-learning 자동 연결)
- **Output**: `planning/command-interfaces.md`
- **Review**: none
- **Translation**: `@translator`

#### Step 9: Quality Framework Design
- **Agent**: `@qa-designer` (Sub-agent)
- **Task**: 교육 품질 프레임워크 설계. 커리큘럼 생성 품질 지표 6개, 교육 효과 측정 지표 7개, 대형 강의 대비 우위 지표, 자동 품질 검증 Hook, 학습자 피드백 루프 설계
- **Verification**:
  - 커리큘럼 품질 지표 6개 (Source Diversity, Content Freshness, Completeness, Question Bank Quality, Generation Time, Expert Alignment) 정의 + 측정 방법
  - 교육 효과 지표 7개 (Mastery Rate, Retention, Socratic Depth, Metacog Score, Transfer Success, Session Completion, Misconception Fix) 정의 + 목표값
  - 자동 품질 검증 로직 (Hook 또는 Post-processing 스크립트)
  - 품질 데이터 수집·저장·리포팅 설계
- **Output**: `planning/quality-framework.md`
- **Review**: none
- **Translation**: none

#### Step 10: Architecture & Design Review
- **Agent**: `@reviewer` (Sub-agent)
- **Task**: Step 5-9 전체 산출물에 대한 종합 적대적 리뷰. 아키텍처 일관성, 에이전트 간 인터페이스 정합성, JSON 스키마 체인 무결성, 커맨드 UX 일관성, 교육학적 설계 무결성 교차 검증
- **Verification**:
  - 각 Planning 산출물(Step 5-9)에 대한 이슈 목록 포함
  - Critical 이슈 0건 (있으면 해결 후 재리뷰)
  - 에이전트 간 데이터 흐름 누락 없음 확인
  - 이중 SOT 일관성 검증
  - Review verdict (PASS/FAIL) 명시
- **Output**: `planning/design-review-report.md`
- **Review**: (자체 리뷰 — 이 단계가 리뷰 단계)
- **Translation**: none

#### Step 11: (human) Complete Design Approval
- **Slash Command**: `/approve-design`
- **Task**: Step 5-10 전체 설계 산출물 종합 리뷰. 사용자에게 아키텍처, 에이전트 설계, 스키마, 커맨드 인터페이스, 품질 프레임워크, 리뷰 결과 제시 및 승인 요청
- **Autopilot Default**: 품질 극대화 기본값으로 승인 + Decision Log 기록

---

### Phase: Implementation (Steps 12-21)

#### Step 12: Project Scaffolding & SOT Init
- **Agent**: `@builder` (Sub-agent)
- **Task**: 프로젝트 디렉터리 구조 생성, 이중 SOT 초기화, 빈 에이전트/커맨드/스킬 파일 스캐폴딩, `data/socratic/` 디렉터리 트리 생성, JSON 스키마 파일 배치
- **Verification**:
  - 디렉터리 구조가 Step 5 아키텍처 블루프린트와 일치
  - `state.yaml` 초기화 완료 (current_step, outputs, workflow_status)
  - `data/socratic/learner-state.yaml` 템플릿 생성
  - `.claude/agents/` 하위에 17개 에이전트 스캐폴딩 파일 존재
  - `.claude/commands/` 하위에 9개 커맨드 스캐폴딩 파일 존재
  - `data/socratic/schemas/` 하위에 JSON 스키마 파일 존재
  - 빈 파일이 아닌, 최소 구조(헤더 + placeholder)가 포함된 스캐폴딩
- **Output**: 프로젝트 스캐폴딩 (다수 파일)
- **Review**: none
- **Translation**: none

#### Step 13: (team) Sub-Agent Implementation
- **Team**: `step-13-agent-impl` (3명)
  - `@implementer-alpha`: Phase 0 에이전트 6개 구현 (`@content-analyzer`, `@topic-scout`, `@web-searcher`, `@deep-researcher`, `@content-curator`, `@curriculum-architect`)
  - `@implementer-beta`: Phase 1-2 에이전트 5개 + `@session-logger` 구현 (`@orchestrator`, `@learner-profiler`, `@knowledge-researcher`, `@path-optimizer`, `@session-planner`, `@session-logger`)
  - `@implementer-gamma`: Phase 3 에이전트 5개 구현 (`@socratic-tutor`, `@misconception-detector`, `@metacog-coach`, `@concept-mapper`, `@progress-tracker`)
- **Checkpoints**: Dense (CP-1: 에이전트 시스템 프롬프트 완성, CP-2: 도구 접근 + 입출력 스키마 구현, CP-3: 교차 테스트 완료)
- **Task**: Step 6 페르소나 설계와 Step 7 JSON 스키마를 기반으로 17개 에이전트 `.md` 파일을 완전하게 구현. 각 에이전트의 시스템 프롬프트, 도구 접근 권한, 입출력 형식, 에러 처리, 서브에이전트 호출 패턴 구현
- **Verification**:
  - 17개 `.claude/agents/*.md` 파일 모두 존재 + 100 bytes 이상
  - 각 에이전트의 시스템 프롬프트가 Step 6 페르소나와 일치
  - 도구 접근 권한이 Step 5 아키텍처와 일치
  - JSON 입출력 형식이 Step 7 스키마와 일치
  - @socratic-tutor의 3단계 문답법(확인/탐구/논박) 프롬프트가 포함됨
  - @misconception-detector의 심각도 분류(minor/moderate/critical) 로직 포함
  - @session-logger의 5초 스냅샷 + 복구 체크포인트 로직 포함
  - 교차 단계 추적성: [trace:step-6] 마커로 페르소나 설계 참조
- **Output**: 17개 에이전트 파일 (`.claude/agents/`)
- **Review**: `@reviewer`
- **Translation**: none (코드 파일)

#### Step 14: Phase 0 Pipeline Implementation
- **Agent**: `@pipeline-builder` (Sub-agent)
- **Pre-processing**: `temp/scripts/extract_phase0_spec.py` — Step 5 아키텍처에서 Phase 0 파이프라인 사양 추출
- **Task**: `/teach` 커맨드의 Phase 0 파이프라인 구현. 6개 에이전트 순차/병렬 호출 로직, User-Resource Priority Policy (Case A/B), 데이터 파이프라인 (scan→scope→search/research→curate→curriculum), 진행 상태 표시, 에러 복구
- **Verification**:
  - `/teach` 커맨드가 Phase 0 파이프라인을 트리거
  - User-Resource Priority Policy (Case A: PRIMARY, Case B: FALLBACK) 구현
  - @web-searcher와 @deep-researcher 병렬 실행 로직
  - 6개 JSON 산출물 파일이 순서대로 생성됨
  - 진행 상태 표시 ([1/7]~[7/7]) 구현
  - 에러 시 재시도 로직 포함
  - auto-curriculum.json 최종 산출물이 Step 7 스키마와 일치
- **Output**: Phase 0 파이프라인 코드 (`.claude/skills/socratic-tutor/`)
- **Review**: `@reviewer`
- **Translation**: none (코드)

#### Step 15: Phase 1-3 Skill Implementation
- **Agent**: `@skill-builder` (Sub-agent)
- **Pre-processing**: `temp/scripts/extract_phase13_spec.py` — Step 5 아키텍처에서 Phase 1-3 Skill 사양 추출
- **Task**: 대화형 튜터링 Skill 구현. Phase 1(콘텐츠 분석, 학습자 프로파일링, 외부 지식 보강), Phase 2(학습 경로 최적화, 세션 설계, 세션 로깅), Phase 3(소크라테스 튜터링, 오개념 감지, 메타인지 코칭, 개념 맵, 전이 챌린지, 진척도 추적) 전체 Skill YAML/MD
- **Verification**:
  - `.claude/skills/socratic-tutor/SKILL.md` 완전한 Skill 정의
  - Phase 1: @content-analyzer, @learner-profiler, @knowledge-researcher 호출 흐름
  - Phase 2: @path-optimizer, @session-planner, @session-logger 호출 흐름
  - Phase 3: @socratic-tutor 중심 + 서브에이전트 호출 흐름
  - learner-state.yaml 상태 관리 로직
  - 세션 시작/종료/복구 상태 머신 구현
  - `/start-learning`, `/end-session`, `/resume` 연동
- **Output**: Socratic Tutor Skill (`.claude/skills/socratic-tutor/`)
- **Review**: `@reviewer`
- **Translation**: none (코드)

#### Step 16: Slash Command Implementation
- **Agent**: `@command-builder` (Sub-agent)
- **Task**: 9개 슬래시 커맨드 구현. Step 8 인터페이스 설계 기반. 각 커맨드의 인자 파싱, 에이전트 호출 체인, 출력 포맷팅, 에러 핸들링
- **Verification**:
  - 9개 `.claude/commands/*.md` 파일 모두 존재 + 100 bytes 이상
  - 각 커맨드의 인자가 Step 8 인터페이스 설계와 일치
  - 에이전트 호출 순서가 Step 8 시퀀스 다이어그램과 일치
  - /teach → /start-learning 자동 연결 로직 포함
  - /resume 세션 복구 로직 포함 (active/ 폴더 스캔 + 체크포인트 복원)
  - 진행 상태 표시 형식이 Step 8과 일치
- **Output**: 9개 커맨드 파일 (`.claude/commands/`)
- **Review**: none
- **Translation**: none (코드)

#### Step 17: Hook & State Management
- **Agent**: `@infra-builder` (Sub-agent)
- **Task**: 세션 관리 인프라 구현. @session-logger 5초 스냅샷 메커니즘, 세션 복구 매니저, learner-state.yaml 갱신 로직, 마스터리 업데이트 알고리즘, 간격 반복 스케줄러, 품질 메트릭 수집
- **Verification**:
  - @session-logger 스냅샷 메커니즘 구현 (5초 간격)
  - 세션 복구 매니저 (active/ → completed/ 이동, interrupted/ 스캔)
  - learner-state.yaml 갱신 로직 (마스터리, 세션 이력)
  - 간격 반복 알고리즘 구현 (복습 스케줄링)
  - 품질 메트릭 수집/저장 로직
  - 디렉터리 구조: data/socratic/sessions/{active,completed,interrupted}/
- **Output**: 상태 관리 인프라 코드
- **Review**: none
- **Translation**: none (코드)

#### Step 18: Integration Testing
- **Agent**: `@tester` (Sub-agent)
- **Pre-processing**: `temp/scripts/generate_test_fixtures.py` — 테스트용 fixture 데이터 생성
- **Task**: 전체 시스템 통합 테스트. Phase 0 파이프라인 end-to-end 테스트 (키워드 → auto-curriculum.json), Phase 1-3 Skill 시뮬레이션 테스트, 에이전트 간 데이터 흐름 테스트, 세션 복구 테스트, 이중 SOT 일관성 테스트
- **Verification**:
  - Phase 0: /teach 키워드 → auto-curriculum.json 생성 성공
  - Phase 1-3: /start-learning → 소크라테스 대화 시작 성공
  - JSON 스키마 적합성: 모든 산출물이 Step 7 스키마와 일치
  - 세션 복구: /resume로 중단된 세션 재개 성공
  - 이중 SOT: state.yaml + learner-state.yaml 동시 갱신 일관성
  - User-Resource Priority: Case A / Case B 분기 동작 확인
  - 에러 복구: 에이전트 실패 시 재시도 동작 확인
- **Output**: `testing/integration-test-report.md`
- **Review**: none
- **Translation**: none

#### Step 19: Final System Review
- **Agent**: `@reviewer` (Sub-agent)
- **Task**: 전체 시스템 최종 적대적 리뷰. 코드 품질, 아키텍처 일관성, 교육학적 무결성, 보안 취약점, 성능 병목, 사용자 경험 종합 검증
- **Verification**:
  - 전체 코드/산출물에 대한 이슈 목록 포함
  - Critical 이슈 0건
  - 17개 에이전트 → 9개 커맨드 → Phase 0 파이프라인 → Phase 1-3 Skill 전체 연결 검증
  - 이중 SOT 무결성 최종 확인
  - Review verdict (PASS/FAIL) 명시
- **Output**: `review/final-system-review.md`
- **Review**: (자체 리뷰)
- **Translation**: none

#### Step 20: (human) System Acceptance
- **Slash Command**: `/accept-system`
- **Task**: 최종 시스템 수락 검사. 사용자에게 전체 시스템 데모(Phase 0 파이프라인 실행, Phase 1-3 Skill 시연), 테스트 결과, 리뷰 결과 제시 및 최종 승인 요청
- **Autopilot Default**: 품질 극대화 기본값으로 승인 + Decision Log 기록

#### Step 21: User Documentation
- **Agent**: `@documenter` (Sub-agent)
- **Task**: 사용자 매뉴얼 작성. 설치/설정 가이드, 9개 슬래시 커맨드 사용법, Phase 0 파이프라인 활용, Phase 1-3 학습 세션 가이드, FAQ, 트러블슈팅
- **Verification**:
  - 9개 커맨드 사용법 + 예시 포함
  - 설치/설정 순서 명시 (MCP 서버 설정 포함)
  - Phase 0 파이프라인 활용 가이드 (Case A/B)
  - Phase 1-3 학습 세션 가이드 (시작 → 대화 → 종료 → 복구)
  - FAQ 최소 10개
  - 트러블슈팅 가이드 최소 5개 시나리오
- **Output**: `SOCRATIC-TUTOR-USER-MANUAL.md`
- **Review**: `@reviewer`
- **Translation**: `@translator`

---

## Step Execution Loop

**각 단계는 반드시 아래 루프를 따른다:**

```
┌─────────────────────────────────────────────────────────┐
│  1. Read SOT current_step                                │
│  2. L0 Anti-Skip: previous step output exists + ≥ 100B  │
│  3. Pre-processing (if defined): run Python script       │
│  4. Dispatch agent (Sub-agent or Team)                   │
│  5. Post-processing (if defined): run validation script  │
│  6. L1 Verification: self-verify against criteria        │
│     └─ FAIL → Abductive Diagnosis → retry (max 10/15)   │
│  7. L1.5 pACS: Pre-mortem + F/C/L → RED < 50 = rework  │
│     └─ RED → Abductive Diagnosis → rework + re-score    │
│  8. L2 Review (if applicable): @reviewer/@fact-checker   │
│     └─ FAIL → Abductive Diagnosis → rework + re-review  │
│  9. Translation (if applicable): @translator             │
│ 10. SOT update: outputs + current_step +1                │
└─────────────────────────────────────────────────────────┘
```

**Quality Gate Protocol (4 Layers):**

| Layer | Name | Type | Trigger | Failure Action |
|-------|------|------|---------|----------------|
| L0 | Anti-Skip Guard | Deterministic | Every step | Block — output missing |
| L1 | Verification Gate | Semantic | Every step with `Verification` | Retry with diagnosis (max 10, ULW: 15) |
| L1.5 | pACS Self-Rating | Confidence | After L1 PASS | RED < 50: rework; YELLOW 50-69: log + proceed |
| L2 | Adversarial Review | External | Steps with `Review:` field | FAIL: rework; Delta ≥ 15: recalibrate |

**Retry Budget:**
- Verification FAIL: max 10 retries (ULW: 15)
- pACS RED: max 10 retries (ULW: 15)
- Review FAIL: max 10 retries (ULW: 15)
- Check: `python3 .claude/hooks/scripts/validate_retry_budget.py --step N --gate {verification|pacs|review} --project-dir . --check-and-increment`

**Abductive Diagnosis (on any quality gate FAIL):**
1. `python3 .claude/hooks/scripts/diagnose_context.py --step N --gate {gate} --project-dir .`
2. Check Fast-Path: FP1/FP2 → immediate retry, FP3 → escalate
3. LLM Diagnosis if no fast-path
4. `python3 .claude/hooks/scripts/validate_diagnosis.py --step N --gate {gate} --project-dir .`
5. Execute fix based on selected hypothesis

**Translation Quality Gate (Steps 5, 6, 8, 21 only — after all other gates PASS):**

```
┌──────────────────────────────────────────────────────────┐
│  Pre-condition: Review PASS (if step has Review field)    │
│  OR: Verification PASS (if no Review field)              │
│                                                           │
│  1. Invoke @translator sub-agent:                        │
│     - Source: English original from SOT outputs.step-N   │
│     - Glossary: translations/glossary.yaml               │
│     - Output: {source-path}.ko.md                        │
│                                                           │
│  2. Translation pACS: Ft/Ct/Nt scored                    │
│     → pacs-logs/step-N-translation-pacs.md               │
│                                                           │
│  3. P1 Validation:                                       │
│     python3 .claude/hooks/scripts/validate_translation.py │
│       --step N --project-dir . --check-pacs              │
│       [--check-sequence if Review step]                   │
│                                                           │
│  4. SOT: outputs.step-N-ko = "{path}.ko.md"             │
│                                                           │
│  5. Trace markers: [trace:step-N] preserved verbatim     │
│                                                           │
│  Failure → Fallback F11 (references/fallback-matrix.md)  │
└──────────────────────────────────────────────────────────┘
```

**Translation-specific SOT key pattern**: `step-N-ko` keys are automatically skipped by Anti-Skip Guard (the `.isdigit()` guard in `validate_step_output()` ignores non-numeric suffixes). No Hook code changes required.

---

## Agent Team Protocol (Steps 6, 13)

```
1. TeamCreate("step-{N}-{name}")
2. SOT active_team init:
   active_team:
     name: "step-{N}-{name}"
     status: "partial"
     tasks_completed: []
     tasks_pending: ["task-alpha", "task-beta", "task-gamma"]
     completed_summaries: {}
3. TaskCreate × 3 (one per teammate)
4. Task tool → spawn 3 teammates (general-purpose subagent_type)
5. TaskUpdate → assign owners
6. Dense Checkpoints:
   CP-1: Core deliverable drafts complete → cross-check
   CP-2: Full implementation complete → integration check
   CP-3: Cross-consistency review → final validation
7. Join Phase: Team Lead aggregates + cross-validates
8. Quality Gates: L1 Verification + L1.5 pACS + L2 Review
9. SOT update: active_team.status → "all_completed"
10. TeamDelete → completed_teams
```

**Teammate Rules:**
- Each teammate performs L1 self-verification before reporting
- Each teammate performs L1.5 pACS self-scoring (included in report message)
- Team Lead performs L2 aggregate verification
- Teammates NEVER write to SOT directly — Team Lead only
- On L2 FAIL: SendMessage with specific feedback → teammate re-executes

---

## Autopilot Integration

| Checkpoint | Autopilot Behavior |
|-----------|-------------------|
| `(human)` steps (4, 11, 20) | Full output generated → auto-approve with quality-maximizing defaults → Decision Log |
| AskUserQuestion | Auto-select best quality option → Decision Log |
| `(hook)` exit code 2 | No change — block respected, feedback forwarded, rework |

**Decision Log Location**: `autopilot-logs/step-N-decision.md`

---

## Fallback Protocol

Reference: `references/fallback-matrix.md`

| Failure | Tier 1 | Tier 2 | Tier 3 |
|---------|--------|--------|--------|
| Sub-agent error | Retry + feedback | Model upgrade | Escalate |
| Teammate failure | SendMessage feedback | Replace teammate | Dissolve team + escalate |
| Verification FAIL | Diagnosis → retry | Alt approach | Escalate (budget exhausted) |
| pACS RED | Weak dim fix | Full rework | Escalate |
| Review FAIL | Address issues | Rework + re-review | Escalate |
| Context overflow | Auto-restore | Step split | Manual restore |
| SOT corruption | Restore last good | Re-init from last step | Escalate |

---

## SOT Management Protocol

### Builder SOT: `.claude/state.yaml`

```yaml
workflow:
  name: "Socratic AI Tutor Builder"
  current_step: 1
  workflow_status: "pending"
  outputs:
    step-1: "research/requirements-manifest.md"
    step-2: "research/tech-feasibility-report.md"
    # ...
  autopilot:
    enabled: true
    decision_log_dir: "autopilot-logs/"
    auto_approved_steps: []
  pacs:
    current_step_score: null
    dimensions:
      F: null
      C: null
      L: null
    weak_dimension: null
    pre_mortem_flag: null
    history: {}
  active_team: null
  completed_teams: []
  parent_genome:
    source: "AgenticWorkflow"
    version: "2026-02-27"
    inherited_dna:
      - "absolute-criteria"
      - "sot-pattern"
      - "3-phase-structure"
      - "4-layer-qa"
      - "safety-hooks"
      - "adversarial-review"
      - "decision-log"
      - "context-preservation"
```

### Target SOT: `data/socratic/learner-state.yaml`

```yaml
learner_id: null
knowledge_state: {}
learning_style: null
current_session: null
path: null
history: []
```

**Write Permissions:**
- `state.yaml` → Orchestrator (this skill) only
- `learner-state.yaml` → Target `@orchestrator` agent only
- All other agents → Read-only + produce output files

---

## Reference Documents

- Execution Protocol (detailed 21-step table): `references/execution-protocol.md`
- Agent Specifications: `references/agent-specs.yaml`
- Fallback Matrix: `references/fallback-matrix.md`
- PRD: `coding-resource/PRD.md`
- Design Document: `coding-resource/socratic-ai-tutor-workflow.md`

## NEVER DO

- `current_step`을 2 이상 한 번에 증가 금지
- 산출물 없이 다음 단계 진행 금지
- "빌드니까 간략하게" 금지 — 절대 기준 1 위반
- 에이전트 수를 13개 미만으로 축소 금지 — PRD 설계 의도 위반
- 소크라테스 문답법 3단계를 2단계로 축소 금지
- Phase 0 파이프라인에서 사용자 확인 질문 추가 금지 — 완전 자동화 원칙 위반
- `(hook)` exit code 2 차단 무시 금지
- `(team)` 단계에서 Teammate가 SOT를 직접 수정 금지
- Review FAIL 상태에서 Translation 실행 금지
- 품질 게이트 FAIL 재시도 시 진단 없이 동일 접근법으로 재시도 금지
