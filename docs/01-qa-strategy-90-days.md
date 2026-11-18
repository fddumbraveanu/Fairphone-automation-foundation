# QA strategy: the first 90 days
To: Lead Developer, Product Owners

## Where I would start
1. Weeks 1–2: learn before changing. Sit in on refinement and a release,
   test alongside the UX designers and the Implementation Manager, discuss 
   with developers where the pain-points are. read the last few months of 
   bugs. Agree severity rules and go/no-go criteria with the Lead Developer 
   and POs.
2. Weeks 3–6: a PR gate on the purchase path (Playwright smoke test run in 
   GitHub Actions), and quality items in the Definition of Done.
3. Weeks 7–12: extend coverage by risk, add the scheduled scan, and share the 
first quality metrics in a sprint review, compared with the baseline from weeks 
1–2, and prepare a launch test plan, so the next big launch is tested against it.

## Test levels and ownership
- Developers: unit and integration tests for their code, as part of DoD.
  Reviewed in the PR like the code itself.
- QA: end-to-end and smoke testing, the scheduled scan, exploratory and release 
  testing, and test strategy.
  triages the weekly scan every Monday and turns findings into Jira tickets
  for developers or content editors, depending on the cause.
- Shared: acceptance criteria, written in (pre)refinement before development.
- How developers take ownership: agreed in the DoD rather than enforced by me,
  test results visible in every PR, and pairing on the first tests.

## What runs when
| When                      | What                                         | Budget  |
| Every PR (blocks merge)   | Unit/integration, E2E smoke on purchase path | < 10 min|
| After deploy to acceptance| Smoke against acceptance, exploratory checks | < 15 min|
| Weekly on live            | Page scan: broken pages, console errors      | < 15 min|
| Manual                    | Exploratory, cross-device, launch rehearsal  | planned |
Why: fast and stable checks block; broad or slow ones report.

## Manual testing
- Sprint release: a short risk-based checklist per story, based on its
  acceptance criteria, done by QA.
- Big launch: a written test plan two weeks ahead, a code freeze before
  launch day, a rehearsal on acceptance, real devices (iOS Safari, Android
  Chrome), and checks in every shop language and currency.
- Who: QA leads; UX and the Implementation Manager join for launches.

## Bug severity
| Level    | Definition                         | Example                               | Release        |
| Blocker  | Customers cannot buy or pay        | Checkout fails, payment not taken     | Blocks release |
| Critical | financial damage or legal exposure | Wrong price, VAT missing on invoices  | Blocks release unless the PO accepts the risk in writing |
| Major    | Important flow broken, workaround  | Gallery swipe broken on iOS, arrows work | Next sprint |
| Minor    | Cosmetic or rare                   | Misaligned label on one language       | Backlog       |

## Go/no-go
- Go when: no open blockers or criticals, smoke green on acceptance,
  launch checklist done.
- Who decides: QA gives the quality recommendation; the PO owns the business
  decision.
- If the PO disagrees: risks are written down, the PO accepts them
  explicitly, a follow-up ticket is created with a date. No silent overrides.

## Definition of Done (basics, to be fleshed out based on existing documentation)
- Acceptance criteria met and tested; new logic has unit tests.
- PR checks green; no new console errors.
- Checked on a mobile viewport 
- basic accessibility (labels present, keyboard usability present).
- Translations present for all shop languages.

## Test environments and data
- Acceptance close to production: same Odoo version, data refreshed regularly.
- Payment provider in test mode, with test cards for success and failure.
- Known test products, gift cards and promo codes that nobody else changes.
- A way to reach acceptance from CI without bot protection blocking it.

## Measuring progress
1. Bugs found in production per release (main outcome metric).
2. Share of bugs found before merge vs. after release (is shift-left working?).
3. Checkout errors in production: checkouts that fail for technical reasons
   (errors, failed payment callbacks), with page speed from the existing Web
   Vitals monitoring.
4. Smoke suite stability: share of runs that needed a retry.
Reported monthly in the sprint review, as trends rather than single numbers.

## What I would NOT do in the first 90 days
- Automate everything: only the purchase path and the highest-risk flows.
- Performance and load testing tools: use existing Web Vitals data first.
- Gatekeeping every change myself: the goal is shared ownership.
- Change the team's tooling: build on GitHub, Jira and Odoo.sh as they are.

## What I need
- Access to acceptance, GitHub Actions and the payment test mode.
- Time in refinement and sprint reviews.
- Lead Developer support for test IDs and the DoD.
- A small budget for real-device testing (e.g. a device cloud) before launches.