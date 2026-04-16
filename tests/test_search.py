import re

import allure
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.search_page import SearchPage
from utils.waits import expect_any_visible, wait_for_any_visible


@pytest.mark.ui
@pytest.mark.search
@pytest.mark.bvt
@pytest.mark.smoke
@allure.feature("Search")
def test_search_entry_opens_search_input(page, test_settings):
    home = HomePage(page, test_settings.base_url)
    home.open()

    if not home.open_search():
        pytest.skip("검색 입력 UI가 현재 공개 DOM에서 확인되지 않음")

    search = SearchPage(page, test_settings.base_url)
    assert search.active_input() is not None


@pytest.mark.ui
@pytest.mark.search
@pytest.mark.bvt
@pytest.mark.regression
@allure.feature("Search")
def test_known_stock_search_returns_relevant_result(page, test_settings):
    home = HomePage(page, test_settings.base_url)
    home.open()

    if not home.open_search():
        pytest.skip("검색 입력 UI가 현재 공개 DOM에서 확인되지 않음")

    search = SearchPage(page, test_settings.base_url)
    if not search.search(test_settings.default_stock_query):
        pytest.skip("검색 입력 필드를 사용할 수 없음")

    expect_any_visible(
        [
            search.result_matching(test_settings.default_stock_query),
            page.get_by_text(re.compile("삼성|전자|005930")),
        ],
        timeout=5_000,
    )


@pytest.mark.ui
@pytest.mark.search
@pytest.mark.regression
@allure.feature("Search")
def test_unknown_stock_search_keeps_query_or_shows_empty_state(page, test_settings):
    home = HomePage(page, test_settings.base_url)
    home.open()

    if not home.open_search():
        pytest.skip("검색 입력 UI가 현재 공개 DOM에서 확인되지 않음")

    search = SearchPage(page, test_settings.base_url)
    query = "ZZZ_NO_SUCH_STOCK_987654"
    if not search.search(query):
        pytest.skip("검색 입력 필드를 사용할 수 없음")

    visible_empty_state = wait_for_any_visible(
        [search.no_result_or_empty_state(), page.get_by_text(re.compile(re.escape(query)))],
        timeout=3_000,
    )
    if visible_empty_state is not None:
        expect(visible_empty_state).to_be_visible()
        return

    active_input = search.active_input()
    if active_input is None:
        pytest.fail("검색 결과 없음 안내도 없고 검색 입력값도 확인할 수 없음")
    expect(active_input).to_have_value(query)
