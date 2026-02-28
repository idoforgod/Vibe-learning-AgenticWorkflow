# Socratic AI Tutor Orchestrator

대학 대형 강의의 한계를 극복하는 완전 자율형 개인화 교육 AI 시스템. 소크라테스 문답법을 핵심으로 **13개 전문 에이전트**가 협업하여 압도적 효율의 1:1 맞춤 교육을 제공한다.

**핵심 혁신: Zero-to-Curriculum** - 키워드 하나만 입력하면 Pre-trained 지식 + 실시간 검색 + 심층 리서치를 결합하여 완전한 교수 커리큘럼을 자동 생성한다.

## Overview

- **Input**: 
  - **키워드/주제** (교수자 또는 학생이 `/teach [키워드]`로 입력)
  - 교수자 업로드 자료 / MOOC·논문 등 공개 콘텐츠 / 학습자 실시간 응답
- **Output**: 
  - **자동 생성 교수 커리큘럼** (모듈/레슨/소크라테스 질문 포함)
  - 실시간 소크라테스식 튜터링 세션
  - 학습 진척도 리포트
  - 개인화 학습 경로 + 적응형 평가
  - 메타인지 훈련 피드백
  - 개념 연결 맵 (시각화)
  - 전이 학습 챌린지
- **Frequency**: On-demand (학습자 접속 시 실시간)
- **Human-in-the-Loop**: 없음 (완전 자율형)

---

## ★ 완전 자동화 실행 정책 (CRITICAL)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       🤖 완전 자동화 실행 원칙                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ✅ 이 시스템의 모든 준비 단계(Phase 0)는 사용자 확인 없이 자동 실행됩니다. │
│                                                                         │
│  ❌ 각 단계에서 사용자에게 확인/허락을 묻지 않습니다.                      │
│  ❌ "다음 단계로 진행할까요?" 같은 질문을 하지 않습니다.                   │
│  ❌ 중간 결과를 보여주고 승인을 기다리지 않습니다.                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 자동화 적용 범위

| 명령어 | 자동화 수준 | 사용자 개입 지점 |
|--------|------------|------------------|
| `/teach` | **완전 자동** | 키워드 입력 → 최종 결과만 출력 |
| `/socratic start` | **자동** | 세션 시작 → 소크라테스 대화만 |
| `/resume` | **자동** | 세션 복구 선택 후 자동 재개 |

### 에이전트 자동 실행 흐름

```
/teach [키워드] 입력
       │
       │  ※ 아래 모든 단계는 사용자 확인 없이 연속 자동 실행
       │
       ├──▶ @content-analyzer ───┐
       │                          │
       ├──▶ @topic-scout ────────┤
       │                          │
       ├──▶ @web-searcher ───────┼──▶ [병렬 가능 구간]
       │                          │
       ├──▶ @deep-researcher ────┤
       │                          │
       ├──▶ @content-curator ────┘
       │
       ├──▶ @curriculum-architect
       │
       └──▶ 최종 결과 출력 (여기서만 사용자에게 상세 정보 제공)
```

### 진행 상태 표시 규칙

```
진행 중 표시 (간략히):
┌────────────────────────────────────────┐
│ 📁 [1/7] 사용자 자료 스캔 중...        │
│ 🔍 [2/7] 주제 구조화 중...             │
│ 🌐 [3/7] 웹 검색 중...                 │
│ 📖 [4/7] 심층 리서치 중...             │
│ ✨ [5/7] 콘텐츠 선별 중...             │
│ 🏗️ [6/7] 커리큘럼 설계 중...           │
│ ✅ 완료!                               │
└────────────────────────────────────────┘

완료 후 표시 (상세히):
┌────────────────────────────────────────┐
│ 📚 커리큘럼 자동 생성 완료!             │
│                                        │
│ • 모듈: 5개                            │
│ • 레슨: 18개                           │
│ • 예상 학습 시간: 14시간                │
│ • 소크라테스 질문: 54개                 │
│                                        │
│ 학습을 시작하려면: /socratic start     │
└────────────────────────────────────────┘
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     🎭 @orchestrator (총괄 지휘)                     │
│         학습자 상태 모니터링 / 에이전트 호출 조율 / 세션 관리          │
└─────────────────────────────────────────────────────────────────────┘
                                    │
     ┌──────────────────────────────┼───────────────────────┬───────────────────────┐
     ▼                              ▼                       ▼                       ▼
┌──────────────┐           ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  CURRICULUM  │           │   RESEARCH   │       │   PLANNING   │       │IMPLEMENTATION│
│  GENESIS     │           │   Phase      │       │   Phase      │       │   Phase      │
│  Phase 0     │           │              │       │              │       │              │
└──────────────┘           └──────────────┘       └──────────────┘       └──────────────┘
       │                          │                       │                       │
  ┌────┼────┐              ┌──────┴──────┐         ┌──────┴──────┐         ┌──────┴──────┐
  ▼    ▼    ▼              ▼             ▼         ▼             ▼         ▼             ▼
@topic @deep  @curriculum @content   @learner   @path       @session   @socratic   @progress
-scout -researcher -architect -analyzer -profiler -optimizer  -planner   -tutor      -tracker
  │         │                                         │                     │
  ▼         ▼                                         ▼       ┌─────────────┼─────────────┐
@web    @content                                  @session    ▼             ▼             ▼
-searcher -curator                                -logger  @misconception  @metacog     @concept
                                                  (BG)     -detector       -coach       -mapper
                                                               │
                                                               ▼
                                                        @knowledge
                                                        -researcher

┌─────────────────────────────────────────────────────────────────────┐
│                  📝 @session-logger (백그라운드 상주)                 │
│    5초마다 자동 스냅샷 / 세션 복구 / 학습 재개 지원 / /resume 연동     │
└─────────────────────────────────────────────────────────────────────┘
```

### 신규 Phase 0 에이전트 (Curriculum Genesis)

| Agent | 역할 | 핵심 기능 |
|-------|------|----------|
| `@content-analyzer` | 사용자 자료 분석기 | **user-resource/ 폴더 자료 최우선 분석** |
| `@topic-scout` | 주제 정찰병 | 키워드에서 학습 범위/하위주제 도출 (user-resource 기반) |
| `@web-searcher` | 웹 검색기 | 실시간 웹 검색으로 최신 자료 수집 (보완용) |
| `@deep-researcher` | 심층 연구원 | Deep Research로 학술자료/전문지식 탐색 (보완용) |
| `@content-curator` | 콘텐츠 큐레이터 | 수집 자료 품질 평가 및 선별 (user-resource 최우선) |
| `@curriculum-architect` | 커리큘럼 설계자 | 완전한 교수 커리큘럼 자동 생성 |

---

## Phase 0: Curriculum Genesis (신규)

**키워드 하나로 완전한 교수 커리큘럼 자동 생성.**
사용자(교수/학생)가 주제만 입력하면, AI가 **User-Resource(사용자 자료) + Pre-trained 지식 + 실시간 검색 + 심층 리서치**를 결합하여 학습 콘텐츠를 수집하고 체계적인 커리큘럼을 설계한다.

### 0.0 사용자 자료 스캔 (User-Resource Scan) - 최우선
- **Location**: `user-resource/` 폴더
- **Trigger**: `/teach [키워드]` 명령 실행 시 **가장 먼저** 실행
- **Task**:
  - `user-resource/` 폴더 존재 여부 확인
  - 폴더 내 모든 파일 스캔 (PDF, DOCX, PPTX, MD, TXT 등)
  - 키워드와 관련된 자료 식별
  - 파일 메타데이터 및 내용 요약 추출
  - 관련 자료를 **최우선 콘텐츠 소스**로 태깅
