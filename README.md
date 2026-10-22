# Autonomous Agentic Workflows

A comprehensive implementation of core AI Agent patterns and an end-to-end autonomous customer email triage & action router system.

---

## 🌟 Architecture & Phases

### Phase 1: Core Agentic Patterns (`phase_1/`)
- **Direct & Augmented Prompt Agents**: Base agent architectures with few-shot reasoning.
- **Knowledge-Augmented (RAG) Agents**: Vector embeddings and semantic chunk search for grounded contextual answers.
- **Action Planning Agent**: Decomposes complex user goals into executable sequential sub-tasks.
- **Evaluation Agent**: Evaluates, grades, and validates agentic outputs against rubric criteria.
- **Routing Agent**: Categorizes incoming inquiries and dynamically dispatches tasks to specialized handlers.

### Phase 2: Autonomous Production Workflow (`phase_2/`)
- **Product-Spec Email Router (`agentic_workflow.py`)**: An end-to-end pipeline that ingests customer emails, extracts intent, queries internal knowledge specifications via RAG, plans response actions, and formulates verified customer communications.

---

## 📁 Repository Structure

```text
├── phase_1/
│   ├── direct_prompt_agent.py
│   ├── augmented_prompt_agent.py
│   ├── knowledge_augmented_prompt_agent.py
│   ├── rag_knowledge_prompt_agent.py
│   ├── action_planning_agent.py
│   ├── evaluation_agent.py
│   ├── routing_agent.py
│   └── workflow_agents/
└── phase_2/
    ├── agentic_workflow.py
    ├── Product-Spec-Email-Router.txt
    └── workflow_agents/
```

---

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/flopezabduch/autonomous-agentic-workflows.git
   cd autonomous-agentic-workflows
   ```

2. **Configure your API keys:**
   Create a `.env` file with your credentials:
   ```bash
   OPENAI_API_KEY="your-api-key"
   ```

3. **Run the autonomous workflow:**
   ```bash
   python phase_2/agentic_workflow.py
   ```
