"""
main.py
-------
Main entry point, CLI visualizer, and comprehensive Unit Test suite for the
Regex -> Epsilon-NFA (Thompson) -> DFA (Subset Construction) pipeline.
"""

import unittest
from typing import List, Tuple
from regex_parser import infix_to_postfix, insert_explicit_concat
from nfa import ThompsonBuilder, NFA
from dfa import subset_construction, DFA
from simulator import DFASimulator


def compile_regex_to_dfa(regex: str) -> Tuple[str, str, NFA, DFA]:
    """
    Full pipeline wrapper:
    Regex -> Explicit Concat -> Postfix -> Epsilon-NFA -> DFA
    """
    explicit_concat = insert_explicit_concat(regex)
    postfix = infix_to_postfix(regex)
    builder = ThompsonBuilder()
    nfa = builder.build_nfa(postfix)
    dfa = subset_construction(nfa)
    return explicit_concat, postfix, nfa, dfa


def print_dfa_table(dfa: DFA) -> None:
    """Pretty prints the transition table of a DFA."""
    alphabet = sorted(list(dfa.alphabet))
    header = f"{'State':<12} | {'Accept?':<8} | " + " | ".join([f"{sym:<6}" for sym in alphabet]) + " | NFA Subset"
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    
    sorted_states = sorted(list(dfa.states), key=lambda s: s.name)
    for state in sorted_states:
        is_acc = "Yes" if state.is_accept else "No"
        trans_str = []
        for sym in alphabet:
            target = state.transitions.get(sym)
            trans_str.append(f"{target.name:<6}" if target else f"{'-':<6}")
        
        sorted_nfa = sorted([f"q{s.state_id}" for s in state.nfa_states])
        subset_str = "{" + ",".join(sorted_nfa) + "}"
        print(f"{state.name:<12} | {is_acc:<8} | " + " | ".join(trans_str) + f" | {subset_str}")
    print("-" * len(header))


def demo() -> None:
    """Demonstrates pipeline execution on a classic regular expression: (a|b)*abb"""
    regex = "(a|b)*abb"
    print("=" * 70)
    print(f" THEORY OF COMPUTATION DEMO: REGEX TO DFA")
    print(f" Input Regular Expression: '{regex}'")
    print("=" * 70)
    
    concat, postfix, nfa, dfa = compile_regex_to_dfa(regex)
    print(f"1. Explicit Concatenation: {concat}")
    print(f"2. Postfix Notation      : {postfix}")
    print(f"3. Epsilon-NFA           : {len(nfa.get_all_states())} states generated via Thompson's Construction.")
    print(f"4. DFA                   : {len(dfa.states)} states generated via Subset Construction.\n")
    
    print("--- DFA Transition Table ---")
    print_dfa_table(dfa)
    print()

    # Sample test strings for (a|b)*abb
    sample_strings = ["abb", "aabb", "babb", "ababb", "a", "ab", "abba", "bbbb"]
    print("--- String Validation Trace ---")
    for s in sample_strings:
        accepted, trace = DFASimulator.validate(dfa, s)
        res_label = "MATCH" if accepted else "NO MATCH"
        print(f"String '{s:<6}' -> Result: [{res_label}]")
    print()


class TestAutomataPipeline(unittest.TestCase):
    """Automated Unit Tests for regular expression matching via Thompson & Subset construction."""

    def check_regex(self, regex: str, positive_cases: List[str], negative_cases: List[str]):
        _, _, _, dfa = compile_regex_to_dfa(regex)
        for s in positive_cases:
            accepted, _ = DFASimulator.validate(dfa, s)
            self.assertTrue(accepted, f"Expected '{s}' to match regex '{regex}'")
        for s in negative_cases:
            accepted, _ = DFASimulator.validate(dfa, s)
            self.assertFalse(accepted, f"Expected '{s}' to NOT match regex '{regex}'")

    def test_single_character(self):
        self.check_regex("a", positive_cases=["a"], negative_cases=["", "b", "aa"])

    def test_concatenation(self):
        self.check_regex("ab", positive_cases=["ab"], negative_cases=["", "a", "b", "aba", "abb"])
        self.check_regex("abc", positive_cases=["abc"], negative_cases=["ab", "ac", "abcd"])

    def test_union(self):
        self.check_regex("a|b", positive_cases=["a", "b"], negative_cases=["", "ab", "ba", "c"])
        self.check_regex("a|b|c", positive_cases=["a", "b", "c"], negative_cases=["", "ab", "bc", "d"])

    def test_kleene_star(self):
        self.check_regex("a*", positive_cases=["", "a", "aa", "aaa", "aaaaa"], negative_cases=["b", "ab", "ba"])

    def test_combined_operations(self):
        # Matches strings of 'a' and 'b' ending in 'abb'
        self.check_regex("(a|b)*abb", 
                         positive_cases=["abb", "aabb", "babb", "ababb", "bbaabb"], 
                         negative_cases=["", "a", "ab", "abba", "abbb", "b"])

        # Matches 'a' followed by any number of 'b's
        self.check_regex("ab*", 
                         positive_cases=["a", "ab", "abb", "abbbb"], 
                         negative_cases=["", "b", "ba", "aab"])

        # Union with Kleene star
        self.check_regex("(a|b)*", 
                         positive_cases=["", "a", "b", "ab", "ba", "aaaa", "bbbb", "ababab"], 
                         negative_cases=["c", "abc"])


if __name__ == "__main__":
    demo()
    print("=" * 70)
    print(" RUNNING UNIT TEST SUITE")
    print("=" * 70)
    unittest.main()
