"""
api.py
------
FastAPI Production REST API Backend for Regular Expression Validation & Automata Engine.
Provides RESTful endpoints for regex parsing, Thompson's NFA construction, Subset Construction DFA,
string matching simulation, and JSON automaton serialization.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from regex_parser import insert_explicit_concat, infix_to_postfix
from nfa import ThompsonBuilder, NFA, State
from dfa import subset_construction, DFA, DFAState
from simulator import DFASimulator

app = FastAPI(
    title="Regular Expression Automata API",
    description="Theory of Computation REST API for Regular Expression Parsing, Epsilon-NFA, DFA, and String Validation.",
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


@app.get("/", include_in_schema=False)
def root():
    """Redirects root URL to interactive Swagger API documentation."""
    return RedirectResponse(url="/docs")


@app.get("/health")
def health_check():
    """Service health check endpoint."""
    return {
        "status": "online",
        "service": "Regular Expression Automata REST Engine",
        "version": "1.0.0"
    }


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
