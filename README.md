# 🔤 Regular Expression Validator & Automata Engine

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.55-FF4B4B?style=for-the-badge&logo=streamlit)](http://localhost:8501)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Vercel Deployment](https://img.shields.io/badge/Vercel-Deployed-success?style=for-the-badge&logo=vercel)](https://toc-regex-validator.vercel.app/docs)

An educational and production-grade **Theory of Computation (TOC)** engine, interactive web application, and REST API backend. Transforms arbitrary infix regular expressions into $\epsilon$-NFAs using **Thompson's Construction Algorithm**, converts $\epsilon$-NFAs into DFAs using **Subset Construction**, and simulates deterministic string validation step-by-step.

---

## 🎓 Academic Details

- **Institution**: S. B. Jain Institute of Technology, Management & Research, Nagpur
- **Department**: Department of Computer Science and Engineering (Data Science)
- **Course**: Theory of Computation / Information Retrieval (N-PECCD601T)
- **Session**: 2025-2026 (EVEN SEMESTER)
- **Guide**: **Dr. Dipak Wajgi**, Associate Professor
- **Group 3 Students**:
  1. **Paras Pardhi** (CD24027)
  2. **Sahil Singh** (CD24039)
  3. **Barkha Thakur** (CD24011)
  4. **Sujal Kawale** (CD25D008)

---

## 🌐 Project Links & URLs

- 💻 **Live Web Application URL**: [http://localhost:8501/](http://localhost:8501/)
- 🐙 **GitHub Repository**: [https://github.com/Barkha777/TOC-Regex-Validator](https://github.com/Barkha777/TOC-Regex-Validator)
- ⚡ **Live Vercel Production API**: [https://toc-regex-validator.vercel.app](https://toc-regex-validator.vercel.app)
- 📚 **Interactive Swagger API Docs**: [https://toc-regex-validator.vercel.app/docs](https://toc-regex-validator.vercel.app/docs)

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
├── app.py              # Streamlit Web Dashboard & Graphviz Automata Visualizer (http://localhost:8501/)
├── api.py              # FastAPI REST API Backend Server
├── regex_parser.py     # Explicit Concat Insertion & Shunting-Yard Parser
├── nfa.py              # State Models & Thompson's Construction Algorithm
├── dfa.py              # DFA Models & Subset Construction Algorithm
├── simulator.py        # DFA String Execution Engine & Trajectory Logger
├── main.py             # CLI Driver & Automated Unit Test Suite
├── generate_perfect_report.py # Academic Word Document Report Generator
├── Group3_PBL_TAE1_Report_Regular_Expression_Validator.docx # Official TAE-1 Word Report
├── requirements.txt    # Production Dependencies
├── vercel.json         # Vercel Serverless Function Configuration
├── README.md           # Project & Deployment Documentation
└── .gitignore          # Git exclusion rules
```

---

## 🛠️ Local Setup & Execution

1. **Clone Repository**:
   ```bash
   git clone https://github.com/Barkha777/TOC-Regex-Validator.git
   cd TOC-Regex-Validator
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch Web Application**:
   ```bash
   streamlit run app.py
   ```
   Access in browser: **[http://localhost:8501/](http://localhost:8501/)**
