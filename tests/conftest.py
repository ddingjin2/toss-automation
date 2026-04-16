from __future__ import annotations

from pathlib import Path

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from config.settings import Settings, settings
from utils.artifacts import attach_file_if_exists, attach_screenshot, ensure_dir, safe_artifact_name


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--headed", action="store_true", default=False, help="Run browser in headed mode"
    )
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        choices=["chromium", "firefox", "webkit"],
        help="Override BROWSER env value",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    return settings


@pytest.fixture(scope="session")
def browser(test_settings: Settings, request: pytest.FixtureRequest) -> Browser:
    selected_browser = request.config.getoption("--browser") or test_settings.browser
    headed = request.config.getoption("--headed")
    with sync_playwright() as playwright:
        browser_type = getattr(playwright, selected_browser)
        browser = browser_type.launch(headless=False if headed else test_settings.headless)
        yield browser
        browser.close()


@pytest.fixture()
def context(
    browser: Browser, test_settings: Settings, request: pytest.FixtureRequest
) -> BrowserContext:
    artifact_root = ensure_dir(test_settings.artifact_dir)
    video_dir = ensure_dir(artifact_root / "videos")

    context = browser.new_context(
        base_url=test_settings.base_url,
        viewport={"width": test_settings.viewport_width, "height": test_settings.viewport_height},
        locale="ko-KR",
        timezone_id="Asia/Seoul",
        record_video_dir=str(video_dir) if test_settings.video_on_failure else None,
    )
    context.set_default_timeout(test_settings.timeout)
    context.set_default_navigation_timeout(test_settings.timeout)

    if test_settings.trace_on_failure:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    trace_path = artifact_root / "traces" / f"{safe_artifact_name(request.node.nodeid)}.zip"

    if test_settings.trace_on_failure:
        ensure_dir(trace_path.parent)
        context.tracing.stop(path=str(trace_path))

    context.close()

    if failed and test_settings.trace_on_failure:
        attach_file_if_exists(trace_path, "playwright-trace", allure.attachment_type.ZIP)


@pytest.fixture()
def page(context: BrowserContext, test_settings: Settings, request: pytest.FixtureRequest) -> Page:
    page = context.new_page()
    yield page

    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    if failed:
        attach_screenshot(page, request.node.nodeid, test_settings.artifact_dir / "screenshots")

    video = page.video
    page.close()

    if failed and video is not None:
        try:
            video_path = Path(video.path())
            attach_file_if_exists(video_path, "failure-video", allure.attachment_type.WEBM)
        except Exception:
            pass
