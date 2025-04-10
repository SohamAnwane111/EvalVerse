# EvalVerse 

A Python-based adaptive MCQ (Multiple Choice Question) platform that:

- Extracts candidate skills from resumes  
- Generates contextually relevant MCQs via LLM agents  
- Applies multi-layer security filtering (content, toxicity, relevance)  
- Evaluates answers and adapts difficulty in real time  

---

## 📦 Project Structure

EvalVerse/
├── **Engine/**  
│   ├── `regex_scanner.py`  
│   │   &nbsp;&nbsp;&nbsp;Utility for extracting patterns from text  
│   └── `OA_session.py`  
│       &nbsp;&nbsp;&nbsp;Main adaptive session logic  
├── **Agents/**  
│   ├── `question_gen.py`  
│   │   &nbsp;&nbsp;&nbsp;QuestionGenerator agent  
│   └── `question_eval.py`  
│       &nbsp;&nbsp;&nbsp;Evaluator agent  
├── **Security/**  
│   ├── `security_filter.py`  
│   │   &nbsp;&nbsp;&nbsp;SecurityFilter decorator orchestrator  
│   └── **Components/**  
│       ├── `content_filter.py`  
│       │   &nbsp;&nbsp;&nbsp;Blocks banned words  
│       ├── `toxicity_filter.py`  
│       │   &nbsp;&nbsp;&nbsp;Detects toxic content  
│       └── `context_relevance_filter.py`  
│           &nbsp;&nbsp;&nbsp;Semantic similarity filter  
├── `llm.py`  
│   &nbsp;&nbsp;&nbsp;LLM wrapper and decorators (`@llm_driver`, `@llm_agent`)  
├── `ResumeIntelligenceModule.py`  
│   &nbsp;&nbsp;&nbsp;Module for extracting skills & experience via LLM  
├── `main.py`  
│   &nbsp;&nbsp;&nbsp;Entry point that kicks off `run_oa_session()`  
└── `README.md`  
    &nbsp;&nbsp;&nbsp;



## 🚀 Major Improvements

### 1. `@LLM_Driver` Decorator Enhancements

- Introduced support for both **ChatGroq** and **ChatOpenAI** dynamically.
- Automatically creates agent instances and registers `run_{agent_name}` methods.
- Added support for agent-specific `description()` functions for dynamic task creation.

---

### 2. Agent Registration via `@LLM_Agent`

- Modular agent definitions via decorated functions.
- Each agent can now define:
  - `role`
  - `goal`
  - `backstory`
  - `tools`
  - `expected_output`
  - `description` lambda for dynamic prompts


## 🔐 Security Layer Additions

### 1. ContentFilter

- Scans output for banned words from a `.sys_dump.key` pickle file.
- Supports:
  - Custom extra words
  - Runtime decorators
  - Fallback return value
- Print logs added:
  - `✅ Passed` / `🚫 Blocked` messages for clarity

---

### 2. ToxicityFilter

- Based on `unitary/toxic-bert` or a custom model (e.g., `facebook/roberta-hate-speech-dynabench-r1-target`)
- Supports:
  - Dynamic threshold for toxicity (default: 0.5)
  - `guard` decorator with fallback
  - Single text or list filtering
- Print logs added with emoji-based clarity

---

### 3. ContextRelevanceFilter

- Uses `all-MiniLM-L6-v2` for semantic similarity.
- Allows checking if output is contextually relevant to a given input.
- Supports threshold tuning (default: 0.5)

---

### 4. SecurityFilter Master Decorator

- Unified interface wrapping Content, Toxicity, and Context filters.
- Logs each stage of filtering with emoji headers.
- On first run, prints **SECURITY FILTER** ASCII art banner.


## 📦 Removed / Deprecated

- ❌ Previous hardcoded agent-task definitions.
- ❌ Static `run_all()` logic (now disabled for dynamic use-cases).
- ❌ Tooling stubs and placeholder decorators replaced with functional runtime tools.

## 🤖 Core Components

### 1. LLM Wrapper & Decorators (`llm.py`)
- **LLM class**  
  Encapsulates API calls, maintains backstory, task, and conversation history.  
- **`@llm_driver(...)`**  
  Class decorator that injects an LLM instance into your class.  
- **`@llm_agent.register_module("AgentName")`**  
  Method decorator that spins up a fresh LLM instance named `"AgentName"` for each call, sets its backstory/task, and restores the original afterward.

### 2. Security Filtering (`security_filter.py`)
Applies three sequential checks on any generated output:
1. **ContentFilter** — blocks banned words or phrases.  
2. **ToxicityFilter** — rejects outputs above a toxicity threshold.  
3. **ContextRelevanceFilter** — uses a small CPU‑friendly embedding model (e.g. BGE‑small) to ensure semantic relevance between provided context (e.g. candidate skills) and the generated question.  
Each step logs pass/fail status for easy debugging.

---

## 📝 Adaptive Q&A Session (`Engine/OA_session.py`)

1. **Extract JSON**  
   Safely extracts the first valid JSON object from LLM output by scanning `{...}` blocks and attempting to parse.  
2. **Generate Question**  
   Uses the `QuestionGenerator` agent wrapped in `SecurityFilter`, with retry logic and backoff, to obtain an MCQ.  
3. **Run Session**  
   - Parses the MCQ JSON  
   - Displays question and options  
   - Collects user input  
   - Evaluates with the `Evaluator` agent  
   - Adapts difficulty level up or down based on correctness  
   - Avoids duplicate questions  
   - Tracks and summarizes total score  

---

## 📂 Resume Intelligence Module

- **Purpose**: Extracts technical skills and work experience from a PDF resume.  
- **Design**:  
  - Decorated with `@llm_driver` to inject LLM  
  - Two agent methods (`TechnicalSkillExtractor` and `ExperienceExtractor`) each set a custom backstory/task before invoking the LLM  

---

## 🔧 Installation & Setup

1. **Clone & Virtual Environment**  
   - `git clone <repo-url>`  
   - `python -m venv venv`  
   - Activate with `source venv/bin/activate` (macOS/Linux) or `.\venv\Scripts\activate` (Windows)

2. **Install Dependencies**  
   - `pip install -r requirements.txt`  

3. **Run**  
   - `python main.py`  

---

## ⚙️ Configuration & Tuning

- **Embedding Model**  
  Change the model in `ContextRelevanceFilter` (default: `bge-small-en-v1.5`) for better CPU performance.  
- **Thresholds**  
  Adjust `toxic_threshold` and `similarity_threshold` in `SecurityFilter` to balance strictness vs. flexibility.  
- **Retry Logic**  
  Modify retry count and delays in `get_question()` for more/less persistence.  
- **Logging**  
  Integrate Python’s `logging` module for file-based or level-based logs instead of prints.

---

> ⚠️ **Note:** This project is still in active development.  