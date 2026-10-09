"""Checkpoint names and default generation settings."""

from __future__ import annotations

from .types import GenerationParams

#: Short names accepted by ``OmniEdu.from_pretrained``.
PRESETS: dict[str, str] = {
    "4B": "OpenDCAI/Omni-Edu-4B",
    "9B": "OpenDCAI/Omni-Edu-9B",
    "27B": "OpenDCAI/Omni-Edu-27B",
}

#: Paper evaluation protocol: greedy, no thinking.
DEFAULT_GENERATION = GenerationParams(temperature=0.0, max_new_tokens=2048, enable_thinking=False)


def resolve_model(name: str) -> str:
    """Map ``"4B"`` to a Hub id, leaving anything else untouched.

    Case is ignored and an optional ``omniedu-`` / ``omni-edu-`` prefix is
    accepted, so ``"4b"``, ``"OmniEdu-4B"`` and ``"4B"`` all resolve. Full Hub
    ids and local checkpoint paths pass straight through.
    """
    if not isinstance(name, str) or not name.strip():
        raise ValueError("model must be a non-empty string")
    key = name.strip()
    if key in PRESETS:
        return PRESETS[key]
    lowered = key.lower()
    for short, repo in PRESETS.items():
        if lowered in (short.lower(), f"omniedu-{short.lower()}", f"omni-edu-{short.lower()}"):
            return repo
    return key


def known_presets() -> dict[str, str]:
    return dict(PRESETS)

