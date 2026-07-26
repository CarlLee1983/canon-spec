---
id: clr-0006-command-id-input-conflict
status: resolved
blocks_candidate: false
affected_refs:
  - sales.order.command-id-idempotency
  - sales.order.command-id-conflict
  - sales.create-order-draft
  - sales.add-order-item
  - sales.submit-order
  - sales.cancel-order
question: What outcome is required when a previously used Command ID is repeated with different input?
requested_decisions:
  - Define Command ID uniqueness scope.
  - Define the stable failure code for an input mismatch.
  - Define comparison of semantically equivalent serialized values.
---

# Command ID reused with different input

The earlier rule defined identical-request replay but not changed-input reuse.

## Resolution

Human domain review selected Sales-wide Command ID uniqueness. The same Command and semantically normalized input returns the original outcome; reuse for another Command or different normalized input returns `COMMAND_ID_CONFLICT` without state changes or Domain Event occurrences.
