import re

import allure
import pytest
from playwright.sync_api import TimeoutError, expect

from pages.stock_detail_page import StockDetailPage
from utils.waits import expect_any_visible


@pytest.mark.ui
@pytest.mark.quote
@pytest.mark.bvt
@pytest.mark.smoke
@allure.feature("Stock Detail")
def test_stock_detail_can_be_reached_from_public_search(page, test_settings):
    stock = StockDetailPage(page, test_settings.base_url)

    assert stock.open_via_search(
        test_settings.default_stock_query
    ), "BVT stock detail path is not reachable from public search"

    expect_any_visible(
        [
            stock.stock_title(test_settings.default_stock_query),
            page.get_by_text(re.compile("삼성전자|005930|Samsung")),
        ],
        timeout=5_000,
    )


@pytest.mark.ui
@pytest.mark.quote
@pytest.mark.bvt
@pytest.mark.regression
@allure.feature("Stock Detail")
def test_stock_detail_quote_or_chart_area_is_visible(page, test_settings):
    stock = StockDetailPage(page, test_settings.base_url)

    assert stock.open_via_search(
        test_settings.default_stock_query
    ), "BVT stock detail path is not reachable from public search"

    expect_any_visible([stock.quote_area, stock.chart_area], timeout=5_000)
    expect(page.locator("body")).not_to_contain_text("Application error")


@pytest.mark.ui
@pytest.mark.quote
@pytest.mark.regression
@allure.feature("Watchlist")
def test_watchlist_or_favorite_action_requires_auth_when_publicly_visible(page, test_settings):
    stock = StockDetailPage(page, test_settings.base_url)

    if not stock.open_via_search(test_settings.default_stock_query):
        pytest.skip("공개 검색 결과에서 종목 상세로 진입할 수 없음. 서비스 UI 변경 확인 필요")

    if not stock.try_click_favorite():
        pytest.skip(
            "관심종목/즐겨찾기 버튼은 공개 DOM에서 확인되지 않음. 스테이징 또는 로그인 세션 필요"
        )

    expect_any_visible([stock.auth_prompt], timeout=3_000)


@pytest.mark.ui
@pytest.mark.quote
@pytest.mark.slow
@pytest.mark.regression
@allure.feature("Loading")
def test_public_market_page_resolves_loading_state_without_error(page, test_settings):
    stock = StockDetailPage(page, test_settings.base_url)
    stock.goto("/")

    loading = page.get_by_text(re.compile("로딩|불러오는 중")).filter(visible=True).first
    try:
        loading.wait_for(state="visible", timeout=500)
        loading.wait_for(state="hidden", timeout=10_000)
    except TimeoutError:
        pass

    expect_any_visible(
        [
            stock.by_text_regex("실시간 차트|지금 뜨는 카테고리|국내 투자자"),
        ],
        timeout=10_000,
    )
    expect(page.locator("body")).not_to_contain_text("Application error")
