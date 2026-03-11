"""
brief.py — Policy brief assembly and section extraction.
"""

from __future__ import annotations

import re
from datetime import date

from debate import DebateState


# ---------------------------------------------------------------------------
# Section extraction
# ---------------------------------------------------------------------------

SECTION_HEADERS = [
    "Executive Summary",
    "Research Findings",
    "Economic Analysis",
    "Counterarguments and Risks",
    "Final Recommendation",
]


def extract_section(synthesis: str, section_name: str) -> str:
    """
    Pull the content under a specific ## heading from the synthesis text.
    Returns the full synthesis if the section header is not found.
    """
    pattern = rf"##\s+{re.escape(section_name)}(.*?)(?=\n##\s|\Z)"
    match = re.search(pattern, synthesis, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return synthesis.strip()


# ---------------------------------------------------------------------------
# Transcript excerpt helpers
# ---------------------------------------------------------------------------

def _truncate(text: str, max_chars: int = 300) -> str:
    text = text.strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + " …"


def _format_round(round_data: dict) -> str:
    lines: list[str] = []
    label_map = {
        "researcher": "**Policy Researcher**",
        "economist": "**Economist**",
        "advocate": "**Devil's Advocate**",
    }
    for key, label in label_map.items():
        if key in round_data:
            lines.append(f"{label}: {_truncate(round_data[key])}")
    return "\n\n".join(lines)


# ---------------------------------------------------------------------------
# Brief renderer
# ---------------------------------------------------------------------------

def render_brief(
    policy_question: str,
    debate_state: DebateState,
    synthesis: str,
) -> str:
    """
    Assemble the final markdown policy brief from the debate state
    and the Director's synthesis.
    """
    today = date.today().strftime("%B %d, %Y")
    deliberation_rounds = sum(
        1 for r in debate_state.rounds if r.get("phase", "").startswith("round_")
    )

    # Header block
    sections = [
        f"# Policy Brief: {policy_question}",
        "",
        f"**Prepared by:** AI Policy Think Tank  ",
        f"**Date:** {today}  ",
        f"**Deliberation rounds:** {deliberation_rounds}  ",
        "",
        "---",
        "",
    ]

    # Director synthesis (verbatim — already contains ## sections)
    sections.append(synthesis.strip())
    sections.append("")
    sections.append("---")
    sections.append("")

    # Debate transcript summary
    sections.append("## Debate Transcript Summary")
    sections.append("")

    for round_data in debate_state.rounds:
        phase = round_data.get("phase", "unknown")
        if phase == "opening":
            sections.append("### Opening Statements")
        elif phase.startswith("round_"):
            n = phase.split("_")[1]
            sections.append(f"### Deliberation Round {n}")
        elif phase == "closing":
            sections.append("### Closing Distillation")
        else:
            sections.append(f"### {phase.replace('_', ' ').title()}")
        sections.append("")
        sections.append(_format_round(round_data))
        sections.append("")

    sections.append("---")
    sections.append("")
    sections.append(
        "*This brief was produced by a multi-agent AI deliberation system. "
        "All analysis is synthetic and intended for illustrative purposes.*"
    )

    return "\n".join(sections)
