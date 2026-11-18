import re

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_home_page_loads(page: Page, language: str):
    response = page.goto(f"/{language}")

    assert response is not None and response.ok
    expect(page).to_have_title(re.compile("Fairphone"))


@pytest.mark.smoke
def test_main_navigation_opens_a_section(page: Page, language: str):
    page.goto(f"/{language}")

    header = page.get_by_role("banner")
    header.get_by_role("link", name="Shop", exact=True).hover()
    header.get_by_role("link", name="Smartphones", exact=True).click()

    expect(page).to_have_url(re.compile("/smartphones"))
    expect(page.locator("html")).to_have_attribute("lang", re.compile(f"^{language}"))
    expect(page.get_by_role("heading", name="Smartphones", level=1)).to_be_visible()