"""Pins each prompt rule a swisstopo test finding produced.

The prompt is the deliverable for most of those findings, so a rule silently dropped by a
later edit is a regression with no other detector. Each class names the questions from
swisstopo's 2026-09-08 round that it answers.
"""

from __future__ import annotations

import pytest

from app.agent.prompts import system_prompt


@pytest.fixture
def prompt() -> str:
    return system_prompt("de")


class TestDisplayDiscipline:
    """Q7: the answer counted 481 buildings and told the user to press a button that was
    never created, quoting its English label into a German interface."""

    def test_forbids_quoting_the_button_label(self, prompt: str) -> None:
        assert "Show result on map" not in prompt

    def test_forbids_describing_a_card_without_display_layer(self, prompt: str) -> None:
        assert "unless `display_layer` returned successfully" in prompt

    def test_requires_displaying_what_was_counted(self, prompt: str) -> None:
        assert "A number the user cannot see on the map is half an answer." in prompt
