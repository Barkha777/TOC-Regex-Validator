# 🔤 Regular Expression Validator & Automata Engine

[![Vercel Deployment](https://img.shields.io/badge/Vercel-Deployed-success?style=for-the-badge&logo=vercel)](https://toc-regex-validator.vercel.app/docs)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.55-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)

An educational and production-grade **Theory of Computation (TOC)** engine, interactive web application, and REST API backend. Transforms arbitrary infix regular expressions into $\epsilon$-NFAs using **Thompson's Construction Algorithm**, converts $\epsilon$-NFAs into DFAs using **Subset Construction**, and simulates deterministic string validation step-by-step.

---

## 🎓 Academic Details

- **Institution**: S. B. Jain Institute of Technology, Management & Research, Nagpur
- **Department**: Department of Computer Science and Engineering (Data Science)
- **Course**: Theory of Computation (Session: 2025-2026 EVEN)
- **Guide**: **Dr. Dipak Wajgi**, Associate Professor
- **Group 3 Students**:
  1. **Paras Pardhi** (CD24027)
  2. **Sahil Singh** (CD24039)
  3. **Barkha Thakur** (CD24011)
  4. **Sujal Kawale** (CD25D008)

---

## 🌐 Live Deployed URLs

- ⚡ **Live Production API**: [https://toc-regex-validator.vercel.app](https://toc-regex-validator.vercel.app)
- 📚 **Interactive Swagger API Docs**: [https://toc-regex-validator.vercel.app/docs](https://toc-regex-validator.vercel.app/docs)
- 💓 **Health Check Endpoint**: [https://toc-regex-validator.vercel.app/health](https://toc-regex-validator.vercel.app/health)
- 💻 **Local Streamlit Dashboard**: `http://localhost:8501`

---

## ⚙️ Theoretical Pipeline & Core Algorithms

```
 Infix Regex       Explicit Concat       Postfix (RPN)        ε-NFA (Thompson)      DFA (Subset Constr.)       Simulator
"(a|b)*abb"  ---> "(a|b)*.a.b.b"  ---> "ab|*a.b.b."  ---> 14 Epsilon States ---> 5 Subset States  ---> Match/Reject Trace
```

1. **Explicit Concatenation Insertion (`regex_parser.py`)**: Automatically inserts explicit concatenation operators `.` (e.g., `a(b|c)*d` $\rightarrow$ `a.(b|c)*.d`).
2. **Shunting-Yard Infix to Postfix (`regex_parser.py`)**: Converts infix expressions to Reverse Polish Notation using operator precedence ($\text{Star } * > \text{Concat } . > \text{Union } \mid$).
3. **Thompson's Construction Algorithm (`nfa.py`)**: Builds single-entry/single-exit $\epsilon$-NFA fragments for symbols, union ($N_1 \mid N_2$), concatenation ($N_1 \cdot N_2$), and Kleene closure ($N^*$).
4. **Subset Construction Algorithm (`dfa.py`)**: Computes $\epsilon$-closures over Depth-First Search and power-set transitions $\text{move}(S, a)$ to build deterministic finite state machines.
5. **DFA String Simulator (`simulator.py`)**: Executes character-by-character transitions and emits a complete step-by-step state trajectory log.

---

## 📁 Repository Structure

```
c:\Users\Barkha\Downloads\TOC\
├── app.py              # Streamlit Web Dashboard & Graphviz Automata Visualizer
├── api.py              # FastAPI REST API Backend Server (Vercel Serverless Function)
├── regex_parser.py     # Explicit Concat Insertion & Shunting-Yard Parser
├── nfa.py              # State Models & Thompson's Construction Algorithm
├── dfa.py              # DFA Models & Subset Construction Algorithm
├── simulator.py        # DFA String Execution Engine & Trajectory Logger
├── main.py             # CLI Driver & Automated Unit Test Suite
├── requirements.txt    # Production Dependencies
├── vercel.json         # Vercel Serverless Function Configuration
├── README.md           # Project & Deployment Documentation
└── .gitignore          # Git exclusion rules
```

---

## 📡 REST API Endpoint Reference

### `POST /api/compile`

**Request Body**:
```json
{
  "regex": "(a|b)*abb",
  "test_string": "ababb"
}
```

**Response Payload**:
```json
{
  "status": "success",
  "regex": "(a|b)*abb",
  "explicit_concat": "(a|b)*.a.b.b",
  "postfix": "ab|*a.b.b.",
  "is_match": true,
  "test_string": "ababb",
  "trace": [
    "Initial State: D0 (Accept: False)",
    "Step 1: Symbol 'a' -> Transition D0 -> D1",
    "Step 2: Symbol 'b' -> Transition D1 -> D3",
    "Step 3: Symbol 'a' -> Transition D3 -> D1",
    "Step 4: Symbol 'b' -> Transition D1 -> D3",
    "Step 5: Symbol 'b' -> Transition D3 -> D4",
    "Final State: D4 -> Result: ACCEPTED"
  ],
  "nfa": {
    "states": ["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13"],
    "start_state": "q0",
    "accept_state": "q13",
    "alphabet": ["a", "b"]
  },
  "dfa": {
    "states": ["D0", "D1", "D2", "D3", "D4"],
    "start_state": "D0",
    "accept_states": ["D4"],
    "subsets": {
      "D0": ["q0", "q2", "q4", "q6", "q7", "q8"],
      "D1": ["q0", "q1", "q10", "q2", "q4", "q5", "q7", "q8", "q9"],
      "D2": ["q0", "q2", "q3", "q4", "q5", "q7", "q8"],
      "D3": ["q0", "q11", "q12", "q2", "q3", "q4", "q5", "q7", "q8"],
      "D4": ["q0", "q13", "q2", "q3", "q4", "q5", "q7", "q8"]
    }
  }
}
```

---

## 🛠️ Local Installation & Execution

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Barkha777/TOC-Regex-Validator.git
   cd TOC-Regex-Validator
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Streamlit Web App**:
   ```bash
   streamlit run app.py
   ```

4. **Run FastAPI Backend Server**:
   ```bash
   python -m uvicorn api:app --reload --port 8000
   ```

5. **Run Automated Unit Test Suite**:
   ```bash
   python main.py
   ```

---

## 📄 License & Attribution

Developed for **Project Based Learning (TAE-1)** in Theory of Computation at **S. B. Jain Institute of Technology, Management & Research, Nagpur**.
