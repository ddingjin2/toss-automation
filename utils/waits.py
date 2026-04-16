from __future__ import annotations

from collections.abc import Iterable

from playwright.sync_api import Locator, Page, TimeoutError, expect


def wait_for_app_ready(page: Page) -> None:
    page.wait_for_load_state("domcontentloaded")
    page.locator("body").wait_for(state="visible")


def _visible_union(locators: list[Locator]) -> Locator:
    visible_locators = [locator.filter(visible=True) for locator in locators]
    combined = visible_locators[0]
    for locator in visible_locators[1:]:
        combined = combined.or_(locator)
    return combined.first


def wait_for_any_visible(locators: Iterable[Locator], timeout: int = 2_000) -> Locator | None:
    locator_list = list(locators)
    if not locator_list:
        raise ValueError("wait_for_any_visible requires at least one locator")
    try:
        visible_locator = _visible_union(locator_list)
        visible_locator.wait_for(state="visible", timeout=timeout)
        return visible_locator
    except TimeoutError:
        return None


def expect_any_visible(locators: Iterable[Locator], timeout: int = 2_000) -> Locator:
    locator_list = list(locators)
    visible = wait_for_any_visible(locator_list, timeout=timeout)
    if visible is None:
        raise AssertionError(
            f"None of {len(locator_list)} expected locators became visible within {timeout}ms"
        )
    expect(visible).to_be_visible()
    return visible
