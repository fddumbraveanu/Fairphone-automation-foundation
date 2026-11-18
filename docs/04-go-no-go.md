# Go/no-go: product launch

It is Thursday 16:00. Tomorrow at 09:00 we release the webshop changes for a new product, 
marketing sends the launch email to 400,000 subscribers at 10:00. Here is what you know:
- The smoke suite passed 46 of 48 tests on acceptance.
- One failure is "add accessory to cart from the product page", on WebKit only. It 
failed in one of three
retries. Over the last two weeks this test failed four times on WebKit and passed 
after a retry each time.
- The other failure is real: on acceptance, the order confirmation email for UK 
customers shows prices
without VAT. A developer says "that's not new, production has done that for months".
- A UX designer found that the new product image gallery cannot be swiped on iOS 
Safari. It works with
the arrows.
- The Product Owner wants to ship: "the launch date is public, we can't move it".

## Message to the team channel

> Go/no-go for tomorrow's launch: **go, with conditions.** 46/48 smoke tests
> green on acceptance.
>
> 1. Add accessory to cart on Webkit: known flaky test. I'll check it on a real
>    iPhone ASAP. Quarantine the test, with a ticket and an owner
> 2. UK order confirmations show prices without VAT. Since it's not new (production
>    has it too), holding the launch doesn't fix it. Logged as Critical. @PO 
>    please confirm you accept this risk for the launch. @devs can we hotfix it 
>    this ASAP after release? I'll give customer service a heads-up.
> 3. Gallery swipe broken on iOS Safari, arrows work. Logged as Major for next
>    sprint.

## What I would change before the next launch
- Hold the go/no-go the day before at noon, not 16:00, with a code freeze two
  days before launch, so there is time to fix what we find.
- Agree severity rules and go/no-go criteria in advance, so the decision is
  checked against them instead of negotiated under pressure.
- A launch test plan that includes real iOS devices and the order emails for
  every country and currency.
- Quarantine known-flaky tests with an owner, so a red run always means
  something.
- Keep a list of known production issues with a severity. "That's not new" is
  only reassuring if it was already tracked and accepted.