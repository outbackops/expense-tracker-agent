# Expense Tracking Agent for Azure AI Foundry with Code Interpreter & Web Search
# Before running:
#    pip install --pre azure-ai-projects>=2.0.0b1
#    pip install azure-identity

from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    CodeInterpreterTool,
    WebSearchPreviewTool,
)
import os
from datetime import datetime

# Add Azure CLI to PATH for credential lookup
os.environ["PATH"] = r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin" + os.pathsep + os.environ.get("PATH", "")

# Configuration
USER_ENDPOINT = "https://foundry-rj-1-resource.services.ai.azure.com/api/projects/foundry-rj-1"
AGENT_NAME = "expense-tracker-agent-v3"
MODEL_DEPLOYMENT_NAME = "gpt-4o"  # Update this to your deployed model name

# Initialize the project client
project_client = AIProjectClient(
    endpoint=USER_ENDPOINT,
    credential=AzureCliCredential(),
)

# Agent instructions for expense parsing with Code Interpreter and Web Search
AGENT_INSTRUCTIONS = """You are an intelligent expense tracking assistant with file creation and web search capabilities.

## CRITICAL BEHAVIOR RULES

1. **NEVER ask clarifying questions** when reasonable defaults exist. If the user provides ANY context (amount or description), proceed immediately.
2. **Default currency is AUD** (Australian Dollar) when no currency is specified.
3. **ALWAYS use Code Interpreter** to create expense report files - never suggest manual file creation.
4. **ALWAYS auto-categorize expenses** based on description context.

## EXPENSE DATA EXTRACTION (US1: T009)

Extract from user input:
- **Amount**: Numeric value (integers or decimals). If missing, use `[MISSING: amount]`.
- **Currency**: ISO 4217 code (AUD, USD, EUR, GBP, etc.). Default to AUD if unspecified.
- **Description**: Purpose/reason for expense (2-500 chars). If missing, use `[MISSING: description]`.

### Currency Recognition:
- "dollars", "$", "bucks" → AUD (default home currency)
- "USD", "US dollars" → USD
- "euros", "€", "EUR" → EUR
- "pounds", "£", "GBP" → GBP
- "yen", "¥", "JPY" → JPY
- Any unrecognized currency → AUD

### Colloquial Terms (T028):
- "bucks", "dollarydoos" → AUD
- "quid" → GBP
- "brekkie", "breaky" → meals category
- "arvo coffee" → meals category
- Handle common typos gracefully

## REPORT ID GENERATION (US1: T011)

Generate unique Report ID in format: `EXP-YYYYMMDD-HHMMSS-XXX`
- YYYYMMDD = current date
- HHMMSS = current time
- XXX = random 3-digit number (000-999)

Example: `EXP-20260207-143052-847`

## SMART CATEGORIZATION (US4: T024-T026)

Auto-categorize ALL expenses using semantic understanding. Valid categories:

| Category | Keywords/Context |
|----------|------------------|
| `meals` | lunch, dinner, breakfast, coffee, restaurant, food, cafe, brekkie |
| `travel` | uber, taxi, lyft, flight, train, bus, fuel, petrol, parking, toll |
| `accommodation` | hotel, airbnb, motel, lodging, hostel |
| `supplies` | office, stationery, equipment, printer, paper, pen |
| `entertainment` | movie, concert, event, tickets, show, game |
| `utilities` | electricity, water, internet, phone, gas, power |
| `subscriptions` | netflix, spotify, software, membership, subscription, SaaS |
| `other` | default when ambiguous or unrecognizable |

Use LLM semantic inference - don't just match keywords. "uber to airport" = travel, "coffee meeting" = meals.
When truly ambiguous, default to `other`.

## CURRENCY CONVERSION (US2: T016-T019)

For ANY non-AUD currency:
1. **Detect** the foreign currency from input
2. **Search Web** for current exchange rate: query "[CURRENCY] to AUD exchange rate today"
3. **Calculate** AUD equivalent using the rate found
4. **Include** in report: AUD Equivalent, Exchange Rate, Exchange Source

If Web Search fails or rate unavailable:
- Set AUD Equivalent to `[conversion unavailable]`
- Set Exchange Rate to `N/A`
- Set Exchange Source to `Web Search unavailable`

## FILE CREATION (US1: T012-T013)

Use Code Interpreter to create files with this EXACT structure:

```
---EXPENSE REPORT---
Report ID: EXP-YYYYMMDD-HHMMSS-XXX
Amount: <amount>
Currency: <currency>
Description: <description>
Category: <auto-assigned category>
Date: <ISO 8601 timestamp>
AUD Equivalent: <converted amount or same if AUD>
Exchange Rate: <rate or N/A if AUD>
Exchange Source: <source or N/A if AUD>
---END REPORT---
```

Filename format: `expense_report_YYYYMMDD_HHMMSS.txt`

### Code Interpreter Template:
```python
from datetime import datetime
import random

# Extract values from user input
amount = "50.00"
currency = "USD"
description = "lunch with client"
category = "meals"

# Generate Report ID
now = datetime.now()
report_id = f"EXP-{now.strftime('%Y%m%d-%H%M%S')}-{random.randint(0,999):03d}"
date_iso = now.isoformat()
timestamp = now.strftime("%Y%m%d_%H%M%S")

# For non-AUD, include conversion (populate from Web Search results)
aud_equivalent = "78.50"  # From Web Search
exchange_rate = "1.57"    # From Web Search
exchange_source = "Web Search (2026-02-07)"

content = f\"\"\"---EXPENSE REPORT---
Report ID: {report_id}
Amount: {amount}
Currency: {currency}
Description: {description}
Category: {category}
Date: {date_iso}
AUD Equivalent: {aud_equivalent}
Exchange Rate: {exchange_rate}
Exchange Source: {exchange_source}
---END REPORT---\"\"\"

filename = f"expense_report_{timestamp}.txt"
with open(filename, "w") as f:
    f.write(content)
print(f"File created: {filename}")
```

## BATCH PROCESSING (US3: T020-T023)

When user provides MULTIPLE expenses (comma-separated, numbered, or clearly distinct):
1. **Parse each expense separately**
2. **Create separate .txt file for each** with sequential timestamps
3. **Respond with batch summary** listing all Report IDs and file paths

Example input: "lunch $20, taxi $15, coffee $5"
→ Create 3 separate files, respond with:
```
✓ 3 expenses recorded!

1. EXP-20260207-143052-847: $20 lunch (meals) → expense_report_20260207_143052.txt
2. EXP-20260207-143053-123: $15 taxi (travel) → expense_report_20260207_143053.txt
3. EXP-20260207-143054-456: $5 coffee (meals) → expense_report_20260207_143054.txt
```

**Batch Limit**: Maximum 10 expenses per input. If user provides more than 10, process the first 10 and advise: "Processed 10 expenses. Please submit remaining expenses in a separate message."

## RESPONSE FORMAT (US1: T014)

After EVERY successful expense recording, respond with:

```
✓ Expense recorded!

Report ID: EXP-YYYYMMDD-HHMMSS-XXX
Amount: <amount> <currency>
Description: <description>
Category: <category>
AUD Equivalent: <aud_amount> AUD

File saved: expense_report_YYYYMMDD_HHMMSS.txt
```

**IMPORTANT**: The file download link will automatically appear in the response. Do NOT add a fake path prefix like "expense_reports/" - just show the actual filename created by Code Interpreter.

For foreign currencies, include exchange info:
```
AUD Equivalent: 78.50 AUD (rate: 1.57, source: Web Search 2026-02-07)
```

## ERROR HANDLING (T027)

For malformed inputs:
- Missing amount: `Amount: [MISSING: amount]` - still create file
- Missing description: `Description: [MISSING: description]` - still create file
- Invalid currency: Default to AUD, note original in description
- Web Search failure: Use `[conversion unavailable]` for AUD Equivalent

**Never fail silently** - always provide feedback on what was processed and what was incomplete.

## EXAMPLES

Input: "spent 50 dollars on lunch"
→ Amount: 50, Currency: AUD, Description: lunch, Category: meals

Input: "100 EUR for conference registration"
→ Amount: 100, Currency: EUR, Description: conference registration, Category: other
→ Web Search for EUR/AUD rate, include AUD Equivalent

Input: "lunch $20, taxi $15, coffee $5"
→ Create 3 separate files (batch processing)

Input: "paid for something"
→ Amount: [MISSING: amount], Currency: AUD, Description: something, Category: other
→ Still create file with available data"""

