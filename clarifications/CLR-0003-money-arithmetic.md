---
id: clr-0003-money-arithmetic
status: resolved
blocks_candidate: false
affected_refs:
  - sales.order.total-equals-quoted-item-subtotals
  - sales.order.item-subtotal-is-pricing-authoritative
  - sales.add-order-item
  - sales.order-item-added
  - sales.order-submitted
  - pricing.quote-order-item
question: What monetary units, Quantity precision, and rounding authority govern Order calculations?
requested_decisions:
  - Define currency semantics and whether mixed currencies are prohibited.
  - Define Quantity fractional support and the owner of precision rules.
  - Define the owner and output boundary of monetary rounding.
---

# Money arithmetic

The earlier draft used abstract MoneySnapshot, UnitPriceSnapshot, and Quantity types without assigning calculation authority.

## Resolution

Human domain review selected exact base-10 fractional Quantity support. Pricing owns permitted Quantity precision, Unit of Measure, Unit Price calculation, and rounding, and returns an authoritative Item subtotal in ISO 4217 currency minor units. Zero-priced Items are permitted; negative Unit Price or Item subtotal values are prohibited. Sales preserves the exact quoted Quantity and snapshot, requires one fixed Order currency, and sums authoritative Item subtotals without recomputing or rounding them.
