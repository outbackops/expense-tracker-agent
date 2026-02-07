# Implementation Plan: Intelligent Expense Tracking Agent

**Branch**: `001-expense-agent` | **Date**: 2026-02-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-expense-agent/spec.md`

## Summary

Build an intelligent expense tracking agent using Azure AI Foundry that automatically processes natural language expense inputs, extracts structured data (amount, currency, description), auto-categorizes expenses, converts foreign currencies to AUD using real-time exchange rates, and generates formatted .txt expense reports. The agent uses Code Interpreter for file generation and Web Search for currency conversion—all business logic resides in LLM instructions with Python serving as a thin client.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: azure-ai-projects>=2.0.0b1, azure-identity, openai  
**Storage**: Plain .txt files in `expense_reports/` folder (no database)  
**Testing**: Manual testing via CLI interaction (agent behavior tested through prompts)  
**Target Platform**: Windows/Linux/macOS (cross-platform Python script)  
**Project Type**: Single script with module import capability  
**Performance Goals**: <10 seconds per expense processing (SC-001)  
**Constraints**: No local state between sessions, no external APIs beyond Azure AI Foundry  
**Scale/Scope**: Single user, up to 10 expenses per batch input

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Data Validation | ✅ PASS | FR-001, FR-002, FR-014 require numeric amounts and ISO 4217 currencies |
| II. Automated File Generation | ✅ PASS | FR-006 mandates Code Interpreter for file creation, not local Python |
| III. Real-Time Intelligence | ✅ PASS | FR-008 requires Web Search for exchange rates |
| IV. Zero User Friction | ✅ PASS | FR-002 defaults to AUD, FR-012 prohibits clarifying questions |
| V. Structured Output | ✅ PASS | FR-011 requires confirmation with file path and details |
| VI. Error Resilience | ✅ PASS | FR-013 requires graceful handling of malformed inputs |
| VII. Audit Trail | ✅ PASS | FR-005 defines Report ID format `EXP-YYYYMMDD-HHMMSS-XXX` |
| VIII. Batch Processing | ✅ PASS | FR-010 requires multi-expense support |
| IX. Smart Categorization | ✅ PASS | FR-004 defines 8 categories with LLM inference |
| X. Currency Intelligence | ✅ PASS | FR-008, FR-009 require conversion and dual display |

**Pre-Research Gate**: ✅ ALL PRINCIPLES SATISFIED - Proceed to Phase 0

### Post-Design Re-Check (Phase 1 Complete)

| Principle | Status | Design Artifact Evidence |
|-----------|--------|--------------------------|
| I. Data Validation | ✅ PASS | data-model.md: Validation Rules section defines numeric/ISO 4217 checks |
| II. Automated File Generation | ✅ PASS | contracts/agent-api.md: CodeInterpreterTool required for every expense |
| III. Real-Time Intelligence | ✅ PASS | research.md: WebSearchPreviewTool decision for exchange rates |
| IV. Zero User Friction | ✅ PASS | data-model.md: AUD default, agent-api.md: no clarification responses |
| V. Structured Output | ✅ PASS | contracts/agent-api.md: Response format includes all required fields |
| VI. Error Resilience | ✅ PASS | data-model.md: [MISSING: field] notation defined |
| VII. Audit Trail | ✅ PASS | data-model.md: Report ID format `EXP-YYYYMMDD-HHMMSS-XXX` specified |
| VIII. Batch Processing | ✅ PASS | data-model.md: Batch Processing section with sequential files |
| IX. Smart Categorization | ✅ PASS | data-model.md: Category enumeration with 8 values |
| X. Currency Intelligence | ✅ PASS | data-model.md: aud_equivalent, exchange_rate fields defined |

**Post-Design Gate**: ✅ ALL PRINCIPLES SATISFIED - Ready for Phase 2 tasks

## Project Structure

### Documentation (this feature)

```text
specs/001-expense-agent/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (API contracts)
└── tasks.md             # Phase 2 output (NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
expense_agent.py         # Main agent script (thin client)
requirements.txt         # Python dependencies
expense_reports/         # Generated expense report files (.txt)
```

**Structure Decision**: Single-file architecture chosen per constitution requirement that "Python code serves only as a thin client." All business logic lives in agent system instructions, not in Python code structure. No src/, tests/, or multi-file organization needed.

## Complexity Tracking

> No violations to justify—design fully complies with constitution.
