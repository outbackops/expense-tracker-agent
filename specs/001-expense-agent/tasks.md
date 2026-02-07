# Tasks: Intelligent Expense Tracking Agent

**Input**: Design documents from `/specs/001-expense-agent/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Not requested - no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

Per plan.md: Single-file architecture with all business logic in agent instructions.

```text
expense_agent.py         # Main agent script (thin client)
requirements.txt         # Python dependencies
expense_reports/         # Generated expense report files (.txt)
```

---

## Phase 1: Setup

**Purpose**: Project initialization and basic dependencies

- [X] T001 Create requirements.txt with azure-ai-projects>=2.0.0b1, azure-identity
- [X] T002 [P] Create expense_reports/ directory for generated reports
- [X] T003 Create expense_agent.py with configuration constants (USER_ENDPOINT, AGENT_NAME, MODEL_DEPLOYMENT_NAME)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Implement Azure authentication with AzureCliCredential and PATH workaround in expense_agent.py
- [X] T005 Implement AIProjectClient initialization in expense_agent.py
- [X] T006 Implement create_expense_agent() function with PromptAgentDefinition, CodeInterpreterTool, and WebSearchPreviewTool in expense_agent.py
- [X] T007 Implement process_expense() function with openai_client.responses.create() in expense_agent.py
- [X] T008 Implement main() function with CLI interactive loop in expense_agent.py

**Checkpoint**: Foundation ready - agent can connect to Azure AI Foundry and invoke tools

---

## Phase 3: User Story 1 - Single Expense Recording (Priority: P1) 🎯 MVP

**Goal**: Process a single expense input and generate a formatted .txt file with all required fields

**Independent Test**: Provide "spent 50 dollars on lunch" and verify .txt file is generated with Report ID, Amount: 50, Currency: USD, Description: lunch, Category: meals, Date

### Implementation for User Story 1

- [X] T009 [US1] Write agent instructions section for expense data extraction (amount, currency, description) in expense_agent.py AGENT_INSTRUCTIONS
- [X] T010 [US1] Write agent instructions section for AUD default currency when unspecified in expense_agent.py AGENT_INSTRUCTIONS
- [X] T011 [US1] Write agent instructions section for Report ID generation format EXP-YYYYMMDD-HHMMSS-XXX in expense_agent.py AGENT_INSTRUCTIONS
- [X] T012 [US1] Write agent instructions section for Code Interpreter file creation with expense_report_YYYYMMDD_HHMMSS.txt format in expense_agent.py AGENT_INSTRUCTIONS
- [X] T013 [US1] Write agent instructions section for structured file content format (Report ID, Amount, Currency, Description, Category, Date) in expense_agent.py AGENT_INSTRUCTIONS
- [X] T014 [US1] Write agent instructions section for response confirmation with file path and extracted details in expense_agent.py AGENT_INSTRUCTIONS
- [X] T015 [US1] Write agent instructions section prohibiting clarifying questions when defaults exist in expense_agent.py AGENT_INSTRUCTIONS

**Checkpoint**: User Story 1 complete - agent can record single expenses with all fields and generate .txt files

---

## Phase 4: User Story 2 - Currency Conversion (Priority: P2)

**Goal**: Auto-convert foreign currencies to AUD using real-time exchange rates from Web Search

**Independent Test**: Provide "100 EUR for conference" and verify report contains both EUR amount AND AUD equivalent with exchange rate

### Implementation for User Story 2

- [X] T016 [US2] Write agent instructions section for detecting non-AUD currencies in expense_agent.py AGENT_INSTRUCTIONS
- [X] T017 [US2] Write agent instructions section for Web Search query format "[CURRENCY] to AUD exchange rate today" in expense_agent.py AGENT_INSTRUCTIONS
- [X] T018 [US2] Write agent instructions section for including AUD Equivalent, Exchange Rate, and Exchange Source in file output in expense_agent.py AGENT_INSTRUCTIONS
- [X] T019 [US2] Write agent instructions section for graceful fallback "[conversion unavailable]" when Web Search fails in expense_agent.py AGENT_INSTRUCTIONS

**Checkpoint**: User Story 2 complete - agent converts foreign currencies to AUD with real-time rates

---

## Phase 5: User Story 3 - Batch Expense Processing (Priority: P3)

**Goal**: Process multiple expenses from a single input, creating separate .txt files for each

**Independent Test**: Provide "lunch $20, taxi $15, coffee $5" and verify three separate .txt files are generated with summary response

### Implementation for User Story 3

- [X] T020 [US3] Write agent instructions section for parsing multiple expenses from comma/delimiter-separated input in expense_agent.py AGENT_INSTRUCTIONS
- [X] T021 [US3] Write agent instructions section for creating separate .txt file per expense with sequential timestamps in expense_agent.py AGENT_INSTRUCTIONS
- [X] T022 [US3] Write agent instructions section for batch summary response listing all Report IDs and file paths in expense_agent.py AGENT_INSTRUCTIONS
- [X] T023 [US3] Write agent instructions section for 10-expense batch limit with split advice in expense_agent.py AGENT_INSTRUCTIONS

**Checkpoint**: User Story 3 complete - agent processes up to 10 expenses per input with individual files

---

## Phase 6: User Story 4 - Smart Categorization (Priority: P3)

**Goal**: Auto-categorize expenses into 8 predefined categories based on description context

**Independent Test**: Provide "uber to airport" and verify Category: travel; provide "Netflix" and verify Category: subscriptions

### Implementation for User Story 4

- [X] T024 [US4] Write agent instructions section defining 8 categories with keyword examples (meals, travel, accommodation, supplies, entertainment, utilities, subscriptions, other) in expense_agent.py AGENT_INSTRUCTIONS
- [X] T025 [US4] Write agent instructions section for LLM semantic inference of category from description context in expense_agent.py AGENT_INSTRUCTIONS
- [X] T026 [US4] Write agent instructions section for defaulting to "other" when category is ambiguous in expense_agent.py AGENT_INSTRUCTIONS

**Checkpoint**: User Story 4 complete - agent auto-categorizes all expenses without user input

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, edge cases, and documentation

- [X] T027 Write agent instructions section for error resilience with [MISSING: field] notation for malformed inputs in expense_agent.py AGENT_INSTRUCTIONS
- [X] T028 Write agent instructions section for handling typos and colloquial terms (bucks→AUD, brekkie→meals) in expense_agent.py AGENT_INSTRUCTIONS
- [X] T029 [P] Update quickstart.md with final agent usage examples in specs/001-expense-agent/quickstart.md
- [X] T030 Run quickstart.md validation - test all documented examples work correctly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can proceed sequentially in priority order (P1 → P2 → P3 → P3)
  - US3 and US4 are both P3 and can be done in either order
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - Core MVP functionality
- **User Story 2 (P2)**: Can start after US1 - Adds currency conversion to existing flow
- **User Story 3 (P3)**: Can start after US1 - Extends single expense to batch
- **User Story 4 (P3)**: Can start after US1 - Adds categorization (can parallel with US3)

### Within Each User Story

- Agent instruction sections build on each other
- Each story adds to AGENT_INSTRUCTIONS constant
- Story complete when independent test passes

### Parallel Opportunities

```bash
# Phase 1 parallel:
T001, T002, T003 can run in parallel (different files)

