"""
nfa.py
------
Defines data structures for NFA states and NFA fragments, and implements
Thompson's Construction Algorithm to build an epsilon-NFA from postfix regex.
"""

from typing import Dict, Set, Optional, List


class State:
    """
    Represents a single state in an NFA.
    
    Attributes:
        state_id (int): Unique numeric identifier for the state.
        transitions (Dict[Optional[str], Set[State]]): 
            Maps an input symbol (or None for epsilon transitions) to a set of destination states.
    """
    def __init__(self, state_id: int):
        self.state_id: int = state_id
        # None represents epsilon transition (\u03b5)
        self.transitions: Dict[Optional[str], Set['State']] = {}

    def add_transition(self, symbol: Optional[str], target: 'State') -> None:
        """Adds a directed transition from this state to the target state on the given symbol."""
        if symbol not in self.transitions:
            self.transitions[symbol] = set()
        self.transitions[symbol].add(target)

    def __repr__(self) -> str:
        return f"q{self.state_id}"

    def __lt__(self, other: 'State') -> bool:
        return self.state_id < other.state_id


class NFA:
    """
    Represents an NFA fragment with exactly one start state and one accept state.
    Thompson's construction ensures all sub-NFAs satisfy this single-entry, single-exit property.
    """
    def __init__(self, start_state: State, accept_state: State):
        self.start_state: State = start_state
        self.accept_state: State = accept_state

    def get_all_states(self) -> Set[State]:
        """Traverses the NFA starting from start_state using BFS to collect all states."""
        visited: Set[State] = set()
        queue: List[State] = [self.start_state]
        visited.add(self.start_state)
        
        while queue:
            current = queue.pop(0)
            for symbol, targets in current.transitions.items():
                for target in targets:
                    if target not in visited:
                        visited.add(target)
                        queue.append(target)
        return visited

    def get_alphabet(self) -> Set[str]:
        """Returns the set of input symbols present in the NFA (excluding epsilon/None)."""
        alphabet: Set[str] = set()
        for state in self.get_all_states():
            for symbol in state.transitions.keys():
                if symbol is not None:
                    alphabet.add(symbol)
        return alphabet


class ThompsonBuilder:
    """
    Implements Thompson's Construction Algorithm components and orchestrator.
    """
    def __init__(self):
        self.state_counter: int = 0

    def _create_state(self) -> State:
        """Helper to instantiate a new State with an auto-incrementing ID."""
        state = State(self.state_counter)
        self.state_counter += 1
        return state

    def symbol(self, char: str) -> NFA:
        """
        Base Case: Primitive NFA for a single character (or symbol).
        Creates: s_start --char--> s_accept
        """
        start = self._create_state()
        accept = self._create_state()
        start.add_transition(char, accept)
        return NFA(start, accept)

    def concat(self, nfa1: NFA, nfa2: NFA) -> NFA:
        """
        Concatenation Primitive (N1 . N2):
        Connects accept state of N1 to start state of N2 via an epsilon transition.
        Creates: N1.start ... N1.accept --\u03b5--> N2.start ... N2.accept
        """
        nfa1.accept_state.add_transition(None, nfa2.start_state)
        return NFA(nfa1.start_state, nfa2.accept_state)

    def union(self, nfa1: NFA, nfa2: NFA) -> NFA:
        """
        Union Primitive (N1 | N2):
        Creates a new start and accept state.
        Adds \u03b5-transitions from new start to N1.start and N2.start.
        Adds \u03b5-transitions from N1.accept and N2.accept to new accept.
        """
        start = self._create_state()
        accept = self._create_state()

        start.add_transition(None, nfa1.start_state)
        start.add_transition(None, nfa2.start_state)

        nfa1.accept_state.add_transition(None, accept)
        nfa2.accept_state.add_transition(None, accept)

        return NFA(start, accept)

    def kleene_star(self, nfa: NFA) -> NFA:
        """
        Kleene Star Primitive (N*):
        Creates a new start and accept state.
        Adds \u03b5-transitions:
          - start --> nfa.start (enter NFA)
          - start --> accept    (skip NFA for empty string)
          - nfa.accept --> nfa.start (loop back for repeated matches)
          - nfa.accept --> accept    (exit loop)
        """
        start = self._create_state()
        accept = self._create_state()

        start.add_transition(None, nfa.start_state)
        start.add_transition(None, accept)

        nfa.accept_state.add_transition(None, nfa.start_state)
        nfa.accept_state.add_transition(None, accept)

        return NFA(start, accept)

    def build_nfa(self, postfix_regex: str) -> NFA:
        """
        Constructs an \u03b5-NFA from a postfix regular expression string using a stack.
        """
        stack: List[NFA] = []

        for char in postfix_regex:
            if char == '.':
                if len(stack) < 2:
                    raise ValueError("Malformed postfix expression for concatenation")
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(self.concat(n1, n2))
            elif char == '|':
                if len(stack) < 2:
                    raise ValueError("Malformed postfix expression for union")
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(self.union(n1, n2))
            elif char == '*':
                if len(stack) < 1:
                    raise ValueError("Malformed postfix expression for Kleene star")
                n1 = stack.pop()
                stack.append(self.kleene_star(n1))
            else:
                # Regular alphabet symbol
                stack.append(self.symbol(char))

        if len(stack) != 1:
            raise ValueError(f"Malformed expression '{postfix_regex}': stack remaining items = {len(stack)}")

        return stack.pop()