- **Output**: `user-resource-scan.json`

```json
{
  "scan_timestamp": "2025-01-14T10:00:00Z",
  "folder_path": "user-resource/",
  "files_found": 5,
  "relevant_files": [
    {
      "file_name": "blockchain_lecture_notes.pdf",
      "file_type": "pdf",
      "file_size": "2.3MB",
      "relevance_to_keyword": 0.95,
      "extracted_topics": ["합의 알고리즘", "스마트 컨트랙트", "DeFi"],
      "priority": "primary",
      "analysis_status": "pending"
    },
    {
      "file_name": "crypto_basics.docx",
      "file_type": "docx",
      "relevance_to_keyword": 0.82,
      "extracted_topics": ["암호학 기초", "해시 함수"],
      "priority": "primary",
      "analysis_status": "pending"
    }
  ],
  "non_relevant_files": ["meeting_notes.txt"],
  "total_relevant_content_size": "4.5MB"
}
```

**중요: User-Resource 우선순위 정책**

### Case A: User-Resource가 있는 경우 (기본 정책)
```
콘텐츠 소스 우선순위:
1. user-resource/ 폴더 자료 (PRIMARY - 최우선)
2. Pre-trained 지식 (SUPPLEMENTARY)
3. 실시간 웹 검색 (SUPPLEMENTARY - 갭 보완용)
4. 심층 리서치 (SUPPLEMENTARY - 갭 보완용)

정책:
- user-resource 자료는 품질 필터 스킵, 품질 점수 1.0 자동 부여
- user-resource의 구조/순서가 커리큘럼의 기본 프레임
- 외부 자료는 user-resource의 '갭을 보완'하는 역할
- 교수자의 의도를 최대한 존중
```

### Case B: User-Resource가 없는 경우 (FALLBACK 정책)
```
콘텐츠 소스 우선순위 (모두 PRIMARY - 동등):
1. Pre-trained 지식 (PRIMARY)
2. 실시간 웹 검색 (PRIMARY)
3. 심층 리서치 (PRIMARY)

FALLBACK 조건:
- user-resource/ 폴더가 존재하지 않음
- 폴더는 존재하나 지원 파일 형식이 없음
- 파일은 있으나 키워드와 관련성이 30% 미만

정책:
- 모든 외부 소스에 동등한 품질 기준 적용 (0.6 이상만)
- Foundation → Synthesis까지 균형 있는 자료 수집
- 소스 다양성 확보 (단일 출처 의존 방지)
- Pre-trained 지식의 정확성을 외부 자료로 검증
- 기존의 외부 자료 수집 + 심층 리서치 방식 유지
```

### 왜 이 정책인가?
```
User-Resource가 있을 때:
- 사용자가 직접 제공한 자료는 해당 학습 맥락에 가장 적합
- 교수자의 강의 자료, 교재, 노트는 커리큘럼의 핵심 기반
- 외부 자료는 user-resource를 '보완'하는 역할

User-Resource가 없을 때:
- 최대한 다양한 외부 소스로 포괄적 커리큘럼 구성
- 품질 필터로 신뢰할 수 있는 자료만 선별
- 소스 간 상호 검증으로 정확성 확보
```

### 0.1 주제 정찰 (Topic Scouting)
- **Agent**: `@topic-scout`
- **Trigger**: `/teach [키워드]` 명령 입력 시
- **Task**:
  - 키워드에서 학습 가능한 범위 파악
  - Pre-trained 지식으로 주제 구조 초안 생성
  - 핵심 하위 주제(Sub-topics) 도출
  - 선수 지식 및 관련 분야 매핑
  - 학습 난이도 스펙트럼 추정
- **Output**: `topic-scope.json`

```json
{
  "keyword": "블록체인",
  "scope_definition": "분산 원장 기술의 원리, 응용, 한계",
  "sub_topics": [
    {"name": "암호학 기초", "depth": "foundation", "estimated_hours": 2},
    {"name": "합의 알고리즘", "depth": "core", "estimated_hours": 4},
    {"name": "스마트 컨트랙트", "depth": "application", "estimated_hours": 3},
    {"name": "DeFi와 실제 응용", "depth": "advanced", "estimated_hours": 3},
    {"name": "한계와 미래", "depth": "synthesis", "estimated_hours": 2}
  ],
  "prerequisites": ["기초 프로그래밍", "네트워크 개념"],
  "related_fields": ["금융", "보안", "분산시스템"],
  "difficulty_range": {"min": 2, "max": 5},
  "total_estimated_hours": 14
}
```

### 0.2 실시간 웹 검색 (Web Search)
- **Agent**: `@web-searcher`
- **Trigger**: Topic Scouting 완료 후 자동 실행
- **Task**:
  - 각 하위 주제별 최신 자료 검색
  - 뉴스, 블로그, 튜토리얼, 공식 문서 수집
  - 최신 트렌드 및 업데이트 사항 파악
  - 실제 사례(Case Study) 검색
- **Output**: `web-search-results.json`

```json
{
  "sub_topic": "합의 알고리즘",
  "search_queries": [
    "consensus algorithm blockchain 2025",
    "PoS vs PoW latest comparison",
    "Ethereum merge impact analysis"
  ],
  "results": [
    {
      "title": "Understanding Proof of Stake in 2025",
      "source": "ethereum.org",
      "type": "official_doc",
      "relevance_score": 0.95,
      "recency": "2025-01",
      "url": "..."
    },
    {
      "title": "Consensus Mechanisms Compared",
      "source": "MIT Technology Review",
      "type": "analysis",
      "relevance_score": 0.88,
      "recency": "2024-12",
      "url": "..."
    }
  ],
  "trending_topics": ["Proof of Stake 2.0", "Layer 2 Consensus"],
  "recent_developments": ["이더리움 샤딩 업데이트", "솔라나 컨센서스 개선"]
}
```

### 0.3 심층 리서치 (Deep Research)
- **Agent**: `@deep-researcher`
- **Trigger**: Web Search와 병렬 실행
- **Task**:
  - 학술 논문 검색 (arXiv, Google Scholar, IEEE)
  - 전문 서적 및 교재 내용 탐색
  - 대학 강의자료/MOOC 콘텐츠 조사
  - 전문가 견해 및 논쟁점 파악
  - 역사적 맥락 및 발전 과정 정리
- **Output**: `deep-research-results.json`

```json
{
  "sub_topic": "합의 알고리즘",
  "academic_sources": [
    {
      "title": "A Survey on Consensus Mechanisms for Blockchain",
      "authors": ["Zhang et al."],
      "source": "IEEE Access",
      "year": 2024,
      "citations": 156,
      "key_insights": [
        "BFT 기반 합의의 확장성 한계",
        "하이브리드 합의 메커니즘의 부상"
      ]
    }
  ],
  "textbook_references": [
    {
      "book": "Mastering Blockchain, 4th Edition",
      "chapter": "Ch.5 Consensus Algorithms",
      "key_concepts": ["Nakamoto Consensus", "PBFT", "Tendermint"]
    }
  ],
  "mooc_resources": [
    {
      "platform": "Coursera",
      "course": "Blockchain Specialization - Princeton",
      "relevant_module": "Week 3: Consensus Protocols"
    }
  ],
  "expert_debates": [
    {
      "topic": "PoS의 중앙화 우려",
      "perspectives": {
        "pro": "에너지 효율성과 환경",
        "con": "부의 집중으로 인한 검열 위험"
      }
    }
  ],
  "historical_context": "2008 비트코인 → 2015 이더리움 → 2022 The Merge"
}
```

