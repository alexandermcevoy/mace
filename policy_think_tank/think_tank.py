"""
think_tank.py — Entry point for the AI Policy Think Tank.

Usage:
    python think_tank.py "Should the US implement a carbon tax?"
    python think_tank.py  # interactive prompt if no argument given

Environment variable required:
    ANTHROPIC_API_KEY  — your Anthropic API key
"""

from __future__ import annotations

import sys
import anthropic

from agents import make_policy_researcher, make_devils_advocate, make_economist, make_director
from debate import run_debate
from brief import render_brief


# ---------------------------------------------------------------------------
# Synthesis instruction (passed to the Director as the final user message)
# ---------------------------------------------------------------------------

SYNTHESIS_INSTRUCTION = """\
The deliberative debate is now complete. Using everything discussed in the
transcript above, produce a comprehensive, structured policy brief.

Output exactly the following five sections using ## markdown headers,
with substantive content under each:

## Executive Summary
(2–3 sentences capturing the core policy question and the think tank's
overall conclusion)

## Research Findings
(Key evidence, precedents, and empirical findings surfaced during debate)

## Economic Analysis
(Cost-benefit assessment, distributional effects, and key assumptions)

## Counterarguments and Risks
(The strongest objections raised, and how they were or were not resolved)

## Final Recommendation
(A clear, defensible policy recommendation with specific justification
drawn from the debate. Do not hedge into uselessness — take a position.)
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_policy_question() -> str:
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:])
    print("AI Policy Think Tank")
    print("=" * 40)
    return input("Enter a policy question: ").strip()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    question = get_policy_question()
    if not question:
        print("Error: no policy question provided.", file=sys.stderr)
        sys.exit(1)

    print(f"\nPolicy question: {question}")
    print("\nInitializing think tank agents...")

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment

    researcher = make_policy_researcher(client)
    advocate   = make_devils_advocate(client)
    economist  = make_economist(client)
    director   = make_director(client)

    # Run the deliberative debate (prints progress to stdout as it goes)
    debate_state = run_debate(
        policy_question=question,
        researcher=researcher,
        advocate=advocate,
        economist=economist,
        director=director,
        num_rounds=2,
    )

    # Director synthesizes the full transcript into a structured brief
    print("\n" + "=" * 60)
    print("PHASE 4: DIRECTOR SYNTHESIS")
    print("=" * 60)
    print("\n[DIRECTOR] synthesizing policy brief...")

    synthesis = director.respond(
        debate_context=debate_state.transcript,
        user_query=question,
        instruction=SYNTHESIS_INSTRUCTION,
    )

    # Render and print the final policy brief
    brief = render_brief(question, debate_state, synthesis)

    print("\n\n" + "=" * 60)
    print("FINAL POLICY BRIEF")
    print("=" * 60 + "\n")
    print(brief)


if __name__ == "__main__":
    main()
