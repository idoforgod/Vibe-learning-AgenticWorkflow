# Socratic AI Tutor — Agent Manifest

[trace:step-6:personas] [trace:step-5:tool-mapping] [trace:step-12:project-scaffolding]

**Generated**: Step 13 — Sub-Agent Implementation
**Total agents**: 17

## Agent Registry

| # | Agent | Model | Phase | Tools | maxTurns | File |
|---|-------|-------|-------|-------|----------|------|
| 1 | @content-analyzer | sonnet | Phase 0+1 | Read, Write, Bash, Glob | 20 | content-analyzer.md |
| 2 | @topic-scout | sonnet | Phase 0 | Read, Write | 10 | topic-scout.md |
| 3 | @web-searcher | haiku | Phase 0 | WebSearch, WebFetch, Read, Write | 25 | web-searcher.md |
| 4 | @deep-researcher | sonnet | Phase 0 | WebSearch, WebFetch, Bash, Read, Write | 30 | deep-researcher.md |
| 5 | @content-curator | sonnet | Phase 0 | Read, Write | 15 | content-curator.md |
| 6 | @curriculum-architect | opus | Phase 0 | Read, Write | 20 | curriculum-architect.md |
| 7 | @orchestrator | opus | Cross-phase | Read, Write, Bash, Task, Glob, Grep | 40 | orchestrator.md |
| 8 | @learner-profiler | sonnet | Phase 1 | Read, Write | 15 | learner-profiler.md |
| 9 | @knowledge-researcher | sonnet | Phase 1 | WebSearch, WebFetch, Bash, Read, Write | 15 | knowledge-researcher.md |
| 10 | @path-optimizer | sonnet | Phase 2 | Read, Write | 15 | path-optimizer.md |
| 11 | @session-planner | haiku | Phase 2 | Read, Write | 10 | session-planner.md |
| 12 | @session-logger | haiku | Phase 2-3 | Read, Write | 10 | session-logger.md |
| 13 | @socratic-tutor | opus | Phase 3 | Read, Write | 30 | socratic-tutor.md |
| 14 | @misconception-detector | haiku | Phase 3 | Read, Write | 10 | misconception-detector.md |
| 15 | @metacog-coach | sonnet | Phase 3 | Read, Write | 10 | metacog-coach.md |
| 16 | @concept-mapper | haiku | Phase 3 | Read, Write | 10 | concept-mapper.md |
| 17 | @progress-tracker | sonnet | Phase 3 | Read, Write | 15 | progress-tracker.md |

## Model Distribution

- **opus** (3): @curriculum-architect, @orchestrator, @socratic-tutor
- **sonnet** (9): @content-analyzer, @topic-scout, @deep-researcher, @content-curator, @learner-profiler, @knowledge-researcher, @path-optimizer, @metacog-coach, @progress-tracker
- **haiku** (5): @web-searcher, @session-planner, @session-logger, @misconception-detector, @concept-mapper

## Cross-Step Dependencies

All 17 agent definitions derive from:
- **Step 5** [trace:step-5:tool-mapping]: Architecture blueprint — tool assignments, model tiers, agent responsibilities
- **Step 6** [trace:step-6:personas]: Agent persona designs — behavioral rules, processing protocols, output schemas
- **Step 12** [trace:step-12:project-scaffolding]: Project scaffolding — directory structure (`data/socratic/`) and SOT initialization that agents read/write
