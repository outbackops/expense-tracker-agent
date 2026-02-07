<!--
=== SYNC IMPACT REPORT ===
Version change: 0.0.0 → 1.0.0 (MAJOR - initial constitution ratification)
Modified principles: N/A (initial creation)
Added sections:
  - Core Principles (10 principles)
  - Tool Automation Standards
  - Agent Behavior Standards
  - Governance
Removed sections: N/A
Templates requiring updates:
  - plan-template.md ✅ (compatible - Constitution Check section exists)
  - spec-template.md ✅ (compatible - Requirements section aligns)
  - tasks-template.md ✅ (compatible - Phase structure works)
Follow-up TODOs: None
========================
-->

# ExpenseTracker Agent Constitution

## Core Principles

### I. Expense Data Validation & Accuracy
All expense amounts MUST be numeric values (integers or decimals). Currency codes MUST be valid ISO 4217 three-letter codes (e.g., AUD, USD, EUR, GBP). Descriptions MUST be non-empty and meaningful (minimum 2 characters, maximum 500 characters). Invalid data MUST be flagged in output, never silently discarded.

### II. Automated File Generation
All expense reports MUST be created using the Code Interpreter tool—never local Python file operations. Generated files MUST be plain `.txt` format with consistent structure: Report ID, Amount, Currency, Description, Category, Date, AUD Equivalent. Files MUST be saved to the `expense_reports/` folder with timestamped filenames (`expense_report_YYYYMMDD_HHMMSS.txt`).

### III. Real-Time Intelligence
The Web Search tool MUST be used for: currency conversion to AUD using current exchange rates, vendor/merchant verification when company names are mentioned, and tax categorization guidance when users inquire about deductibility. Web search results MUST be cited in the agent's response when influencing output.

### IV. Zero User Friction
Default currency MUST be AUD (Australian Dollar) when no currency is specified. The agent MUST auto-detect expense categories without user input. The agent MUST NOT ask clarifying questions when reasonable defaults exist. If the user provides an amount and any context, proceed immediately with file generation.

### V. Structured Output Consistency
Every agent response MUST include: (1) confirmation of expense recorded, (2) extracted fields (Amount, Currency, Description, Category), (3) AUD equivalent if foreign currency, (4) full file path of the generated report. Output format MUST be predictable for API consumers.

### VI. Error Resilience
Malformed inputs MUST be handled gracefully by extracting maximum available information. Missing fields MUST be flagged in the output with `[MISSING: field_name]` notation. The agent MUST never fail silently—always provide feedback on what was processed and what was incomplete.

### VII. Audit Trail Compliance
Every generated expense report MUST include: unique Report ID (format: `EXP-YYYYMMDD-HHMMSS-XXX` where XXX is a random 3-digit number), creation timestamp in ISO 8601 format, and all extracted expense fields. Report IDs MUST be included in both the file content and the agent's response.

### VIII. Multi-Expense Batch Processing
The agent MUST support parsing multiple expenses from a single user input (e.g., "lunch $20, taxi $15, coffee $5"). Each expense MUST generate a separate report file. Batch responses MUST summarize all processed expenses with their respective file paths.

### IX. Smart Categorization
Expenses MUST be automatically categorized using LLM reasoning based on description context. Valid categories: `meals`, `travel`, `accommodation`, `supplies`, `entertainment`, `utilities`, `subscriptions`, `other`. Category inference MUST be based on keywords and semantic understanding—never require user input for categorization.

### X. Currency Intelligence
Foreign currencies MUST be auto-converted to AUD using real-time exchange rates fetched via Web Search tool. Both original amount/currency AND AUD equivalent MUST appear in the generated report. Exchange rate source and fetch timestamp MUST be noted in the report.

## Tool Automation Standards

All business logic MUST reside in the agent's system instructions—Python code serves only as a thin client for Azure connection and response display. The following tools are authorized and MUST be used for their designated purposes:

| Tool | Purpose | Mandatory Use Case |
|------|---------|-------------------|
| Code Interpreter | File generation | Every expense report |
| Web Search | Real-time data | Currency conversion, vendor lookup |

No external APIs, databases, or user-managed connections are permitted. All processing happens within the agent sandbox.

## Agent Behavior Standards

1. **Response Time**: Agent MUST respond within a single turn—no multi-turn clarification dialogues for standard expense inputs.
2. **Idempotency**: Duplicate inputs SHOULD generate new reports (append-only model, no deduplication).
3. **Language**: Agent MUST handle typos, shorthand (e.g., "brekkie" → meals), and colloquial currency references (e.g., "bucks" → AUD).
4. **Batch Limit**: Agent SHOULD process up to 10 expenses per input; beyond 10, advise user to split input.

## Governance

This constitution supersedes all other development practices for the ExpenseTracker Agent project. Amendments require:
1. Documentation of proposed change
2. Version increment (MAJOR for principle changes, MINOR for additions, PATCH for clarifications)
3. Update to agent system instructions to reflect constitutional changes

All code changes, agent instruction updates, and feature additions MUST verify compliance with these principles. Complexity beyond these standards MUST be justified in writing.

**Version**: 1.0.0 | **Ratified**: 2026-02-07 | **Last Amended**: 2026-02-07
