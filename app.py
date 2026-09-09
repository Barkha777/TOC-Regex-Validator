"""
app.py
------
Streamlit Web Application for Regular Expression Validation & Automata Visualization.
Powered by Thompson's Construction Algorithm and Subset Construction.
Includes explicit Form Submit functionality, full description rendering for selected presets,
and bold, prominent subtopic tab styling.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Set

from regex_parser import insert_explicit_concat, infix_to_postfix
from nfa import ThompsonBuilder, NFA, State
from dfa import subset_construction, DFA, DFAState
from simulator import DFASimulator

# --- Page Configuration ---
st.set_page_config(
    page_title="Regex Validator & Automata Visualizer",
    page_icon="🔤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #555555;
        margin-bottom: 1.5rem;
    }
    .preset-card {
        padding: 1rem;
        border-radius: 8px;
        background-color: #E3F2FD;
        border-left: 5px solid #2196F3;
        margin-bottom: 1.2rem;
        color: #0D47A1;
    }
    .match-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #D4EDDA;
        color: #155724;
        font-weight: bold;
        font-size: 1.2rem;
        border: 1px solid #C3E6CB;
        margin-bottom: 1rem;
    }
    .reject-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #F8D7DA;
        color: #721C24;
        font-weight: bold;
        font-size: 1.2rem;
        border: 1px solid #F5C6CB;
        margin-bottom: 1rem;
    }
    .stButton>button {
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    /* Bold Subtopic Tab Styling */
    button[data-baseweb="tab"] {
        font-size: 1.2rem !important;
        font-weight: 800 !important;
    }
    button[data-baseweb="tab"] div, button[data-baseweb="tab"] p {
        font-size: 1.2rem !important;
        font-weight: 800 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p, button[data-baseweb="tab"][aria-selected="true"] div {
        font-weight: 900 !important;
        color: #D32F2F !important;
    }
</style>
""", unsafe_allow_html=True)


def build_graphviz_nfa(nfa: NFA):
    """Generates a DOT graph representation of an Epsilon-NFA."""
    import graphviz
    dot = graphviz.Digraph(comment="Epsilon-NFA", graph_attr={'rankdir': 'LR'})
    
    # Invisible start node arrow
    dot.node('', shape='none')
    dot.edge('', f"q{nfa.start_state.state_id}")
    
    states = nfa.get_all_states()
    for s in sorted(states, key=lambda x: x.state_id):
        shape = 'doublecircle' if s == nfa.accept_state else 'circle'
        color = 'green' if s == nfa.accept_state else 'black'
        dot.node(f"q{s.state_id}", f"q{s.state_id}", shape=shape, color=color)
        
    for s in states:
        for symbol, targets in s.transitions.items():
            sym_label = "ε" if symbol is None else str(symbol)
            for t in targets:
                dot.edge(f"q{s.state_id}", f"q{t.state_id}", label=sym_label)
                
    return dot


def build_graphviz_dfa(dfa: DFA):
    """Generates a DOT graph representation of a DFA."""
    import graphviz
    dot = graphviz.Digraph(comment="DFA", graph_attr={'rankdir': 'LR'})
    
    # Invisible start node arrow
    dot.node('', shape='none')
    dot.edge('', dfa.start_state.name)
    
    for s in sorted(list(dfa.states), key=lambda x: x.name):
        shape = 'doublecircle' if s.is_accept else 'circle'
        color = 'green' if s.is_accept else 'black'
        dot.node(s.name, s.name, shape=shape, color=color)
        
    for s in dfa.states:
        for symbol, target in s.transitions.items():
            dot.edge(s.name, target.name, label=str(symbol))
            
    return dot


def generate_nfa_table(nfa: NFA) -> pd.DataFrame:
    """Generates a pandas DataFrame for the NFA transition table."""
    states = sorted(list(nfa.get_all_states()), key=lambda x: x.state_id)
    alphabet = sorted(list(nfa.get_alphabet()))
    symbols = alphabet + ["ε"]
    
    data = []
    for s in states:
        row = {
            "State": f"q{s.state_id}" + (" *" if s == nfa.accept_state else ""),
        }
        for sym in symbols:
            lookup_sym = None if sym == "ε" else sym
            targets = s.transitions.get(lookup_sym, set())
            if targets:
                sorted_targets = sorted([f"q{t.state_id}" for t in targets])
                row[sym] = "{" + ",".join(sorted_targets) + "}"
            else:
                row[sym] = "-"
        data.append(row)
        
    return pd.DataFrame(data).set_index("State")


def generate_dfa_table(dfa: DFA) -> pd.DataFrame:
    """Generates a pandas DataFrame for the DFA transition table."""
    states = sorted(list(dfa.states), key=lambda x: x.name)
    alphabet = sorted(list(dfa.alphabet))
    
    data = []
    for s in states:
        row = {
            "DFA State": s.name + (" *" if s.is_accept else ""),
            "NFA Subset": "{" + ",".join(sorted([f"q{ns.state_id}" for ns in s.nfa_states])) + "}"
        }
        for sym in alphabet:
            target = s.transitions.get(sym)
            row[sym] = target.name if target else "-"
        data.append(row)
        
    return pd.DataFrame(data).set_index("DFA State")


