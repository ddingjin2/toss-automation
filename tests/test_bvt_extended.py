import re

import allure
import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.stock_detail_page import StockDetailPage
from utils.assertions import (
    expect_any_text,
    expect_no_private_account_data,
    expect_no_public_error,
)
from utils.waits import expect_any_visible, wait_for_any_visible


def open_search_from_home(page: Page, base_url: str) -> SearchPage:
    home = HomePage(page, base_url)
    home.open()
    assert home.open_search(), "BVT search entry is not available on the public home page"
    search = SearchPage(page, base_url)
    assert search.active_input() is not None, "BVT search input is not visible or usable"
    return search


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.smoke
@allure.feature("BVT")
@allure.story("TI-WEB-037")
def test_ti_web_037_home_first_load_stabilizes_within_timeout(page, test_settings):
    page.goto(test_settings.base_url, wait_until="domcontentloaded", timeout=10_000)
    page.locator("body").wait_for(state="visible", timeout=10_000)

    expect_any_text(page, ["홈", "피드|뉴스", "주식 골라보기", "내 계좌"], timeout=10_000)
    expect_any_text(page, ["실시간 차트|지수 목록|국내 장|해외"], timeout=10_000)
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.smoke
@allure.feature("BVT")
@allure.story("TI-WEB-038")
def test_ti_web_038_home_does_not_show_full_page_error(page, test_settings):
    HomePage(page, test_settings.base_url).open()

    expect_no_public_error(page)
    expect_any_text(page, ["홈", "실시간 차트|지수 목록|주식 골라보기"])


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.smoke
@allure.feature("BVT")
@allure.story("TI-WEB-039")
def test_ti_web_039_search_input_accepts_user_query(page, test_settings):
    search = open_search_from_home(page, test_settings.base_url)
    search_input = search.active_input()
    assert search_input is not None

    search_input.click()
    search_input.fill(test_settings.default_stock_query)

    expect(search_input).to_be_focused()
    expect(search_input).to_have_value(test_settings.default_stock_query)
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.smoke
@pytest.mark.search
@allure.feature("BVT")
@allure.story("TI-WEB-040")
def test_ti_web_040_known_stock_search_returns_basic_response(page, test_settings):
    search = open_search_from_home(page, test_settings.base_url)
    assert search.search(test_settings.default_stock_query), "BVT search input is not usable"

    expect_any_visible(
        [
            search.result_matching(test_settings.default_stock_query),
            page.get_by_text(re.compile("삼성|전자|005930")),
        ],
        timeout=5_000,
    )
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.smoke
@allure.feature("BVT")
@allure.story("TI-WEB-041")
def test_ti_web_041_account_entry_does_not_expose_private_account_data(page, test_settings):
    home = HomePage(page, test_settings.base_url)
    home.open()

    assert home.go_to_account(), "BVT account entry is not available on the public home page"

    expect_any_text(page, ["로그인|인증|토스|앱|계좌|QR"], timeout=3_000)
    expect_no_private_account_data(page)
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.smoke
@pytest.mark.quote
@allure.feature("BVT")
@allure.story("TI-WEB-042")
def test_ti_web_042_live_chart_basic_list_is_visible(page, test_settings):
    HomePage(page, test_settings.base_url).open()

    expect_any_text(page, ["실시간 차트"], timeout=5_000)
    expect_any_text(page, ["순위|현재가|등락률|거래대금"], timeout=5_000)
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.smoke
@pytest.mark.quote
@allure.feature("BVT")
@allure.story("TI-WEB-043")
def test_ti_web_043_market_status_and_index_summary_are_visible(page, test_settings):
    HomePage(page, test_settings.base_url).open()

    expect_any_text(page, ["국내 장|해외|프리마켓|정규장"], timeout=5_000)
    expect_any_text(page, ["코스피|코스닥|나스닥|S&P 500|다우존스"], timeout=5_000)
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.smoke
@pytest.mark.responsive
@allure.feature("BVT")
@allure.story("TI-WEB-044")
def test_ti_web_044_mobile_home_core_content_renders(page, test_settings):
    page.set_viewport_size(
        {
            "width": test_settings.mobile_viewport_width,
            "height": test_settings.mobile_viewport_height,
        }
    )
    HomePage(page, test_settings.base_url).open()

    expect_any_text(page, ["홈", "실시간 차트|지수 목록"], timeout=5_000)
    assert page.viewport_size["width"] == test_settings.mobile_viewport_width
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.smoke
@allure.feature("BVT")
@allure.story("TI-WEB-045")
def test_ti_web_045_navigation_round_trip_restores_home(page, test_settings):
    home = HomePage(page, test_settings.base_url)
    home.open()

    assert (
        home.go_to_feed() or home.go_to_stock_picker()
    ), "BVT public navigation entry is not clickable"

    page.go_back(wait_until="domcontentloaded")
    expect_any_text(page, ["홈", "실시간 차트|지수 목록|주식 골라보기"], timeout=5_000)
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.regression
@allure.feature("BVT")
@allure.story("TI-WEB-046")
def test_ti_web_046_footer_compliance_copy_is_visible(page, test_settings):
    HomePage(page, test_settings.base_url).open()

    expect_any_text(page, ["투자 판단|투자 유의사항|고객센터"], timeout=5_000)
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.regression
@pytest.mark.search
@allure.feature("BVT")
@allure.story("TI-WEB-047")
def test_ti_web_047_unknown_stock_search_fails_safely(page, test_settings):
    search = open_search_from_home(page, test_settings.base_url)
    query = "ZZZ_NO_SUCH_STOCK_987654"
    assert search.search(query), "BVT search input is not usable"

    empty_or_query = wait_for_any_visible(
        [
            search.no_result_or_empty_state(),
            page.get_by_text(re.compile(re.escape(query))),
        ],
        timeout=3_000,
    )
    if empty_or_query is None:
        active_input = search.active_input()
        if active_input is None:
            pytest.fail("없는 종목 검색 후 빈 결과 안내 또는 입력값 유지 상태를 확인할 수 없음")
        expect(active_input).to_have_value(query)
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.smoke
@pytest.mark.quote
@allure.feature("BVT")
@allure.story("TI-WEB-048")
def test_ti_web_048_stock_detail_opens_without_application_error(page, test_settings):
    stock = StockDetailPage(page, test_settings.base_url)
    assert stock.open_via_search(
        test_settings.default_stock_query
    ), "BVT stock detail path is not reachable from public search"

    expect_any_visible(
        [
            stock.stock_title(test_settings.default_stock_query),
            stock.quote_area,
            stock.chart_area,
            page.get_by_text(re.compile("삼성전자|005930|Samsung")),
        ],
        timeout=5_000,
    )
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.regression
@allure.feature("BVT")
@allure.story("TI-WEB-049")
def test_ti_web_049_home_recovers_after_refresh(page, test_settings):
    HomePage(page, test_settings.base_url).open()

    page.reload(wait_until="domcontentloaded")

    expect_any_text(page, ["홈", "실시간 차트|지수 목록"], timeout=5_000)
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.regression
@pytest.mark.responsive
@allure.feature("BVT")
@allure.story("TI-WEB-050")
def test_ti_web_050_desktop_viewport_renders_market_content(page, test_settings):
    page.set_viewport_size({"width": 1440, "height": 900})
    HomePage(page, test_settings.base_url).open()

    expect_any_text(page, ["실시간 차트", "지수 목록|코스피|나스닥"], timeout=5_000)
    assert page.viewport_size["width"] == 1440
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.regression
@allure.feature("BVT")
@allure.story("TI-WEB-051")
def test_ti_web_051_public_navigation_items_are_clickable(page, test_settings):
    home = HomePage(page, test_settings.base_url)

    for nav_pattern in [
        HomePage.NAV_HOME,
        HomePage.NAV_FEED,
        HomePage.NAV_STOCK_PICKER,
    ]:
        home.open()
        nav_item = expect_any_visible([home.nav_item(nav_pattern)], timeout=3_000)
        nav_item.click()
        page.wait_for_load_state("domcontentloaded")
        expect(page.locator("body")).to_be_visible()
        assert page.url != "about:blank"
        expect_no_public_error(page)

    home.open()
    expect_any_visible([home.nav_item(HomePage.NAV_ACCOUNT)], timeout=3_000)
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.regression
@allure.feature("BVT")
@allure.story("TI-WEB-052")
def test_ti_web_052_initial_loading_state_resolves_to_final_content(page, test_settings):
    page.goto(test_settings.base_url, wait_until="domcontentloaded", timeout=10_000)

    expect_any_text(page, ["홈", "실시간 차트|지수 목록|국내 장|해외"], timeout=10_000)
    expect_no_public_error(page)
