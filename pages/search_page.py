from __future__ import annotations

import re

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class SearchPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

    def input_candidates(self) -> list[Locator]:
        return [
            self.page.get_by_placeholder(re.compile("검색|종목|주식")),
            self.textbox(re.compile("검색|종목|주식")),
            self.page.locator("input[type='search'][data-section-name='검색']"),
            self.page.locator("input[type='search'][placeholder*='검색']"),
        ]

    def active_input(self) -> Locator | None:
        return self.first_visible(self.input_candidates(), timeout=2_000)

    def search(self, query: str) -> bool:
        search_input = self.active_input()
        if search_input is None:
            return False
        search_input.fill(query)
        self.page.keyboard.press("Enter")
        self.page.wait_for_load_state("domcontentloaded")
        return True

    def result_matching(self, keyword: str) -> Locator:
        return self.page.get_by_text(re.compile(re.escape(keyword))).first

    def open_first_result(self, keyword: str) -> bool:
        candidates = [
            self.page.get_by_role("link", name=re.compile(re.escape(keyword))),
            self.page.locator("a").filter(has_text=re.compile(re.escape(keyword))),
        ]
        return self.click_first_visible(
            candidates, timeout=3_000, description=f"{keyword} search result"
        )

    def no_result_or_empty_state(self) -> Locator:
        return self.by_text_regex("검색 결과가 없|결과 없음|찾을 수 없|일치하는")
