# Contract Linter

Run from the Canon Spec repository root:

    uv run python tools/contract-lint/contract_lint.py .

The command exits with zero only when JSON Schemas, contract documents, references, traceability, producer declarations, prohibited-term boundaries, and implementation manifest revision sets are valid. A manifest revision set is valid only when it is complete, version-accurate, free of repeated targets, and identical across manifests.

Diagnostics use stable uppercase codes so repository automation can classify failures without parsing prose.

