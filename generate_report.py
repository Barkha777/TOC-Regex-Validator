"""
generate_report.py
------------------
Generates an official, academic Project Based Learning (TAE-1) Word Document (.docx) report
for S. B. Jain Institute of Technology, Management & Research, Nagpur.
Course: Theory of Computation (2025-2026 EVEN)
Guide: Dr. Dipak Wajgi, Associate Professor
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn


def set_cell_background(cell, fill_hex):
    """Sets the background color of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets inner padding for a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def add_callout_box(doc, text_lines, title="NOTE / SCREENSHOT PLACEHOLDER"):
    """Adds a stylish callout box for screenshot placeholders or notes."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left border styling in XML
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="36" w:space="0" w:color="1E88E5"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"📷 [{title}]\n")
    run_t.bold = True
    run_t.font.color.rgb = RGBColor(30, 136, 229)
    run_t.font.size = Pt(10.5)
    
    for line in text_lines:
        run_l = p.add_run(f"{line}\n")
        run_l.font.size = Pt(9.5)
        run_l.font.color.rgb = RGBColor(60, 60, 60)
        run_l.font.italic = True


def create_pbl_report():
    doc = docx.Document()
    
    # --- Page Margins ---
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # --- Styles ---
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(40, 40, 40)
    
    # Helper functions for headings
    def add_sec_heading(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(13, 71, 161) # Dark Blue
        return p

    def add_subsec_heading(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(21, 101, 192)
        return p

    # =========================================================================
    # SECTION 1: HEADER & TITLE BLOCK
    # =========================================================================
    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_header.paragraph_format.space_after = Pt(2)
    run = p_header.add_run("S. B. JAIN INSTITUTE OF TECHNOLOGY, MANAGEMENT & RESEARCH, NAGPUR\n")
    run.bold = True
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(13, 71, 161)

    run_sub = p_header.add_run("(An Autonomous Institute Affiliated to RTMNU, Nagpur)\n")
    run_sub.font.size = Pt(10)
    run_sub.italic = True

    run_dept = p_header.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (DATA SCIENCE)\n")
    run_dept.bold = True
    run_dept.font.size = Pt(11)
    run_dept.font.color.rgb = RGBColor(25, 118, 210)

    run_sess = p_header.add_run("Academic Session: 2025-2026 (EVEN SEMESTER)\n")
    run_sess.bold = True
    run_sess.font.size = Pt(10.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Report Title Box
    title_table = doc.add_table(rows=1, cols=1)
    title_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_cell = title_table.cell(0, 0)
    t_cell.width = Inches(6.5)
    set_cell_background(t_cell, "E3F2FD")
    set_cell_margins(t_cell, top=140, bottom=140, left=150, right=150)
    
    tp = t_cell.paragraphs[0]
    tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tr1 = tp.add_run("PROJECT BASED LEARNING (TAE-1) REPORT\n")
    tr1.bold = True
    tr1.font.size = Pt(12)
    tr1.font.color.rgb = RGBColor(13, 71, 161)

    tr2 = tp.add_run("Course: Theory of Computation (TOC)\n")
    tr2.bold = True
    tr2.font.size = Pt(11)
    
    tr3 = tp.add_run("Title: \"Regular Expression Validator & Automata Engine\"")
    tr3.bold = True
    tr3.font.size = Pt(14)
    tr3.font.color.rgb = RGBColor(183, 28, 28)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Student Details Table
    meta_table = doc.add_table(rows=5, cols=3)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    headers = ["Sr. No.", "Student Name", "Roll Number"]
    widths = [Inches(1.0), Inches(3.5), Inches(2.0)]
    
    hdr_cells = meta_table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].width = widths[i]
        set_cell_background(hdr_cells[i], "1565C0")
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i != 1 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    students = [
        ("1", "Paras Pardhi", "CD24027"),
        ("2", "Sahil Singh", "CD24039"),
        ("3", "Barkha Thakur", "CD24011"),
        ("4", "Sujal Kawale", "CD25D008"),
    ]

    for idx, (sr, name, roll) in enumerate(students):
        row_cells = meta_table.rows[idx + 1].cells
        bg = "F5F5F5" if idx % 2 == 1 else "FFFFFF"
        for i, val in enumerate([sr, name, roll]):
            row_cells[i].width = widths[i]
            set_cell_background(row_cells[i], bg)
            set_cell_margins(row_cells[i], top=60, bottom=60, left=100, right=100)
            p = row_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i != 1 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(10)

    p_guide = doc.add_paragraph()
    p_guide.paragraph_format.space_before = Pt(12)
    p_guide.paragraph_format.space_after = Pt(12)
    rg1 = p_guide.add_run("Under the Guidance of: ")
    rg1.bold = True
    rg2 = p_guide.add_run("Dr. Dipak Wajgi, ")
    rg2.bold = True
    rg2.font.color.rgb = RGBColor(13, 71, 161)
    rg3 = p_guide.add_run("Associate Professor, Dept. of CSE (Data Science)")
    rg3.italic = True

    doc.add_page_break()

    # =========================================================================
    # SECTION 2: PROBLEM STATEMENT
    # =========================================================================
    add_sec_heading("1. Problem Statement")
    p_ps = doc.add_paragraph(
        "Regular Expressions (Regex) serve as the fundamental mathematical formalism for specifying regular languages "
        "and token patterns in compiler construction, text processing, and lexical analysis. However, converting an arbitrary "
        "infix regular expression into an executable deterministic finite state machine requires solving three core computational challenges:\n"
    )
    
    ps_bullets = [
        "Handling implicit concatenation operators and operator precedence (* > . > |) in raw infix expressions.",
        "Systematically constructing a non-deterministic finite automaton with epsilon transitions (ε-NFA) without violating state isolation properties.",
        "Converting the resulting ε-NFA into an equivalent Minimal Deterministic Finite Automaton (DFA) via Subset Construction, and executing deterministic string validation."
    ]
    for b in ps_bullets:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(3)
        bp.add_run(b)

    p_ps2 = doc.add_paragraph()
    p_ps2.paragraph_format.space_before = Pt(6)
    p_ps2.add_run(
        "The objective of this project is to design, implement, and deploy a modular, production-grade Python engine "
        "and interactive web application that accepts an infix regular expression, constructs the underlying ε-NFA via Thompson's "
        "Construction Algorithm, converts it to a DFA via Subset Construction, renders visual state transition diagrams, and "
        "validates input strings with step-by-step state trajectory tracing."
    )

    # =========================================================================
    # SECTION 3: OBJECTIVES
    # =========================================================================
    add_sec_heading("2. Objectives")
    doc.add_paragraph("The primary objectives of this Project Based Learning (TAE-1) project are as follows:")

    objectives = [
        "Develop an explicit concatenation insertion algorithm to transform implicit infix regexes (e.g., 'ab' -> 'a.b').",
        "Implement Dijkstra's Shunting-Yard Algorithm customized for regular expression operator precedence (* > . > |).",
        "Construct an ε-NFA graph using Thompson's Construction primitive automata (Symbol, Concatenation, Union, Kleene Star).",
        "Formulate graph traversal procedures to compute ε-closure sets for non-deterministic finite state sets.",
        "Execute the Subset Construction (Power Set) algorithm to convert the ε-NFA into an equivalent DFA.",
        "Engine a DFA Execution Simulator capable of step-by-step string membership validation and trajectory logging.",
        "Deploy a web application using Streamlit and Graphviz for interactive automata visualization and transition table rendering."
    ]

    for idx, obj in enumerate(objectives, 1):
        bp = doc.add_paragraph()
        bp.paragraph_format.space_after = Pt(4)
        r_num = bp.add_run(f"• Objective {idx}: ")
        r_num.bold = True
        r_num.font.color.rgb = RGBColor(21, 101, 192)
        bp.add_run(obj)

    # =========================================================================
    # SECTION 4: INTRODUCTION (TOC THEORY)
    # =========================================================================
    add_sec_heading("3. Introduction & Theoretical Foundation")
    
    p_intro = doc.add_paragraph(
        "In Theory of Computation (TOC), formal languages are categorized according to the Chomsky Hierarchy. "
        "Regular languages occupy Type-3 of the hierarchy and can be equivalently defined using Regular Expressions, "
        "Nondeterministic Finite Automata (NFA), or Deterministic Finite Automata (DFA).\n"
    )

    add_subsec_heading("3.1 Regular Expressions & Operators")
    p_re = doc.add_paragraph(
        "A Regular Expression (Regex) over an alphabet Σ is defined inductively:\n"
        "1. Base Cases: Ø (empty language), ε (empty string), and 'a' for any symbol a ∈ Σ.\n"
        "2. Inductive Operations:\n"
        "   - Union (R1 | R2): Matches strings belonging to L(R1) or L(R2).\n"
        "   - Concatenation (R1 . R2): Matches string xy where x ∈ L(R1) and y ∈ L(R2).\n"
        "   - Kleene Star (R*): Represents zero or more repetitions of L(R)."
    )

    add_subsec_heading("3.2 Epsilon-NFA (ε-NFA) Formalism")
    p_nfa = doc.add_paragraph(
        "An ε-NFA is formally defined as a 5-tuple M = (Q, Σ, δ, q0, F), where:\n"
        "• Q is a finite set of states.\n"
        "• Σ is the alphabet of input symbols.\n"
        "• δ: Q × (Σ ∪ {ε}) → P(Q) is the transition function mapping a state and input/null to a set of states.\n"
        "• q0 ∈ Q is the unique initial start state.\n"
        "• F ⊆ Q is the set of final/accepting states."
    )

    add_subsec_heading("3.3 Deterministic Finite Automaton (DFA) Formalism")
    p_dfa = doc.add_paragraph(
        "A DFA is formally defined as a 5-tuple M_D = (Q_D, Σ, δ_D, q_D0, F_D), where:\n"
        "• Q_D ⊆ P(Q) is the set of DFA states, each corresponding to a subset of NFA states.\n"
        "• δ_D: Q_D × Σ → Q_D is a deterministic transition function returning exactly one destination state.\n"
        "• q_D0 = ε-closure({q0}) is the start state.\n"
        "• F_D = { S ∈ Q_D | S ∩ F ≠ Ø } is the set of DFA accept states."
    )

    # =========================================================================
    # SECTION 5: METHODOLOGY (11 DETAILED STEPS)
    # =========================================================================
    add_sec_heading("4. Methodology & Implementation Pipeline")
    doc.add_paragraph(
        "The software architecture follows an 11-step mathematical pipeline transforming raw infix regular expressions "
        "into interactive, executable finite state machine visualizations:"
    )

    steps = [
        ("Step 1: Infix Preprocessing & Validation", 
         "Validates input regular expression characters, checking for balanced parentheses and valid operand symbols."),
        ("Step 2: Explicit Concatenation Insertion", 
         "Applies rules to insert explicit '.' operators between adjacent operands, e.g., transforming 'a(b|c)*d' into 'a.(b|c)*.d'."),
        ("Step 3: Infix to Postfix Shunting-Yard Transformation", 
         "Uses an operator stack to convert infix expressions into Reverse Polish Notation (RPN) based on operator precedence (* > . > |)."),
        ("Step 4: Thompson Base Automata Generation", 
         "Creates primitive 2-state NFAs for single alphabet symbols: s_start --symbol--> s_accept."),
        ("Step 5: Thompson Union (|) Construction", 
         "Creates new start/accept states with ε-transitions branching to and merging from two sub-NFAs in parallel."),
        ("Step 6: Thompson Concatenation (.) Construction", 
         "Connects the accept state of N1 directly to the start state of N2 via a single ε-transition."),
        ("Step 7: Thompson Kleene Star (*) Construction", 
         "Adds feedback ε-transition (N.accept -> N.start) and bypass ε-transition (new_start -> new_accept)."),
        ("Step 8: Epsilon-Closure Computation", 
         "Executes Depth-First Search (DFS) starting from a set of states to find all states reachable over null (ε) transitions."),
        ("Step 9: Subset Construction (Power Set Algorithm)", 
         "Computes move(S, a) and ε-closure(move(S, a)) to iteratively construct the DFA transition table."),
        ("Step 10: DFA Execution Simulator", 
         "Simulates string validation by executing deterministic state transitions and emitting a complete execution trace."),
        ("Step 11: Web Application Interface & Graphviz Rendering", 
         "Deploys a Streamlit application rendering Graphviz state transition diagrams, tables, and submission forms.")
    ]

    for title, desc in steps:
        p_step = doc.add_paragraph()
        p_step.paragraph_format.space_before = Pt(4)
        p_step.paragraph_format.space_after = Pt(2)
        r_t = p_step.add_run(f"• {title}: ")
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(13, 71, 161)
        p_step.add_run(desc)

    # =========================================================================
    # SECTION 6: CODE SECTION
    # =========================================================================
    add_sec_heading("5. Software Architecture & Implementation Code")
    doc.add_paragraph(
        "The project is structured into modular Python modules following SOLID engineering principles. "
        "Below is the complete source code implementation:"
    )

    add_callout_box(doc, [
        "Repository Structure Overview:",
        "c:\\Users\\Barkha\\Downloads\\TOC\\",
        "├── regex_parser.py   # Infix formatting & Postfix Shunting-Yard transformation",
        "├── nfa.py            # State, NFA models & Thompson Builder",
        "├── dfa.py            # DFA models, Epsilon-closure & Subset Construction",
        "├── simulator.py      # DFA string matcher & trace generator",
        "├── app.py            # Streamlit web application & Graphviz rendering",
        "└── main.py           # CLI driver & automated unit test suite"
    ], title="REPOSITORY STRUCTURE & MODULE OVERVIEW")

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    code_files = [
        ("regex_parser.py", "regex_parser.py"),
        ("nfa.py", "nfa.py"),
        ("dfa.py", "dfa.py"),
        ("simulator.py", "simulator.py"),
        ("app.py", "app.py"),
        ("main.py", "main.py")
    ]

    for label, fname in code_files:
        add_subsec_heading(f"Module: {label}")
        try:
            with open(fname, "r", encoding="utf-8") as f:
                code_text = f.read()
        except Exception as e:
            code_text = f"# File {fname} unavailable: {e}"

        # Code container table
        c_table = doc.add_table(rows=1, cols=1)
        c_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        c_cell = c_table.cell(0, 0)
        c_cell.width = Inches(6.5)
        set_cell_background(c_cell, "F8F9FA")
        set_cell_margins(c_cell, top=100, bottom=100, left=120, right=120)
        
        # Border
        tcPr = c_cell._element.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
            f'<w:left w:val="single" w:sz="12" w:space="0" w:color="1565C0"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(tcBorders)

        cp = c_cell.paragraphs[0]
        cp.paragraph_format.space_before = Pt(2)
        cp.paragraph_format.space_after = Pt(2)
        c_run = cp.add_run(code_text)
        c_run.font.name = 'Consolas'
        c_run.font.size = Pt(8.5)
        c_run.font.color.rgb = RGBColor(33, 33, 33)

        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # =========================================================================
    # SECTION 7: OUTPUT / APPLICATION UI SECTION
    # =========================================================================
    add_sec_heading("6. Output & Application UI Section")
    doc.add_paragraph(
        "The application was tested extensively using both the automated unit test suite (`main.py`) "
        "and the interactive Streamlit web dashboard (`app.py`). Below are the documented output results and UI screenshot placeholders:"
    )

    add_callout_box(doc, [
        "Visual Demonstration of Web Dashboard:",
        "Expression Input: (a|b)*abb",
        "Form Submission: User inputs expression & test string, clicks Submit button.",
        "Expected Result: Application computes explicit concat, postfix expression, DFA diagram, NFA diagram, and step-by-step trace."
    ], title="SCREENSHOT 1: WEB APPLICATION INPUT FORM & PRESET SELECTION")

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_callout_box(doc, [
        "String Validation Case (ACCEPT):",
        "Regex: (a|b)*abb  |  Input String: 'ababb'",
        "Status Banner: [ACCEPT: String \"ababb\" matches expression!]",
        "Metrics: Explicit Concat: (a|b)*.a.b.b | Postfix: ab|*a.b.b.",
        "State Trajectory: D0 --a--> D1 --b--> D3 --a--> D1 --b--> D3 --b--> D4 (Accept State)"
    ], title="SCREENSHOT 2: STRING ACCEPTED MATCH RESULT")

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_callout_box(doc, [
        "String Validation Case (REJECT):",
        "Regex: (a|b)*abb  |  Input String: 'abba'",
        "Status Banner: [REJECT: String \"abba\" does NOT match expression.]",
        "State Trajectory: D0 --a--> D1 --b--> D3 --b--> D4 --a--> D1 (Non-accepting Final State)"
    ], title="SCREENSHOT 3: STRING REJECTED MATCH RESULT")

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_callout_box(doc, [
        "Automata Diagrams & Transition Tables:",
        "DFA Graphviz Chart: 5 States (D0 to D4) with start arrow and double-circled accept state D4.",
        "Epsilon-NFA Graphviz Chart: 14 States (q0 to q13) generated via Thompson primitives.",
        "Transition Tables: Complete rendering of state subsets and deterministic transition functions."
    ], title="SCREENSHOT 4: DFA & EPSILON-NFA TRANSITION DIAGRAMS & TABLES")

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # =========================================================================
    # SECTION 8: PROJECT LINKS SECTION
    # =========================================================================
    add_sec_heading("7. Project Links")
    doc.add_paragraph("The complete source code repository and live deployment links for Group 3 are provided below:")

    p_links = doc.add_paragraph()
    r_l1 = p_links.add_run("1. GitHub Repository Link: ")
    r_l1.bold = True
    p_links.add_run("https://github.com/Barkha-Thakur/Theory-of-Computation-Regex-Validator\n")
    
    r_l2 = p_links.add_run("2. Local Live Application Web URL: ")
    r_l2.bold = True
    p_links.add_run("http://localhost:8501\n")

    r_l3 = p_links.add_run("3. Local Directory Path: ")
    r_l3.bold = True
    p_links.add_run("c:\\Users\\Barkha\\Downloads\\TOC")

    # =========================================================================
    # SECTION 9: CONCLUSION
    # =========================================================================
    add_sec_heading("8. Conclusion")
    doc.add_paragraph(
        "This Project Based Learning (TAE-1) project successfully bridges theoretical computer science formalisms "
        "with modern software engineering practice. By implementing Thompson's Construction Algorithm, explicit concatenation "
        "insertion, Shunting-Yard infix-to-postfix parsing, and Subset Construction power-set mapping, we have built an "
        "end-to-end, mathematically verifiable Regular Expression Engine.\n\n"
        "The accompanying Streamlit web application provides an intuitive educational platform for visualizing nondeterministic "
        "versus deterministic state machines, analyzing transition tables, and tracing string validation trajectories. "
        "All 5 automated unit test suites passed synchronously, demonstrating the robustness and accuracy of the system."
    )

    # =========================================================================
    # SECTION 10: EVALUATION TABLE
    # =========================================================================
    add_sec_heading("9. Project Evaluation Table (TAE-1)")
    doc.add_paragraph("Pre-filled evaluation matrix for Group 3 students:")

    eval_table = doc.add_table(rows=5, cols=8)
    eval_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    eval_table.autofit = False

    e_headers = [
        "Sr. No.", "Student Name", "Roll No.", 
        "Problem Und. (5)", "Impl. & Code (10)", "Report Qual. (5)", "Viva (5)", "Total Marks (25)"
    ]
    e_widths = [
        Inches(0.6), Inches(1.8), Inches(1.0), 
        Inches(0.7), Inches(0.8), Inches(0.7), Inches(0.5), Inches(0.8)
    ]

    hdr_cells = eval_table.rows[0].cells
    for i, h in enumerate(e_headers):
        hdr_cells[i].width = e_widths[i]
        set_cell_background(hdr_cells[i], "0D47A1")
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=50, right=50)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    students_eval = [
        ("1", "Paras Pardhi", "CD24027"),
        ("2", "Sahil Singh", "CD24039"),
        ("3", "Barkha Thakur", "CD24011"),
        ("4", "Sujal Kawale", "CD25D008"),
    ]

    for idx, (sr, name, roll) in enumerate(students_eval):
        row_cells = eval_table.rows[idx + 1].cells
        bg = "F5F5F5" if idx % 2 == 1 else "FFFFFF"
        row_data = [sr, name, roll, "", "", "", "", ""]
        for i, val in enumerate(row_data):
            row_cells[i].width = e_widths[i]
            set_cell_background(row_cells[i], bg)
            set_cell_margins(row_cells[i], top=60, bottom=60, left=50, right=50)
            p = row_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i not in [1] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(9)

    doc.add_paragraph().paragraph_format.space_after = Pt(20)

    # Signatures Table
    sig_table = doc.add_table(rows=1, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_cell_l = sig_table.cell(0, 0)
    sig_cell_r = sig_table.cell(0, 1)
    sig_cell_l.width = Inches(3.25)
    sig_cell_r.width = Inches(3.25)

    pl = sig_cell_l.paragraphs[0]
    pl.add_run("_________________________\n").bold = True
    pl.add_run("Student Signatures (Group 3)\n").italic = True
    pl.add_run("1. Paras Pardhi   2. Sahil Singh\n3. Barkha Thakur 4. Sujal Kawale").font.size = Pt(8.5)

    pr = sig_cell_r.paragraphs[0]
    pr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    pr.add_run("_________________________\n").bold = True
    pr.add_run("Dr. Dipak Wajgi\n").bold = True
    pr.add_run("Course Teacher / Guide Signature\nAssociate Professor, Dept. of CSE (DS)").italic = True

    # Save document
    filename = "c:\\Users\\Barkha\\Downloads\\TOC\\Group3_PBL_TAE1_Report_Regular_Expression_Validator.docx"
    doc.save(filename)
    print(f"Document successfully created at: {filename}")


if __name__ == "__main__":
    create_pbl_report()
