from __future__ import annotations

import re

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage
from pages.home_page import HomePage
from pages.search_page import SearchPage


class StockDetailPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

    def open_via_search(self, query: str) -> bool:
        home = HomePage(self.page, self.base_url)
        home.open()
        if not home.open_search():
            return False
        search = SearchPage(self.page, self.base_url)
        if not search.search(query):
            return False
        return search.open_first_result(query)

    @property
    def quote_area(self) -> Locator:
        return self.by_text_regex("시세|차트|거래량|거래대금|전일|고가|저가")

    @property
    def chart_area(self) -> Locator:
        return self.by_text_regex("차트|1일|1주|1개월|1년")

    @property
    def auth_prompt(self) -> Locator:
        return self.by_text_regex("로그인|인증|토스 앱|내 계좌|계좌")

    def stock_title(self, query: str) -> Locator:
        return self.by_text_regex(re.escape(query))

    def favorite_button_candidates(self) -> list[Locator]:
        return [
            self.button(re.compile("관심|즐겨찾기|추가")),
            self.page.get_by_label(re.compile("관심|즐겨찾기|추가")),
            self.page.locator("[aria-label*='관심'], [aria-label*='즐겨찾기']"),
        ]

    def try_click_favorite(self) -> bool:
        return self.click_first_visible(
            self.favorite_button_candidates(),
            timeout=1_500,
            description="favorite or watchlist button",
        )
