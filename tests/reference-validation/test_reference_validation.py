from __future__ import annotations

from pathlib import Path

import contract_lint

from conftest import read_yaml, write_yaml


def diagnostic_codes(root: Path) -> set[str]:
    return {diagnostic.code for diagnostic in contract_lint.lint_repository(root)}


def test_duplicate_id_fails(repo_factory) -> None:
    root = repo_factory()
    path = root / "contracts" / "sales" / "events" / "order-cancelled.yaml"
    document = read_yaml(path)
    document["id"] = "sales.order-submitted"
    write_yaml(path, document)

    assert "DUPLICATE_ID" in diagnostic_codes(root)


def test_invalid_reference_fails(repo_factory) -> None:
    root = repo_factory()
    path = root / "contracts" / "sales" / "commands" / "submit-order.yaml"
    document = read_yaml(path)
    document["effects"]["events"][0]["event_ref"] = "sales.event-does-not-exist"
    write_yaml(path, document)

    assert "MISSING_REFERENCE" in diagnostic_codes(root)


def test_event_without_producer_fails(repo_factory) -> None:
    root = repo_factory()
    path = root / "contracts" / "sales" / "events" / "order-submitted.yaml"
    document = read_yaml(path)
    document.pop("producer")
    write_yaml(path, document)

    assert "EVENT_WITHOUT_PRODUCER" in diagnostic_codes(root)


def test_prohibited_technology_in_business_contract_fails(repo_factory) -> None:
    root = repo_factory()
    path = root / "contracts" / "sales" / "context.yaml"
    document = read_yaml(path)
    document["summary"] += " A Controller is required."
    write_yaml(path, document)

    assert "PROHIBITED_TERM" in diagnostic_codes(root)

