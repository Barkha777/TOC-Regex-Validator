"""
simulator.py
------------
Simulates DFA processing on input strings and provides detailed execution traces.
"""

from typing import Tuple, List
from dfa import DFA, DFAState


class DFASimulator:
    """
    Executes a DFA on candidate input strings to test membership in the language.
    """

    @staticmethod
    def validate(dfa: DFA, input_string: str) -> Tuple[bool, List[str]]:
        """
        Validates an input string against the DFA.

        Args:
            dfa (DFA): The compiled Deterministic Finite Automaton.
            input_string (str): The candidate string to test.

        Returns:
            Tuple[bool, List[str]]: (is_accepted, step_by_step_execution_trace)
        """
        current_state: DFAState = dfa.start_state
        trace: List[str] = [
            f"Initial State: {current_state.name} (Accept: {current_state.is_accept})"
        ]

        # Handle empty string \u03b5
        if input_string == "":
            is_accepted = current_state.is_accept
            trace.append(f"Input is empty string (\u03b5). Accepted: {is_accepted}")
            return is_accepted, trace

        for idx, char in enumerate(input_string):
            if char not in current_state.transitions:
                trace.append(
                    f"Step {idx + 1}: Symbol '{char}' -> No valid transition from state {current_state.name}. Trap/Rejected."
                )
                return False, trace

            next_state = current_state.transitions[char]
            trace.append(
                f"Step {idx + 1}: Symbol '{char}' -> Transition {current_state.name} -> {next_state.name}"
            )
            current_state = next_state

        is_accepted = current_state.is_accept
        status = "ACCEPTED" if is_accepted else "REJECTED (Ended in non-accepting state)"
        trace.append(f"Final State: {current_state.name} -> Result: {status}")

        return is_accepted, trace
