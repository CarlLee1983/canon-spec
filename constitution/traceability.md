# Traceability

## Normative

Every addressable artifact MUST have a globally unique, stable `id`. References MUST contain the exact target identifier and MUST resolve within the repository.

- `rule_ref` MUST resolve to an invariant identifier.
- `event_ref` MUST resolve to an Event contract identifier.
- `contract_ref` and entries in `contract_refs` MUST resolve to a top-level contract or an addressable invariant.
- `scenario_ref` MUST resolve to a Scenario contract identifier.
- `command_ref` MUST resolve to a Command contract identifier.

An acceptance scenario MUST cite every rule, Command, and Event whose behavior it verifies. It MUST NOT become a second source of normative rules; its `given`, `when`, and `then` fields are executable observations of cited contracts.

Every invariant MUST be cited by at least one Scenario. Every Event MUST cite its producing Command. Every implementation manifest MUST pin its complete contract set as identifier-version pairs and MUST request a traceability output that maps deliverables and tests back to those pairs.

References MUST NOT depend on file paths. Moving a file without changing its identifier MUST NOT change the meaning of a reference.

An Event count in a Command or Scenario MUST measure producer-side business occurrences before any delivery retry or redelivery. A delivery duplicate MUST NOT be interpreted as a second business occurrence.

## Explanatory

The linter builds a repository-wide identifier index, resolves references by identifier, and reports missing or duplicate targets. File paths remain useful navigation hints but are not contract identity.
