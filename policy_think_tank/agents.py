"""
agents.py — Agent class, system prompts, and Anthropic API calls.
"""

from __future__ import annotations

import anthropic
from dataclasses import dataclass, field
from typing import Optional

MODEL = "claude-sonnet-4-6"

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Message:
    role: str    # "user" or "assistant"
    content: str


# ---------------------------------------------------------------------------
# System prompts
# ---------------------------------------------------------------------------

RESEARCHER_PROMPT = """\
You are a Policy Researcher in a structured policy think tank.

Your responsibilities:
- Gather and summarize relevant empirical evidence, academic literature,
  and historical precedents on the policy question posed.
- Cite specific examples, studies, or programs (real or illustrative)
  to ground your claims in evidence.
- Present findings in an organized, neutral manner — your job is
  evidence-gathering, not advocacy.
- When challenged by other agents, defend well-supported citations or
  honestly acknowledge genuine gaps in the evidence base.
- Keep responses focused and under 400 words unless more depth is
  explicitly requested.

You are participating in a multi-round deliberative debate. Read all
prior contributions carefully and respond only when the Director addresses
you. Prefix every response with "RESEARCHER:".
"""

DEVILS_ADVOCATE_PROMPT = """\
You are the Devil's Advocate in a structured policy think tank.

Your responsibilities:
- Steelman the strongest possible opposition to the policy position
  being developed, even if you personally support it.
- Identify unstated assumptions, logical gaps, and second-order
  consequences that other agents may overlook.
- Raise empirical objections: where does the evidence conflict? Where
  are studies underpowered? Where do real-world outcomes diverge from
  theory?
- Challenge the Economist's models and the Researcher's citations
  directly and specifically — do not raise generic concerns.
- You are not obstructionist. Your goal is a more robust final policy.
  End each response by naming the single most important objection you raised.
- Keep responses focused and under 400 words.

Prefix every response with "DEVIL'S ADVOCATE:".
"""

ECONOMIST_PROMPT = """\
You are an Economist in a structured policy think tank.

Your responsibilities:
- Analyze the cost-benefit tradeoffs of the proposed policy, including
  direct costs, opportunity costs, and distributional effects.
- Estimate budgetary impacts using transparent back-of-envelope reasoning
  where precise data is unavailable — always state your assumptions.
- Identify which populations bear costs and which receive benefits.
- Assess market distortions, incentive effects, and behavioral responses
  likely to result from the policy.
- When the Devil's Advocate challenges your analysis, engage with the
  specific critique rather than restating your prior position.
- Keep responses focused and under 400 words.

Prefix every response with "ECONOMIST:".
"""

DIRECTOR_PROMPT = """\
You are the Director of a policy think tank running a structured
deliberative debate. You orchestrate three specialist agents:
a Policy Researcher, a Devil's Advocate, and an Economist.

During the debate your role is to:
- Issue targeted, specific instructions to each specialist per round,
  directing them to address unresolved tensions, evidence gaps, or
  unanswered objections raised by other agents.
- Keep the debate productive: push hard on genuine disagreements
  and move on when consensus is reached.

When producing the final policy brief synthesis, output exactly the
following section headers (as markdown H2s) with substantive content
under each:

## Executive Summary
## Research Findings
## Economic Analysis
## Counterarguments and Risks
## Final Recommendation

The Final Recommendation must take a clear, defensible position
supported by the debate evidence. Do not hedge into uselessness.
"""


# ---------------------------------------------------------------------------
# Agent class
# ---------------------------------------------------------------------------

@dataclass
class Agent:
    name: str
    role_label: str
    system_prompt: str
    client: anthropic.Anthropic = field(repr=False)

    def respond(
        self,
        debate_context: list[Message],
        user_query: str,
        instruction: Optional[str] = None,
    ) -> str:
        """
        Build an Anthropic messages list from debate_context, append the
        instruction as the final user turn, and call the API.

        Transcript normalization:
        - Director instructions are treated as "user" turns.
        - All agent contributions between Director instructions are
          bundled into a single "assistant" turn with prefixed labels,
          ensuring strict user/assistant alternation required by the API.
        """
        messages = _normalize_transcript(debate_context, user_query)

        if instruction:
            # Ensure we don't end on an assistant turn before appending
            if messages and messages[-1]["role"] == "user":
                # Merge into the last user message
                messages[-1]["content"] += f"\n\n{instruction}"
            else:
                messages.append({"role": "user", "content": instruction})

        # Guarantee the messages list starts with a user turn
        if not messages or messages[0]["role"] != "user":
            messages.insert(0, {"role": "user", "content": user_query})

        response = self.client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=self.system_prompt,
            messages=messages,
        )
        return response.content[0].text


# ---------------------------------------------------------------------------
# Transcript normalization
# ---------------------------------------------------------------------------

def _normalize_transcript(
    transcript: list[Message],
    policy_question: str,
) -> list[dict]:
    """
    Convert the flat transcript into a strictly alternating
    user/assistant message list for the Anthropic API.

    Convention used when building the transcript:
    - Director instructions are stored with role "user"
    - All specialist agent responses are stored with role "assistant"
    - When multiple specialists respond in sequence without a Director
      turn in between, their messages are bundled into one "assistant"
      block.
    """
    if not transcript:
        return [{"role": "user", "content": policy_question}]

    normalized: list[dict] = []

    for msg in transcript:
        if not normalized:
            normalized.append({"role": msg.role, "content": msg.content})
            continue

        last = normalized[-1]
        if last["role"] == msg.role:
            # Same role — bundle into one block
            last["content"] += f"\n\n{msg.content}"
        else:
            normalized.append({"role": msg.role, "content": msg.content})

    return normalized


# ---------------------------------------------------------------------------
# Agent factories
# ---------------------------------------------------------------------------

def make_policy_researcher(client: anthropic.Anthropic) -> Agent:
    return Agent(
        name="Policy Researcher",
        role_label="RESEARCHER",
        system_prompt=RESEARCHER_PROMPT,
        client=client,
    )


def make_devils_advocate(client: anthropic.Anthropic) -> Agent:
    return Agent(
        name="Devil's Advocate",
        role_label="DEVIL'S ADVOCATE",
        system_prompt=DEVILS_ADVOCATE_PROMPT,
        client=client,
    )


def make_economist(client: anthropic.Anthropic) -> Agent:
    return Agent(
        name="Economist",
        role_label="ECONOMIST",
        system_prompt=ECONOMIST_PROMPT,
        client=client,
    )


def make_director(client: anthropic.Anthropic) -> Agent:
    return Agent(
        name="Director",
        role_label="DIRECTOR",
        system_prompt=DIRECTOR_PROMPT,
        client=client,
    )