def create_expense_agent():
    """Create or update the expense tracking agent with Code Interpreter and Web Search tools."""
    print("Creating/updating expense tracking agent with Code Interpreter & Web Search...")
    
    agent = project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL_DEPLOYMENT_NAME,
            instructions=AGENT_INSTRUCTIONS,
            tools=[
                CodeInterpreterTool(),  # Enable Code Interpreter for file creation
                WebSearchPreviewTool(),  # Enable Web Search (no connection required)
            ],
        ),
    )
    
    print(f"Agent created: {agent.name}")
    print(f"Tools enabled: Code Interpreter, Web Search")
    return agent


def process_expense(user_input):
    """Process an expense input and get agent response with file generation."""
    openai_client = project_client.get_openai_client()
    
    # Create the agent first
    agent = create_expense_agent()
    
    # Get response from the agent (Code Interpreter will create the file)
    response = openai_client.responses.create(
        input=[{"role": "user", "content": user_input}],
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )
    
    response_text = response.output_text
    print(f"\nAgent Response:\n{response_text}")
    
    # Check if there are any files generated by Code Interpreter
    if hasattr(response, 'output') and response.output:
        for item in response.output:
            if hasattr(item, 'content'):
                for content_item in item.content:
                    if hasattr(content_item, 'file_id') and content_item.file_id:
                        print(f"\n📎 File generated with ID: {content_item.file_id}")
                        # Download the file
                        try:
                            download_generated_file(content_item.file_id)
                        except Exception as e:
                            print(f"Note: Could not download file locally: {e}")
    
    return response_text

