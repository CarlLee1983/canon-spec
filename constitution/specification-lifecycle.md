# Specification Lifecycle

## Normative

Every contract MUST declare one lifecycle status:

- `draft`: incomplete or awaiting domain review; implementation work MUST treat unresolved clarifications as blockers.
- `candidate`: internally coherent, fully traceable, lint-clean, and ready for human domain acceptance.
- `accepted`: explicitly approved by an authorized human domain reviewer.
- `deprecated`: still resolvable for compatibility but superseded for new work.
- `retired`: no longer eligible for new implementations.

A contract MUST begin as `draft`. Automated tooling and AI agents MUST NOT promote a contract to `accepted`. Promotion from `draft` to `candidate` requires all schema, reference, coverage, ambiguity, and consistency checks to pass and all blocking clarifications to be resolved.

Any normative change MUST update the contract version according to `compatibility.md`. A deprecated contract MUST identify its replacement or state that no replacement exists.

## Explanatory

Lifecycle status communicates review confidence, not deployment state. A technically valid draft may still contain explicit questions that prevent faithful implementation.

