from __future__ import annotations

import itertools
import shutil
import sys
from pathlib import Path
from typing import Any, Callable

import pytest
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LINTER_DIR = PROJECT_ROOT / "tools" / "contract-lint"
sys.path.insert(0, str(LINTER_DIR))


def read_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def write_yaml(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(value, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


@pytest.fixture
def repo_factory(tmp_path: Path) -> Callable[[], Path]:
    counter = itertools.count(1)

    def create() -> Path:
        destination = tmp_path / f"canon-spec-{next(counter)}"
        shutil.copytree(
            PROJECT_ROOT,
            destination,
            ignore=shutil.ignore_patterns(
                ".venv",
                ".pytest_cache",
                "__pycache__",
                "*.pyc",
            ),
        )
        return destination

    return create

