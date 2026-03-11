"""
debate.py — Debate orchestration loop, DebateState, and transcript management.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from agents import Agent, Message


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

@dataclass
class DebateState:
    policy_question: str
    rounds: list[dict] = field(default_factory=list)
    transcript: list[Message] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Transcript helpers
# ---------------------------------------------------------------------------

def append_to_transcript(
    transcript: list[Message],
    role_label: str,
    content: str,
    api_role: str = "assistant",
) -> None:
    """Append a labeled message to the shared transcript."""
    transcript.append(Message(role=api_role, content=f"[{role_label}]: {content}"))


def append_instruction(
    transcript: list[Message],
    instruction: str,
) -> None:
    """Append a Director instruction (user-role) to the transcript."""
    transcript.append(Message(role="user", content=f"[DIRECTOR INSTRUCTION]: {instruction}"))


# ---------------------------------------------------------------------------
# Director instruction builders
# ---------------------------------------------------------------------------

def _opening_instruction(agent_name: str, policy_question: str) -> str:
    instructions = {
        "researcher": (
            f"Policy Researcher, please provide your opening research findings on "
            f"the following policy question:\n\n\"{policy_question}\"\n\n"
            "Cover key empirical evidence, relevant historical precedents, and "
            "important literature. Be specific and cite concrete examples."
        ),
        "economist": (
            "Economist, the Policy Researcher has provided their opening findings. "
            "Please provide your opening economic analysis of this policy question. "
            "Cover the primary costs and benefits, distributional effects, and any "
            "significant market or incentive considerations. Be transparent about "
            "your assumptions."
        ),
        "advocate": (
            "Devil's Advocate, the Researcher and Economist have given their opening "
            "statements. Please challenge their analyses: identify the most significant "
            "unstated assumptions, empirical weaknesses, and potential second-order "
            "consequences they have overlooked. End by naming your single most "
            "important objection."
        ),
    }
    return instructions[agent_name]


def build_director_instruction(
    round_num: int,
    agent_name: str,
    previous_responses: dict[str, str],
) -> str:
    """
    Generate a targeted per-round instruction for a specialist agent,
    referencing what other agents said in the most recent round.
    """
    da_text = previous_responses.get("advocate", "")
    researcher_text = previous_responses.get("researcher", "")
    economist_text = previous_responses.get("economist", "")

    if agent_name == "researcher":
        objection_hint = ""
        if da_text:
            # Extract the "most important objection" the DA named
            lines = [l.strip() for l in da_text.splitlines() if l.strip()]
            last_line = lines[-1] if lines else ""
            objection_hint = f'\n\nThe Devil\'s Advocate ended with: "{last_line}"'
        return (
            f"Policy Researcher (Round {round_num}): The Devil's Advocate has raised "
            f"serious objections to the evidence base. Address their critique directly "
            f"with specific counter-evidence or concede where the evidence is genuinely "
            f"weak.{objection_hint}"
        )

    elif agent_name == "economist":
        return (
            f"Economist (Round {round_num}): The Devil's Advocate has challenged your "
            f"economic framing. Respond to their specific critique — do not simply "
            f"restate your prior position. Where are your cost-benefit estimates most "
            f"vulnerable, and how do you defend them?"
        )

    elif agent_name == "advocate":
        return (
            f"Devil's Advocate (Round {round_num}): The Researcher and Economist have "
            f"responded to your objections. Have they adequately addressed your most "
            f"important concern? If not, press harder. If yes, identify a new, deeper "
            f"vulnerability in their analysis. End again by naming your single most "
            f"important remaining objection."
        )

    return f"Round {round_num}: Please continue your analysis."


def _closing_instruction(agent_name: str) -> str:
    role_map = {
        "researcher": "Policy Researcher",
        "economist": "Economist",
        "advocate": "Devil's Advocate",
    }
    role = role_map.get(agent_name, agent_name)
    return (
        f"{role}: In exactly one sentence, state the single strongest reason "
        f"for or against this policy based on everything discussed."
    )


# ---------------------------------------------------------------------------
# Main debate loop
# ---------------------------------------------------------------------------

def run_debate(
    policy_question: str,
    researcher: Agent,
    advocate: Agent,
    economist: Agent,
    director: Agent,
    num_rounds: int = 2,
) -> DebateState:
    """
    Orchestrate the full multi-round deliberative debate.

    Returns a DebateState with the complete transcript.
    """
    state = DebateState(policy_question=policy_question)

    # Seed transcript with the policy question as the first user message
    state.transcript.append(
        Message(role="user", content=f"Policy question under deliberation: {policy_question}")
    )

    agents_ordered = [
        ("researcher", researcher),
        ("economist", economist),
        ("advocate", advocate),
    ]

    # ------------------------------------------------------------------
    # Phase 1: Opening statements
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("PHASE 1: OPENING STATEMENTS")
    print("=" * 60)

    opening_responses: dict[str, str] = {}
    for key, agent in agents_ordered:
        instr = _opening_instruction(key, policy_question)
        append_instruction(state.transcript, instr)

        print(f"\n[{agent.role_label}] thinking...")
        response = agent.respond(
            debate_context=state.transcript,
            user_query=policy_question,
            instruction=None,
        )
        opening_responses[key] = response
        append_to_transcript(state.transcript, agent.role_label, response)
        print(f"\n{agent.role_label}:\n{response}")

    state.rounds.append({"phase": "opening", **opening_responses})

    # ------------------------------------------------------------------
    # Phase 2: Deliberation rounds
    # ------------------------------------------------------------------
    previous_responses = opening_responses.copy()

    for round_num in range(1, num_rounds + 1):
        print("\n" + "=" * 60)
        print(f"PHASE 2: DELIBERATION ROUND {round_num}")
        print("=" * 60)

        round_responses: dict[str, str] = {}
        for key, agent in agents_ordered:
            instr = build_director_instruction(round_num, key, previous_responses)
            append_instruction(state.transcript, instr)

            print(f"\n[{agent.role_label}] thinking...")
            response = agent.respond(
                debate_context=state.transcript,
                user_query=policy_question,
                instruction=None,
            )
            round_responses[key] = response
            append_to_transcript(state.transcript, agent.role_label, response)
            print(f"\n{agent.role_label}:\n{response}")

        state.rounds.append({"phase": f"round_{round_num}", **round_responses})
        previous_responses = round_responses.copy()

    # ------------------------------------------------------------------
    # Phase 3: Closing distillation
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("PHASE 3: CLOSING DISTILLATION")
    print("=" * 60)

    closing_responses: dict[str, str] = {}
    for key, agent in agents_ordered:
        instr = _closing_instruction(key)
        append_instruction(state.transcript, instr)

        print(f"\n[{agent.role_label}] distilling...")
        response = agent.respond(
            debate_context=state.transcript,
            user_query=policy_question,
            instruction=None,
        )
        closing_responses[key] = response
        append_to_transcript(state.transcript, agent.role_label, response)
        print(f"\n{agent.role_label}: {response}")

    state.rounds.append({"phase": "closing", **closing_responses})

    return state
