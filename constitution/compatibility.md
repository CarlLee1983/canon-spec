# Compatibility and Versioning

## Normative

Contract `version` values MUST use semantic versioning.

- A major version MUST change when an accepted observer could distinguish a previously conforming implementation as non-conforming.
- A minor version MUST change for backward-compatible additions, including new optional behavior with explicit semantics.
- A patch version MUST change for non-normative clarification or correction that does not change observable behavior.

The `schema_version` identifies the serialization vocabulary and MUST be evaluated independently from the business contract `version`.

An implementation manifest MUST pin every referenced contract by identifier and exact version. Two implementations claiming the same conformance target MUST list the same identifier-version pairs.

Removing or renaming a stable identifier MUST be treated as a breaking change. Deprecated identifiers MUST remain resolvable until the owning contract is retired.

## Explanatory

Compatibility is defined by business observations, not by source-code signatures, storage layouts, or transport shapes.

