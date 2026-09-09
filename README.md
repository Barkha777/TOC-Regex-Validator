# Regular Expression Validator & Automata Engine

A production-grade Theory of Computation engine and REST API backend built in Python. Supports regular expression parsing, explicit concatenation insertion, Infix to Postfix Shunting-Yard conversion, Thompson's Construction Epsilon-NFA generation, Subset Construction DFA generation, and deterministic string simulation.

---

## 🚀 Deploying to Vercel (Step-by-Step Guide)

This repository is pre-configured with `vercel.json` and `@vercel/python` for 1-click serverless deployment on Vercel.

### Method 1: Deploy via GitHub (Recommended)

1. **Initialize Git & Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Regular Expression Validator API"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/Theory-of-Computation-Regex-Validator.git
   git push -u origin main
   ```

2. **Connect to Vercel**:
   - Go to [vercel.com/new](https://vercel.com/new) and log in.
   - Select **Import Git Repository** and choose `Theory-of-Computation-Regex-Validator`.
   - Click **Deploy**. Vercel will automatically detect `vercel.json` and build the serverless Python functions!

3. **Access Your Live Production API**:
   - Live URL: `https://your-project.vercel.app`
   - Live Swagger Docs: `https://your-project.vercel.app/docs`
   - Live Health Check: `https://your-project.vercel.app/health`

---

## 🛠️ Local Development & Testing

### 1. Run FastAPI Backend Server
```bash
python -m uvicorn api:app --reload --port 8000
```
- Open Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Run Streamlit Web Application
```bash
streamlit run app.py
```
- Open Dashboard: [http://localhost:8501](http://localhost:8501)

### 3. Run Automated Unit Test Suite
```bash
python main.py
```

---

## 📡 API Endpoint Reference

### `POST /api/compile`
- **Request**:
  ```json
  {
    "regex": "(a|b)*abb",
    "test_string": "ababb"
  }
  ```
- **Response**: Returns explicit concatenation, postfix expression, match boolean, execution trajectory, NFA graph data, and DFA power-set transition table.
