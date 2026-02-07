# Research: Intelligent Expense Tracking Agent

**Feature**: 001-expense-agent  
**Date**: 2026-02-07  
**Status**: Complete

## Research Tasks

### 1. Azure AI Foundry Agent SDK Patterns

**Task**: Research best practices for Azure AI Foundry agent creation using Python SDK

**Decision**: Use `AIProjectClient` with `PromptAgentDefinition` for agent creation

**Rationale**:
- `azure-ai-projects` SDK provides `AIProjectClient` as the primary interface
- `PromptAgentDefinition` allows defining agent with model, instructions, and tools
- `create_version()` method creates or updates agent definitions
- OpenAI-compatible client obtained via `get_openai_client()` for responses

**Alternatives Considered**:
- Direct OpenAI API calls: Rejected—lacks Azure AI Foundry tool integration
- REST API directly: Rejected—SDK provides cleaner abstraction
- Assistants API: Rejected—PromptAgentDefinition is the recommended pattern for Foundry agents

**Code Pattern**:
```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, CodeInterpreterTool, WebSearchPreviewTool

project_client = AIProjectClient(endpoint=ENDPOINT, credential=credential)
agent = project_client.agents.create_version(
    agent_name=AGENT_NAME,
    definition=PromptAgentDefinition(
        model=MODEL_NAME,
        instructions=INSTRUCTIONS,
        tools=[CodeInterpreterTool(), WebSearchPreviewTool()],
    ),
)
openai_client = project_client.get_openai_client()
response = openai_client.responses.create(
    input=[{"role": "user", "content": user_input}],
    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
)
```

---

### 2. Code Interpreter Tool for File Generation

**Task**: Research how Code Interpreter creates and returns files in Azure AI Foundry

**Decision**: Code Interpreter executes Python code in agent sandbox, can create files that persist for download

**Rationale**:
- Code Interpreter runs Python in isolated sandbox within agent
- Files created via `open()` and `write()` in sandbox are accessible
- Agent instructions can direct Code Interpreter to create specific file formats
- No local file system access needed—agent handles everything

**Alternatives Considered**:
- Local Python file operations: Rejected—violates constitution principle II
- Azure Blob Storage: Rejected—adds external dependency
- Base64 encoding in response: Rejected—less user-friendly than downloadable files

**Implementation Notes**:
- Agent instructions must explicitly tell LLM to use Code Interpreter for file creation
- Timestamp generation should happen in Code Interpreter Python code
- Report ID generation (random component) handled by Code Interpreter

---

### 3. Web Search Tool for Currency Conversion

**Task**: Research Web Search tool capabilities for real-time exchange rate lookup

**Decision**: Use `WebSearchPreviewTool()` (no connection required) for exchange rate queries

**Rationale**:
- `WebSearchPreviewTool` is built-in and requires no user-managed connections
- Agent instructions can direct searches for "EUR to AUD exchange rate"
- Results are current within minutes of real-time
- No external forex API needed

**Alternatives Considered**:
- BingGroundingTool with managed connection: Rejected—requires user setup
- External forex API (exchangerate-api.com): Rejected—adds dependency
- Hardcoded rates: Rejected—violates constitution principle III

**Implementation Notes**:
- Agent instructions should specify to search for "[CURRENCY] to AUD exchange rate today"
- Instruct agent to cite source and note timestamp in report
- Handle search failure gracefully with "[conversion unavailable]"

---

### 4. Authentication Strategy

**Task**: Research authentication options for Azure AI Foundry

**Decision**: Use `AzureCliCredential` with PATH workaround for fresh Azure CLI installations

**Rationale**:
- `DefaultAzureCredential` chains multiple credential types but may not find Azure CLI in PATH
- `AzureCliCredential` directly uses `az` command after `az login`
- Adding Azure CLI path to environment ensures credential resolution

**Alternatives Considered**:
- DefaultAzureCredential only: Rejected—PATH issues on fresh installations
- Service Principal: Rejected—adds complexity for single-user scenario
- Managed Identity: Rejected—only works in Azure-hosted environments

**Code Pattern**:
```python
import os
os.environ["PATH"] = r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin" + os.pathsep + os.environ.get("PATH", "")
from azure.identity import AzureCliCredential
credential = AzureCliCredential()
```

---

### 5. Expense Categorization Strategy

**Task**: Research approach for automatic expense categorization

**Decision**: Pure LLM inference via system instructions—no code-based classification

**Rationale**:
- LLM reasoning handles semantic understanding (e.g., "brekkie" → meals)
- Eight categories are well-defined and described in instructions
- No training data or ML model needed
- Handles ambiguity via "other" category

**Alternatives Considered**:
- Keyword matching in Python: Rejected—brittle, can't handle variations
- ML classification model: Rejected—adds complexity and dependency
- User-specified categories: Rejected—violates zero-friction principle

**Category Definitions** (for agent instructions):
| Category | Keywords/Patterns |
|----------|-------------------|
| meals | food, lunch, dinner, breakfast, coffee, restaurant, cafe |
| travel | uber, taxi, flight, train, bus, fuel, parking, toll |
| accommodation | hotel, airbnb, motel, lodging, stay |
| supplies | office, stationery, printer, paper, equipment |
| entertainment | movie, concert, event, tickets, games |
| utilities | electricity, water, gas, internet, phone |
| subscriptions | netflix, spotify, software, membership, monthly |
| other | default when no clear match |

---

### 6. Report ID Format

**Task**: Research unique ID generation strategy

**Decision**: Format `EXP-YYYYMMDD-HHMMSS-XXX` generated in Code Interpreter

**Rationale**:
- Timestamp component ensures chronological ordering
- Random 3-digit suffix (XXX) prevents collisions within same second
- Human-readable format aids manual lookup
- Generated within Code Interpreter for consistency

**Implementation**:
```python
from datetime import datetime
import random
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
suffix = str(random.randint(100, 999))
report_id = f"EXP-{timestamp}-{suffix}"
```

---

## Summary

All research tasks complete. No NEEDS CLARIFICATION items remain.

| Topic | Decision | Key Rationale |
|-------|----------|---------------|
| SDK Pattern | AIProjectClient + PromptAgentDefinition | Official Azure AI Foundry pattern |
| File Generation | Code Interpreter tool | Constitution principle II compliance |
| Currency Conversion | WebSearchPreviewTool | No managed connection required |
| Authentication | AzureCliCredential + PATH fix | Works with fresh Azure CLI install |
| Categorization | LLM inference only | Semantic understanding, zero code |
| Report ID | EXP-YYYYMMDD-HHMMSS-XXX | Unique, human-readable, chronological |
