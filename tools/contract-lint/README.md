# Contract Linter

Run from the Canon Spec repository root:

    uv run python tools/contract-lint/contract_lint.py .

The command exits with zero only when JSON Schemas, contract documents, references, traceability, producer declarations, prohibited-term boundaries, and implementation manifest revision sets are valid. A manifest revision set is valid only when it is complete, version-accurate, free of repeated targets, and identical across manifests.

The linter also enforces the lifecycle rule in `constitution/ambiguity-policy.md`: a contract cited by an unresolved Clarification Request marked `blocks_candidate: true` MUST NOT declare `candidate` or `accepted`. This makes the promotion checklist item "all blocking Clarification Requests affecting the revision are resolved" machine-checkable rather than a manual review step.

Diagnostics use stable uppercase codes so repository automation can classify failures without parsing prose.

