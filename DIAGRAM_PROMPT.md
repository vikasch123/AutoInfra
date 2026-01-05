# Architecture Diagram Generation Prompt

Use this prompt with AI diagramming tools (Mermaid, Draw.io, Excalidraw, ChatGPT, Claude, etc.) to generate the AutoInfra.ai architecture diagram.

---

## Prompt for AI Diagramming Tool

```
Create a system architecture diagram for AutoInfra.ai - an AI-powered infrastructure as code generation platform.

**System Components:**

Frontend:
- Web UI (HTML/CSS/JavaScript) - Single Page Application
- Mermaid.js for diagram rendering
- Prism.js for code syntax highlighting

Backend:
- FastAPI server (Python)
- Intent Extractor (LLM-based or keyword matching)
- Terraform Generator (Jinja2 templates)
- Diagram Generator (Mermaid syntax)
- Terraform Validator (pattern matching)
- Cost Estimator (pricing calculations)
- Security Analyzer (pattern matching)

External Services:
- OpenAI API (optional, for intent extraction)

**Data Flow (show with arrows):**

1. User Request → FastAPI /generate endpoint
2. FastAPI → Intent Extractor (extracts structured JSON from natural language)
3. Intent Extractor → Terraform Generator (uses Jinja2 templates to generate code)
4. Intent Extractor → Diagram Generator (creates Mermaid diagram syntax)
5. Terraform Code → Terraform Validator (validates syntax and structure)
6. Intent + Resource Count → Cost Estimator (calculates monthly costs)
7. Intent + Terraform Code → Security Analyzer (analyzes security posture)
8. Intent → Explanation Generator (creates markdown explanation)
9. All Results → FastAPI Response (JSON)
10. FastAPI → Frontend (displays in tabs: Code, Diagram, Validation, Cost, Security, Explanation)
11. Frontend → Mermaid.js (renders diagram syntax to SVG)

**Key Features to Highlight:**
- Intent extraction supports both LLM (OpenAI) and mock mode (keyword matching)
- Template-based Terraform generation (Jinja2)
- Pattern matching for validation and security analysis
- Client-side diagram rendering (Mermaid.js)
- All analysis is deterministic (no AI, just rules)

**Style:**
- Use clear component boxes
- Show data flow with labeled arrows
- Group related components
- Use different colors for Frontend, Backend, External Services
- Include brief labels on arrows showing what data flows (e.g., "Intent JSON", "Terraform Code", "Validation Results")

Create a professional, clean diagram suitable for presentations.
```

---

## Alternative: Mermaid Code Prompt

If using Mermaid directly, use this:

```
Generate Mermaid flowchart code for AutoInfra.ai architecture showing:

1. User sends request to FastAPI
2. FastAPI calls Intent Extractor (LLM or keyword matching)
3. Intent Extractor returns JSON intent
4. Terraform Generator uses Jinja2 templates + intent → Terraform code
5. Diagram Generator uses intent → Mermaid syntax
6. Terraform Validator analyzes code → validation results
7. Cost Estimator uses intent → cost breakdown
8. Security Analyzer uses intent + code → security analysis
9. All results combined → JSON response
10. Frontend displays in tabs
11. Mermaid.js renders diagram

Show components as boxes, data flow as arrows with labels.
Use subgraphs for Frontend, Backend, External Services.
```

---

## Quick Text Description for Manual Diagrams

**AutoInfra.ai Architecture:**

```
[User] → [Web UI] → [FastAPI /generate]
                          ↓
                    [Intent Extractor]
                    (OpenAI or Keyword)
                          ↓
                    [Intent JSON]
                    ↙    ↓    ↘
        [Terraform Gen] [Diagram Gen] [Explanation Gen]
        (Jinja2)        (Mermaid)     (Template)
              ↓              ↓              ↓
        [Terraform Code] [Mermaid Text] [Markdown]
              ↓
    [Validator] [Cost Estimator] [Security Analyzer]
    (Pattern)   (Pricing)        (Pattern)
              ↓              ↓              ↓
        [Validation]    [Cost Data]    [Security Report]
              ↓              ↓              ↓
                    [JSON Response]
                          ↓
                    [Frontend Tabs]
                    (Code/Diagram/Validation/Cost/Security/Explanation)
                          ↓
                    [Mermaid.js]
                    (Renders SVG)
```

---

## For ChatGPT/Claude (Conversational)

```
I need an architecture diagram for AutoInfra.ai. It's a web app that converts natural language to Terraform infrastructure code.

Flow:
1. User types request in web UI
2. FastAPI backend receives it
3. Intent Extractor (uses OpenAI or keyword matching) extracts structured data
4. Terraform Generator uses Jinja2 templates to create Terraform code
5. Diagram Generator creates Mermaid diagram syntax
6. Validator checks code (pattern matching)
7. Cost Estimator calculates costs (pricing lookup)
8. Security Analyzer scores security (pattern matching)
9. All results sent back as JSON
10. Frontend displays in 6 tabs
11. Mermaid.js renders diagram to SVG

Show this as a flowchart with components and data flow arrows. Make it presentation-ready.
```

---

Use any of these prompts with your preferred diagramming tool!
