"""Shared fixtures for all tests: env URL and browser setup."""
import os

import pytest
from playwright.sync_api import Page

DEFAULT_BASE_URL = "https://www.fairphone.com"
DEFAULT_LANGUAGE = "en"

@pytest.fixture(scope="session")
def base_url(pytestconfig) -> str:
    url = pytestconfig.getoption("base_url") or os.getenv("BASE_URL") or DEFAULT_BASE_URL
    return url.rstrip("/")

@pytest.fixture(scope="session")
def language() -> str:
    return os.getenv("LANGUAGE", DEFAULT_LANGUAGE)

@pytest.fixture
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1366, "height": 900},
        "locale": "en-GB",
    }

@pytest.fixture
def page(page: Page) -> Page:
    page.add_locator_handler(
        page.locator("button.reject_all"),
        lambda button: button.click(),
    )
    return page