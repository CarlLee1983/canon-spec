> Canon Spec is an implementation-neutral business contract repository.
> It defines business behavior without prescribing how that behavior must be implemented.

# Canon Spec

Canon Spec only defines behavior; it does not implement Sales or any other application. Contracts, schemas, scenarios, decisions, clarification requests, and conformance tooling belong here. Production domain code, delivery interfaces, persistence adapters, deployment assets, and product user interfaces do not.

Business language and invariants usually survive technology generations. Framework code answers how one implementation works today; a business contract answers what every conforming implementation must continue to do. The repository therefore treats contracts as durable knowledge assets and implementation code as one replaceable realization.

## Relationship between contract and implementation

The normative chain is:

    constitution
        ↓ governs
    contracts ── observed by ── scenarios
        ↓ pinned by
    implementation manifest
        ↓ assigned to
    implementation and executable conformance tests

Contracts under [contracts](contracts/) are the sole source of normative business behavior. Scenarios express observable test oracles for cited rules. An implementation manifest pins exact contract revisions and describes a delivery target, but it cannot add or change a business rule.

The current [Sales Context](contracts/sales/README.md) is a candidate example. It includes one Order Aggregate, four Commands, four Events, one state machine, two cross-context dependency contracts, and nineteen acceptance Scenarios. No Sales implementation exists in this repository.

## Repository map

- [constitution](constitution/) defines authorship, lifecycle, compatibility, ambiguity, and traceability policy.
- [schemas](schemas/) contains JSON Schema Draft 2020-12 definitions for every supported artifact kind.
- [contracts](contracts/) contains normative business contracts and acceptance Scenarios.
- [decisions](decisions/) preserves important trade-offs without replacing authoritative contracts.
- [clarifications](clarifications/) contains unresolved questions that implementers must not guess.
- [implementation-manifests](implementation-manifests/) pins a contract set for a future implementation target.
- [tools/contract-lint](tools/contract-lint/) validates the specification repository itself.
- [tests](tests/) tests schema, reference, and traceability validation.
- [Traditional Chinese Order guide](docs/zh-TW/order-business-logic.html) visualizes the current behavior for humans without becoming a normative source.

## Add a Context

1. Choose a stable lowercase Context ID and create contracts/CONTEXT-ID/context.yaml plus a vocabulary file.
2. State owned responsibilities and explicit exclusions. Do not import rules from neighboring domains by assumption.
3. Add Aggregate, Command, Event, state-machine, interaction, and Scenario files only as the boundary requires.
4. Give every artifact schema_version, id, version, status, and kind.
5. Put every normative rule in one authoritative contract and cite it elsewhere by stable reference.
6. Add unresolved questions to clarifications before writing examples that depend on them.
7. Run the linter and tests. Keep the new Context in draft until human domain review.

Copying the Sales files can help with shape, but their business rules must not be copied into another Context without domain evidence.

## Add a Command, Event, and Scenario

For a Command:

1. define actor and typed inputs;
2. cite preconditions through rule_ref or contract_ref;
3. define a stable success code, state changes, and exact Event counts;
4. define stable failure codes, unchanged state, and no-Event behavior;
5. define Command ID replay semantics and prohibit assumptions.

For each Event, use a past-tense business fact name, define its payload and duplicate-delivery semantics, and cite exactly one producing Command.

For each Scenario, cite the Command, relevant invariant IDs, and relevant Events. Specify given facts, one Command invocation, the expected outcome code, state assertions, Event counts, and forbidden side effects. A Scenario that checks only success is incomplete.

## Run Contract Linter

The repository uses Python tooling managed by uv:

    uv sync
    uv run python tools/contract-lint/contract_lint.py .
    uv run pytest

The linter validates all JSON Schemas, YAML contracts, Decision front matter, references, unique IDs, Command outcome completeness, invariant coverage, Event producers, Scenario structure, prohibited technology leakage, and the completeness and equality of manifest contract revisions.

A successful run exits with status zero and prints a summary. A failed run prints stable diagnostic codes, paths, and messages.

## Give an Implementation Manifest to Codex

Provide Codex with the repository and exactly one manifest, for example [the TypeScript Sales manifest](implementation-manifests/typescript/sales-basic.yaml), then instruct it to:

1. read AGENTS.md and the constitution;
2. resolve every pinned contract_ref and exact version;
3. stop on open blocking Clarification Requests;
4. implement only the requested deliverables outside this specification repository;
5. execute every pinned Scenario through a conformance adapter; and
6. return the traceability output required by the manifest.

The manifest is a task boundary, not permission to reinterpret the pinned contracts.

## Create a Clarification Request

Follow [the clarification guide](clarifications/README.md). Record one decision question, affected stable references, observable points that need a ruling, and whether it blocks candidate promotion. List competing interpretations without choosing one. After human resolution, update the authoritative contract and scenarios before closing the request.

## Promote draft to candidate

A human reviewer may consider draft to candidate only when:

- every schema and example validates;
- every reference resolves and every ID is unique;
- every invariant has Scenario coverage;
- every Command has explicit success and failure semantics;
- every Event has a valid Producer;
- every Scenario asserts forbidden side effects;
- all blocking Clarification Requests affecting the revision are resolved;
- cross-context interactions, if any, define success, failure, idempotency, and duplicate handling;
- compatibility impact and version changes are correct; and
- the complete linter and test suite pass.

Only an authorized human domain reviewer may later mark a candidate accepted.

## One acceptance contract, multiple languages

[The TypeScript manifest](implementation-manifests/typescript/sales-basic.yaml) and [the Go manifest](implementation-manifests/go/sales-basic.yaml) intentionally pin the same identifier-version set and state the same deliverables, architecture constraints, completion conditions, and forbidden observations. Today they differ only in target language and task identity; a manifest MAY later carry language-specific delivery detail, but such detail MUST NOT weaken that shared set. Both must execute the same Scenarios, so conformance is compared at the business boundary, not through identical code structure.

## Current limitations

The Sales 2.0.0 example is `candidate`: internally coherent, fully traceable, and lint-clean, but not yet `accepted`. Its original eight blocking Clarification Requests are resolved. Only an authorized human domain reviewer may mark it accepted. Payment, refund, Return, fulfillment, shipment, tax, discount, inventory, invoicing, and Product-master behavior remain outside the conformance target and MUST NOT be inferred by an implementation.

Pricing is authoritative for fractional Quantity validity, Unit of Measure, price calculation, and Item-subtotal rounding. Customer is authoritative for Customer existence and actor authorization. Their internal implementations remain outside this repository; Sales implementations consume them through the pinned Interaction contracts.
