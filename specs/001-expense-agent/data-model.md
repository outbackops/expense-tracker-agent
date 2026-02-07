# Data Model: Intelligent Expense Tracking Agent

**Feature**: 001-expense-agent  
**Date**: 2026-02-07  
**Status**: Complete

## Overview

This agent uses a file-based storage model with no database. Each expense generates a standalone `.txt` file containing all relevant data.

## Entities

### ExpenseReport

The primary entity representing a recorded expense.

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| report_id | string | Yes | Unique identifier | Format: `EXP-YYYYMMDD-HHMMSS-XXX` |
| amount | decimal | Yes | Expense amount | Numeric, positive value |
| currency | string | Yes | ISO 4217 code | 3-letter code (AUD, USD, EUR, etc.) |
| description | string | Yes | Expense purpose | 2-500 characters, non-empty |
| category | enum | Yes | Expense category | One of 8 predefined values |
| date | datetime | Yes | Record timestamp | ISO 8601 format |
| aud_equivalent | decimal | Conditional | AUD conversion | Required if currency ≠ AUD |
| exchange_rate | decimal | Conditional | Conversion rate | Required if currency ≠ AUD |
| exchange_source | string | Conditional | Rate source | Required if currency ≠ AUD |
| notes | string | No | Additional info | Free text, captures original input |

### Category (Enumeration)

| Value | Description | Example Keywords |
|-------|-------------|------------------|
| `meals` | Food and beverages | lunch, dinner, coffee, restaurant |
| `travel` | Transportation | uber, taxi, flight, fuel, parking |
| `accommodation` | Lodging | hotel, airbnb, motel |
| `supplies` | Office/work materials | stationery, equipment, printer |
| `entertainment` | Recreation | movie, concert, tickets |
| `utilities` | Services | electricity, internet, phone |
| `subscriptions` | Recurring services | netflix, software, membership |
| `other` | Uncategorized | default fallback |

## File Format

### Filename Convention

```
expense_report_YYYYMMDD_HHMMSS.txt
```

Example: `expense_report_20260207_143052.txt`

### File Content Structure

```text
---EXPENSE REPORT---
Report ID: EXP-20260207-143052-847
Amount: 50.00
Currency: USD
Description: lunch with client
Category: meals
Date: 2026-02-07T14:30:52
AUD Equivalent: 78.50
Exchange Rate: 1.57
Exchange Source: Web Search (2026-02-07)
---END REPORT---
```

### Field Order (Mandatory)

1. Report ID
2. Amount
3. Currency
4. Description
5. Category
6. Date
7. AUD Equivalent (if foreign currency)
8. Exchange Rate (if foreign currency)
9. Exchange Source (if foreign currency)

### Missing Field Notation

When a required field cannot be extracted:

```text
Amount: [MISSING: amount]
Description: [MISSING: description]
```

## Relationships

```
┌─────────────────────────────────────────────────────────┐
│                    User Input                           │
│  "spent 50 dollars on lunch"                           │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  LLM Processing                         │
│  Extract: amount=50, currency=USD, desc=lunch          │
│  Infer: category=meals                                 │
│  Convert: AUD equivalent via Web Search                │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Code Interpreter                           │
│  Generate: report_id, timestamp                        │
│  Create: expense_report_YYYYMMDD_HHMMSS.txt            │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                expense_reports/                         │
│  expense_report_20260207_143052.txt                    │
└─────────────────────────────────────────────────────────┘
```

## State Transitions

ExpenseReport has no state transitions—it is created once and immutable. The agent follows an append-only model:

| Action | Result |
|--------|--------|
| New expense input | New .txt file created |
| Duplicate input | New .txt file created (no deduplication) |
| Correction request | New .txt file created (original preserved) |

## Validation Rules

### Amount Validation
- Must be parseable as numeric (integer or decimal)
- Must be positive (>0)
- If non-numeric text provided, flag as `[MISSING: amount]`

### Currency Validation
- Must be 3-letter ISO 4217 code
- Common aliases interpreted: "dollars"→USD, "bucks"→AUD, "euros"→EUR, "pounds"→GBP
- Unknown currencies default to AUD

### Description Validation
- Minimum 2 characters
- Maximum 500 characters
- If empty, flag as `[MISSING: description]`

### Category Validation
- Must be one of 8 predefined values
- LLM selects based on description context
- Ambiguous cases default to `other`

## Batch Processing

When multiple expenses are provided in a single input:

```
Input: "lunch $20, taxi $15, coffee $5"

Output:
├── expense_report_20260207_143052.txt  (lunch, $20, meals)
├── expense_report_20260207_143053.txt  (taxi, $15, travel)
└── expense_report_20260207_143054.txt  (coffee, $5, meals)
```

Each expense generates a separate file with sequential timestamps.
