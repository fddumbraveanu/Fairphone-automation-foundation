# Fairphone automation foundation

End-to-end smoke suite and weekly page scan for www.fairphone.com,
built with Playwright for Python, pytest and GitHub Actions.

## How to run locally

```
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium

pytest -m smoke --headed          # smoke suite, visible browser
pytest -m scan --tracing off      # weekly page scan
```

Configuration (environment variables, all optional):
- `BASE_URL`: target shop, default `https://www.fairphone.com`
- `LANGUAGE`: shop language, default `en` (also `nl`, `de`, `fr`)

## What each workflow does

- ...

## Decisions and why

- ...

## Findings

- The shop picks language and country by geo-IP; English has no URL prefix.
- Main menu is a hover menu.
- Two `<h1>` elements on the Smartphones page.
- Text labels differ per language ("Shop" is "E-Boutique" in French).
- Sitemap lists technical routes (`/auth0/...`, `/add/take_back/product`).
- Console: deprecated `unload` handler on almost every page.
- GitHub-hosted runners were not blocked by bot protection at the time of writing.

## Known limitations

- ...

## What I left out, and what I would do with another day

- ...

## What was new to me

- ...

## Use of AI assistance

- ...