### 0.4 콘텐츠 큐레이션 (Content Curation)
- **Agent**: `@content-curator`
- **Trigger**: 검색 + 리서치 완료 후
- **Task**:
  - 수집된 모든 자료 품질 평가
  - 중복 제거 및 상충 정보 해결
  - 신뢰도/최신성/교육적 가치 기준 선별
  - 난이도별 자료 분류
  - 소크라테스 질문 생성에 적합한 핵심 자료 선정
- **Output**: `curated-content.json`

```json
{
  "keyword": "블록체인",
  "curation_summary": {
    "total_collected": 87,
    "after_quality_filter": 34,
    "final_selected": 22
  },
  "curated_materials": {
    "foundation": [
      {
        "id": "mat_001",
        "title": "암호학 해시 함수 기초",
        "source": "Khan Academy + Pre-trained",
        "type": "concept_explanation",
        "quality_score": 0.92,
        "socratic_potential": "high"
      }
    ],
    "core": [...],
    "application": [...],
    "advanced": [...]
  },
  "knowledge_gaps_identified": [
    "한국어 고급 자료 부족 → Pre-trained 지식으로 보완",
    "최신 L2 합의 메커니즘 → 웹 검색으로 보완"
  ],
  "conflict_resolutions": [
    {
      "topic": "PoS 에너지 효율",
      "conflict": "수치 불일치 (99% vs 99.95%)",
      "resolution": "이더리움 공식 발표 기준 99.95% 채택"
    }
  ]
}
```

### 0.5 커리큘럼 자동 설계 (Curriculum Architecture)
- **Agent**: `@curriculum-architect`
- **Trigger**: 콘텐츠 큐레이션 완료 후
- **Task**:
  - 학습 목표(Learning Objectives) 체계 수립
  - 모듈/레슨 구조 설계
  - 개념 의존성 그래프 구축
  - 각 레슨별 소크라테스 질문 세트 배치
  - 평가 지점 및 전이 챌린지 배치
  - 예상 학습 시간 및 난이도 곡선 설계
- **Output**: `auto-curriculum.json`

```json
{
  "curriculum_id": "CURR_blockchain_001",
  "title": "블록체인 완전 정복",
  "generated_from_keyword": "블록체인",
  "generation_method": {
    "pretrained_knowledge": "40%",
    "web_search": "25%",
    "deep_research": "35%"
  },
  "learning_objectives": [
    "LO1: 블록체인의 핵심 원리를 설명할 수 있다",
    "LO2: 다양한 합의 메커니즘의 장단점을 비교 분석할 수 있다",
    "LO3: 스마트 컨트랙트의 작동 원리를 이해하고 응용 사례를 설계할 수 있다",
    "LO4: 블록체인 기술의 한계를 인식하고 적절한 적용 영역을 판단할 수 있다"
  ],
  "structure": {
    "total_modules": 5,
    "total_lessons": 18,
    "total_hours": 14,
    "modules": [
      {
        "module_id": "M1",
        "title": "기초: 왜 블록체인인가?",
        "duration": "2시간",
        "lessons": [
          {
            "lesson_id": "L1.1",
            "title": "신뢰 문제와 중앙화의 한계",
            "duration": "30min",
            "content_sources": ["mat_001", "mat_002"],
            "concepts": ["double_spending", "trusted_third_party"],
            "socratic_questions": {
              "level_1": ["은행이 없다면 어떻게 거래를 신뢰할 수 있을까요?"],
              "level_2": ["중앙 기관의 '신뢰'는 어디서 오는 걸까요?"],
              "level_3": ["은행도 실패할 수 있다면, '신뢰'의 진짜 의미는?"]
            },
            "learning_check": {
              "type": "socratic_dialogue",
              "mastery_threshold": 0.7
            }
          },
          {
            "lesson_id": "L1.2",
            "title": "해시 함수와 암호학적 연결",
            "duration": "40min",
            "concepts": ["hash_function", "immutability"],
            "socratic_questions": {...},
            "hands_on": "간단한 해시 실험"
          },
          {
            "lesson_id": "L1.3",
            "title": "블록의 구조와 체인 형성",
            "duration": "50min",
            "concepts": ["block_structure", "chain_linking"],
            "transfer_challenge": {
              "type": "same_field",
              "prompt": "Git의 커밋 히스토리와 블록체인의 유사점은?"
            }
          }
        ]
      },
      {
        "module_id": "M2",
        "title": "핵심: 합의 알고리즘",
        "duration": "4시간",
        "lessons": [
          {
            "lesson_id": "L2.1",
            "title": "비잔틴 장군 문제",
            "concepts": ["byzantine_fault", "consensus"],
            "socratic_questions": {
              "level_3": ["모든 장군이 '정직'하다고 가정할 수 없다면, 어떻게 합의에 도달할 수 있을까요?"]
            }
          },
          {
            "lesson_id": "L2.2",
            "title": "작업증명(PoW)의 천재성과 대가",
            "concepts": ["proof_of_work", "mining", "energy_cost"],
            "expert_debate_integration": true
          },
          {
            "lesson_id": "L2.3",
            "title": "지분증명(PoS)과 The Merge",
            "content_freshness": "2025-01 웹검색 반영",
            "concepts": ["proof_of_stake", "validator", "slashing"]
          },
          {
            "lesson_id": "L2.4",
            "title": "합의 메커니즘 비교 분석",
            "type": "synthesis",
            "transfer_challenge": {
              "type": "far_transfer",
              "prompt": "민주주의 투표 시스템과 PoS의 유사점과 차이점은?"
            }
          }
        ]
      },
      {
        "module_id": "M3",
        "title": "응용: 스마트 컨트랙트",
        "duration": "3시간",
        "lessons": [...]
      },
      {
        "module_id": "M4",
        "title": "심화: DeFi와 실제 세계",
        "duration": "3시간",
        "lessons": [...]
      },
      {
        "module_id": "M5",
        "title": "종합: 한계, 비판, 미래",
        "duration": "2시간",
        "lessons": [
          {
            "lesson_id": "L5.1",
            "title": "블록체인이 해결하지 못하는 문제들",
            "socratic_questions": {
              "level_3": ["블록체인이 '만능'이 아니라면, 언제 사용하고 언제 사용하지 말아야 할까요?"]
            }
          },
          {
            "lesson_id": "L5.2",
            "title": "미래 전망과 당신의 판단",
            "type": "capstone",
            "transfer_challenge": {
              "type": "far_transfer",
              "prompt": "블록체인의 '탈중앙화' 철학을 교육 시스템에 적용한다면?"
            }
          }
        ]
      }
    ]
  },
  "concept_dependency_graph": {
    "nodes": ["double_spending", "hash_function", "block_structure", ...],
    "edges": [
      {"from": "hash_function", "to": "block_structure"},
      {"from": "byzantine_fault", "to": "proof_of_work"},
      ...
    ]
  },
  "assessment_points": [
    {"after": "M1", "type": "concept_check", "socratic_depth": 2},
    {"after": "M2", "type": "synthesis_challenge", "socratic_depth": 3},
    {"after": "M4", "type": "application_project"},
    {"after": "M5", "type": "capstone_debate"}
  ],
  "adaptive_paths": {
    "accelerated": "선수지식 보유 시 M1 스킵 가능",
    "foundation_support": "암호학 기초 부족 시 보충 모듈 삽입",
    "deep_dive_options": ["PoS 심화", "스마트컨트랙트 코딩", "DeFi 실전"]
  }
}
```

