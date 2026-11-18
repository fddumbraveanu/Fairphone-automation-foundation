from collections import Counter
from pathlib import Path

import pytest
from playwright.sync_api import Error, Page

from helpers.sitemap import is_content_page, parse_sitemap, weekly_sample

SAMPLE_SIZE = 25
REPORT_PATH = Path("reports/scan-findings.md")


@pytest.mark.scan
def test_sampled_pages_have_no_errors(page: Page, base_url: str):
    sitemap = page.request.get(f"{base_url}/sitemap.xml")
    assert sitemap.ok, f"Sitemap returned {sitemap.status}"
    urls = [url for url in parse_sitemap(sitemap.text()) if is_content_page(url)]
    sample = weekly_sample(urls, SAMPLE_SIZE)

    broken_pages, failed_requests, console_errors = [], [], []

    def on_console(message):
        if message.type == "error":
            console_errors.append((page.url, message.text))

    def on_response(response):
        if response.status >= 400 and response.request.resource_type != "document":
            failed_requests.append((response.url, response.status))

    page.on("console", on_console)
    page.on("response", on_response)

    for url in sample:
        page.context.clear_cookies()
        try:
            response = page.goto(url)
        except Error as error:
            broken_pages.append((url, type(error).__name__))
            continue
        if response is None or response.status >= 400:
            broken_pages.append((url, response.status if response else "no response"))

    write_findings(sample, broken_pages, failed_requests, console_errors)
    assert not broken_pages, f"{len(broken_pages)} sampled page(s) returned 400+: {broken_pages}"


def write_findings(sample, broken_pages, failed_requests, console_errors):
    REPORT_PATH.parent.mkdir(exist_ok=True)
    grouped_console = [(f"{count}x", message) 
                       for message, count in Counter(m for _, m in console_errors).most_common()]
    details = "\n".join(f"{where}: {what}" for where, what in console_errors)
    REPORT_PATH.with_name("scan-console-details.txt").write_text(details, encoding="utf-8")
    sections = {
        "Pages returning 400+ (fail the job)": broken_pages,
        "Resources returning 400+ (report only)": failed_requests,
        "Browser console errors (report only)": grouped_console,
    }
    lines = [f"# Scan job: {len(sample)} pages checked"]
    for title, findings in sections.items():
        lines.append(f"\n## {title}: {len(findings)}")
        lines += [f"- {where}: {what}" for where, what in findings]
    lines.append(f"\n## Pages checked: {len(sample)}")
    lines += [f"- {url}" for url in sample]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")