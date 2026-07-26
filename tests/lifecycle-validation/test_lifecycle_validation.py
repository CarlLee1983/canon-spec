from __future__ import annotations

from pathlib import Path

import contract_lint

from conftest import read_yaml, write_yaml


def diagnostic_codes(root: Path) -> set[str]:
    return {diagnostic.code for diagnostic in contract_lint.lint_repository(root)}


CLARIFICATION = "CLR-0010-command-id-retention.md"


def promote_order_aggregate(root: Path) -> None:
    path = root / "contracts" / "sales" / "aggregates" / "order.yaml"
    document = read_yaml(path)
    document["status"] = "candidate"
    write_yaml(path, document)


def set_clarification(root: Path, *, status: str, blocking: bool) -> None:
    """Pin both front-matter fields so the test states its own precondition."""
    path = root / "clarifications" / CLARIFICATION
    lines = []
    for line in path.read_text(encoding="utf-8").split("\n"):
        if line.startswith("status:"):
            line = f"status: {status}"
        elif line.startswith("blocks_candidate:"):
            line = f"blocks_candidate: {str(blocking).lower()}"
        lines.append(line)
    path.write_text("\n".join(lines), encoding="utf-8")


def test_blocking_clarification_blocks_promoted_contract(repo_factory) -> None:
    root = repo_factory()
    set_clarification(root, status="open", blocking=True)
    promote_order_aggregate(root)

    assert "BLOCKED_CONTRACT_PROMOTED" in diagnostic_codes(root)


def test_non_blocking_clarification_allows_promoted_contract(repo_factory) -> None:
    root = repo_factory()
    set_clarification(root, status="open", blocking=False)
    promote_order_aggregate(root)

    assert "BLOCKED_CONTRACT_PROMOTED" not in diagnostic_codes(root)


def test_resolved_blocking_clarification_allows_promoted_contract(repo_factory) -> None:
    root = repo_factory()
    set_clarification(root, status="resolved", blocking=True)
    promote_order_aggregate(root)

    assert "BLOCKED_CONTRACT_PROMOTED" not in diagnostic_codes(root)
