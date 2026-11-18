import random
import xml.etree.ElementTree as ET
from datetime import date

SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
TECHNICAL_ROUTES = ("/auth0/", "/add/")


def parse_sitemap(xml_text: str) -> list[str]:
    root = ET.fromstring(xml_text)
    return [loc.text.strip() for loc in root.findall("sm:url/sm:loc", SITEMAP_NS)]


def is_content_page(url: str) -> bool:
    return not any(route in url for route in TECHNICAL_ROUTES)


def weekly_sample(urls: list[str], size: int = 25) -> list[str]:
    year, week, _ = date.today().isocalendar()
    rng = random.Random(f"{year}-W{week}")
    return rng.sample(urls, min(size, len(urls)))