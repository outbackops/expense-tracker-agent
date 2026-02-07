# Feature Specification: Intelligent Expense Tracking Agent

**Feature Branch**: `001-expense-agent`  
**Created**: 2026-02-07  
**Status**: Draft  
**Input**: User description: "Build an intelligent expense tracking agent that automatically processes user expense inputs and generates structured expense reports as .txt files."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Single Expense Recording (Priority: P1)

As a user, I want to describe an expense in natural language (e.g., "spent 50 dollars on lunch") and have the agent automatically extract the amount, currency, and description, categorize it, and generate a formatted expense report file.

**Why this priority**: This is the core functionality—without single expense recording, the agent has no purpose. It delivers immediate value by automating what would otherwise be manual data entry and file creation.

**Independent Test**: Can be fully tested by providing a single expense input and verifying a correctly formatted .txt file is generated with all required fields (Report ID, Amount, Currency, Description, Category, Date).

**Acceptance Scenarios**:

1. **Given** the agent is running, **When** user says "spent 50 dollars on lunch", **Then** agent generates a .txt file with Amount: 50, Currency: USD, Description: lunch, Category: meals, and a unique Report ID.
2. **Given** user provides no currency (e.g., "paid 30 for taxi"), **When** agent processes the input, **Then** agent defaults to AUD currency and generates the report.
3. **Given** user provides an expense, **When** agent completes processing, **Then** agent responds with confirmation including the file path and extracted expense details.

---

### User Story 2 - Currency Conversion (Priority: P2)

As a user dealing with foreign expenses, I want the agent to automatically convert foreign currencies to AUD using real-time exchange rates so I can see the equivalent value in my home currency.

**Why this priority**: Currency conversion adds significant value for users with international expenses but builds on top of the core expense recording functionality.

**Independent Test**: Can be tested by providing an expense in a foreign currency (e.g., "100 EUR for hotel") and verifying both the original amount/currency AND the AUD equivalent appear in the generated report.

**Acceptance Scenarios**:

1. **Given** user says "100 EUR for conference registration", **When** agent processes the input, **Then** agent uses Web Search to fetch current EUR/AUD exchange rate and includes both EUR amount and AUD equivalent in the report.
2. **Given** user provides expense in USD, GBP, or other major currency, **When** agent generates report, **Then** the exchange rate source and timestamp are noted in the report.
3. **Given** Web Search is unavailable, **When** agent processes foreign currency, **Then** agent flags the AUD equivalent as "conversion unavailable" rather than failing.

---

### User Story 3 - Batch Expense Processing (Priority: P3)

As a user with multiple expenses to record, I want to describe several expenses in a single input (e.g., "lunch $20, taxi $15, coffee $5") and have the agent create separate report files for each expense.

**Why this priority**: Batch processing improves efficiency for power users but is an enhancement to the core single-expense flow.

**Independent Test**: Can be tested by providing multiple comma-separated expenses and verifying separate .txt files are generated for each, with a summary response listing all file paths.

**Acceptance Scenarios**:

1. **Given** user says "lunch $20, taxi $15, coffee $5", **When** agent processes the input, **Then** agent creates three separate .txt files, one for each expense.
2. **Given** batch input is processed, **When** agent responds, **Then** response includes a summary with all expense details and their respective file paths.
3. **Given** user provides more than 10 expenses in one input, **When** agent processes, **Then** agent advises user to split the input into smaller batches.

---

### User Story 4 - Smart Categorization (Priority: P3)

As a user, I want the agent to automatically categorize my expenses based on the description context so I don't have to specify categories manually.

**Why this priority**: Auto-categorization reduces user effort but is not essential for the core recording function.

**Independent Test**: Can be tested by providing expenses with various descriptions and verifying appropriate categories are assigned (e.g., "uber ride" → travel, "office supplies at Staples" → supplies).

**Acceptance Scenarios**:

