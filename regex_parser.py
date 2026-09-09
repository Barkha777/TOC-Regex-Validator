"""
regex_parser.py
---------------
Provides tools for preprocessing and parsing regular expressions.
Supports:
  - Operators: '|' (Union), '.' (Concatenation), '*' (Kleene Star), '(' and ')' (Grouping)
  - Explicit concatenation insertion (e.g., 'ab' -> 'a.b')
  - Infix to Postfix conversion via Dijkstra's Shunting-Yard Algorithm.
"""

def insert_explicit_concat(regex: str) -> str:
    """
    Inserts explicit concatenation operator '.' into a regular expression.
    
    Concatenation occurs between:
      1. Symbol and Symbol: 'ab' -> 'a.b'
      2. Symbol and '('   : 'a(b)' -> 'a.(b)'
      3. '*' and Symbol   : 'a*b' -> 'a*.b'
      4. '*' and '('      : 'a*(b)' -> 'a*.(b)'
      5. ')' and Symbol   : '(a)b' -> '(a).b'
      6. ')' and '('      : '(a)(b)' -> '(a).(b)'
    """
    if not regex:
        return ""
    
    result = []
    operators = {'|', '*', '(', ')'}
    
    for i in range(len(regex)):
        c1 = regex[i]
        result.append(c1)
        
        if i + 1 < len(regex):
            c2 = regex[i + 1]
            
            # Conditions under which c1 can end an operand
            c1_is_operand_end = (c1 not in operators and c1 != '.') or c1 in {'*', ')'}
            # Conditions under which c2 can start an operand
            c2_is_operand_start = (c2 not in operators and c2 != '.') or c2 == '('
            
            if c1_is_operand_end and c2_is_operand_start:
                result.append('.')
                
    return "".join(result)


def infix_to_postfix(regex: str) -> str:
    """
    Converts an infix regular expression to postfix (Reverse Polish Notation)
    using Dijkstra's Shunting-Yard algorithm.
    
    Operator Precedence:
      '*' : 3 (Highest)
      '.' : 2 (Concatenation)
      '|' : 1 (Union, Lowest)
    """
    # First ensure explicit concatenation operators are present
    formatted_regex = insert_explicit_concat(regex)
    
    output = []
    operator_stack = []
    
    precedence = {
        '*': 3,
        '.': 2,
        '|': 1
    }
    
    for char in formatted_regex:
        if char not in precedence and char not in {'(', ')'}:
            # Character is an alphabet symbol
            output.append(char)
        elif char == '(':
            operator_stack.append(char)
        elif char == ')':
            # Pop operators until matching '(' is found
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            if not operator_stack:
                raise ValueError(f"Mismatched parentheses in expression: {regex}")
            operator_stack.pop()  # Discard '('
        else:
            # Token is an operator: '*', '.', or '|'
            while (operator_stack and 
                   operator_stack[-1] != '(' and 
                   precedence.get(operator_stack[-1], 0) >= precedence[char]):
                output.append(operator_stack.pop())
            operator_stack.append(char)
            
    while operator_stack:
        op = operator_stack.pop()
        if op in {'(', ')'}:
            raise ValueError(f"Mismatched parentheses in expression: {regex}")
        output.append(op)
        
    return "".join(output)


if __name__ == "__main__":
    # Quick self-test for parser module
    test_cases = [
        ("a", "a"),
        ("ab", "a.b"),
        ("a*b", "a*.b"),
        ("(a|b)*abb", "(a|b)*.a.b.b"),
    ]
    for expr, expected_concat in test_cases:
        concat = insert_explicit_concat(expr)
        postfix = infix_to_postfix(expr)
        print(f"Infix: {expr:<12} | Concat: {concat:<16} | Postfix: {postfix}")
