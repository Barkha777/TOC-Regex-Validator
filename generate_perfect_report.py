"""
generate_perfect_report.py
--------------------------
Generates the EXACT Project Based Learning (Tae -1) Word Document (.docx) report matching
the reference friend document layout, headers, bullet symbols, titles, and formatting.

Topic: "Regular Expression Validator"
Group 3:
  1. Paras Pardhi (CD24027)
  2. Sahil Singh (CD24039)
  3. Barkha Thakur (CD24011)
  4. Sujal Kawale (CD25D008)

Course: Information Retrieval (N-PECCD601T) / Theory of Computation
Department: CSE (Data Science)
Guide: Dr. Dipak Wajgi, Associate Professor
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os, shutil


def set_cell_background(cell, fill_hex):
    """Sets the background color of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    """Sets inner padding for a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def add_page_header_banner(doc):
    """Adds the standard SBJAIN institution header table at the top of a page."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "FFFFFF")
    set_cell_margins(cell, top=40, bottom=40, left=40, right=40)
    
    # Thin border around header box
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'<w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'<w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.1

    r1 = p.add_run("S. B. JAIN INSTITUTE OF TECHNOLOGY, MANAGEMENT\n& RESEARCH, NAGPUR\n")
    r1.bold = True
    r1.font.size = Pt(11)

    r2 = p.add_run("(An Autonomous Institute, Affiliated to R.T.M. Nagpur University)\n")
    r2.font.size = Pt(8.5)

    r3 = p.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (DATA SCIENCE)\n")
    r3.bold = True
    r3.font.size = Pt(9.5)

    r4 = p.add_run("To create competent and creative professional in the field of Data Science to address the data-driven\ndecision-making for the benefits of industry and society")
    r4.font.size = Pt(7.5)
    r4.italic = True

    doc.add_paragraph().paragraph_format.space_after = Pt(10)