# Phase 3-6: User stories are sequential due to single AGENT_INSTRUCTIONS file
# However, US3 and US4 can be worked on in parallel if coordinated

# Phase 7 parallel:
T027, T028 (agent instructions) then T029, T030 (documentation)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T008)
3. Complete Phase 3: User Story 1 (T009-T015)
4. **STOP and VALIDATE**: Test "spent 50 dollars on lunch" generates correct .txt file
5. Deploy/demo if ready - core expense tracking works!

### Incremental Delivery

1. Setup + Foundational → Agent connects to Azure ✓
2. Add US1 → Single expense recording → **MVP Ready!**
3. Add US2 → Currency conversion works → Deploy/Demo
4. Add US3 → Batch processing works → Deploy/Demo
5. Add US4 → Smart categorization works → Deploy/Demo
6. Polish → Error handling complete → **Production Ready!**

---

## Summary

| Phase | Tasks | Purpose |
|-------|-------|---------|
| Setup | T001-T003 | Project files and dependencies |
| Foundational | T004-T008 | Azure connection and agent framework |
| US1 (P1) | T009-T015 | Single expense recording 🎯 MVP |
| US2 (P2) | T016-T019 | Currency conversion |
| US3 (P3) | T020-T023 | Batch processing |
| US4 (P3) | T024-T026 | Smart categorization |
| Polish | T027-T030 | Error handling and docs |

**Total Tasks**: 30
**Tasks per User Story**: US1=7, US2=4, US3=4, US4=3
**Parallel Opportunities**: Setup phase (3 tasks), US3/US4 coordination possible
**MVP Scope**: Phase 1-3 (T001-T015) = 15 tasks
