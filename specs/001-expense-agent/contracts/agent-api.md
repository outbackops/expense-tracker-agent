# Agent API Contract: Intelligent Expense Tracking Agent

**Feature**: 001-expense-agent  
**Date**: 2026-02-07  
**Version**: 1.0.0

## Overview

This document defines the contract between the Python client and the Azure AI Foundry agent. The agent is invoked via the OpenAI-compatible Responses API with an agent reference.

## Endpoint

```
POST /responses
```

**Base URL**: Obtained via `project_client.get_openai_client()`

## Request Format

### Single Expense

```json
{
  "input": [
    {
      "role": "user",
      "content": "spent 50 dollars on lunch"
    }
  ],
  "extra_body": {
    "agent": {
      "name": "expense-tracker-agent-v3",
      "type": "agent_reference"
    }
  }
}
```

### Batch Expenses

```json
{
  "input": [
    {
      "role": "user",
      "content": "lunch $20, taxi $15, coffee $5"
    }
  ],
  "extra_body": {
    "agent": {
      "name": "expense-tracker-agent-v3",
      "type": "agent_reference"
    }
  }
}
```

## Response Format

### Successful Single Expense

```json
{
  "output_text": "✓ Expense recorded!\n\nReport ID: EXP-20260207-143052-847\nAmount: 50.00 USD\nDescription: lunch\nCategory: meals\nAUD Equivalent: 78.50 AUD\n\nFile saved: expense_reports/expense_report_20260207_143052.txt",
  "output": [
    {
      "content": [
        {
          "type": "text",
          "text": "..."
        },
        {
          "type": "file",
          "file_id": "file-abc123"
        }
      ]
    }
  ]
}
```

### Successful Batch Response

```json
{
  "output_text": "✓ 3 expenses recorded!\n\n1. EXP-20260207-143052-847: $20 lunch (meals) → expense_report_20260207_143052.txt\n2. EXP-20260207-143053-123: $15 taxi (travel) → expense_report_20260207_143053.txt\n3. EXP-20260207-143054-456: $5 coffee (meals) → expense_report_20260207_143054.txt",
  "output": [...]
}
```

### Partial Success (Missing Fields)

```json
{
  "output_text": "⚠️ Expense recorded with warnings!\n\nReport ID: EXP-20260207-143052-847\nAmount: [MISSING: amount]\nDescription: lunch\nCategory: meals\n\nNote: Amount could not be extracted from input.\n\nFile saved: expense_reports/expense_report_20260207_143052.txt"
}
```

### Currency Conversion Response

```json
{
  "output_text": "✓ Expense recorded!\n\nReport ID: EXP-20260207-143052-847\nAmount: 100.00 EUR\nDescription: conference registration\nCategory: other\nAUD Equivalent: 167.50 AUD (rate: 1.675, source: Web Search 2026-02-07)\n\nFile saved: expense_reports/expense_report_20260207_143052.txt"
}
```

## Input Parsing Rules

### Amount Extraction

| Input | Extracted Amount |
|-------|------------------|
| "50 dollars" | 50.00 |
| "$50" | 50.00 |
| "fifty dollars" | 50.00 |
| "spent 50 on..." | 50.00 |
| "paid 50.99" | 50.99 |
| "some money" | [MISSING: amount] |

### Currency Extraction

| Input | Extracted Currency |
|-------|-------------------|
| "50 dollars" | USD |
| "50 USD" | USD |
| "50 bucks" | AUD |
| "50 euros" | EUR |
| "€50" | EUR |
| "£50" | GBP |
| "50" (no currency) | AUD (default) |

### Category Inference

| Description Keywords | Inferred Category |
|---------------------|-------------------|
| lunch, dinner, coffee, restaurant, food | meals |
| uber, taxi, flight, train, bus, fuel, parking | travel |
| hotel, airbnb, motel, lodging | accommodation |
| office, stationery, equipment, printer | supplies |
| movie, concert, event, tickets | entertainment |
| electricity, water, internet, phone | utilities |
| netflix, spotify, subscription, membership | subscriptions |
| (ambiguous/unknown) | other |

## Error Handling

### Agent Response Codes

| Scenario | Agent Behavior |
|----------|----------------|
| Valid expense input | Generate report, return confirmation |
| Missing amount | Flag `[MISSING: amount]`, generate partial report |
| Missing description | Flag `[MISSING: description]`, generate partial report |
| Batch >10 expenses | Process first 10, advise user to split |
| Web Search unavailable | Flag `[conversion unavailable]`, continue |
| Code Interpreter failure | Return error message, no file created |

## Agent Configuration

### Agent Definition

```python
PromptAgentDefinition(
    model="gpt-4o",
    instructions=AGENT_INSTRUCTIONS,  # See agent-instructions.md
    tools=[
        CodeInterpreterTool(),
        WebSearchPreviewTool(),
    ],
)
```

### Required Tools

| Tool | Purpose | Invocation Trigger |
|------|---------|-------------------|
| CodeInterpreterTool | File generation | Every expense (mandatory) |
| WebSearchPreviewTool | Exchange rates | Foreign currency detected |

## File Output Contract

### Generated File Location

```
expense_reports/expense_report_YYYYMMDD_HHMMSS.txt
```

### File Content Schema

```
---EXPENSE REPORT---
Report ID: {EXP-YYYYMMDD-HHMMSS-XXX}
Amount: {decimal}
Currency: {ISO 4217}
Description: {string}
Category: {enum}
Date: {ISO 8601}
[AUD Equivalent: {decimal}]
[Exchange Rate: {decimal}]
[Exchange Source: {string}]
---END REPORT---
```

Fields in `[]` are conditional (included only for foreign currencies).

## Versioning

| Version | Changes |
|---------|---------|
| 1.0.0 | Initial contract definition |

**Breaking Change Policy**: Major version increment required for:
- Changing required response fields
- Modifying file format structure
- Altering category enumeration values
