from __future__ import annotations

from pathlib import Path

import contract_lint

from conftest import read_yaml, write_yaml


def diagnostic_codes(root: Path) -> set[str]:
    return {diagnostic.code for diagnostic in contract_lint.lint_repository(root)}


def test_invariant_without_scenario_coverage_fails(repo_factory) -> None:
    root = repo_factory()
    path = root / "contracts" / "sales" / "aggregates" / "order.yaml"
    document = read_yaml(path)
    document["invariants"].append(
        {
            "id": "sales.order.uncovered-test-invariant",
            "statement": "An Order MUST satisfy this deliberately uncovered test rule.",
            "category": "value",
        }
    )
    write_yaml(path, document)

    assert "UNCOVERED_INVARIANT" in diagnostic_codes(root)


def test_manifest_omitting_a_contract_fails(repo_factory) -> None:
    root = repo_factory()
    omitted = "sales.order-lifecycle"
    for language in ("typescript", "go"):
        path = root / "implementation-manifests" / language / "sales-basic.yaml"
        document = read_yaml(path)
        document["contract_revisions"] = [
            revision
            for revision in document["contract_revisions"]
            if revision["contract_ref"] != omitted
        ]
        write_yaml(path, document)

    codes = diagnostic_codes(root)
    assert "MANIFEST_INCOMPLETE_CONTRACT_SET" in codes
    assert "MANIFEST_CONTRACT_SET_MISMATCH" not in codes

