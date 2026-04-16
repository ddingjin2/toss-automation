import re

import allure
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from utils.waits import expect_any_visible


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.smoke
@allure.feature("Home")
def test_home_public_shell_displays_navigation_and_market_sections(page, test_settings):
    home = HomePage(page, test_settings.base_url)
    home.open()

    expect(home.nav_item(HomePage.NAV_HOME).first).to_be_visible()
    expect_any_visible([home.nav_item(HomePage.NAV_FEED), home.by_text_regex("피드|뉴스")])
    expect_any_visible(
        [home.nav_item(HomePage.NAV_STOCK_PICKER), home.by_text_regex("주식 골라보기")]
    )
    expect_any_visible([home.search_hint])
    expect_any_visible([home.live_chart_heading])
    expect_any_visible([home.category_section])


@pytest.mark.ui
@pytest.mark.regression
@allure.feature("Home")
def test_home_footer_disclaimer_is_visible(page, test_settings):
    home = HomePage(page, test_settings.base_url)
    home.open()

    expect(home.investment_disclaimer.first).to_be_visible()


@pytest.mark.ui
@pytest.mark.bvt
@pytest.mark.smoke
@allure.feature("Auth Entry")
def test_account_entry_guides_user_to_auth_or_account_context(page, test_settings):
    home = HomePage(page, test_settings.base_url)
    home.open()

    assert home.go_to_account(), "BVT account entry is not available on the public home page"

    expect_any_visible(
        [
            page.get_by_text(re.compile("로그인|인증|토스|앱|계좌|QR")),
            page.get_by_role("button", name=re.compile("로그인|확인|시작|열기")),
        ],
        timeout=3_000,
    )


@pytest.mark.ui
@pytest.mark.regression
@allure.feature("Home")
def test_live_chart_filters_are_clickable_without_full_page_error(page, test_settings):
    home = HomePage(page, test_settings.base_url)
    home.open()

    clicked = home.select_live_chart_filter("국내") or home.select_live_chart_filter("전체")
    if not clicked:
        pytest.skip("실시간 차트 필터가 현재 공개 DOM에서 확인되지 않음")

    expect(page.locator("body")).not_to_contain_text("Application error")
