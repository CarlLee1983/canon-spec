from __future__ import annotations

from pathlib import Path

import contract_lint

from conftest import PROJECT_ROOT, read_yaml, write_yaml


def diagnostic_codes(root: Path) -> set[str]:
    return {diagnostic.code for diagnostic in contract_lint.lint_repository(root)}


def test_valid_contract_repository_passes() -> None:
    diagnostics = contract_lint.lint_repository(PROJECT_ROOT)
    assert diagnostics == [], "\n".join(
        f"{item.path}: {item.code}: {item.message}" for item in diagnostics
    )


def test_missing_required_field_fails(repo_factory) -> None:
    root = repo_factory()
    path = root / "contracts" / "sales" / "commands" / "submit-order.yaml"
    document = read_yaml(path)
    document.pop("summary")
    write_yaml(path, document)

    assert "SCHEMA_VALIDATION" in diagnostic_codes(root)


def test_manifest_technology_targets_are_allowed(repo_factory) -> None:
    root = repo_factory()
    targets = (
        (
            root
            / "implementation-manifests"
            / "typescript"
            / "sales-basic.yaml",
            "TypeScript",
        ),
        (
            root / "implementation-manifests" / "go" / "sales-basic.yaml",
            "Go",
        ),
    )
    for path, language in targets:
        document = read_yaml(path)
        document["implementation_target"]["language"] = language
        write_yaml(path, document)

    diagnostics = contract_lint.lint_repository(root)
    assert diagnostics == [], "\n".join(
        f"{item.path}: {item.code}: {item.message}" for item in diagnostics
    )