### 0.6 커리큘럼 생성 완료 알림
- **Agent**: `@orchestrator`
- **Task**:
  - 생성된 커리큘럼 요약 제시
  - 예상 학습 시간 및 구조 안내
  - 학습 시작 여부 확인
  - 커리큘럼 수정 요청 수렴 (선택)
- **Output**: 사용자에게 직접 응답

```
📚 커리큘럼 자동 생성 완료!

키워드: "블록체인"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 생성 소스:
   • Pre-trained 지식: 40%
   • 실시간 웹 검색: 25% (2025년 1월 최신)
   • 심층 리서치: 35% (학술논문 12편, MOOC 3개)

📖 커리큘럼 구조:
   • 5개 모듈 / 18개 레슨
   • 예상 학습 시간: 14시간
   • 난이도: 초급 → 고급 점진적 상승

🎯 학습 목표:
   1. 블록체인 핵심 원리 설명
   2. 합의 메커니즘 비교 분석
   3. 스마트 컨트랙트 응용 설계
   4. 적절한 적용 영역 판단

🔥 특별 포함:
   • 소크라테스 질문 54개 (레슨당 3개)
   • 전이 챌린지 6개 (같은 분야 + 다른 분야)
   • 전문가 논쟁 통합 (PoS 중앙화 이슈 등)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
학습을 시작할까요? /start-learning 입력
커리큘럼 수정이 필요하면 말씀해주세요.
```

---

## Phase 1: Research

학습 콘텐츠 분석 및 학습자 진단.

### 1.1 콘텐츠 분석
- **Agent**: `@content-analyzer`
- **Trigger**: 새 학습자료 업로드 시 자동 실행
- **Task**: 
  - 핵심 개념(Key Concepts) 추출
  - 학습 목표(Learning Objectives) 정의
  - 선수 지식(Prerequisites) 매핑
  - 난이도 레벨 태깅
  - 소크라테스 질문 뱅크 생성 (개념당 3단계 질문)
- **Output**: `content-analysis.json`

```json
{
  "content_id": "uuid",
  "title": "업로드 자료명",
  "key_concepts": [
    {
      "id": "concept_001",
      "name": "개념명",
      "definition": "정의",
      "prerequisites": ["concept_000"],
      "difficulty": 1-5,
      "socratic_questions": {
        "level_1_confirm": ["이게 맞나요?", "..."],
        "level_2_explore": ["왜 그럴까요?", "반례는?", "..."],
        "level_3_refute": ["하지만 이 경우는 어떤가요?", "..."]
      }
    }
  ],
  "learning_objectives": [...],
  "concept_graph": {...}
}
```

### 1.2 학습자 프로파일링
- **Agent**: `@learner-profiler`
- **Trigger**: 학습자 최초 접속 / 주기적 재진단
- **Task**:
  - 사전 지식 수준 진단 (적응형 진단 테스트)
  - 학습 스타일 파악 (시각/청각/읽기/실습)
  - 응답 패턴 분석 (속도, 자신감, 오류 유형)
  - 동기 수준 추정
- **Output**: `learner-profile.json`

```json
{
  "learner_id": "uuid",
  "knowledge_state": {
    "concept_001": {"mastery": 0.7, "confidence": 0.8},
    "concept_002": {"mastery": 0.3, "confidence": 0.9}
  },
  "learning_style": "visual",
  "response_pattern": {
    "avg_response_time": 15,
    "confidence_accuracy_gap": 0.2,
    "common_error_types": ["overgeneralization", "missing_edge_cases"]
  },
  "motivation_level": "high"
}
```

### 1.3 외부 지식 보강 (On-demand)
- **Agent**: `@knowledge-researcher`
- **Trigger**: 오개념 감지 시 / 학습자 질문이 자료 범위 초과 시
- **Task**:
  - 웹 검색으로 추가 설명 자료 수집
  - 학술 논문/MOOC에서 보충 콘텐츠 탐색
  - 다양한 관점의 설명 방식 수집
- **Output**: `supplementary-knowledge.md`

---

## Phase 2: Planning

개인화 학습 경로 및 세션 설계.

### 2.1 학습 경로 최적화
- **Agent**: `@path-optimizer`
- **Trigger**: 프로파일링 완료 후 / 세션 종료 후 갱신
- **Task**:
  - 학습자 수준에 맞는 개념 순서 결정
  - 적응형 난이도 곡선 설계 (Zone of Proximal Development)
  - 복습 주기 스케줄링 (간격 반복 알고리즘)
  - 전이 학습 챌린지 배치 시점 결정
- **Output**: `learning-path.json`

```json
{
  "learner_id": "uuid",
  "current_position": "concept_003",
  "path": [
    {"concept": "concept_003", "target_mastery": 0.8, "estimated_time": "15min"},
    {"concept": "concept_004", "target_mastery": 0.8, "estimated_time": "20min"},
    {"type": "transfer_challenge", "source_concept": "concept_003", "target_domain": "same_field"},
    ...
  ],
  "review_schedule": [
    {"concept": "concept_001", "review_at": "2025-01-15T10:00:00Z"}
  ]
}
```

### 2.2 세션 설계
- **Agent**: `@session-planner`
- **Trigger**: 학습자 세션 시작 요청 시
- **Task**:
  - 오늘의 학습 목표 설정
  - 소크라테스 대화 흐름 설계 (Warm-up → Deep Dive → Synthesis)
  - 메타인지 체크포인트 배치
  - 탈출 조건 정의 (목표 달성 OR 학습자 종료 요청)
- **Output**: `session-plan.json`

```json
{
  "session_id": "uuid",
  "learner_id": "uuid",
  "objectives": ["concept_003 mastery >= 0.8"],
  "structure": {
    "warm_up": {
      "duration": "3min",
      "activity": "이전 개념 빠른 복습",
      "question_level": 1
    },
    "deep_dive": {
      "duration": "15-25min",
      "activity": "핵심 개념 소크라테스 탐구",
      "question_levels": [1, 2, 3],
      "metacog_checkpoints": [5, 15]
    },
    "synthesis": {
      "duration": "5min",
      "activity": "개념 연결 + 전이 챌린지 미리보기"
    }
  },
  "exit_conditions": {
    "success": "all objectives met",
    "user_exit": "anytime allowed",
    "timeout": "45min soft limit"
  }
}
```

### 2.3 세션 로깅 (백그라운드 자동 로깅)
- **Agent**: `@session-logger`
- **Trigger**: 세션 시작 시 자동으로 백그라운드 실행
- **Task**:
  - **5초마다 자동으로** 학습 상태 스냅샷 저장
  - 현재 위치 (module, lesson, phase, question_level) 기록
  - 대화 컨텍스트 (last_ai_message, last_user_response) 보존
  - 학습 진행 메트릭 (questions_asked, mastery_updates) 추적
  - 비정상 종료 시 복구 체크포인트 역할
- **Output**: `data/socratic/sessions/active/{session_id}.log.json`

