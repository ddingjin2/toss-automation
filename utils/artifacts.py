from __future__ import annotations

import re
from pathlib import Path

import allure
from playwright.sync_api import Page


def safe_artifact_name(nodeid: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", nodeid).strip("_")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def attach_screenshot(page: Page, name: str, artifact_dir: Path) -> Path | None:
    ensure_dir(artifact_dir)
    path = artifact_dir / f"{safe_artifact_name(name)}.png"
    try:
        page.screenshot(path=str(path), full_page=True)
        allure.attach.file(
            str(path), name="failure-screenshot", attachment_type=allure.attachment_type.PNG
        )
        return path
    except Exception:
        return None


def attach_file_if_exists(path: Path, name: str, attachment_type: allure.attachment_type) -> None:
    if path.exists():
        allure.attach.file(str(path), name=name, attachment_type=attachment_type)
