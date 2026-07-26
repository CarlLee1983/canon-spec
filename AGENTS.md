# Canon Spec Working Agreement

## Repository purpose

This repository defines implementation-neutral business contracts. It MUST NOT contain production business implementations, delivery adapters, persistence models, deployment assets, or product user interfaces.

## Sources of truth

1. `/contracts` is the sole source of truth for normative business behavior.
2. Implementation code, API documentation, database structures, and implementation tests are subordinate to the contracts.
3. The same rule MUST NOT be defined in more than one document.
4. Other documents MUST refer to rules and contracts through stable `rule_ref`, `contract_ref`, or `scenario_ref` identifiers.
5. Normative content and explanatory content MUST be visibly separated.
6. Normative content MUST use MUST, MUST NOT, SHALL, or SHALL NOT.
7. Undefined behavior MUST NOT be inferred.
8. Implementers MUST NOT resolve specification conflicts themselves.
9. Every invariant MUST be referenced by at least one acceptance scenario.
10. Every Command MUST define both its successful effects and its failure outcomes, or explicitly declare that it has no domain failures.
11. Every Domain Event MUST identify a Producer.
12. Every cross-context interaction MUST define success, failure, idempotency, and duplicate-handling semantics.

## Change workflow

- Read this file, the relevant constitution documents, and the affected contracts before editing.
- Preserve business and implementation separation. Technology names are permitted only in implementation manifests and tooling documentation.
- Add or change a business rule in exactly one contract, then update references and scenarios.
- Record unresolved business questions under `/clarifications`; do not hide them in defaults or examples.
- Keep new Sales contracts in `draft` until human domain review authorizes another lifecycle state.
- Run the contract linter and its complete test suite before reporting a specification change as complete.

## Verification

From the repository root, run:

    uv run python tools/contract-lint/contract_lint.py .
    uv run pytest

