# Canon Spec Principles

## Normative

1. A business contract MUST describe observable business behavior without prescribing an implementation technology.
2. Normative business rules MUST live under `contracts/` and MUST have one authoritative definition.
3. Acceptance scenarios MUST verify both required outcomes and forbidden side effects.
4. An implementation MUST conform to the referenced contract revision; an implementation manifest MUST NOT amend business behavior.
5. A contract conflict or omission MUST produce a Specification Clarification Request rather than an inferred rule.
6. Contract identifiers and addressable rule identifiers MUST remain stable within a major version.
7. Tooling MAY validate and transform specifications but MUST NOT contain production business behavior.

## Explanatory

Business knowledge generally outlives a framework, storage engine, or transport. Canon Spec therefore records the durable behavior first, then lets multiple implementations prove conformance against the same acceptance observations.

The project motto is: Define once. Implement anywhere. Verify everywhere.

