from __future__ import annotations

import re
from collections.abc import Iterable

from playwright.sync_api import Page, expect

from utils.waits import expect_any_visible

PUBLIC_ERROR_PATTERNS = [
    "Application error",
    "404 Not Found",
    "500 Internal",
    "Internal Server Error",
    "문제가 발생했어요",
    "잠시 후 다시 시도",
    "다시 시도해 주세요",
]

PRIVATE_ACCOUNT_PATTERNS = [
    "평가금액",
    "계좌번호",
    "주문가능",
    "예수금",
]


def expect_no_public_error(page: Page) -> None:
    body = page.locator("body")
    for pattern in PUBLIC_ERROR_PATTERNS:
        expect(body).not_to_contain_text(re.compile(pattern))


def expect_no_private_account_data(page: Page) -> None:
    body = page.locator("body")
    for pattern in PRIVATE_ACCOUNT_PATTERNS:
        expect(body).not_to_contain_text(pattern)


def expect_any_text(page: Page, patterns: Iterable[str], timeout: int = 3_000) -> None:
    expect_any_visible(
        [page.get_by_text(re.compile(pattern)) for pattern in patterns], timeout=timeout
    )
