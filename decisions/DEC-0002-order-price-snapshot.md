---
schema_version: "1.0"
kind: decision
id: DEC-0002
version: "2.0.0"
status: draft
title: Pricing owns quote arithmetic and Sales preserves its snapshot
problem: Re-reading a live price or repeating Pricing arithmetic inside Sales could silently change Item subtotals and Order totals.
background: Sales owns Order consistency but Pricing owns Product quotation, fractional Quantity validity, Unit of Measure, calculation, and rounding.
decision: Adopt pricing.quote-order-item as the authority for the final Item subtotal and sales.order.item-retains-price-snapshot as the retention rule; Sales sums quoted same-currency subtotals without recomputing or rounding them.
rejected_options:
  - Let a Customer provide an unverified Unit Price Snapshot.
  - Recalculate every Order from a current live price.
  - Duplicate Pricing precision and rounding rules inside Sales.
consequences:
  - Price Quotes must contain Product, exact Quantity, Unit of Measure, Unit Price, Currency Code, final Item subtotal, identity, and validity evidence.
  - Zero-priced Items remain possible, while negative Item values cannot smuggle refund, Return, discount, or credit behavior into Sales.
  - Fractional Quantity support does not force Sales to own Product-specific precision rules.
  - Sales implementations require a Pricing dependency port and deterministic conformance fixture.
revisit_when:
  - A reviewed Pricing Contract replaces quote-time Item subtotals with another authoritative pricing lifecycle.
  - Human domain reviewers require repricing before submission.
contract_refs:
  - sales
  - sales.order
  - sales.order.item-retains-price-snapshot
  - sales.order.item-subtotal-is-pricing-authoritative
  - sales.add-order-item
  - pricing
  - pricing.quote-order-item
---

# Pricing owns quote arithmetic and Sales preserves its snapshot

The YAML front matter records the trade-off. Normative behavior remains authoritative only in the referenced contracts.
