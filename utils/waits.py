from __future__ import annotations

from collections.abc import Iterable

from playwright.sync_api import Locator, Page, TimeoutError, expect


def wait_for_app_ready(page: Page) -> None:
    page.wait_for_load_state("domcontentloaded")
    page.locator("body").wait_for(state="visible")


def wait_for_any_visible(locators: Iterable[Locator], timeout: int = 2_000) -> Locator | None:
    for locator in locators:
        try:
            visible_locator = locator.filter(visible=True).first
            visible_locator.wait_for(state="visible", timeout=timeout)
            return visible_locator
        except TimeoutError:
            continue
    return None


def expect_any_visible(locators: Iterable[Locator], timeout: int = 2_000) -> Locator:
    visible = wait_for_any_visible(locators, timeout=timeout)
    if visible is None:
        raise AssertionError("None of the expected locators became visible")
    expect(visible).to_be_visible()
    return visible
