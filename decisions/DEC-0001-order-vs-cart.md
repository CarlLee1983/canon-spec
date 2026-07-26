---
schema_version: "1.0"
kind: decision
id: DEC-0001
version: "1.0.0"
status: draft
title: Order and Cart are distinct concepts
problem: Future implementers might collapse Order, shopping cart, quotation, or invoice into one model and accidentally transfer rules between distinct business concepts.
background: The Sales slice owns an Order lifecycle, while cart behavior, quotations, and invoicing are outside its stated boundary.
decision: Adopt the canonical distinctions referenced by sales.vocabulary without restating them as rules in this Decision Record.
rejected_options:
  - Use one generic commerce document whose type flag represents Cart, Order, Quotation, and Invoice.
  - Treat Order as a renamed shopping cart.
consequences:
  - Future contexts require explicit contracts rather than unrelated lifecycle rules added to Order.
  - Technical primitives may be reused without collapsing the conceptual boundaries.
revisit_when:
  - Human domain review produces evidence that the business uses one canonical concept with one lifecycle for two or more of these terms.
contract_refs:
  - sales
  - sales.vocabulary
  - sales.order
---

# Order and Cart are distinct concepts

The machine-readable decision record is the YAML front matter above. The authoritative terminology remains in [the Sales vocabulary](../contracts/sales/vocabulary.yaml); this record preserves why the distinction was chosen.
