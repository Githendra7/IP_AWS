# System Architecture

The ProtoStruc environment isolates operational API logic from heavy artificial intelligence processing chunks, preventing bottlenecks while strictly enforcing typing across the stack via Pydantic.

## The Multi-Agent AI Workflow

ProtoStruc uses **LangGraph** driven by **Groq (`llama-3.3-70b-versatile`)** to create deterministic sequences that mirror collegiate and industry-standard product development pathways. 

### Phase 1: Functional Decomposition
The system takes raw user input (e.g., "A robotic vacuum") and builds an exhaustive breakdown structure. 
1. **Recursion Rule**: It mandates 3 exact levels of depth (`MainFunction` -> `SubFunction` -> `SubSubFunction`).
2. **Technical Enforcements**: Each fundamental action defines explicitly how it passes `Material`, `Energy`, and `Information` flow.
3. **Validator Agent**: A heavily prompted strict supervisor (powered typically by `llama-3.1-8b-instant`) mathematically verifies that inputs conform to JSON bounds and rejects hallucinated data.

### Phase 2: Morphological Charting
Consumes the JSON output of Phase 1 to suggest real-world application vectors.
* Generates an array of concepts ranging from conservative, market-ready iterations, to extremely advanced theoretical boundaries for each decomposed sub-metric.

### Phase 3: Risk Analysis
Executes a simulated FMEA (Failure Mode and Effects Analysis) across the chosen vectors. Determines severity limits and scores variables utilizing classic systems engineering paradigms.

---

## Authentication Mapping

ProtoStruc utilizes a manual JWT-minting pipeline backed directly against Supabase infrastructure.
- Valid tokens map straight to a user's UUID.
- Reset modules are securely bound to `uuid_generate_v4()` generation triggers, with absolute 15-minute expiration lifespans locked to UTC timespaces.

## Frontend State Mapping

The UI handles localized hydration dynamically across responsive layers:
* Sidebar parameters utilize `isSidebarOpen` overlaying logic spanning independent mobile hooks vs desktop breakpoints (`md:-ml-72`).
* External SDK wrappers (`lib/api.ts`) handle standard API intercepts throwing native Javascript Error limits upward to be cleanly trapped in `motion.div` alert cards.
