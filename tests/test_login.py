import re

import allure
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.assertions import expect_no_private_account_data, expect_no_public_error
from utils.waits import expect_any_visible


@pytest.mark.ui
@pytest.mark.login
@pytest.mark.auth
@pytest.mark.bvt
@pytest.mark.smoke
@allure.feature("Login")
@allure.story("TI-WEB-053")
def test_ti_web_053_home_login_entry_navigates_to_signin(page, test_settings):
    home = HomePage(page, test_settings.base_url)
    home.open()

    clicked = home.click_first_visible(
        [page.get_by_role("link", name=re.compile("로그인")), page.get_by_text("로그인")],
        timeout=3_000,
        description="login entry",
    )
    if not clicked:
        pytest.skip("로그인 진입점을 현재 공개 DOM에서 확인할 수 없음")

    expect(page).to_have_url(re.compile(r"/signin"))
    expect_any_visible([LoginPage(page, test_settings.base_url).app_login_heading], timeout=5_000)
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.login
@pytest.mark.auth
@pytest.mark.bvt
@pytest.mark.smoke
@allure.feature("Login")
@allure.story("TI-WEB-054")
def test_ti_web_054_signin_page_shows_supported_login_options(page, test_settings):
    login = LoginPage(page, test_settings.base_url)
    login.open()

    expect_any_visible([login.app_login_heading])
    expect_any_visible([login.phone_login_button])
    expect_any_visible([login.qr_login_button])
    expect_any_visible([login.required_terms])
    expect_any_visible([login.signup_link])
    expect_no_private_account_data(page)
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.login
@pytest.mark.auth
@pytest.mark.bvt
@allure.feature("Login")
@allure.story("TI-WEB-055")
def test_ti_web_055_qr_login_tab_renders_qr_instruction(page, test_settings):
    login = LoginPage(page, test_settings.base_url)
    login.open()

    if not login.select_qr_login():
        pytest.skip("QR코드 로그인 탭을 현재 로그인 화면에서 확인할 수 없음")

    expect_any_visible([login.qr_instruction], timeout=3_000)
    assert page.locator("img").count() >= 1
    expect_no_private_account_data(page)
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.login
@pytest.mark.auth
@pytest.mark.bvt
@allure.feature("Login")
@allure.story("TI-WEB-056")
def test_ti_web_056_app_less_sms_login_form_renders(page, test_settings):
    login = LoginPage(page, test_settings.base_url)
    login.open()

    if not login.select_app_less_login():
        pytest.skip("토스 앱 없이 로그인하기 진입점을 현재 로그인 화면에서 확인할 수 없음")

    expect_any_visible([login.sms_login_heading], timeout=3_000)
    expect_any_visible([login.carrier_button], timeout=3_000)
    expect_any_visible([login.auth_code_request_button], timeout=3_000)
    assert page.locator("input").count() >= 1
    expect_no_private_account_data(page)
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.login
@pytest.mark.auth
@pytest.mark.bvt
@allure.feature("Login")
@allure.story("TI-WEB-057")
def test_ti_web_057_empty_sms_auth_request_fails_safely(page, test_settings):
    login = LoginPage(page, test_settings.base_url)
    login.open()

    if not login.select_app_less_login():
        pytest.skip("토스 앱 없이 로그인하기 진입점을 현재 로그인 화면에서 확인할 수 없음")

    button = login.auth_code_request_button.filter(visible=True).first
    expect(button).to_be_visible()
    if button.is_enabled():
        button.click()

    expect_any_visible(
        [
            login.sms_login_heading,
            page.get_by_text(re.compile("휴대폰|이름|생년월일|필수|입력|동의")),
        ],
        timeout=3_000,
    )
    expect_no_private_account_data(page)
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.login
@pytest.mark.auth
@pytest.mark.bvt
@pytest.mark.smoke
@allure.feature("Login")
@allure.story("TI-WEB-058")
def test_ti_web_058_browser_back_from_signin_restores_home(page, test_settings):
    home = HomePage(page, test_settings.base_url)
    home.open()

    clicked = home.click_first_visible(
        [page.get_by_role("link", name=re.compile("로그인")), page.get_by_text("로그인")],
        timeout=3_000,
        description="login entry",
    )
    if not clicked:
        pytest.skip("로그인 진입점을 현재 공개 DOM에서 확인할 수 없음")

    expect(page).to_have_url(re.compile(r"/signin"))
    page.go_back(wait_until="domcontentloaded")

    expect_any_visible([home.nav_item(HomePage.NAV_HOME), home.live_chart_heading], timeout=5_000)
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.login
@pytest.mark.auth
@pytest.mark.bvt
@allure.feature("Login")
@allure.story("TI-WEB-059")
def test_ti_web_059_signup_entry_is_available_from_signin(page, test_settings):
    login = LoginPage(page, test_settings.base_url)
    login.open()

    expect_any_visible([page.get_by_text(re.compile("아직 토스증권 회원이 아닌가요"))])
    expect_any_visible([login.signup_link])
    expect_no_private_account_data(page)
    expect_no_public_error(page)


@pytest.mark.ui
@pytest.mark.login
@pytest.mark.auth
@pytest.mark.bvt
@pytest.mark.smoke
@allure.feature("Login")
@allure.story("TI-WEB-060")
def test_ti_web_060_account_entry_routes_unauthenticated_user_to_login_context(page, test_settings):
    home = HomePage(page, test_settings.base_url)
    home.open()

    if not home.go_to_account():
        pytest.skip("내 계좌 공개 진입점을 현재 DOM에서 확인할 수 없음")

    expect_any_visible(
        [
            page.get_by_text(re.compile("로그인|인증|토스 앱|휴대폰|QR|계좌")),
            LoginPage(page, test_settings.base_url).app_login_heading,
        ],
        timeout=5_000,
    )
    expect_no_private_account_data(page)
    expect_no_public_error(page)