```
백그라운드 로깅 프로세스:
┌───────────────────────────────────────────────────────────────┐
│                  @session-logger (백그라운드)                  │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  세션 시작 ──▶ start_background_logging() 호출                │
│                      │                                        │
│                      ▼                                        │
│              ┌─────────────────┐                              │
│              │  while (active) │                              │
│              │    sleep(5초)   │                              │
│              │    save_snapshot│──▶ snapshots/{timestamp}.json│
│              │    update_log   │──▶ {session_id}.log.json     │
│              └─────────────────┘                              │
│                      │                                        │
│                      ▼                                        │
│  세션 종료 ──▶ end_session() 호출                             │
│              └─▶ active/ → completed/ 폴더 이동               │
│                                                               │
└───────────────────────────────────────────────────────────────┘

세션 복구 프로세스:
┌───────────────────────────────────────────────────────────────┐
│                    /resume 명령 실행                           │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  1. SessionRecoveryManager.check_recoverable_sessions()       │
│     ├── active/ 폴더 스캔 (5분 이상 업데이트 없음 = 비정상)    │
│     └── interrupted/ 폴더 스캔 (명시적 중단)                  │
│                                                               │
│  2. 복구 가능 세션 발견 시:                                    │
│     ├── 사용자에게 복구 프롬프트 표시                          │
│     └── SessionRecoveryManager.recover_session(session_id)    │
│         ├── 로그 파일에서 마지막 상태 로드                     │
│         ├── 스냅샷에서 체크포인트 복원                         │
│         ├── 대화 컨텍스트 복원                                │
│         └── @socratic-tutor 복원 상태로 재개                  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

**핵심 로그 스키마**:
```json
{
  "session_id": "uuid",
  "session_info": {
    "started_at": "2026-01-14T10:00:00Z",
    "last_updated_at": "2026-01-14T10:23:45Z",
    "status": "active",
    "total_duration_seconds": 1425
  },
  "current_position": {
    "module_id": "M2",
    "lesson_id": "L2.3",
    "lesson_title": "반복문 기초",
    "current_phase": "deep_dive",
    "current_question_level": 2,
    "lesson_progress_pct": 45,
    "awaiting_response": true,
    "pending_question": "for 루프에서 i가 어떻게 변하나요?"
  },
  "conversation_context": {
    "last_ai_message": "for i in range(5)에서...",
    "last_user_response": "5번 반복되나요?",
    "dialogue_history_summary": "반복문 개념 탐구 중"
  },
  "recovery_checkpoint": {
    "checkpoint_id": "CP_20260114_102345",
    "recoverable": true,
    "resume_instruction": "L2.3 (반복문 기초) - deep_dive 단계. Level 2 질문 응답 대기"
  }
}
```

---

## Phase 3: Implementation

실시간 튜터링 및 피드백 생성.

### 3.1 소크라테스 튜터링 (핵심)
- **Agent**: `@socratic-tutor`
- **Trigger**: 세션 시작
- **Task**:
  - 3단계 문답법 균형 적용
    - Level 1 (확인): "이게 맞나요?" "X와 Y 중 어느 것이...?"
    - Level 2 (탐구): "왜 그렇게 생각하나요?" "반례는 없을까요?"
    - Level 3 (논박): "하지만 이 경우는요?" "당신 논리대로라면..."
  - 학습자 응답에 따른 동적 질문 조정
  - 절대 정답을 직접 제시하지 않음 (유도만)
  - 적절한 힌트 제공 (scaffolding)
- **Sub-agents 호출**:
  - `@misconception-detector`: 매 응답마다 오개념 체크
  - `@metacog-coach`: 체크포인트에서 메타인지 질문
- **Output**: `session-transcript.json`

```
소크라테스 대화 흐름 예시:

[Level 1 - 확인]
AI: "그렇다면 수요가 증가하면 가격은 어떻게 될까요?"
학습자: "올라가요"
AI: "맞습니다. 그런데..."

[Level 2 - 탐구]  
AI: "왜 가격이 올라갈까요? 그 메커니즘을 설명해볼 수 있나요?"
학습자: "사람들이 더 많이 원하니까요"
AI: "좋아요. 그런데 공급자 입장에서는 어떤 일이 일어날까요?"

[Level 3 - 논박]
AI: "만약 공급이 무한하다면요? 그래도 가격이 오를까요?"
학습자: "음... 아닐 것 같아요"
AI: "그렇다면 가격 상승의 진짜 조건은 무엇일까요?"

[메타인지 체크포인트]
AI: "잠깐, 방금 당신의 생각이 어떻게 바뀌었는지 알아차렸나요? 
     처음에는 '수요 증가 = 가격 상승'이라고 했는데, 
     지금은 어떤 조건이 추가되었죠?"
```

### 3.2 오개념 감지 및 교정
- **Agent**: `@misconception-detector`
- **Trigger**: 학습자 응답마다 실시간 호출
- **Task**:
  - 응답에서 오개념 패턴 탐지
  - 오개념 심각도 분류 (minor/moderate/critical)
  - Critical 감지 시 `@knowledge-researcher` 자동 호출
- **Output**: `misconception-alert.json`

```json
{
  "detected": true,
  "type": "overgeneralization",
  "severity": "moderate",
  "student_claim": "모든 수요 증가는 가격 상승을 유발한다",
  "correct_understanding": "공급 탄력성에 따라 다름",
  "recommended_action": "Level 3 논박 질문으로 유도"
}
```

### 3.3 메타인지 코칭
- **Agent**: `@metacog-coach`
- **Trigger**: 세션 플랜의 체크포인트 도달 시
- **Task**:
  - "왜 그렇게 생각했나요?" 질문
  - 사고 과정 명시화 유도
  - 자기 오류 인식 촉진
  - 학습 전략 제안
- **Output**: 대화에 직접 삽입

```
메타인지 질문 유형:
- "방금 답을 바꿨는데, 무엇이 생각을 바꾸게 했나요?"
- "이 문제를 풀 때 어떤 전략을 사용했나요?"
- "어디서 막혔고, 어떻게 해결했나요?"
- "다음에 비슷한 문제를 만나면 어떻게 접근하겠어요?"
```

### 3.4 개념 연결 맵 생성
- **Agent**: `@concept-mapper`
- **Trigger**: 세션 종료 시 / 새 개념 학습 완료 시
- **Task**:
  - 학습한 개념들의 관계 시각화
  - 선수-후속 관계, 유사 개념, 대조 개념 표시
  - 학습자의 이해 경로 시각화
- **Output**: `concept-map.json` + 시각화 렌더링

```json
{
  "nodes": [
    {"id": "concept_001", "label": "수요", "mastery": 0.9},
    {"id": "concept_002", "label": "공급", "mastery": 0.85},
    {"id": "concept_003", "label": "균형가격", "mastery": 0.7}
  ],
  "edges": [
    {"from": "concept_001", "to": "concept_003", "type": "prerequisite"},
    {"from": "concept_002", "to": "concept_003", "type": "prerequisite"},
    {"from": "concept_001", "to": "concept_002", "type": "contrast"}
  ]
}
```

### 3.5 전이 학습 챌린지
- **Agent**: `@socratic-tutor` (확장 모드)
- **Trigger**: 개념 마스터리 80% 이상 달성 시
- **Task**:
  - **Same-field Transfer**: 같은 분야 내 응용 문제
    - 예: 경제학 수요-공급 → 노동시장 임금 결정
  - **Far Transfer**: 완전히 다른 분야로 적용
    - 예: 경제학 균형 → 생태계 평형 → 조직 내 권력 균형
  - 소크라테스식 유도로 학습자가 스스로 연결점 발견
- **Output**: `transfer-challenge-result.json`

```
전이 챌린지 예시:

AI: "수요-공급 균형을 잘 이해했네요. 
     이제 전혀 다른 상황을 생각해볼까요?
     
     회사에서 '좋은 아이디어'에 대한 수요와 공급이 있다고 상상해보세요.
     - 경영진은 혁신적 아이디어를 원합니다 (수요)
     - 직원들은 아이디어를 제안할 수 있습니다 (공급)
     
     그런데 많은 회사에서 혁신이 잘 안 일어납니다.
     수요-공급 프레임워크로 이 현상을 설명해볼 수 있을까요?"

