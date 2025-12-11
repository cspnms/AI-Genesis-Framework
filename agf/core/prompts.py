"""Prompt building hooks for potential LLM integration.

AGF is intentionally usable without any AI connectivity. This module documents
how prompts could be constructed if a future plugin wishes to ask an LLM to
propose project structures, infer missing metadata, or generate new templates.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SpecificationPrompt:
    """Represents a structured prompt for an external AI."""

    description: str
    expected_outputs: List[str]
    constraints: List[str]

    def to_message(self) -> str:
        constraint_text = "\n".join(f"- {item}" for item in self.constraints)
        outputs_text = "\n".join(f"* {item}" for item in self.expected_outputs)
        return (
            "You are assisting AGF in planning a new project.\n"
            f"Description:\n{self.description}\n\n"
            f"Constraints:\n{constraint_text}\n\n"
            f"Outputs:\n{outputs_text}\n"
        )


def build_spec_prompt(description: str, targets: List[str] | None = None) -> SpecificationPrompt:
    targets = targets or ["Project layout", "Key modules", "Testing approach"]
    constraints = [
        "Prefer simple, maintainable code",
        "Favor clear documentation",
        "Keep dependencies minimal",
    ]
    return SpecificationPrompt(description=description, expected_outputs=targets, constraints=constraints)


def prompt_to_dict(prompt: SpecificationPrompt) -> Dict[str, str]:
    return {
        "description": prompt.description,
        "constraints": "\n".join(prompt.constraints),
        "expected_outputs": "\n".join(prompt.expected_outputs),
        "message": prompt.to_message(),
    }
