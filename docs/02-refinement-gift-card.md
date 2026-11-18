# Refinement: pay with a gift card

Story: As a customer, I want to pay with a Fairphone gift card at checkout, 
so that I can use a gift I received.

The PO's notes: "Gift cards are sold on the webshop in fixed amounts (€25, 
€50, €100) and sent by email with a code. At checkout the customer enters 
the code and the amount comes off the order. If the card is worth more than 
the order, the rest stays on the card for next time. Customers can also have 
a promo code. Gift cards are valid for one year."

## Questions, ranked by importance
1. Gift card and promo code together: allowed? If so, in which order: promo
   on the full price first, then the gift card?
2. When is the balance deducted: when the code is applied, or when the order
   is paid? What stops the same card being spent twice in two open checkouts?
3. If the remaining amount is paid by card or iDEAL and that payment fails or
   is abandoned, is the gift card amount released again?
4. Returns and cancellations: does the gift card part go back to the card,
   and does it maintain its validity ?
5. Can more than one gift card be used in one order?
6. Currencies and shops: can an EU (EUR) card be used on the UK or US shop?
7. Does the gift card pay for shipping?
8. Code security: format and length, case sensitivity, and a limit on uses?
   I.E. one time or timed promo codes

## Assumptions (until answered)
- Allowed together, Promo code applies first, gift card second.
- The balance is reserved when applied and deducted when the order is paid.
- One gift card per order.
- after payment failure, gift card amount is released again

## Acceptance criteria
- Given a valid gift card worth less than the order, when I apply the code,
  then its value is deducted and I pay the rest with another payment method.
- Given a valid gift card worth more than the order, when I apply it, then
  the order total is €0 and the remaining balance stays on the card.
- Given a promo code and a gift card, when I apply both, then the promo is
  applied first and the gift card on the reduced total.
- Given an invalid, expired or empty card, when I apply the code, then I see
  a clear error message and the order total does not change.
- The cart, the order confirmation and the invoice show the gift card amount
  and the remaining balance.

## Edge cases and negative scenario
| Scenario | Where to test | Why there |
|---|---|---|
| Edge: card value exactly equals the order total | Unit test (developer) | Pure calculation; fast, and boundaries are cheapest to test there |
| Edge: card expires between applying it and paying | Integration test (developer) | Needs a controlled clock; impossible on a real shop |
| Edge: remaining payment fails at the payment provider | E2E on acceptance, provider in test mode | Crosses Odoo and the provider; only E2E shows the whole flow |
| Negative: the same card used in two checkouts at the same time | Integration test (developer), plus one manual check on acceptance | Timing cannot be controlled reliably in E2E |


## Non-functional requirements
- Security: codes cannot be guessed, and full codes never appear in emails, 
  URLs or logs.
- Consistency: the same gift card can never be spent twice or end up with a
  negative balance, even when used in two checkouts at the same moment
- Performance: applying a code is a responsve action(preferably < 1s)