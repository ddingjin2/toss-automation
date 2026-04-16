from __future__ import annotations

import re
from collections.abc import Iterable

from playwright.sync_api import Locator, Page, TimeoutError


class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def goto(self, path: str = "/") -> None:
        target = self.base_url if path == "/" else f"{self.base_url}{path}"
        self.page.goto(target, wait_until="domcontentloaded")
        self.wait_until_ready()

    def wait_until_ready(self) -> None:
        self.page.wait_for_load_state("domcontentloaded")
        self.page.locator("body").wait_for(state="visible")

    def by_text(self, text: str, exact: bool = False) -> Locator:
        return self.page.get_by_text(text, exact=exact)

    def by_text_regex(self, pattern: str) -> Locator:
        return self.page.get_by_text(re.compile(pattern))

    def link(self, name: str | re.Pattern[str]) -> Locator:
        return self.page.get_by_role("link", name=name)

    def button(self, name: str | re.Pattern[str]) -> Locator:
        return self.page.get_by_role("button", name=name)

    def textbox(self, name: str | re.Pattern[str] | None = None) -> Locator:
        if name is None:
            return self.page.get_by_role("textbox")
        return self.page.get_by_role("textbox", name=name)

    def first_visible(self, locators: Iterable[Locator], timeout: int = 1_500) -> Locator | None:
        for locator in locators:
            try:
                visible_locator = locator.filter(visible=True).first
                visible_locator.wait_for(state="visible", timeout=timeout)
                return visible_locator
            except TimeoutError:
                continue
        return None

    def click_first_visible(
        self,
        locators: Iterable[Locator],
        timeout: int = 1_500,
        description: str = "candidate locator",
    ) -> bool:
        visible = self.first_visible(locators, timeout=timeout)
        if visible is None:
            return False
        visible.click()
        return True

    def is_visible(self, locator: Locator, timeout: int = 1_000) -> bool:
        try:
            locator.first.wait_for(state="visible", timeout=timeout)
            return True
        except TimeoutError:
            return False

    def any_text_visible(self, patterns: list[str], timeout: int = 1_000) -> bool:
        candidates = [self.by_text_regex(pattern) for pattern in patterns]
        return self.first_visible(candidates, timeout=timeout) is not None
