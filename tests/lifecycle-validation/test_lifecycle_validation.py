from __future__ import annotations

from pathlib import Path

import contract_lint

from conftest import read_yaml, write_yaml


def diagnostic_codes(root: Path) -> set[str]:
    return {diagnostic.code for diagnostic in contract_lint.lint_repository(root)}


def promote_order_aggregate(root: Path) -> None:
    path = root / "contracts" / "sales" / "aggregates" / "order.yaml"
    document = read_yaml(path)
    document["status"] = "candidate"
    write_yaml(path, document)


def test_blocking_clarification_blocks_promoted_contract(repo_factory) -> None:
    root = repo_factory()
    clarification = root / "clarifications" / "CLR-0010-command-id-retention.md"
    clarification.write_text(
        clarification.read_text(encoding="utf-8").replace(
            "blocks_candidate: false", "blocks_candidate: true"
        ),
        encoding="utf-8",
    )
    promote_order_aggregate(root)

    assert "BLOCKED_CONTRACT_PROMOTED" in diagnostic_codes(root)


def test_non_blocking_clarification_allows_promoted_contract(repo_factory) -> None:
    root = repo_factory()
    promote_order_aggregate(root)

    assert "BLOCKED_CONTRACT_PROMOTED" not in diagnostic_codes(root)


def test_resolved_blocking_clarification_allows_promoted_contract(repo_factory) -> None:
    root = repo_factory()
    clarification = root / "clarifications" / "CLR-0011-concurrent-order-commands.md"
    clarification.write_text(
        clarification.read_text(encoding="utf-8").replace(
            "blocks_candidate: false", "blocks_candidate: true"
        ),
        encoding="utf-8",
    )
    promote_order_aggregate(root)

    assert "BLOCKED_CONTRACT_PROMOTED" not in diagnostic_codes(root)
