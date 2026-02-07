# Quickstart: Intelligent Expense Tracking Agent

**Feature**: 001-expense-agent  
**Date**: 2026-02-07

## Prerequisites

1. **Azure AI Foundry Access**: Project with gpt-4o model deployed
2. **Azure CLI**: Installed and logged in (`az login`)
3. **Python 3.11+**: Installed on your system

## Setup (2 minutes)

### 1. Install Dependencies

```powershell
pip install azure-ai-projects>=2.0.0b1 azure-identity
```

### 2. Configure the Agent

Edit `expense_agent.py` and update the configuration at the top:

```python
USER_ENDPOINT = "https://your-resource.services.ai.azure.com/api/projects/your-project"
AGENT_NAME = "expense-tracker-agent-v3"
MODEL_DEPLOYMENT_NAME = "gpt-4o"
```

### 3. Authenticate

```powershell
az login
```

## Running the Agent

### Interactive Mode (CLI)

```powershell
python expense_agent.py
```

You'll see:
```
============================================================
Expense Tracking Agent
(with Code Interpreter + Web Search)
============================================================

Enter your expense information (or 'quit' to exit)
Examples:
  - 'I have an expense of 50 USD for lunch'
  - '100 EUR for office supplies, convert to USD'
  - '75 pounds for taxi in London'

The agent can search the web for real-time info (e.g., exchange rates)
and will create a text file for each expense.
------------------------------------------------------------

Your expense: 
```

### Module Import (API Integration)

```python
from expense_agent import process_expense

response = process_expense("spent 50 dollars on lunch")
print(response)
```

## Usage Examples

### Single Expense

**Input**: `spent 50 dollars on lunch`

**Output**:
```
✓ Expense recorded!

Report ID: EXP-20260207-143052-847
Amount: 50.00 USD
Description: lunch
Category: meals
AUD Equivalent: 78.50 AUD

File saved: expense_reports/expense_report_20260207_143052.txt
```

### Currency Conversion

**Input**: `100 EUR for conference registration`

**Output**:
```
✓ Expense recorded!

Report ID: EXP-20260207-143123-456
Amount: 100.00 EUR
Description: conference registration
Category: other
AUD Equivalent: 167.50 AUD (rate: 1.675)

File saved: expense_reports/expense_report_20260207_143123.txt
```

### Batch Expenses

**Input**: `lunch $20, taxi $15, coffee $5`

**Output**:
```
✓ 3 expenses recorded!

1. EXP-20260207-143200-111: $20 lunch (meals)
2. EXP-20260207-143201-222: $15 taxi (travel)
3. EXP-20260207-143202-333: $5 coffee (meals)

Files saved:
- expense_reports/expense_report_20260207_143200.txt
- expense_reports/expense_report_20260207_143201.txt
- expense_reports/expense_report_20260207_143202.txt
```

### No Currency Specified (Defaults to AUD)

**Input**: `paid 30 for parking`

**Output**:
```
✓ Expense recorded!

Report ID: EXP-20260207-143300-789
Amount: 30.00 AUD
Description: parking
Category: travel

File saved: expense_reports/expense_report_20260207_143300.txt
```

## Generated File Format

Each expense creates a `.txt` file in `expense_reports/`:

```text
---EXPENSE REPORT---
Report ID: EXP-20260207-143052-847
Amount: 50.00
Currency: USD
Description: lunch
Category: meals
Date: 2026-02-07T14:30:52
AUD Equivalent: 78.50
Exchange Rate: 1.57
Exchange Source: Web Search (2026-02-07)
---END REPORT---
```

## Troubleshooting

### "Azure CLI not found on path"

Add Azure CLI to PATH manually:
```python
import os
os.environ["PATH"] = r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin" + os.pathsep + os.environ.get("PATH", "")
```

### "DefaultAzureCredential failed"

Use `AzureCliCredential` instead:
```python
from azure.identity import AzureCliCredential
credential = AzureCliCredential()
```

### Agent asks clarifying questions

Check that agent instructions include "MUST NOT ask clarifying questions when reasonable defaults exist."

## Next Steps

- View generated reports in `expense_reports/` folder
- Modify agent instructions for custom behavior
- Integrate with other systems via module import
