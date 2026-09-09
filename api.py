"""
api.py
------
FastAPI Production REST API & Visual Web Application for Regular Expression Validation & Automata Engine.
Serves an interactive visual Web UI at '/' (mirroring Streamlit) with Graphviz SVG diagrams,
bold subtopic tabs, preset loaders, and REST API endpoints for Vercel & local deployment.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from regex_parser import insert_explicit_concat, infix_to_postfix
from nfa import ThompsonBuilder, NFA, State
from dfa import subset_construction, DFA, DFAState
from simulator import DFASimulator

app = FastAPI(
    title="Regular Expression Automata API & Web Application",
    description="Theory of Computation Engine for Regular Expression Parsing, Epsilon-NFA, DFA, and String Validation.",
    version="1.0.0"
)

# Enable CORS for cross-origin frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RegexRequest(BaseModel):
    regex: str = Field(..., example="(a|b)*abb", description="Input regular expression")
    test_string: Optional[str] = Field("", example="ababb", description="Candidate string for membership validation")


class TransitionDTO(BaseModel):
    from_state: str
    to_state: str
    symbol: str


class NFADTO(BaseModel):
    states: List[str]
    start_state: str
    accept_state: str
    alphabet: List[str]
    transitions: List[TransitionDTO]


class DFADTO(BaseModel):
    states: List[str]
    start_state: str
    accept_states: List[str]
    alphabet: List[str]
    transitions: List[TransitionDTO]
    subsets: Dict[str, List[str]]


class CompileResponse(BaseModel):
    status: str
    regex: str
    explicit_concat: str
    postfix: str
    is_match: bool
    test_string: str
    trace: List[str]
    nfa: NFADTO
    dfa: DFADTO


@app.get("/health")
def health_check():
    """Service health check endpoint."""
    return {
        "status": "online",
        "service": "Regular Expression Automata Engine",
        "version": "1.0.0"
    }


@app.get("/docs-redirect", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url="/docs")


@app.get("/", response_class=HTMLResponse)
def index_web_app():
    """Serves the full interactive visual Web Application at root URL."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Regular Expression Automata Engine</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/viz.js/2.1.2/viz.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/viz.js/2.1.2/full.render.js"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #FAFAFA; color: #333; }
        .container { max-width: 1100px; margin-top: 2rem; margin-bottom: 3rem; }
        .main-title { font-size: 2.3rem; font-weight: 700; color: #1E88E5; margin-bottom: 0.2rem; }
        .sub-title { font-size: 1.05rem; color: #555555; margin-bottom: 1.5rem; }
        .card-custom { background: #FFFFFF; border-radius: 10px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 1.5rem; border: 1px solid #E0E0E0; }
        .btn-submit { background-color: #FF4B4B; color: white; font-weight: 700; font-size: 1.1rem; border: none; padding: 0.75rem; border-radius: 8px; width: 100%; transition: 0.2s; }
        .btn-submit:hover { background-color: #E03E3E; color: white; }
        .match-box { padding: 1rem; border-radius: 8px; background-color: #D4EDDA; color: #155724; font-weight: bold; font-size: 1.2rem; border: 1px solid #C3E6CB; }
        .reject-box { padding: 1rem; border-radius: 8px; background-color: #F8D7DA; color: #721C24; font-weight: bold; font-size: 1.2rem; border: 1px solid #F5C6CB; }
        .nav-tabs .nav-link { font-size: 1.15rem; font-weight: 800; color: #555; }
        .nav-tabs .nav-link.active { color: #D32F2F; font-weight: 900; border-bottom: 3px solid #D32F2F; }
        .svg-container svg { max-width: 100%; height: auto; }
        .preset-card { background-color: #E3F2FD; border-left: 5px solid #2196F3; padding: 1rem; border-radius: 6px; margin-bottom: 1rem; color: #0D47A1; }
    </style>
</head>
<body>
    <div class="container">
        <div class="main-title">Regular Expression Automata Engine</div>
        <div class="sub-title">Theory of Computation: Thompson's Construction (&epsilon;-NFA) & Subset Construction (DFA)</div>

        <div class="card-custom">
            <label class="form-label fw-bold">Load Preset Expression</label>
            <select id="presetSelect" class="form-select mb-3" onchange="loadPreset()">
                <option value="custom">Custom Input</option>
                <option value="abb" selected>Ends with 'abb' -> (a|b)*abb</option>
                <option value="ab">Starts with 'a' and ends with 'b' -> a(a|b)*b</option>
                <option value="even_a">Even number of 'a's -> (b|a.b*.a)*</option>
                <option value="union">Simple Union -> a|b|c</option>
                <option value="star">Repetition -> a*b</option>
            </select>

            <div id="presetCard" class="preset-card">
                <h5 class="fw-bold mb-1" id="presetTitle">📌 Selected Preset: Ends with 'abb'</h5>
                <div id="presetDesc">Language of strings over {a,b} that end with substring 'abb'</div>
            </div>

            <h4 class="fw-bold mb-3">1. Enter Inputs & Submit</h4>
            <div class="row g-3">
                <div class="col-md-6">
                    <label class="form-label fw-bold">Regular Expression (Operators: |, *, (), implicit concat)</label>
                    <input type="text" id="regexInput" class="form-control" value="(a|b)*abb">
                </div>
                <div class="col-md-6">
                    <label class="form-label fw-bold">Test Input String</label>
                    <input type="text" id="testStringInput" class="form-control" value="ababb">
                </div>
            </div>
            <button class="btn btn-submit mt-3" onclick="compileAndRun()">🚀 Submit Inputs & Generate Automata Answers</button>
        </div>

        <div id="resultsSection" class="card-custom">
            <h4 class="fw-bold mb-3">2. Generated Automata Answers & Validation</h4>
            <div class="row align-items-center mb-4">
                <div class="col-md-6">
                    <div id="statusBanner" class="match-box">ACCEPT: String "ababb" matches expression!</div>
                </div>
                <div class="col-md-3 text-center">
                    <small class="text-muted d-block fw-bold">Explicit Concat Form</small>
                    <h5 id="explicitConcatText" class="fw-bold text-primary">(a|b)*.a.b.b</h5>
                </div>
                <div class="col-md-3 text-center">
                    <small class="text-muted d-block fw-bold">Postfix Expression</small>
                    <h5 id="postfixText" class="fw-bold text-primary">ab|*a.b.b.</h5>
                </div>
            </div>

            <ul class="nav nav-tabs mb-3" id="automataTabs" role="tablist">
                <li class="nav-item">
                    <button class="nav-link active" id="dfa-tab" data-bs-toggle="tab" data-bs-target="#dfaPane" type="button">📊 1. DFA (Subset Construction)</button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" id="nfa-tab" data-bs-toggle="tab" data-bs-target="#nfaPane" type="button">🔄 2. &epsilon;-NFA (Thompson's Algorithm)</button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" id="trace-tab" data-bs-toggle="tab" data-bs-target="#tracePane" type="button">📝 3. Execution Trace</button>
                </li>
            </ul>

            <div class="tab-content" id="tabContent">
                <div class="tab-pane fade show active" id="dfaPane">
                    <h4 class="fw-bold text-danger mb-3">📊 1. DFA (Subset Construction)</h4>
                    <div class="row">
                        <div class="col-md-7">
                            <h6 class="fw-bold">DFA State Transition Diagram</h6>
                            <div id="dfaDiagram" class="svg-container border rounded p-2 text-center"></div>
                        </div>
                        <div class="col-md-5">
                            <h6 class="fw-bold">DFA Transition Table</h6>
                            <div class="table-responsive">
                                <table class="table table-bordered table-striped" id="dfaTable"></table>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="tab-pane fade" id="nfaPane">
                    <h4 class="fw-bold text-primary mb-3">🔄 2. &epsilon;-NFA (Thompson's Algorithm)</h4>
                    <div class="row">
                        <div class="col-md-7">
                            <h6 class="fw-bold">&epsilon;-NFA State Transition Diagram</h6>
                            <div id="nfaDiagram" class="svg-container border rounded p-2 text-center"></div>
                        </div>
                        <div class="col-md-5">
                            <h6 class="fw-bold">&epsilon;-NFA Transition Table</h6>
                            <div class="table-responsive">
                                <table class="table table-bordered table-striped" id="nfaTable"></table>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="tab-pane fade" id="tracePane">
                    <h4 class="fw-bold text-success mb-3">📝 3. Step-by-Step DFA Simulation Trace</h4>
                    <div id="traceLog" class="bg-light p-3 rounded border font-monospace"></div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const viz = new Viz();
        const presets = {
            custom: { title: "Custom Expression Input", desc: "Enter any regular expression and test string above.", regex: "", test: "" },
            abb: { title: "Selected Preset: Ends with 'abb'", desc: "Language of strings over {a,b} that end with substring 'abb'", regex: "(a|b)*abb", test: "ababb" },
            ab: { title: "Selected Preset: Starts with 'a' and ends with 'b'", desc: "Language of strings over {a,b} that start with 'a' and end with 'b'", regex: "a(a|b)*b", test: "abb" },
            even_a: { title: "Selected Preset: Even number of 'a's", desc: "Language of strings over {a,b} containing an even count of symbol 'a'", regex: "(b|a.b*.a)*", test: "baba" },
            union: { title: "Selected Preset: Simple Union (a|b|c)", desc: "Language matching exact single symbols 'a', 'b', or 'c'", regex: "a|b|c", test: "b" },
            star: { title: "Selected Preset: Repetition (a*b)", desc: "Language matching zero or more 'a's followed by a single 'b'", regex: "a*b", test: "aaab" }
        };

        function loadPreset() {
            const val = document.getElementById("presetSelect").value;
            const p = presets[val];
            document.getElementById("presetTitle").innerText = "📌 " + p.title;
            document.getElementById("presetDesc").innerText = p.desc;
            if (val !== "custom") {
                document.getElementById("regexInput").value = p.regex;
                document.getElementById("testStringInput").value = p.test;
            }
        }

        async function compileAndRun() {
            const regex = document.getElementById("regexInput").value;
            const test_string = document.getElementById("testStringInput").value;

            try {
                const response = await fetch('/api/compile', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ regex: regex, test_string: test_string })
                });

                if (!response.ok) {
                    const err = await response.json();
                    alert("Error: " + err.detail);
                    return;
                }

                const data = await response.json();
                renderResults(data);
            } catch (err) {
                alert("Failed to execute request: " + err);
            }
        }

        function renderResults(data) {
            document.getElementById("explicitConcatText").innerText = data.explicit_concat;
            document.getElementById("postfixText").innerText = data.postfix;

            const banner = document.getElementById("statusBanner");
            if (data.is_match) {
                banner.className = "match-box";
                banner.innerText = `ACCEPT: String "${data.test_string}" matches expression!`;
            } else {
                banner.className = "reject-box";
                banner.innerText = `REJECT: String "${data.test_string}" does NOT match expression.`;
            }

            // Render DFA Dot
            let dfaDot = "digraph DFA { rankdir=LR; node [shape=circle]; \\n";
            dfaDot += '"" [shape=none]; "" -> "' + data.dfa.start_state + '";\\n';
            data.dfa.states.forEach(s => {
                const isAcc = data.dfa.accept_states.includes(s);
                const shape = isAcc ? "doublecircle" : "circle";
                const color = isAcc ? "green" : "black";
                dfaDot += `"${s}" [shape=${shape}, color=${color}];\\n`;
            });
            data.dfa.transitions.forEach(t => {
                dfaDot += `"${t.from_state}" -> "${t.to_state}" [label="${t.symbol}"];\\n`;
            });
            dfaDot += "}";

            viz.renderSVGElement(dfaDot).then(svg => {
                const container = document.getElementById("dfaDiagram");
                container.innerHTML = "";
                container.appendChild(svg);
            });

            // Render NFA Dot
            let nfaDot = "digraph NFA { rankdir=LR; node [shape=circle]; \\n";
            nfaDot += '"" [shape=none]; "" -> "' + data.nfa.start_state + '";\\n';
            data.nfa.states.forEach(s => {
                const isAcc = s === data.nfa.accept_state;
                const shape = isAcc ? "doublecircle" : "circle";
                const color = isAcc ? "green" : "black";
                nfaDot += `"${s}" [shape=${shape}, color=${color}];\\n`;
            });
            data.nfa.transitions.forEach(t => {
                nfaDot += `"${t.from_state}" -> "${t.to_state}" [label="${t.symbol}"];\\n`;
            });
            nfaDot += "}";

            viz.renderSVGElement(nfaDot).then(svg => {
                const container = document.getElementById("nfaDiagram");
                container.innerHTML = "";
                container.appendChild(svg);
            });

            // Render DFA Table
            let dfaTblHtml = "<thead><tr><th>DFA State</th><th>NFA Subset</th>";
            data.dfa.alphabet.forEach(a => dfaTblHtml += `<th>${a}</th>`);
            dfaTblHtml += "</tr></thead><tbody>";

            data.dfa.states.forEach(s => {
                const isAcc = data.dfa.accept_states.includes(s);
                const subset = "{" + (data.dfa.subsets[s] || []).join(",") + "}";
                dfaTblHtml += `<tr><td><strong>${s}${isAcc ? ' *' : ''}</strong></td><td>${subset}</td>`;
                data.dfa.alphabet.forEach(a => {
                    const trans = data.dfa.transitions.find(t => t.from_state === s && t.symbol === a);
                    dfaTblHtml += `<td>${trans ? trans.to_state : '-'}</td>`;
                });
                dfaTblHtml += "</tr>";
            });
            dfaTblHtml += "</tbody>";
            document.getElementById("dfaTable").innerHTML = dfaTblHtml;

            // Render NFA Table
            let nfaTblHtml = "<thead><tr><th>State</th>";
            data.nfa.alphabet.concat(["ε"]).forEach(a => nfaTblHtml += `<th>${a}</th>`);
            nfaTblHtml += "</tr></thead><tbody>";

            data.nfa.states.forEach(s => {
                const isAcc = s === data.nfa.accept_state;
                nfaTblHtml += `<tr><td><strong>${s}${isAcc ? ' *' : ''}</strong></td>`;
                data.nfa.alphabet.concat(["ε"]).forEach(a => {
                    const targets = data.nfa.transitions.filter(t => t.from_state === s && t.symbol === a).map(t => t.to_state);
                    nfaTblHtml += `<td>${targets.length ? '{' + targets.join(',') + '}' : '-'}</td>`;
                });
                nfaTblHtml += "</tr>";
            });
            nfaTblHtml += "</tbody>";
            document.getElementById("nfaTable").innerHTML = nfaTblHtml;

            // Render Trace
            document.getElementById("traceLog").innerHTML = data.trace.map(t => `<div>${t}</div>`).join("");
        }

        // Run default on load
        window.onload = compileAndRun;
    </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content)


@app.post("/api/compile", response_model=CompileResponse)
def compile_regex(request: RegexRequest):
    """
    Main Compilation & Execution Endpoint.
    1. Inserts explicit concatenation '.'
    2. Transforms infix expression to postfix
    3. Builds Thompson's Epsilon-NFA
    4. Computes Subset Construction DFA
    5. Validates candidate test string
    """
    if not request.regex:
        raise HTTPException(status_code=400, detail="Regular expression cannot be empty.")

    try:
        explicit_concat = insert_explicit_concat(request.regex)
        postfix = infix_to_postfix(request.regex)
        
        builder = ThompsonBuilder()
        nfa = builder.build_nfa(postfix)
        dfa = subset_construction(nfa)
        
        is_match, trace = DFASimulator.validate(dfa, request.test_string or "")
        
        # Serialize NFA
        nfa_states = sorted(list(nfa.get_all_states()), key=lambda x: x.state_id)
        nfa_transitions = []
        for s in nfa_states:
            for symbol, targets in s.transitions.items():
                sym_str = "ε" if symbol is None else str(symbol)
                for t in targets:
                    nfa_transitions.append(TransitionDTO(
                        from_state=f"q{s.state_id}",
                        to_state=f"q{t.state_id}",
                        symbol=sym_str
                    ))
                    
        nfa_dto = NFADTO(
            states=[f"q{s.state_id}" for s in nfa_states],
            start_state=f"q{nfa.start_state.state_id}",
            accept_state=f"q{nfa.accept_state.state_id}",
            alphabet=sorted(list(nfa.get_alphabet())),
            transitions=nfa_transitions
        )
        
        # Serialize DFA
        dfa_states = sorted(list(dfa.states), key=lambda x: x.name)
        dfa_transitions = []
        dfa_subsets = {}
        
        for s in dfa_states:
            sorted_nfa = sorted([f"q{ns.state_id}" for ns in s.nfa_states])
            dfa_subsets[s.name] = sorted_nfa
            for symbol, target in s.transitions.items():
                dfa_transitions.append(TransitionDTO(
                    from_state=s.name,
                    to_state=target.name,
                    symbol=symbol
                ))
                
        dfa_dto = DFADTO(
            states=[s.name for s in dfa_states],
            start_state=dfa.start_state.name,
            accept_states=[s.name for s in dfa.accept_states],
            alphabet=sorted(list(dfa.alphabet)),
            transitions=dfa_transitions,
            subsets=dfa_subsets
        )
        
        return CompileResponse(
            status="success",
            regex=request.regex,
            explicit_concat=explicit_concat,
            postfix=postfix,
            is_match=is_match,
            test_string=request.test_string or "",
            trace=trace,
            nfa=nfa_dto,
            dfa=dfa_dto
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to compile regular expression: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
