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

- **Smoke tests** (`smoke.yml`) run on every pull request and on demand. Two
workers, one retry, 10-minute timeout. HTML report, traces and screenshots of
failed tests are downloadable from the run, saved for 14 days.

- **Weekly page scan** (`scan.yml`) runs Monday 06:17 Amsterdam time and on
demand. It visits 25 pages from the sitemap, one at a time. A short summary
appears on the run page; full details are in the `scan-results` artifact, saved 
for 30 days.

## Decisions and why

- **Cookie banner.** Handled once in a fixture with `add_locator_handler`, so no
test needs to know about it. I decline optional cookies: fewer third-party
scripts in the run, and the most likely choice on a live shop. It uses the
`reject_all` class because that is the same in every language, and the banner
is not what we test.
- **Selectors.** Role- and text-based (`get_by_role`), scoped to a region such as
the header, with `exact=True` where labels overlap. They read like the user
journey and break loudly when something changes. The one exception is the
cookie banner.
- **No fixed sleeps.** Playwright's auto-waiting handles timing, including the
hover menu animation.
- **Flaky tests.** One retry in CI, and reruns stay visible in the report.
Known-flaky tests get a `quarantine` marker: they still run but never block a
merge, and each needs an owner and a ticket. `--strict-markers` turns a typo'd
marker into an error, so a test cannot silently drop out of the gate.
- **What fails the scan, and what is only reported.** A sampled page returning
400+ fails the job: the sitemap promises the page exists. Console errors and
failing resources are reported but do not fail it, as those tend to be ignored
long term.
- **How the scan samples.** 25 pages a week, chosen with a seed based on the week
number. The sample is identical all week, so a finding can be reproduced, and
rotates weekly, covering the ~1,670 sitemap URLs in a little over a year.
Cookies are cleared between pages so there is no interference.

## Findings on the site

Possible improvements:
- The sitemap lists technical routes (`/auth0/...`, `/add/take_back/product`)
  in all four languages. These are not content pages; worth checking whether
  they belong in the sitemap. They are excluded from the scan.
- Almost every page logs a deprecated `unload` handler in the console
  (22 of 25 pages in the latest scan). Browsers are phasing this event out.
- The Smartphones page has two `<h1>` elements. Not a WCAG failure, but screen
  reader users and search engines expect one main heading.

Observations relevant to automation:
- Language and country are chosen by geo-IP, so a CI runner may see a
  different shop than a visitor in the Netherlands. The suite sets the
  language explicitly for this reason.
- The site already has language-independent hooks for its own JavaScript
  (`data-fp-navigation-hover`). Adding `data-testid` attributes would follow
  the same pattern.
- GitHub-hosted runners were not blocked by bot protection at the time of
  writing.

## Known limitations

- Text selectors depend on language: navigation passes in English, Dutch and
  German, and fails in French at the "Shop" hover.
- Desktop only: the hover menu has no mobile equivalent in these tests.
- Chromium only, no WebKit or Firefox yet.

## What I left out, and what I would do with another day

- WebKit and mobile-viewport runs.
- `data-testid` attributes on key elements, agreed with the developers, to make
  the suite language-independent.

## What was new to me

- Playwright with Python (I had used it with TypeScript), GitHub Actions (I had
used Azure DevOps pipelines), pytest fixtures, and how Odoo handles languages
in URLs.

## Use of AI assistance

- I used Claude as a guide and reviewer. I typed and ran every line myself and
asked for explanations for every line. Testing caught suggestions that were 
wrong: an environment-variable line would have broken CI when the variable was 
empty, and one suggested action version still ran on Node 20 when upgrading to 
Node 24.