import logging
import urllib.parse
from typing import TYPE_CHECKING, Self, cast, override

from brlaw_mcp_server.domain.base import BaseLegalPrecedent

if TYPE_CHECKING:
    from patchright.async_api import Page


_LOGGER = logging.getLogger(__name__)


class StfLegalPrecedent(BaseLegalPrecedent):
    """A legal precedent from the Supreme Federal Court of Brazil (STF)."""

    @override
    @classmethod
    async def research(
        cls, browser: "Page", *, summary_search_prompt: str, desired_page: int = 1
    ) -> "list[Self]":
        url = (
            "https://jurisprudencia.stf.jus.br/pages/search?"
            + urllib.parse.urlencode(
                {
                    "base": "acordaos",
                    "pesquisa_inteiro_teor": "false",
                    "sinonimo": "true",
                    "plural": "true",
                    "radicais": "false",
                    "buscaExata": "true",
                    "page": str(desired_page),
                    "pageSize": "10",
                    "queryString": summary_search_prompt,
                }
            )
        )

        response = await browser.goto(
            url,
            wait_until="networkidle",  # Page keeps loading async.
        )

        if response is None or response.status >= 300:  # noqa: PLR2004  # constant used only once.
            _LOGGER.error(
                "The server's response wasn't as expected",
                extra={
                    "browser_headers": await response.request.all_headers()
                    if response
                    else None,
                    "request_url": url,
                    "response_status": response.status if response else None,
                    "response_content": await browser.content(),
                },
            )

            raise RuntimeError("The server's response wasn't as expected")

        numbers_of_results_locators = await browser.locator(
            "div.mat-tooltip-trigger > span.ml-5.font-weight-500"
        ).all()

        if len(numbers_of_results_locators) == 0:
            raise RuntimeError("Failed to get the number of results")

        txt_numbers_of_precedents = await numbers_of_results_locators[0].text_content()
        if txt_numbers_of_precedents is None:
            raise RuntimeError("Failed to get the number of results")

        numbers_of_precedents = int(
            txt_numbers_of_precedents.strip("() ").replace(".", "")
        )

        if numbers_of_precedents == 0:
            return []

        results_locators = await browser.locator("div[id^=result-index-]").all()
        if len(results_locators) == 0:
            raise RuntimeError("Failed to find the results when there are results")

        # Needed ahead to read the copied summaries.
        await browser.context.grant_permissions(["clipboard-read"])

        return_value: list[Self] = []
        for result_locator in results_locators:
            await result_locator.locator("app-clipboard").click()
            handle = await browser.evaluate_handle(
                "() => navigator.clipboard.readText()"
            )
            summary = cast("str", await handle.json_value())

            return_value.append(
                cls(
                    summary=summary,
                )
            )

        return return_value
