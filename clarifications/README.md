# Specification Clarification Requests

Clarification Requests preserve unresolved domain questions without inventing business rules. An open request marked `blocks_candidate: true` prevents the affected contract from advancing to candidate.

Create `CLR-NNNN-topic.md` with YAML front matter:

    ---
    id: clr-NNNN-topic
    status: open
    blocks_candidate: true
    affected_refs:
      - stable.contract-or-rule-id
    question: The single decision the domain reviewer must make.
    requested_decisions:
      - One observable point that must be resolved.
    ---

The body should explain why the answer matters and list known interpretations without selecting one. When a human reviewer resolves it, update the authoritative contract first, add or update Scenarios, record the resolution here, and rerun the linter.

## Open requests

None. Every recorded question has a human domain decision.

## Resolved requests

- [CLR-0001: submitted Order cancellation](CLR-0001-submitted-order-cancellation.md)
- [CLR-0002: Price Snapshot authority](CLR-0002-price-snapshot-authority.md)
- [CLR-0003: money arithmetic](CLR-0003-money-arithmetic.md)
- [CLR-0004: Customer authority](CLR-0004-customer-authority.md)
- [CLR-0005: cancelled Order Item modification](CLR-0005-cancelled-order-item-modification.md)
- [CLR-0006: Command ID input conflict](CLR-0006-command-id-input-conflict.md)
- [CLR-0007: Order ID allocation](CLR-0007-order-id-allocation.md)
- [CLR-0008: Order Item identity](CLR-0008-order-item-identity.md)
- [CLR-0009: cross-context dependency unavailability](CLR-0009-dependency-unavailability.md)
- [CLR-0010: Command ID reservation lifetime](CLR-0010-command-id-retention.md)
- [CLR-0011: concurrent Commands against one Order](CLR-0011-concurrent-order-commands.md)
- [CLR-0012: Order Item removal](CLR-0012-order-item-removal.md)

These requests were resolved by human domain decisions for the Sales revision. The authoritative behavior is defined only by the referenced contracts and Scenarios; these records preserve question and resolution history.
