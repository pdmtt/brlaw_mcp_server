import asyncio
from os import environ

import pytest
from patchright.async_api import async_playwright

from brlaw_mcp_server.domain.base import BaseLegalPrecedent
from brlaw_mcp_server.domain.stf import StfLegalPrecedent
from brlaw_mcp_server.domain.stj import StjLegalPrecedent
from brlaw_mcp_server.domain.tst import TstLegalPrecedent


@pytest.mark.parametrize(
    ("summary", "should_return_results"),
    [
        pytest.param(
            "asdjnaskjdnaajhsbajkhsdjkabsndk12931092381902098",  # Bogus criteria
            False,
            id="should_not_return_results",
        ),
        pytest.param(
            "fraude execução",  # Criteria known to return results.
            True,
            id="should_return_results",
        ),
    ],
)
@pytest.mark.parametrize(
    "class_", [StjLegalPrecedent, TstLegalPrecedent, StfLegalPrecedent]
)
async def test_research_legal_precedents(
    summary: str,
    should_return_results: bool,
    class_: type[BaseLegalPrecedent],
) -> None:
    """Test the research method of the STJLegalPrecedent class.

    :param summary: The summary to search for.
    :param should_return_results: Whether the research should return results."""

    async with asyncio.timeout(30), async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless="CI" in environ,
        )

        page = await browser.new_page()

        for desired_results_page in range(1, 3):
            precedents = await class_.research(
                page,
                summary_search_prompt=summary,
                desired_page=desired_results_page,
            )

            assert should_return_results == bool(precedents)
            if not should_return_results:
                return

            assert all(isinstance(precedent, class_) for precedent in precedents)