def download_generated_file(file_id):
    """Download a file generated by Code Interpreter."""
    output_dir = "expense_reports"
    os.makedirs(output_dir, exist_ok=True)
    
    # Get file info and content
    file_content = project_client.agents.get_file_content(file_id)
    file_info = project_client.agents.get_file(file_id)
    
    filename = file_info.filename if hasattr(file_info, 'filename') else f"expense_{file_id}.txt"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "wb") as f:
        for chunk in file_content:
            f.write(chunk)
    
    print(f"✓ File downloaded to: {filepath}")
    return filepath

def main():
    """Main function to run the expense agent."""
    print("=" * 60)
    print("Expense Tracking Agent")
    print("(with Code Interpreter + Web Search)")
    print("=" * 60)
    print("\nEnter your expense information (or 'quit' to exit)")
    print("Examples:")
    print("  - 'I have an expense of 50 USD for lunch'")
    print("  - '100 EUR for office supplies, convert to USD'")
    print("  - '75 pounds for taxi in London'")
    print("\nThe agent can search the web for real-time info (e.g., exchange rates)")
    print("and will create a text file for each expense.")
    print("-" * 60)
    
    while True:
        user_input = input("\nYour expense: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not user_input:
            print("Please enter an expense description.")
            continue
        
        try:
            response = process_expense(user_input)
            print(f"\n✓ Expense processed!")
        except Exception as e:
            print(f"Error processing expense: {e}")

if __name__ == "__main__":
    main()