학습자: "음... 공급이 부족한 건가요?"

AI: "흥미로운 가설이네요. 정말 직원들에게 아이디어가 없을까요?
     아니면 '공급을 막는 무언가'가 있을까요?"
```

### 3.6 진척도 추적 및 리포트
- **Agent**: `@progress-tracker`
- **Trigger**: 매 세션 종료 시 / 요청 시
- **Task**:
  - 개념별 마스터리 업데이트
  - 학습 성장 곡선 분석
  - 취약점 및 강점 식별
  - 다음 세션 추천
- **Output**: `progress-report.json` + 시각화

```json
{
  "learner_id": "uuid",
  "session_summary": {
    "duration": "28min",
    "concepts_covered": ["concept_003"],
    "mastery_change": {"concept_003": 0.4 -> 0.82},
    "socratic_depth_reached": 3,
    "metacognitive_moments": 2,
    "misconceptions_corrected": 1
  },
  "overall_progress": {
    "total_concepts": 50,
    "mastered": 12,
    "in_progress": 5,
    "not_started": 33,
    "estimated_completion": "15 sessions"
  },
  "growth_insights": [
    "논리적 추론 능력 15% 향상",
    "과잉일반화 오류 빈도 감소",
    "메타인지 응답 품질 향상"
  ],
  "recommendations": [
    "다음 세션: concept_004 (현재 경로)",
    "복습 필요: concept_001 (3일 후)",
    "도전 추천: concept_003 far-transfer"
  ]
}
```

---

## Claude Code Configuration

### Sub-agents

```yaml
agents:
  # ═══════════════════════════════════════════════════════════
  # Phase 0: Curriculum Genesis (신규)
  # ═══════════════════════════════════════════════════════════
  
  topic-scout:
    description: "키워드에서 학습 범위와 하위 주제 도출. Pre-trained 지식 기반 초안 생성"
    prompt_prefix: |
      당신은 교육과정 설계 전문가입니다.
      주어진 키워드에서:
      1. 학습 가능한 범위를 정의하세요
      2. 체계적인 하위 주제를 도출하세요
      3. 선수 지식과 관련 분야를 매핑하세요
      4. 난이도 스펙트럼을 추정하세요
      
  web-searcher:
    description: "실시간 웹 검색으로 최신 학습 자료 수집"
    tools: [web-search, web-fetch]
    prompt_prefix: |
      각 하위 주제에 대해 최신 자료를 검색하세요:
      - 공식 문서, 튜토리얼, 최신 뉴스
      - 실제 사례와 케이스 스터디
      - 최신 트렌드와 업데이트 사항
      신뢰도와 최신성을 함께 평가하세요.
      
  deep-researcher:
    description: "심층 리서치로 학술자료/전문지식 탐색"
    tools: [web-search, scholar-search, deep-research]
    prompt_prefix: |
      학술적 깊이가 있는 자료를 탐색하세요:
      - 학술 논문 (arXiv, IEEE, Google Scholar)
      - 전문 서적 및 교재
      - 대학 강의자료 및 MOOC
      - 전문가 견해와 논쟁점
      역사적 맥락과 발전 과정도 정리하세요.
      
  content-curator:
    description: "수집된 자료의 품질 평가 및 선별"
    prompt_prefix: |
      수집된 모든 자료를 다음 기준으로 평가하세요:
      - 신뢰도 (출처의 권위)
      - 최신성 (발행 시점)
      - 교육적 가치 (설명 품질)
      - 소크라테스 질문 생성 적합성
      중복을 제거하고 상충 정보를 해결하세요.
      
  curriculum-architect:
    description: "완전한 교수 커리큘럼 자동 설계"
    prompt_prefix: |
      당신은 최고의 커리큘럼 설계자입니다.
      큐레이션된 콘텐츠로 완전한 커리큘럼을 설계하세요:
      - 명확한 학습 목표 (Learning Objectives)
      - 논리적 모듈/레슨 구조
      - 개념 의존성 그래프
      - 각 레슨별 3단계 소크라테스 질문
      - 전이 학습 챌린지 배치
      - 적응형 학습 경로 옵션

  # ═══════════════════════════════════════════════════════════
  # Phase 1-3: 기존 에이전트
  # ═══════════════════════════════════════════════════════════
  
  orchestrator:
    description: "전체 시스템 총괄. 학습자 상태 모니터링 및 에이전트 호출 조율"
    tools: [state-manager]
    always_on: true
    
  content-analyzer:
    description: "학습 콘텐츠에서 핵심 개념, 학습목표, 소크라테스 질문 추출"
    tools: [web-search, document-parser]
    prompt_prefix: |
      당신은 교육 콘텐츠 분석 전문가입니다.
      모든 개념에 대해 3단계 소크라테스 질문을 생성하세요:
      1) 확인 질문 2) 탐구 질문 3) 논박 질문
      
  learner-profiler:
    description: "학습자 수준 진단 및 학습 스타일 파악"
    tools: [adaptive-test-engine]
    prompt_prefix: |
      당신은 교육 심리학 전문가입니다.
      학습자의 지식 상태와 학습 스타일을 정확히 진단하세요.
      
  path-optimizer:
    description: "개인화 학습 경로 생성 및 최적화"
    prompt_prefix: |
      당신은 적응형 학습 시스템 설계자입니다.
      Zone of Proximal Development를 고려하여 
      최적의 학습 순서와 난이도 곡선을 설계하세요.
      
  session-planner:
    description: "각 튜터링 세션의 구조와 흐름 설계"
    prompt_prefix: |
      당신은 소크라테스 대화 설계자입니다.
      Warm-up → Deep Dive → Synthesis 구조로
      효과적인 세션을 설계하세요.
      
  socratic-tutor:
    description: "핵심 에이전트. 소크라테스 문답법으로 실시간 튜터링"
    tools: [misconception-detector-call, metacog-coach-call]
    temperature: 0.7
    prompt_prefix: |
      당신은 소크라테스입니다. 절대 답을 직접 알려주지 마세요.
      
      3단계 질문을 균형있게 사용하세요:
      - Level 1 (확인): 기본 이해 확인
      - Level 2 (탐구): "왜?" "어떻게?" 깊은 사고 유도
      - Level 3 (논박): 모순 드러내기, 반례 제시
      
      학습자가 스스로 진리를 발견하도록 유도하세요.
      
  misconception-detector:
    description: "학습자 응답에서 오개념 실시간 탐지"
    prompt_prefix: |
      다음 응답에서 오개념을 탐지하세요.
      심각도를 minor/moderate/critical로 분류하세요.
      critical인 경우 즉시 교정이 필요합니다.
      
  knowledge-researcher:
    description: "오개념 교정 및 심화를 위한 추가 자료 검색"
    tools: [web-search, scholar-search]
    trigger: "misconception_severity == critical"
    
  metacog-coach:
    description: "메타인지 훈련 - 사고 과정 인식 유도"
    prompt_prefix: |
      학습자가 자신의 사고 과정을 인식하도록 도우세요.
      "왜 그렇게 생각했나요?"
      "무엇이 생각을 바꾸게 했나요?"
      "다음에는 어떻게 접근하겠어요?"
      
  concept-mapper:
    description: "학습 개념들의 관계를 시각화"
    tools: [graph-renderer]
    
  progress-tracker:
    description: "학습 진척도 추적 및 리포트 생성"
    tools: [analytics-engine, visualization]
