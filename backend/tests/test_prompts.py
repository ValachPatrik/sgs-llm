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


class TestPlaceKindDiscipline:
    """Q3: "Stadt Bern" resolved to nothing and the answer fell back to the canton.
    Q4: "in Bern" became the canton without asking. division_by_name orders
    coarsest-first and takes LIMIT 1, so an omitted kind is silently the canton."""

    def test_requires_place_kind_alongside_place(self, prompt: str) -> None:
        assert "Always pass `place_kind` together with `place`" in prompt

    def test_strips_the_administrative_word_into_the_kind(self, prompt: str) -> None:
        assert "Stadt Bern" in prompt
        assert "The word is the `kind`, not part of the `name`." in prompt

    def test_asks_when_a_name_is_both_a_canton_and_a_commune(self, prompt: str) -> None:
        assert "both a canton and a commune" in prompt

    def test_does_not_ask_when_the_request_already_says_which(self, prompt: str) -> None:
        assert "When the request does say which, do not ask." in prompt