1. **Given** user says "dinner at restaurant", **When** agent processes, **Then** agent assigns category "meals".
2. **Given** user says "uber to airport", **When** agent processes, **Then** agent assigns category "travel".
3. **Given** user says "Netflix subscription", **When** agent processes, **Then** agent assigns category "subscriptions".
4. **Given** description is ambiguous, **When** agent cannot determine category confidently, **Then** agent assigns "other" category.

---

### Edge Cases

- What happens when user provides amount without any description? → Agent flags description as "[MISSING: description]" and still generates report with available data.
- What happens when user provides non-numeric amount (e.g., "spent some money on lunch")? → Agent flags amount as "[MISSING: amount]" and includes the original text in notes.
- What happens when user provides invalid currency code? → Agent attempts to interpret (e.g., "bucks" → AUD, "euros" → EUR) or defaults to AUD if unrecognizable.
- What happens when expense_reports folder doesn't exist? → Agent creates the folder automatically via Code Interpreter.
- How does system handle special characters in descriptions? → Agent sanitizes for filename safety while preserving original in report content.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Agent MUST extract numeric amount from natural language expense descriptions.
- **FR-002**: Agent MUST identify currency from input, defaulting to AUD when unspecified.
- **FR-003**: Agent MUST extract meaningful description/purpose from user input.
- **FR-004**: Agent MUST auto-categorize expenses into one of: meals, travel, accommodation, supplies, entertainment, utilities, subscriptions, other.
- **FR-005**: Agent MUST generate unique Report IDs in format `EXP-YYYYMMDD-HHMMSS-XXX` (XXX = random 3-digit number).
- **FR-006**: Agent MUST create .txt files using Code Interpreter tool (not local Python file operations).
- **FR-007**: Agent MUST save all reports to `expense_reports/` folder with timestamped filenames.
- **FR-008**: Agent MUST use Web Search tool to fetch real-time exchange rates for currency conversion.
- **FR-009**: Agent MUST include both original currency amount AND AUD equivalent for foreign currencies.
- **FR-010**: Agent MUST support batch processing of multiple expenses separated by commas or natural delimiters.
- **FR-011**: Agent MUST respond with confirmation including file path and key expense details after each interaction.
- **FR-012**: Agent MUST NOT ask clarifying questions when reasonable defaults exist.
- **FR-013**: Agent MUST handle malformed inputs by extracting maximum available information and flagging missing fields.
- **FR-014**: Agent MUST validate that amounts are numeric and currencies are valid ISO 4217 codes.

### Key Entities

- **Expense Report**: A structured record containing Report ID, Amount, Currency, Description, Category, Date, and AUD Equivalent. Saved as individual .txt files.
- **Category**: One of eight predefined expense types (meals, travel, accommodation, supplies, entertainment, utilities, subscriptions, other) assigned automatically based on description context.
- **Exchange Rate**: Real-time currency conversion rate fetched via Web Search, including source and timestamp metadata.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can record a single expense and receive a generated .txt file in under 10 seconds.
- **SC-002**: 95% of expense inputs result in successful file generation (graceful handling of edge cases).
- **SC-003**: Auto-categorization accuracy reaches 85% for common expense types (meals, travel, supplies).
- **SC-004**: Currency conversion provides AUD equivalent within 5% of actual market rate at time of query.
- **SC-005**: Users can process up to 10 expenses in a single batch input successfully.
- **SC-006**: Zero clarifying questions asked for inputs containing amount and any context/description.
- **SC-007**: All generated reports contain valid Report ID, timestamp, and at least 3 of 6 core fields populated.
- **SC-008**: Agent response always includes file path confirmation for successful expense recordings.

## Assumptions

- User has Azure AI Foundry access with gpt-4o model deployed.
- Code Interpreter and Web Search tools are available and enabled in Azure AI Foundry.
- AUD is the home currency for all users (default when unspecified).
- Exchange rates are acceptable with up to 15-minute delay from real-time.
- Users primarily interact in English language.
- Expense amounts are assumed to be positive values.