```

### Slash Commands

```yaml
commands:
  # ═══════════════════════════════════════════════════════════
  # Phase 0: Curriculum Genesis 커맨드 (신규)
  # ═══════════════════════════════════════════════════════════
  
  /teach:
    description: "키워드로 자동 커리큘럼 생성 (Zero-to-Curriculum)"
    args:
      - name: keyword
        type: string
        required: true
        description: "학습/교수하고 싶은 주제, 이슈, 대상"
      - name: depth
        type: enum[quick, standard, deep]
        required: false
        default: standard
        description: "리서치 깊이 (quick: 웹검색만, standard: +심층리서치, deep: +학술논문)"
      - name: target_hours
        type: integer
        required: false
        description: "목표 학습 시간 (미지정시 자동 추정)"
    action: |
      1. @topic-scout: 키워드에서 학습 범위/하위주제 도출
      2. 병렬 실행:
         - @web-searcher: 실시간 웹 검색
         - @deep-researcher: 심층 리서치 (depth에 따라)
      3. @content-curator: 수집 자료 품질 평가 및 선별
      4. @curriculum-architect: 커리큘럼 자동 설계
      5. 사용자에게 커리큘럼 요약 제시
    example: |
      /teach 블록체인
      /teach "머신러닝" --depth=deep --target_hours=20
      /teach 양자역학 --depth=quick
      
  /teach-from-file:
    description: "업로드된 자료 기반 커리큘럼 생성"
    args:
      - name: file
        type: file
        required: true
      - name: expand
        type: boolean
        default: true
        description: "웹검색/심층리서치로 자료 확장 여부"
    action: |
      1. @content-analyzer: 업로드 자료 분석
      2. @topic-scout: 자료에서 학습 범위 파악
      3. (expand=true일 경우) @web-searcher + @deep-researcher 실행
      4. @content-curator: 통합 큐레이션
      5. @curriculum-architect: 커리큘럼 설계

  # ═══════════════════════════════════════════════════════════
  # Phase 1-3: 기존 커맨드
  # ═══════════════════════════════════════════════════════════
  
  /start-learning:
    description: "학습 세션 시작"
    args:
      - name: topic
        type: string
        required: false
    action: |
      1. @learner-profiler로 학습자 상태 확인
      2. @session-planner로 세션 설계
      3. @socratic-tutor 활성화
      
  /upload-content:
    description: "새 학습 자료 업로드 및 분석"
    args:
      - name: file
        type: file
        required: true
    action: |
      @content-analyzer로 즉시 분석 실행
      완료 후 학습 경로에 자동 통합
      
  /my-progress:
    description: "현재 학습 진척도 확인"
    action: |
      @progress-tracker로 리포트 생성 및 시각화
      
  /concept-map:
    description: "학습한 개념들의 연결 맵 보기"
    action: |
      @concept-mapper로 현재까지 학습 개념 시각화
      
  /challenge:
    description: "전이 학습 챌린지 요청"
    args:
      - name: type
        type: enum[same-field, far-transfer]
        required: false
        default: same-field
    action: |
      마스터한 개념 중 하나를 선택하여 전이 챌린지 시작
      
  /end-session:
    description: "현재 세션 종료"
    action: |
      1. 세션 요약 생성
      2. 진척도 업데이트
      3. 다음 세션 추천
```

### Required Skills

```yaml
skills:
  # Curriculum Genesis
  - topic-analysis: 키워드에서 학습 범위/구조 도출
  - content-quality-scoring: 학습 자료 품질 평가
  - curriculum-design: 교수법 기반 커리큘럼 설계
  - knowledge-integration: Pre-trained + 검색 + 리서치 통합
  
  # Socratic Tutoring
  - socratic-questioning: 소크라테스 문답법 패턴 및 질문 생성
  - adaptive-learning: 적응형 학습 알고리즘 (간격 반복, ZPD)
  - misconception-patterns: 일반적 오개념 패턴 데이터베이스
  - metacognition-prompts: 메타인지 유도 질문 템플릿
  - knowledge-graph: 개념 관계 그래프 구축
```

### MCP Servers

```yaml
mcp_servers:
  # Curriculum Genesis
  - web-search-mcp: 실시간 웹 검색 엔진
  - deep-research-mcp: 심층 리서치 엔진 (Claude Deep Research 연동)
  - scholar-search-mcp: 학술 자료 검색 (Google Scholar, arXiv, IEEE)
  - mooc-connector-mcp: MOOC 플랫폼 콘텐츠 접근 (Coursera, edX)
  
  # Tutoring & Analytics
  - adaptive-test-mcp: 적응형 진단 테스트 엔진
  - graph-renderer-mcp: 개념 맵 시각화
  - analytics-mcp: 학습 분석 및 리포트 생성
```

---

## Execution Flow

### Flow A: 키워드 기반 자동 커리큘럼 생성 (/teach)

#### Case A: User-Resource가 있는 경우 (User-Resource 중심)

```
[사용자: /teach 블록체인]
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Phase 0: CURRICULUM GENESIS (User-Resource 중심 모드)            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────┐                    │
│  │ Step 0: USER-RESOURCE 스캔 (최우선)      │                    │
│  │ • user-resource/ 폴더 확인               │                    │
│  │ • 관련 자료 발견! ✓                      │──▶ user-resource   │
│  │ • PRIMARY 소스로 태깅                    │    -scan.json      │
│  └────────────────┬────────────────────────┘                    │
│                   │                                              │
│                   ▼                                              │
│  ┌─────────────────────────────────────────┐                    │
│  │ @content-analyzer: 사용자 자료 심층 분석 │──▶ user-content    │
│  │ • 핵심 개념 추출                         │    -analysis.json  │
│  │ • 학습 목표 도출                         │                    │
│  │ • 소크라테스 질문 포인트 식별            │                    │
│  │ • 커버리지 갭 식별                       │                    │
│  └────────────────┬────────────────────────┘                    │
│                   │                                              │
│                   ▼                                              │
│  ┌─────────────────────────────────────────┐                    │
│  │ @topic-scout: 주제 정찰                  │──▶ topic-scope.json│
│  │ • user-resource 분석 결과 기반 범위 파악 │                    │
│  │ • Pre-trained 지식으로 갭 보완           │                    │
│  │ • 하위 주제 도출                         │                    │
│  └────────────────┬────────────────────────┘                    │
│                   │                                              │
│          ┌────────┴────────┐                                    │
│          ▼                 ▼                                    │
│  ┌──────────────┐  ┌──────────────┐                             │
│  │@web-searcher │  │@deep-        │                             │
│  │ (갭 보완용)   │  │ researcher   │                             │
│  │ • 갭 영역만   │  │ (갭 보완용)  │                             │
│  │   검색       │  │ • 갭 영역만  │                             │
│  │ • SUPPLEM-   │  │   리서치     │                             │
│  │   ENTARY     │  │ • SUPPLEM-   │                             │
│  └──────┬───────┘  │   ENTARY     │                             │
│         │          └──────┬───────┘                             │
│         │      병렬 실행    │                                    │
│         └────────┬─────────┘                                    │
│                  ▼                                              │
│  ┌─────────────────────────────────────────┐                    │
│  │ @content-curator: 콘텐츠 큐레이션        │──▶ curated.json    │
│  │ • user-resource 자료 무조건 포함 (1.0)   │                    │
│  │ • 외부 자료는 갭 보완용으로만 선별       │                    │
│  │ • 품질 평가, 중복 제거, 충돌 해결        │                    │
│  └────────────────┬────────────────────────┘                    │
│                   ▼                                              │
│  ┌─────────────────────────────────────────┐                    │
│  │ @curriculum-architect: 커리큘럼 설계     │──▶ curriculum.json │
│  │ • user-resource 콘텐츠 중심 구조화       │                    │
│  │ • user-resource 순서/구조 반영           │                    │
│  │ • 모듈/레슨 구조화                       │                    │
│  │ • 소크라테스 질문 배치                   │                    │
│  │ • 전이 챌린지 설계                       │                    │
│  └─────────────────────────────────────────┘                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
    [커리큘럼 요약 제시 - user-resource 기반]
         │
         ▼
    /start-learning → [Flow B로 이동]
