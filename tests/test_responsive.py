import allure
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from utils.waits import expect_any_visible


@pytest.mark.ui
@pytest.mark.responsive
@pytest.mark.bvt
@pytest.mark.smoke
@allure.feature("Responsive")
def test_home_mobile_viewport_renders_market_content(page, test_settings):
    page.set_viewport_size(
        {
            "width": test_settings.mobile_viewport_width,
            "height": test_settings.mobile_viewport_height,
        }
    )
    home = HomePage(page, test_settings.base_url)
    home.open()

    expect_any_visible([home.nav_item(HomePage.NAV_HOME), home.live_chart_heading])
    assert page.viewport_size["width"] == test_settings.mobile_viewport_width
    expect(page.locator("body")).not_to_contain_text("Application error")


@pytest.mark.ui
@pytest.mark.responsive
@pytest.mark.regression
@allure.feature("Responsive")
def test_home_desktop_viewport_keeps_core_market_sections_visible(page, test_settings):
    page.set_viewport_size({"width": 1440, "height": 900})
    home = HomePage(page, test_settings.base_url)
    home.open()

    expect_any_visible([home.live_chart_heading])
    expect_any_visible([home.category_section])
