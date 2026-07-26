---
schema_version: "1.0"
kind: decision
id: DEC-0007
version: "1.0.0"
status: draft
title: A Command ID reservation never expires
problem: Sales-wide Command ID uniqueness was defined without a lifetime, so nothing said whether an identifier reused long after its original Command should conflict or succeed as a new Command.
background: CLR-0006 established Sales-wide uniqueness and normalized input comparison, and the Order Aggregate carries both the replay rule and the conflict rule. The strictest reading of those rules already implied unbounded reservation, but no contract said so, which left implementers to infer a bound or its absence.
decision: State unbounded reservation explicitly in sales.order.command-id-conflict. The reservation of an accepted Command ID MUST NOT lapse with the passage of time, so age alone never turns a reuse back into an acceptable new Command.
rejected_options:
  - Define a business retention period after which a Command ID is free and its reuse is a new Command.
  - Leave the lifetime outside the business contract so each deployment chooses, accepting that two conforming implementations may answer the same reuse differently.
consequences:
  - Replay and conflict outcomes are deterministic for the life of the Sales Context rather than dependent on when a request arrives.
  - Every conforming implementation carries accepted Command ID history without a time bound, and cannot reclaim that storage without becoming non-conforming.
  - No Scenario outcome changes, because the rule makes an existing implication explicit rather than altering observable behavior.
  - A future retention period would be a breaking change, since a reuse that conflicts today would then succeed.
revisit_when:
  - The unbounded retention obligation becomes materially harder to meet than the determinism it buys.
  - Human domain reviewers introduce a business meaning for Command ID age, such as an archival or closure boundary.
contract_refs:
  - sales
  - sales.order
  - sales.order.command-id-conflict
  - sales.order.command-id-idempotency
  - sales.vocabulary
---

# A Command ID reservation never expires

The YAML front matter records the trade-off. Normative behavior remains authoritative only in the referenced contracts. Resolves [CLR-0010](../clarifications/CLR-0010-command-id-retention.md).

The obligation this creates is real and deliberately visible. An implementation cannot expire Command IDs and remain conforming, which is a storage cost that grows without limit. The decision accepts that cost because the alternative prices it in correctness: a bounded reservation makes the answer to an identical request depend on when it arrives, and a caller cannot tell a lapsed reservation from a genuinely new Command.

**Falsified if:** the retention obligation grows costly enough that implementations would rather accept non-determinism, or `contracts/sales/aggregates/order.yaml` no longer states that an accepted Command ID reservation does not lapse.
