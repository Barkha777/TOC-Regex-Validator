"""
dfa.py
------
Implements Subset Construction (Power Set Construction) algorithm to convert
an epsilon-NFA to a Deterministic Finite Automaton (DFA).
"""

from typing import Dict, Set, FrozenSet, List, Optional
from nfa import NFA, State


class DFAState:
    """
    Represents a single state in a DFA, which corresponds to a subset (frozenset)
    of NFA states.
    
    Attributes:
        name (str): Label for the DFA state (e.g., 'D0', 'D1').
        nfa_states (FrozenSet[State]): The set of underlying NFA states.
        is_accept (bool): True if at least one underlying NFA state is an NFA accept state.
        transitions (Dict[str, DFAState]): Deterministic transitions mapping input symbol to target DFAState.
    """
    def __init__(self, name: str, nfa_states: FrozenSet[State], is_accept: bool):
        self.name: str = name
        self.nfa_states: FrozenSet[State] = nfa_states
        self.is_accept: bool = is_accept
        self.transitions: Dict[str, 'DFAState'] = {}

    def add_transition(self, symbol: str, target: 'DFAState') -> None:
        """Adds a deterministic transition on symbol to target DFAState."""
        self.transitions[symbol] = target

    def __repr__(self) -> str:
        sorted_nfa = sorted([f"q{s.state_id}" for s in self.nfa_states])
        acc_tag = "*" if self.is_accept else ""
        return f"{acc_tag}{self.name}{{{','.join(sorted_nfa)}}}"


class DFA:
    """
    Represents a complete Deterministic Finite Automaton.
    """
    def __init__(self, start_state: DFAState, alphabet: Set[str]):
        self.start_state: DFAState = start_state
        self.alphabet: Set[str] = alphabet
        self.states: Set[DFAState] = set()
        self.accept_states: Set[DFAState] = set()
        self._collect_automaton_info()

    def _collect_automaton_info(self) -> None:
        """Traverses the DFA from the start_state to collect all reachable states and accept states."""
        visited: Set[DFAState] = set()
        queue: List[DFAState] = [self.start_state]
        visited.add(self.start_state)

        while queue:
            current = queue.pop(0)
            self.states.add(current)
            if current.is_accept:
                self.accept_states.add(current)
                
            for symbol, target in current.transitions.items():
                if target not in visited:
                    visited.add(target)
                    queue.append(target)


def epsilon_closure(states: Set[State]) -> FrozenSet[State]:
    """
    Computes the \u03b5-closure of a set of NFA states.
    The \u03b5-closure is the set of all NFA states reachable from any state in `states`
    by following 0 or more \u03b5 (None) transitions.
    """
    closure: Set[State] = set(states)
    stack: List[State] = list(states)

    while stack:
        current = stack.pop()
        # Epsilon transitions are stored under key `None`
        for target in current.transitions.get(None, set()):
            if target not in closure:
                closure.add(target)
                stack.append(target)

    return frozenset(closure)


def move(states: FrozenSet[State], symbol: str) -> Set[State]:
    """
    Computes the set of NFA states reachable from any state in `states` on input `symbol`.
    (Does NOT include \u03b5-closure of the destination states).
    """
    reachable: Set[State] = set()
    for state in states:
        for target in state.transitions.get(symbol, set()):
            reachable.add(target)
    return reachable


def subset_construction(nfa: NFA) -> DFA:
    """
    Converts an \u03b5-NFA into a DFA using the Subset Construction algorithm.
    """
    alphabet = nfa.get_alphabet()
    state_counter = 0

    # 1. Start state of DFA is the \u03b5-closure of the NFA start state
    initial_nfa_set = epsilon_closure({nfa.start_state})
    
    # Map frozenset of NFA states -> DFAState object
    nfa_set_to_dfa_state: Dict[FrozenSet[State], DFAState] = {}
    
    def create_dfa_state(nfa_set: FrozenSet[State]) -> DFAState:
        nonlocal state_counter
        is_accept = any(s == nfa.accept_state for s in nfa_set)
        name = f"D{state_counter}"
        state_counter += 1
        dfa_state = DFAState(name, nfa_set, is_accept)
        nfa_set_to_dfa_state[nfa_set] = dfa_state
        return dfa_state

    start_dfa_state = create_dfa_state(initial_nfa_set)
    unprocessed: List[FrozenSet[State]] = [initial_nfa_set]

    # 2. Process subsets until no new subsets are discovered
    while unprocessed:
        current_nfa_set = unprocessed.pop(0)
        current_dfa_state = nfa_set_to_dfa_state[current_nfa_set]

        for symbol in sorted(alphabet):
            # Compute move(current_nfa_set, symbol)
            move_set = move(current_nfa_set, symbol)
            
            if not move_set:
                # No transition on this symbol from current subset
                continue

            # Compute \u03b5-closure of the move destination
            target_nfa_set = epsilon_closure(move_set)

            if target_nfa_set not in nfa_set_to_dfa_state:
                new_state = create_dfa_state(target_nfa_set)
                unprocessed.append(target_nfa_set)

            target_dfa_state = nfa_set_to_dfa_state[target_nfa_set]
            current_dfa_state.add_transition(symbol, target_dfa_state)

    return DFA(start_dfa_state, alphabet)