def create_exact_report():
    doc = docx.Document()

    # --- Page Margins (Normal 1 inch) ---
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Base Font
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    def add_title_heading(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(14)
        return p

    def add_sub_heading(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(12)
        return p

    def add_para_with_diamond(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        r_sym = p.add_run("❖ ")
        r_sym.bold = True
        p.add_run(text)
        return p

    # =========================================================================
    # PAGE 1: TITLE PAGE (INTACT EXACT FORMAT)
    # =========================================================================
    add_page_header_banner(doc)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(12)
    p_title.paragraph_format.line_spacing = 1.25

    rt1 = p_title.add_run("A Project Based Learning Report On\n\n")
    rt1.font.size = Pt(12)

    rt2 = p_title.add_run("“Regular Expression Validator”\n\n")
    rt2.bold = True
    rt2.font.size = Pt(18)

    rt3 = p_title.add_run("As a Tae -1 Report\n\n")
    rt3.bold = True
    rt3.font.size = Pt(13)

    rt4 = p_title.add_run("is submitted in partial fulfillment of the requirement for the award of degree of\n")
    rt4.font.size = Pt(11)

    rt5 = p_title.add_run("Bachelor of Technology\n")
    rt5.font.size = Pt(12)

    rt6 = p_title.add_run("(VI Semester B. Tech. for the course Information Retrieval (N-PECCD601T)\n")
    rt6.font.size = Pt(11)

    rt7 = p_title.add_run("in\n")
    rt7.font.size = Pt(11)

    rt8 = p_title.add_run("CSE (Data Science)\n\n")
    rt8.bold = True
    rt8.font.size = Pt(13)

    rt9 = p_title.add_run("Submitted by\n\n")
    rt9.font.size = Pt(11)

    rt10 = p_title.add_run(
        "Paras Pardhi (CD24027)\n"
        "Sahil Singh ( CD24039)\n"
        "Barkha Thakur (CD24011)\n"
        "Sujal Kawale (CD25D008)\n\n"
    )
    rt10.bold = True
    rt10.font.size = Pt(13)

    rt11 = p_title.add_run("Under the guidance of\n")
    rt11.italic = True
    rt11.font.size = Pt(11)

    rt12 = p_title.add_run("Dr. Dipak Wajgi\n")
    rt12.bold = True
    rt12.font.size = Pt(12)

    rt13 = p_title.add_run("Associate Professor\n\n")
    rt13.font.size = Pt(11)

    rt14 = p_title.add_run("Department of Emerging Technologies\nCSE (Data Science)\n\n")
    rt14.bold = True
    rt14.font.size = Pt(12)

    rt15 = p_title.add_run("S. B. Jain Institute of Technology, Management and Research, Nagpur\n")
    rt15.bold = True
    rt15.font.size = Pt(13)

    rt16 = p_title.add_run("(An Autonomous Institute Affiliated to R. T.M. Nagpur University)\n\n")
    rt16.font.size = Pt(10)

    rt17 = p_title.add_run("Academic Session: 2025-2026 (EVEN)")
    rt17.bold = True
    rt17.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: PROBLEM STATEMENT, OBJECTIVES, INTRODUCTION
    # =========================================================================
    add_page_header_banner(doc)

    add_title_heading(" Problem Statement:")
    p_ps = doc.add_paragraph(
        "To design and implement a web-based Regular Expression Validator using Finite Automata "
        "(ε-NFA and DFA) to check whether a given input string is accepted or rejected by the generated automaton."
    )
    p_ps.paragraph_format.space_after = Pt(12)

    add_title_heading(" Objectives: The main objectives of this project are:")
    objectives_list = [
        "To understand the basic working of Regular Expressions and Finite Automata (ε-NFA and DFA).",
        "To allow users to enter a regular expression and candidate input string.",
        "To construct an Epsilon-NFA from the regular expression using Thompson's Construction Algorithm.",
        "To convert the Epsilon-NFA into a Deterministic Finite Automaton (DFA) using Subset Construction.",
        "To check whether an input string is accepted or rejected by the defined automaton.",
        "To display the transition path followed by the input string.",
        "To provide a simple and interactive visualization of the finite automaton state diagram.",
        "To make the concepts of finite automata easier to understand through practical implementation."
    ]
    for obj in objectives_list:
        bp = doc.add_paragraph()
        bp.paragraph_format.space_after = Pt(3)
        r_b = bp.add_run("•  ")
        r_b.bold = True
        bp.add_run(obj)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_title_heading(" Introduction:")
    doc.add_paragraph(
        "Theory of Computation deals with mathematical models that help us understand how machines process and recognize input strings."
    ).paragraph_format.space_after = Pt(4)

    doc.add_paragraph(
        "A Regular Expression is a fundamental mathematical pattern used to specify regular languages. It can be converted into Finite Automata for string recognition."
    ).paragraph_format.space_after = Pt(4)

    doc.add_paragraph(
        "This project presents a web-based Regular Expression Validator using Finite Automata. The user can enter a regular expression and a candidate test string. "
        "The system automatically builds the corresponding Epsilon-NFA and DFA, processes the string, and evaluates string membership."
    ).paragraph_format.space_after = Pt(4)

    doc.add_paragraph(
        "The system shows the complete transition path and finally tells whether the given string is Accepted or Rejected."
    ).paragraph_format.space_after = Pt(6)

    add_para_with_diamond(
        "Theory of Computation is an important area of computer science that deals with the study of abstract machines and the problems "
        "that can be solved using them. It helps us understand how a machine reads input, processes it according to a set of rules, and produces "
        "a particular result. One of the basic and widely used models in Theory of Computation is the Finite Automaton."
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: INTRODUCTION CONTINUATION
    # =========================================================================
    add_page_header_banner(doc)

    add_para_with_diamond(
        "A Regular Expression is a mathematical model used to specify and recognize formal patterns over an alphabet. "
        "It consists of basic symbols and operations such as union (|), concatenation (.), and Kleene star (*). "
        "Finite Automata serve as the underlying computational engines to validate whether a string belongs to the language defined by the regex."
    )

    add_para_with_diamond(
        "In an Epsilon-NFA, transitions can occur spontaneously without consuming an input symbol (ε-transitions). "
        "In a Deterministic Finite Automaton (DFA), for every state and input symbol, there is exactly one defined next state. "
        "Thompson's Construction algorithm converts a regex into an ε-NFA, and Subset Construction converts the ε-NFA into an equivalent DFA."
    )

    add_para_with_diamond(
        "Although Regular Expression and Automata concepts are usually explained using state diagrams and transition tables, students may find "
        "it difficult to understand how an actual string moves through different states. A static diagram only shows the structure of the automaton "
        "and does not clearly show the complete execution of a particular input string."
    )

    add_para_with_diamond(
        "To make this concept more practical and easier to understand, this project develops a web-based Regular Expression Validator. "
        "The application allows the user to enter a regular expression and test string. The system transforms the expression and evaluates the string."
    )

    add_para_with_diamond(
        "The application also provides visual state diagrams for both ε-NFA and DFA, and displays the transition path followed by the input string. "
        "The current state can be highlighted during execution, allowing the user to observe how the DFA changes its state after reading each input symbol."
    )

    add_para_with_diamond(
        "For example, a regular expression (a|b)*abb can be designed to accept strings ending with 'abb'. For an input such as 'ababb', "
        "the DFA processes each symbol and finally reaches the accepting state. Therefore, the string is accepted. Similarly, an input such as 'abba' ends in a non-accepting state and is rejected."
    )

    add_para_with_diamond(
        "Thus, the project connects the theoretical concept of Finite Automata with a practical interactive application. "
        "It helps students understand Thompson's Construction, Subset Construction, transition functions, string processing and acceptance conditions in a simple and visual way."
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 4 & 5: METHODOLOGY
    # =========================================================================
    add_page_header_banner(doc)

    add_title_heading(" Methodology :")
    doc.add_paragraph(
        "The methodology followed for developing the Regular Expression Validator is divided into the following steps:"
    ).paragraph_format.space_after = Pt(8)

    add_sub_heading("1. Understanding the Automata Concept")
    doc.add_paragraph(
        "First, the basic concept of Deterministic Finite Automata and Epsilon-NFAs was studied. The five main components of a DFA were identified:\n"
        "M = (Q, Σ, δ, q₀, F)\n"
        "where Q represents states, Σ represents the input alphabet, δ represents the transition function, q₀ is the start state and F represents the final states."
    ).paragraph_format.space_after = Pt(8)

    add_sub_heading("2. Designing the User Interface")
    doc.add_paragraph(
        "A simple web interface was designed so that users can enter all the required regular expression information. Separate fields are provided for:"
    )
    ui_fields = ["Regular Expression Input", "Test Input String", "Preset Expression Selector", "Form Submit Option", "Automata Diagrams & Tables"]
    for field in ui_fields:
        bp = doc.add_paragraph()
        bp.paragraph_format.space_after = Pt(2)
        bp.add_run("•  ").bold = True
        bp.add_run(field)
    doc.add_paragraph("The interface also contains buttons for building the finite automaton and running the input string.").paragraph_format.space_after = Pt(8)

    add_sub_heading("3. Defining the Regular Expression")
    doc.add_paragraph(
        "The user enters the regular expression. The system automatically inserts explicit concatenation operators (.) where concatenation is implicit (e.g., 'ab' -> 'a.b')."
    ).paragraph_format.space_after = Pt(8)

    add_sub_heading("4. Converting Infix Regular Expression to Postfix")
    doc.add_paragraph(
        "Dijkstra's Shunting-Yard algorithm is implemented to convert the infix expression into postfix (Reverse Polish Notation) based on operator precedence (* > . > |)."
    ).paragraph_format.space_after = Pt(8)

    add_sub_heading("5. Building the Epsilon-NFA (Thompson's Construction)")
    doc.add_paragraph(
        "Using the postfix expression, Thompson's Construction Algorithm builds primitive NFAs for symbols, unions (|), concatenations (.), and Kleene closure (*)."
    ).paragraph_format.space_after = Pt(8)

    doc.add_page_break()

    # Page 5 Methodology Continuation
    add_page_header_banner(doc)

    add_sub_heading("6. Entering the Input String")
    doc.add_paragraph(
        "The user enters a string that belongs to the defined alphabet.\n"
        "For example:\n"
        "ababb\n"
        "The system first checks whether all characters in the input string are valid according to the selected alphabet."
    ).paragraph_format.space_after = Pt(8)

    add_sub_heading("7. Processing the String (Subset Construction & DFA Transition)")
    doc.add_paragraph(
        "The Epsilon-NFA is converted into a DFA using Subset Construction (ε-closures and move functions). "
        "The application starts from the start state and processes the string character by character.\n"
        "For every input symbol:\n\n"
        "                      Current State + Input Symbol\n"
        "                                    ↓\n"
        "                           Transition Function\n"
        "                                    ↓\n"
        "                                Next State\n\n"
        "The process continues until the complete string has been read."
    ).paragraph_format.space_after = Pt(8)

    add_sub_heading("8. Displaying the Transition Path")
    doc.add_paragraph(
        "The application records and displays the states visited during execution.\n"
        "For example:\n"
        "D0 → D1 → D3 → D1 → D3 → D4\n"
        "The user can also view the step-by-step execution trace."
    ).paragraph_format.space_after = Pt(8)

    add_sub_heading("9. Checking Acceptance")
    doc.add_paragraph(
        "After the complete input string is processed, the final state is compared with the set of accepting states.\n"
        "If the final state is an accepting state → String Accepted\n"
        "If the final state is not an accepting state → String Rejected"
    ).paragraph_format.space_after = Pt(8)

    add_sub_heading("10. Testing the Application")
    doc.add_paragraph(
        "Different input strings are tested to verify that the DFA gives the correct result. Both accepted and rejected strings are tested to ensure that the transition logic and acceptance condition work correctly."
    ).paragraph_format.space_after = Pt(8)

    add_sub_heading("11. Deployment")
    doc.add_paragraph(
        "The completed web application is stored in a GitHub repository (https://github.com/Barkha777/TOC-Regex-Validator) and can be deployed using Vercel, allowing the project to be accessed through a web browser."
    ).paragraph_format.space_after = Pt(8)

    doc.add_page_break()

    # =========================================================================
    # PAGE 6 & 7: CODE SECTION (NO IMAGES, CLEAN SPACING)
    # =========================================================================
    add_page_header_banner(doc)

    add_title_heading("CODE:")
    # Leaving clean blank lines for student to add screenshot of code if desired
    for _ in range(12):
        doc.add_paragraph()

    doc.add_page_break()

    add_page_header_banner(doc)
    for _ in range(15):
        doc.add_paragraph()

    doc.add_page_break()

    # =========================================================================
    # PAGE 8 & 9: OUTPUT SECTION (NO IMAGES, CLEAN SPACING)
    # =========================================================================
    add_page_header_banner(doc)

    add_title_heading(" Output:")
    # Leaving clean blank lines for student to add screenshot of output
    for _ in range(12):
        doc.add_paragraph()

    doc.add_page_break()

    add_page_header_banner(doc)
    for _ in range(15):
        doc.add_paragraph()

    doc.add_page_break()

    # =========================================================================
    # PAGE 10: PROJECT LINKS, CONCLUSION, EVALUATION PARAMETERS
    # =========================================================================
    add_page_header_banner(doc)

    add_title_heading(" PROJECT LINKS")
    p_links = doc.add_paragraph()
    p_links.paragraph_format.space_after = Pt(8)
    p_links.add_run("GitHub Repository:\n").bold = True
    r_g = p_links.add_run("https://github.com/Barkha777/TOC-Regex-Validator\n\n")
    r_g.underline = True
    r_g.font.color.rgb = RGBColor(0, 0, 255)

    p_links.add_run("Live Website:\n").bold = True
    r_w = p_links.add_run("https://toc-regex-validator.vercel.app/\n")
    r_w.underline = True
    r_w.font.color.rgb = RGBColor(0, 0, 255)

    add_title_heading(" Conclusion:")
    doc.add_paragraph(
        "The project successfully demonstrates the working of a Regular Expression Validator through an interactive web-based application."
    ).paragraph_format.space_after = Pt(4)

    doc.add_paragraph(
        "The system allows users to enter a regular expression, converts it into an ε-NFA using Thompson's Construction, generates an equivalent DFA using Subset Construction, and tests different input strings. "
        "It shows the transition path followed by the string and determines whether the string is accepted or rejected based on the final state."
    ).paragraph_format.space_after = Pt(4)

    doc.add_paragraph(
        "The visual diagram and step-by-step execution make the concept of Regular Expressions, Thompson's Construction, and Subset Construction easier to understand and demonstrate. "
        "Overall, the project provides a simple and practical way to connect the theoretical concepts of Theory of Computation with their implementation."
    ).paragraph_format.space_after = Pt(10)

    # Evaluation Parameters Table (Matches exact reference format)
    p_tbl_title = doc.add_paragraph()
    p_tbl_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_tt = p_tbl_title.add_run("Evaluation Parameters")
    r_tt.bold = True
    r_tt.font.size = Pt(11)

    eval_table = doc.add_table(rows=5, cols=8)
    eval_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    eval_table.autofit = False

    headers = [
        "Sr.\nNo", "Roll No. /USN No.", "Name of Student", 
        "Faculty\nAssessment\n(4M)", "Submission\n(3M)", "Viva\n(3M)", "Total\n(10M)", "Signature"
    ]
    widths = [
        Inches(0.4), Inches(1.3), Inches(1.7), 
        Inches(0.7), Inches(0.7), Inches(0.5), Inches(0.6), Inches(0.6)
    ]

    hdr_cells = eval_table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].width = widths[i]
        set_cell_background(hdr_cells[i], "FFFFFF")
        set_cell_margins(hdr_cells[i], top=40, bottom=40, left=40, right=40)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(8.5)

    students = [
        ("1", "CD24027", "Paras Pardhi"),
        ("2", "CD24039", "Sahil Singh"),
        ("3", "CD24011", "Barkha Thakur"),
        ("4", "CD25D008", "Sujal Kawale")
    ]

    for idx, (sr, roll, name) in enumerate(students):
        row_cells = eval_table.rows[idx + 1].cells
        row_data = [sr, roll, name, "", "", "", "", ""]
        for i, val in enumerate(row_data):
            row_cells[i].width = widths[i]
            set_cell_background(row_cells[i], "FFFFFF")
            set_cell_margins(row_cells[i], top=40, bottom=40, left=40, right=40)
            p = row_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i != 2 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if i in [0, 1, 2]:
                r.bold = True

    # Border for Evaluation Table
    for row in eval_table.rows:
        for cell in row.cells:
            tcPr = cell._element.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                f'<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                f'<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(tcBorders)

    doc.add_paragraph().paragraph_format.space_after = Pt(20)

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sig = p_sig.add_run("Signature of Course In-Charge")
    r_sig.bold = True
    r_sig.font.size = Pt(11)

    # Save to local workspace & Desktop
    local_path = r"c:\Users\Barkha\Downloads\TOC\Group3_PBL_TAE1_Report_Regular_Expression_Validator.docx"
    doc.save(local_path)
    print(f"Report saved locally to: {local_path}")

    # Copy to Desktop and OneDrive Desktop
    desktops = [
        r"C:\Users\Barkha\Desktop",
        r"C:\Users\Barkha\OneDrive\Desktop"
    ]
    for d in desktops:
        if os.path.exists(d):
            dst = os.path.join(d, "Group3_PBL_TAE1_Report_Regular_Expression_Validator.docx")
            try:
                shutil.copy2(local_path, dst)
                print(f"Report successfully copied to Desktop: {dst}")
            except Exception as e:
                print(f"Could not copy to {dst}: {e}")

if __name__ == "__main__":
    create_exact_report()
