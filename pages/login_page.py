from __future__ import annotations

import re

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

    def open(self, redirect_path: str = "/") -> None:
        self.goto(f"/signin?redirectUrl={redirect_path}")

    @property
    def app_login_heading(self) -> Locator:
        return self.by_text_regex("토스 앱으로 로그인")

    @property
    def phone_login_button(self) -> Locator:
        return self.button(re.compile("휴대폰 번호로 로그인"))

    @property
    def qr_login_button(self) -> Locator:
        return self.button(re.compile("QR코드로 로그인"))

    @property
    def app_less_login_button(self) -> Locator:
        return self.button(re.compile("토스 앱 없이 로그인하기"))

    @property
    def login_submit_button(self) -> Locator:
        return self.button(re.compile("^로그인$|인증번호 받기"))

    @property
    def signup_link(self) -> Locator:
        return self.link(re.compile("가입하기"))

    @property
    def required_terms(self) -> Locator:
        return self.by_text_regex("필수 약관에 모두 동의")

    @property
    def qr_instruction(self) -> Locator:
        return self.by_text_regex("QR코드|문자 3개|휴대폰 카메라")

    @property
    def sms_login_heading(self) -> Locator:
        return self.by_text_regex("문자 인증으로 로그인")

    @property
    def carrier_button(self) -> Locator:
        return self.button(re.compile("통신사"))

    @property
    def auth_code_request_button(self) -> Locator:
        return self.button(re.compile("인증번호 받기"))

    def select_qr_login(self) -> bool:
        return self.click_first_visible([self.qr_login_button], description="QR login tab")

    def select_app_less_login(self) -> bool:
        return self.click_first_visible(
            [self.app_less_login_button], description="app-less login button"
        )

    def select_phone_login(self) -> bool:
        return self.click_first_visible([self.phone_login_button], description="phone login tab")