```

#### Case B: User-Resource가 없는 경우 (FALLBACK - 외부 자료 집중)

```
[사용자: /teach 블록체인]
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Phase 0: CURRICULUM GENESIS (FALLBACK 모드 - 외부 자료 집중)     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────┐                    │
│  │ Step 0: USER-RESOURCE 스캔              │                    │
│  │ • user-resource/ 폴더 확인               │                    │
│  │ • 관련 자료 없음 ✗                       │──▶ fallback_mode   │
│  │ • FALLBACK 모드 활성화                   │    = true          │
│  └────────────────┬────────────────────────┘                    │
│                   │                                              │
│                   ▼ (심층 분석 단계 스킵)                        │
│                                                                  │
│  ┌─────────────────────────────────────────┐                    │
│  │ @topic-scout: 주제 정찰                  │──▶ topic-scope.json│
│  │ • Pre-trained 지식 기반 범위 파악        │                    │
│  │ • 전체 주제 구조 도출                    │                    │
│  │ • 모든 하위 주제에 대한 검색 쿼리 생성   │                    │
│  └────────────────┬────────────────────────┘                    │
│                   │                                              │
│          ┌────────┴────────┐                                    │
│          ▼                 ▼                                    │
│  ┌──────────────┐  ┌──────────────┐                             │
│  │@web-searcher │  │@deep-        │                             │
│  │ (PRIMARY)    │  │ researcher   │                             │
│  │ • 전체 주제  │  │ (PRIMARY)    │                             │
│  │   검색       │  │ • 전체 주제  │                             │
│  │ • 균형있게   │  │   리서치     │                             │
│  │   수집       │  │ • 균형있게   │                             │
│  └──────┬───────┘  │   수집       │                             │
│         │          └──────┬───────┘                             │
│         │      병렬 실행    │                                    │
│         └────────┬─────────┘                                    │
│                  ▼                                              │
│  ┌─────────────────────────────────────────┐                    │
│  │ @content-curator: 콘텐츠 큐레이션        │──▶ curated.json    │
│  │ • 모든 소스 동등 우선순위 (PRIMARY)      │                    │
│  │ • 품질 필터 적용 (0.6 이상)              │                    │
│  │ • 소스 다양성 확보                       │                    │
│  │ • 깊이 레벨별 균형                       │                    │
│  └────────────────┬────────────────────────┘                    │
│                   ▼                                              │
│  ┌─────────────────────────────────────────┐                    │
│  │ @curriculum-architect: 커리큘럼 설계     │──▶ curriculum.json │
│  │ • 표준 설계 모드                         │                    │
│  │ • topic-scout 구조 기반                  │                    │
│  │ • 모듈/레슨 구조화                       │                    │
│  │ • 소크라테스 질문 배치                   │                    │
│  │ • 전이 챌린지 설계                       │                    │
│  └─────────────────────────────────────────┘                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
    [커리큘럼 요약 제시 - 외부 자료 기반]
    "user-resource 폴더에 자료를 추가하면
     더 맞춤화된 커리큘럼을 생성합니다"
         │
         ▼
    /start-learning → [Flow B로 이동]
```

### Flow B: 학습 세션 실행 (/start-learning)

```
[학습자: /start-learning 또는 커리큘럼 생성 후 자동 연결]
     │
     ▼
┌─────────────────┐
│ /start-learning │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ @learner-profiler: 수준 진단            │──▶ learner-profile.json
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ @path-optimizer: 학습 경로 생성/갱신    │──▶ learning-path.json
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ @session-planner: 오늘 세션 설계        │──▶ session-plan.json
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    @socratic-tutor: 실시간 대화                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  [매 응답마다]                                            │   │
│  │  └──▶ @misconception-detector 호출                       │   │
│  │       └──▶ critical이면 @knowledge-researcher 호출       │   │
│  │                                                          │   │
│  │  [체크포인트마다]                                         │   │
│  │  └──▶ @metacog-coach 호출                                │   │
│  │                                                          │   │
│  │  [목표 달성 시]                                           │   │
│  │  └──▶ @concept-mapper 호출                               │   │
│  │  └──▶ Transfer Challenge 제안                            │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────┬────────────────────────────────────────────────────────┘
         │
         ▼ [세션 종료]
┌─────────────────────────────────────────┐
│ @progress-tracker: 리포트 생성          │──▶ progress-report.json
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ @path-optimizer: 경로 갱신              │──▶ learning-path.json (updated)
└─────────────────────────────────────────┘
```

---

## Quality Metrics

### 커리큘럼 자동 생성 품질 지표

| 지표 | 설명 | 목표 |
|------|------|------|
| Source Diversity | 소스 유형 다양성 (Pre-trained/Web/Academic) | 3종 균형 |
| Content Freshness | 최신 정보 반영률 (1년 이내) | > 60% |
| Curriculum Completeness | 학습 목표 대비 콘텐츠 커버리지 | > 95% |
| Question Bank Quality | 생성된 소크라테스 질문 적절성 | > 85% |
| Generation Time | 키워드 → 커리큘럼 생성 소요 시간 | < 5분 |
| Expert Alignment | 전문가 커리큘럼과의 일치도 (검증용) | > 80% |

### 교육 효과 측정 지표

| 지표 | 설명 | 목표 |
|------|------|------|
| Mastery Rate | 목표 마스터리 달성 비율 | > 85% |
| Retention Rate | 1주 후 복습 테스트 점수 유지율 | > 80% |
| Socratic Depth | 평균 도달 질문 단계 | Level 2.5+ |
| Metacog Score | 메타인지 응답 품질 점수 | > 7/10 |
| Transfer Success | 전이 챌린지 성공률 | > 60% |
| Session Completion | 자발적 세션 완료율 | > 90% |
| Misconception Fix | 오개념 교정 성공률 | > 95% |

### 대형 강의 대비 우위 지표

| 대형 강의 한계 | AI 튜터 해결 | 측정 방법 |
|---------------|-------------|----------|
| 일방향 강의 | 100% 쌍방향 문답 | 질문-응답 비율 |
| 획일적 진도 | 완전 개인화 경로 | 학습자별 경로 분산 |
| 피드백 부재 | 실시간 + 매 응답 | 평균 피드백 지연시간 |
| 수동적 암기 | 소크라테스 탐구 | Level 2-3 질문 비율 |

---

## 대형 강의 vs AI 튜터 비교

```
┌────────────────────┬────────────────────┬────────────────────┐
│      측면          │    대형 강의        │   소크라테스 AI    │
├────────────────────┼────────────────────┼────────────────────┤
│ 학생 대 교수 비율   │     300:1          │       1:1          │
│ 개인화 수준        │       없음          │      완전          │
│ 질문 기회          │    거의 없음        │     무제한         │
│ 피드백 지연        │   1-2주 (과제)      │      0초           │
│ 진도 적응          │       불가          │      실시간        │
│ 오개념 교정        │     발견 어려움     │     즉시 감지      │
│ 메타인지 훈련      │       없음          │     내장           │
│ 운영 시간          │    주 3시간         │      24/7          │
│ 확장성             │     물리적 한계     │      무한          │
└────────────────────┴────────────────────┴────────────────────┘
```