def main():
    st.markdown('<div class="main-title">Regular Expression Automata Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Theory of Computation: Thompson\'s Construction (ε-NFA) & Subset Construction (DFA)</div>', unsafe_allow_html=True)

    # --- Sidebar Controls ---
    st.sidebar.header("Configuration & Presets")
    
    # Presets mapping: short name -> (Full Description, Regex, Test String)
    presets = {
        "Custom Input": ("Custom Expression Input", "", ""),
        "Ends with 'abb'": (
            "Language of strings over {a,b} that end with substring 'abb'",
            "(a|b)*abb",
            "ababb"
        ),
        "Starts with 'a' and ends with 'b'": (
            "Language of strings over {a,b} that start with 'a' and end with 'b'",
            "a(a|b)*b",
            "abb"
        ),
        "Even number of 'a's": (
            "Language of strings over {a,b} containing an even count of symbol 'a'",
            "(b|a.b*.a)*",
            "baba"
        ),
        "Simple Union (a|b|c)": (
            "Language matching exact single symbols 'a', 'b', or 'c'",
            "a|b|c",
            "b"
        ),
        "Repetition (a*b)": (
            "Language matching zero or more 'a's followed by a single 'b'",
            "a*b",
            "aaab"
        )
    }
    
    selected_preset_key = st.sidebar.selectbox("Load Preset Expression", list(presets.keys()))
    desc, preset_regex, preset_string = presets[selected_preset_key]
    
    default_regex = preset_regex if preset_regex else "(a|b)*abb"
    default_string = preset_string if preset_string else "ababb"

    # --- Full Display Card for Selected Preset ---
    if selected_preset_key != "Custom Input":
        st.markdown(f"""
        <div class="preset-card">
            <h4 style="margin:0 0 0.5rem 0; color:#0D47A1;">📌 Selected Preset: {selected_preset_key}</h4>
            <p style="margin:0 0 0.4rem 0;"><b>Description:</b> {desc}</p>
            <p style="margin:0;"><b>Pattern:</b> <code>{preset_regex}</code> &nbsp;|&nbsp; <b>Sample Test String:</b> <code>{preset_string}</code></p>
        </div>
        """, unsafe_allow_html=True)

    # --- Form for Submission ---
    st.subheader("1. Enter Inputs & Submit")
    with st.form(key="input_form"):
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            regex_input = st.text_input("Regular Expression (Operators: |, *, (), implicit concat)", value=default_regex)
        with col_in2:
            test_string = st.text_input("Test Input String", value=default_string)
            
        submit_button = st.form_submit_button(
            label="🚀 Submit Inputs & Generate Automata Answers", 
            type="primary", 
            use_container_width=True
        )

    # Manage session state for generated results
    if submit_button or "has_submitted" not in st.session_state:
        st.session_state["has_submitted"] = True
        st.session_state["regex_input"] = regex_input
        st.session_state["test_string"] = test_string

    if not st.session_state.get("has_submitted"):
        st.info("👆 Enter a regular expression and test string, then click **Submit Inputs & Generate Automata Answers**.")
        return

    active_regex = st.session_state["regex_input"]
    active_string = st.session_state["test_string"]

    if not active_regex:
        st.error("Please enter a non-empty regular expression.")
        return

    # --- Automata Construction ---
    try:
        explicit_concat = insert_explicit_concat(active_regex)
        postfix = infix_to_postfix(active_regex)
        builder = ThompsonBuilder()
        nfa = builder.build_nfa(postfix)
        dfa = subset_construction(nfa)
        is_match, trace = DFASimulator.validate(dfa, active_string)
    except Exception as e:
        st.error(f"Syntax Error in Regular Expression '{active_regex}': {e}")
        return

    st.markdown("---")
    st.subheader("2. Generated Automata Answers & Validation")

    # --- Validation Summary Header ---
    col1, col2, col3 = st.columns([1.5, 1, 1])
    with col1:
        st.markdown("**Validation Result:**")
        if is_match:
            st.markdown(f'<div class="match-box">ACCEPT: String "{active_string}" matches expression!</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="reject-box">REJECT: String "{active_string}" does NOT match expression.</div>', unsafe_allow_html=True)

    with col2:
        st.metric("Explicit Concat Form", explicit_concat)
    with col3:
        st.metric("Postfix Expression", postfix)

    st.markdown("---")

    # --- Tabs for Generated Answers with Bold Subtopic Labels ---
    tab_dfa, tab_nfa, tab_trace = st.tabs([
        "📊 1. DFA (Subset Construction)", 
        "🔄 2. ε-NFA (Thompson's Algorithm)", 
        "📝 3. Execution Trace"
    ])

    with tab_dfa:
        st.markdown("### **📊 1. DFA (Subset Construction)**")
        col_dfa_chart, col_dfa_table = st.columns([1.2, 1])
        
        with col_dfa_chart:
            st.markdown("##### **DFA State Transition Diagram**")
            try:
                dot_dfa = build_graphviz_dfa(dfa)
                st.graphviz_chart(dot_dfa)
            except Exception as e:
                st.warning(f"Graphviz rendering unavailable: {e}")
                
        with col_dfa_table:
            st.markdown("##### **DFA Transition Table**")
            df_dfa = generate_dfa_table(dfa)
            st.dataframe(df_dfa, use_container_width=True)

    with tab_nfa:
        st.markdown("### **🔄 2. ε-NFA (Thompson's Algorithm)**")
        col_nfa_chart, col_nfa_table = st.columns([1.2, 1])
        
        with col_nfa_chart:
            st.markdown("##### **ε-NFA State Transition Diagram**")
            try:
                dot_nfa = build_graphviz_nfa(nfa)
                st.graphviz_chart(dot_nfa)
            except Exception as e:
                st.warning(f"Graphviz rendering unavailable: {e}")
                
        with col_nfa_table:
            st.markdown("##### **ε-NFA Transition Table**")
            df_nfa = generate_nfa_table(nfa)
            st.dataframe(df_nfa, use_container_width=True)

    with tab_trace:
        st.markdown(f"### **📝 3. Step-by-Step DFA Simulation Trace for '{active_string}'**")
        for step in trace:
            st.text(step)


if __name__ == "__main__":
    main()
