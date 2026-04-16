from __future__ import annotations

import re

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class HomePage(BasePage):
    NAV_HOME = re.compile("홈")
    NAV_FEED = re.compile("피드|뉴스")
    NAV_STOCK_PICKER = re.compile("주식 골라보기")
    NAV_ACCOUNT = re.compile("내 계좌")

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

    def open(self) -> None:
        self.goto("/")

    @property
    def search_hint(self) -> Locator:
        return self.by_text_regex("검색")

    @property
    def live_chart_heading(self) -> Locator:
        return self.by_text_regex("실시간 차트")

    @property
    def category_section(self) -> Locator:
        return self.by_text_regex("지금 뜨는 카테고리")

    @property
    def investor_trend_section(self) -> Locator:
        return self.by_text_regex("국내 투자자.*동향")

    @property
    def investment_disclaimer(self) -> Locator:
        return self.by_text_regex("투자 정보.*투자 판단.*참고")

    def nav_item(self, name: str | re.Pattern[str]) -> Locator:
        return self.link(name)

    def open_search(self) -> bool:
        opened = self.click_first_visible(
            [
                self.page.get_by_placeholder(re.compile("검색|종목|주식")),
                self.search_hint,
                self.button(re.compile("검색")),
            ],
            timeout=2_000,
            description="search entry",
        )
        if not opened:
            self.page.keyboard.press("/")
        return self.first_visible(self.search_input_candidates(), timeout=2_000) is not None

    def search_input_candidates(self) -> list[Locator]:
        return [
            self.page.get_by_placeholder(re.compile("검색|종목|주식")),
            self.textbox(re.compile("검색|종목|주식")),
            self.page.locator("input[type='search'][data-section-name='검색']"),
            self.page.locator("input[type='search'][placeholder*='검색']"),
        ]

    def go_to_feed(self) -> bool:
        return self.click_first_visible(
            [self.nav_item(self.NAV_FEED)], description="feed navigation"
        )

    def go_to_stock_picker(self) -> bool:
        return self.click_first_visible(
            [self.nav_item(self.NAV_STOCK_PICKER), self.by_text_regex("주식 골라보기")],
            description="stock picker navigation",
        )

    def go_to_account(self) -> bool:
        return self.click_first_visible(
            [self.nav_item(self.NAV_ACCOUNT)], description="account navigation"
        )

    def select_live_chart_filter(self, label: str) -> bool:
        return self.click_first_visible(
            [
                self.button(re.compile(label)),
                self.by_text(label, exact=True),
            ],
            timeout=1_500,
            description=f"live chart filter {label}",
        )
