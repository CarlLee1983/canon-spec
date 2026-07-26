#!/usr/bin/env python3
"""Validate Canon Spec schemas, contracts, references, and traceability."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator

import yaml
from jsonschema import Draft202012Validator


SCHEMA_BY_KIND = {
    "context": "context.schema.json",
    "vocabulary": "vocabulary.schema.json",
    "aggregate": "aggregate.schema.json",
    "command": "command.schema.json",
    "event": "event.schema.json",
    "interaction": "interaction.schema.json",
    "state-machine": "state-machine.schema.json",
    "scenario": "scenario.schema.json",
    "decision": "decision.schema.json",
    "implementation-manifest": "implementation-manifest.schema.json",
}

EXPECTED_SCHEMAS = frozenset(SCHEMA_BY_KIND.values())

PROHIBITED_CONTRACT_TERMS = (
    "Controller",
    "Prisma",
    "GORM",
    "Laravel",
    "Next.js",
    "PostgreSQL",
    "MySQL",
    "Kafka",
    "RabbitMQ",
    "HTTP 200",
    "REST endpoint",
)

REFERENCE_LIST_KEYS = frozenset(
    {
        "owned_aggregates",
        "commands",
        "events",
        "state_machines",
        "interactions",
    }
)


@dataclass(frozen=True)
class Diagnostic:
    code: str
    path: Path
    message: str


@dataclass(frozen=True)
class Document:
    path: Path
    data: dict[str, Any]
    category: str

    @property
    def kind(self) -> str | None:
        value = self.data.get("kind")
        return value if isinstance(value, str) else None

    @property
    def identifier(self) -> str | None:
        value = self.data.get("id")
        return value if isinstance(value, str) else None


def _display_path(path: Path, root: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def _yaml_document(path: Path, category: str, root: Path) -> tuple[Document | None, list[Diagnostic]]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return None, [
            Diagnostic(
                "YAML_PARSE_ERROR",
                _display_path(path, root),
                str(exc),
            )
        ]
    if not isinstance(value, dict):
        return None, [
            Diagnostic(
                "DOCUMENT_NOT_MAPPING",
                _display_path(path, root),
                "The document root must be a mapping.",
            )
        ]
    return Document(path, value, category), []


def _front_matter_document(
    path: Path, category: str, root: Path
) -> tuple[Document | None, list[Diagnostic]]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [
            Diagnostic("DOCUMENT_READ_ERROR", _display_path(path, root), str(exc))
        ]

    if not text.startswith("---\n"):
        return None, [
            Diagnostic(
                "FRONT_MATTER_MISSING",
                _display_path(path, root),
                "Markdown record must start with YAML front matter.",
            )
        ]

    closing = text.find("\n---\n", 4)
    if closing < 0:
        return None, [
            Diagnostic(
                "FRONT_MATTER_UNTERMINATED",
                _display_path(path, root),
                "YAML front matter has no closing delimiter.",
            )
        ]

    try:
        value = yaml.safe_load(text[4:closing])
    except yaml.YAMLError as exc:
        return None, [
            Diagnostic(
                "YAML_PARSE_ERROR",
                _display_path(path, root),
                str(exc),
            )
        ]

    if not isinstance(value, dict):
        return None, [
            Diagnostic(
                "DOCUMENT_NOT_MAPPING",
                _display_path(path, root),
                "YAML front matter must be a mapping.",
            )
        ]
    return Document(path, value, category), []


def _load_schemas(root: Path) -> tuple[dict[str, dict[str, Any]], list[Diagnostic]]:
    schemas: dict[str, dict[str, Any]] = {}
    diagnostics: list[Diagnostic] = []
    schema_dir = root / "schemas"

    present = {path.name for path in schema_dir.glob("*.json")}
    for missing in sorted(EXPECTED_SCHEMAS - present):
        diagnostics.append(
            Diagnostic(
                "SCHEMA_MISSING",
                Path("schemas") / missing,
                "Required JSON Schema is missing.",
            )
        )

    for path in sorted(schema_dir.glob("*.json")):
        display = _display_path(path, root)
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            diagnostics.append(Diagnostic("SCHEMA_JSON_INVALID", display, str(exc)))
            continue
        if not isinstance(value, dict):
            diagnostics.append(
                Diagnostic("SCHEMA_NOT_MAPPING", display, "Schema root must be an object.")
            )
            continue
        try:
            Draft202012Validator.check_schema(value)
        except Exception as exc:
            diagnostics.append(Diagnostic("SCHEMA_INVALID", display, str(exc)))
            continue
        schemas[path.name] = value

    return schemas, diagnostics


def _discover_documents(root: Path) -> tuple[list[Document], list[Diagnostic]]:
    documents: list[Document] = []
    diagnostics: list[Diagnostic] = []

    for base, category in (
        (root / "contracts", "contract"),
        (root / "implementation-manifests", "manifest"),
    ):
        for path in sorted(base.rglob("*.yaml")):
            document, errors = _yaml_document(path, category, root)
            diagnostics.extend(errors)
            if document is not None:
                documents.append(document)

    for path in sorted((root / "decisions").glob("DEC-*.md")):
        document, errors = _front_matter_document(path, "decision", root)
        diagnostics.extend(errors)
        if document is not None:
            documents.append(document)

    for path in sorted((root / "clarifications").glob("CLR-*.md")):
        document, errors = _front_matter_document(path, "clarification", root)
        diagnostics.extend(errors)
        if document is not None:
            documents.append(document)

    return documents, diagnostics


def _json_path(parts: Iterable[Any]) -> str:
    rendered = "$"
    for part in parts:
        if isinstance(part, int):
            rendered += f"[{part}]"
        else:
            rendered += f".{part}"
    return rendered


def _schema_diagnostics(
    documents: Iterable[Document],
    schemas: dict[str, dict[str, Any]],
    root: Path,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for document in documents:
        if document.category == "clarification":
            missing = [
                key
                for key in ("id", "status", "blocks_candidate", "affected_refs", "question")
                if key not in document.data
            ]
            if missing:
                diagnostics.append(
                    Diagnostic(
                        "CLARIFICATION_METADATA_MISSING",
                        _display_path(document.path, root),
                        "Missing fields: " + ", ".join(missing),
                    )
                )
            continue

        kind = document.kind
        schema_name = SCHEMA_BY_KIND.get(kind or "")
        if schema_name is None:
            diagnostics.append(
                Diagnostic(
                    "UNKNOWN_KIND",
                    _display_path(document.path, root),
                    f"Unsupported or missing kind: {kind!r}.",
                )
            )
            continue
        schema = schemas.get(schema_name)
        if schema is None:
            continue
        validator = Draft202012Validator(schema)
        for error in sorted(validator.iter_errors(document.data), key=lambda item: list(item.path)):
            diagnostics.append(
                Diagnostic(
                    "SCHEMA_VALIDATION",
                    _display_path(document.path, root),
                    f"{_json_path(error.path)}: {error.message}",
                )
            )
    return diagnostics


def _walk_ids(value: Any, trail: tuple[Any, ...] = ()) -> Iterator[tuple[str, tuple[Any, ...]]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_trail = trail + (key,)
            if key == "id" and isinstance(child, str):
                yield child, child_trail
            yield from _walk_ids(child, child_trail)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_ids(child, trail + (index,))


def _identifier_index(
    documents: Iterable[Document], root: Path
) -> tuple[dict[str, tuple[Document, tuple[Any, ...]]], list[Diagnostic]]:
    index: dict[str, tuple[Document, tuple[Any, ...]]] = {}
    diagnostics: list[Diagnostic] = []
    for document in documents:
        for identifier, trail in _walk_ids(document.data):
            if identifier in index:
                original, original_trail = index[identifier]
                diagnostics.append(
                    Diagnostic(
                        "DUPLICATE_ID",
                        _display_path(document.path, root),
                        (
                            f"{identifier!r} at {_json_path(trail)} duplicates "
                            f"{_display_path(original.path, root)}:{_json_path(original_trail)}."
                        ),
                    )
                )
            else:
                index[identifier] = (document, trail)
    return index, diagnostics


def _walk_references(
    value: Any, trail: tuple[Any, ...] = ()
) -> Iterator[tuple[str, str, tuple[Any, ...]]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_trail = trail + (key,)
            if key.endswith("_ref") and isinstance(child, str):
                yield key, child, child_trail
            elif (key.endswith("_refs") or key in REFERENCE_LIST_KEYS) and isinstance(child, list):
                for index, target in enumerate(child):
                    if isinstance(target, str):
                        yield key, target, child_trail + (index,)
            yield from _walk_references(child, child_trail)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_references(child, trail + (index,))


def _reference_diagnostics(
    documents: Iterable[Document],
    known_ids: set[str],
    root: Path,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for document in documents:
        for key, target, trail in _walk_references(document.data):
            if target not in known_ids:
                diagnostics.append(
                    Diagnostic(
                        "MISSING_REFERENCE",
                        _display_path(document.path, root),
                        f"{_json_path(trail)} ({key}) cannot resolve {target!r}.",
                    )
                )

        if document.kind == "event":
            producer = document.data.get("producer")
            if isinstance(producer, dict):
                context = producer.get("context")
                if isinstance(context, str) and context not in known_ids:
                    diagnostics.append(
                        Diagnostic(
                            "MISSING_REFERENCE",
                            _display_path(document.path, root),
                            f"$.producer.context cannot resolve {context!r}.",
                        )
                    )
    return diagnostics


def _command_diagnostics(
    documents: Iterable[Document],
    root: Path,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for document in documents:
        if document.kind != "command":
            continue

        effects = document.data.get("effects")
        state_changes: list[Any] = []
        events: list[Any] = []
        if isinstance(effects, dict):
            if isinstance(effects.get("state_changes"), list):
                state_changes = effects["state_changes"]
            if isinstance(effects.get("events"), list):
                events = effects["events"]
        if not state_changes and not events:
            diagnostics.append(
                Diagnostic(
                    "COMMAND_NO_SUCCESS_EFFECT",
                    _display_path(document.path, root),
                    "Command must define at least one successful state change or Event.",
                )
            )

        failures = document.data.get("failures")
        no_failures = document.data.get("no_failures")
        explicit_failure = isinstance(failures, list) and len(failures) > 0
        explicit_none = isinstance(no_failures, dict) and no_failures.get("declared") is True
        if not explicit_failure and not explicit_none:
            diagnostics.append(
                Diagnostic(
                    "COMMAND_FAILURES_UNDECLARED",
                    _display_path(document.path, root),
                    "Command must define failures or explicitly declare no domain failures.",
                )
            )

        command_id = document.data.get("input", {}).get("command_id")
        if not isinstance(command_id, dict) or command_id.get("required") is not True:
            diagnostics.append(
                Diagnostic(
                    "COMMAND_ID_INPUT_MISSING",
                    _display_path(document.path, root),
                    "Command must require command_id for declared idempotency.",
                )
            )
    return diagnostics


def _traceability_diagnostics(
    documents: Iterable[Document],
    root: Path,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    aggregates = [document for document in documents if document.kind == "aggregate"]
    scenarios = [document for document in documents if document.kind == "scenario"]
    commands = [document for document in documents if document.kind == "command"]
    events = [document for document in documents if document.kind == "event"]

    scenario_refs: set[str] = set()
    command_scenarios: set[str] = set()
    for scenario in scenarios:
        refs = scenario.data.get("contract_refs")
        if isinstance(refs, list):
            scenario_refs.update(ref for ref in refs if isinstance(ref, str))
        when = scenario.data.get("when")
        if isinstance(when, dict) and isinstance(when.get("command_ref"), str):
            command_scenarios.add(when["command_ref"])
        if not all(key in scenario.data for key in ("given", "when", "then")):
            diagnostics.append(
                Diagnostic(
                    "SCENARIO_STRUCTURE",
                    _display_path(scenario.path, root),
                    "Scenario must contain given, when, and then.",
                )
            )
        forbidden = scenario.data.get("then", {}).get("forbidden")
        if not isinstance(forbidden, list) or not forbidden:
            diagnostics.append(
                Diagnostic(
                    "SCENARIO_FORBIDDEN_MISSING",
                    _display_path(scenario.path, root),
                    "Scenario must assert at least one forbidden side effect.",
                )
            )

    for aggregate in aggregates:
        invariants = aggregate.data.get("invariants")
        if not isinstance(invariants, list):
            continue
        for invariant in invariants:
            if not isinstance(invariant, dict) or not isinstance(invariant.get("id"), str):
                continue
            invariant_id = invariant["id"]
            if invariant_id not in scenario_refs:
                diagnostics.append(
                    Diagnostic(
                        "UNCOVERED_INVARIANT",
                        _display_path(aggregate.path, root),
                        f"Invariant {invariant_id!r} is not cited by any Scenario.",
                    )
                )

    for command in commands:
        if command.identifier and command.identifier not in command_scenarios:
            diagnostics.append(
                Diagnostic(
                    "COMMAND_WITHOUT_SCENARIO",
                    _display_path(command.path, root),
                    f"Command {command.identifier!r} is not exercised by any Scenario.",
                )
            )

    commands_by_id = {
        command.identifier: command
        for command in commands
        if command.identifier is not None
    }
    contexts_by_id = {
        document.identifier: document
        for document in documents
        if document.kind == "context" and document.identifier is not None
    }

    for event in events:
        producer = event.data.get("producer")
        if not isinstance(producer, dict):
            diagnostics.append(
                Diagnostic(
                    "EVENT_WITHOUT_PRODUCER",
                    _display_path(event.path, root),
                    "Event must identify its producing Context and Command.",
                )
            )
            continue
        command_ref = producer.get("command_ref")
        context = producer.get("context")
        if not isinstance(command_ref, str) or not isinstance(context, str):
            diagnostics.append(
                Diagnostic(
                    "EVENT_WITHOUT_PRODUCER",
                    _display_path(event.path, root),
                    "Event producer must contain string context and command_ref values.",
                )
            )
            continue
        command = commands_by_id.get(command_ref)
        if command is None:
            continue
        emitted = {
            item.get("event_ref")
            for item in command.data.get("effects", {}).get("events", [])
            if isinstance(item, dict)
        }
        if event.identifier not in emitted:
            diagnostics.append(
                Diagnostic(
                    "EVENT_PRODUCER_MISMATCH",
                    _display_path(event.path, root),
                    f"Producer Command {command_ref!r} does not emit {event.identifier!r}.",
                )
            )
        if context not in contexts_by_id:
            diagnostics.append(
                Diagnostic(
                    "EVENT_PRODUCER_CONTEXT_INVALID",
                    _display_path(event.path, root),
                    f"Producer Context {context!r} is not a Context contract.",
                )
            )

    for scenario in scenarios:
        when = scenario.data.get("when")
        then = scenario.data.get("then")
        if not isinstance(when, dict) or not isinstance(then, dict):
            continue
        command_ref = when.get("command_ref")
        if not isinstance(command_ref, str):
            continue
        command = commands_by_id.get(command_ref)
        outcome = then.get("outcome")
        if command is None or not isinstance(outcome, dict):
            continue
        status = outcome.get("status")
        code = outcome.get("code")
        declared_codes: set[str] = set()
        if status == "success":
            success = command.data.get("success")
            if isinstance(success, dict) and isinstance(success.get("code"), str):
                declared_codes.add(success["code"])
        elif status == "failure":
            failures = command.data.get("failures")
            if isinstance(failures, list):
                declared_codes.update(
                    failure["code"]
                    for failure in failures
                    if isinstance(failure, dict) and isinstance(failure.get("code"), str)
                )
        if isinstance(code, str) and code not in declared_codes:
            diagnostics.append(
                Diagnostic(
                    "SCENARIO_OUTCOME_UNDECLARED",
                    _display_path(scenario.path, root),
                    f"Outcome {status!r}/{code!r} is not declared by {command_ref!r}.",
                )
            )

    return diagnostics


def _prohibited_term_diagnostics(root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for path in sorted((root / "contracts").rglob("*.yaml")):
        text = path.read_text(encoding="utf-8")
        for term in PROHIBITED_CONTRACT_TERMS:
            pattern = re.compile(
                rf"(?<![A-Za-z0-9_]){re.escape(term)}(?![A-Za-z0-9_])",
                flags=re.IGNORECASE,
            )
            if pattern.search(text):
                diagnostics.append(
                    Diagnostic(
                        "PROHIBITED_TERM",
                        _display_path(path, root),
                        f"Business contract contains prohibited technology term {term!r}.",
                    )
                )
    return diagnostics


def _manifest_diagnostics(
    documents: Iterable[Document],
    root: Path,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    manifests = [document for document in documents if document.kind == "implementation-manifest"]
    contract_versions = {
        document.identifier: document.data.get("version")
        for document in documents
        if document.category == "contract"
        and document.identifier is not None
        and isinstance(document.data.get("version"), str)
    }

    revision_sets: dict[str, tuple[tuple[str, str], ...]] = {}
    for manifest in manifests:
        revisions = manifest.data.get("contract_revisions")
        normalized: list[tuple[str, str]] = []
        seen: set[str] = set()
        if isinstance(revisions, list):
            for revision in revisions:
                if not isinstance(revision, dict):
                    continue
                ref = revision.get("contract_ref")
                version = revision.get("version")
                if not isinstance(ref, str) or not isinstance(version, str):
                    continue
                if ref in seen:
                    diagnostics.append(
                        Diagnostic(
                            "DUPLICATE_MANIFEST_REF",
                            _display_path(manifest.path, root),
                            f"Manifest repeats contract_ref {ref!r}.",
                        )
                    )
                seen.add(ref)
                normalized.append((ref, version))
                actual_version = contract_versions.get(ref)
                if actual_version is None:
                    diagnostics.append(
                        Diagnostic(
                            "MANIFEST_TARGET_NOT_CONTRACT",
                            _display_path(manifest.path, root),
                            f"Manifest target {ref!r} is not a top-level business contract.",
                        )
                    )
                elif actual_version != version:
                    diagnostics.append(
                        Diagnostic(
                            "MANIFEST_VERSION_MISMATCH",
                            _display_path(manifest.path, root),
                            (
                                f"Manifest pins {ref!r} at {version!r}, "
                                f"but the repository contains {actual_version!r}."
                            ),
                        )
                    )
        missing = sorted(set(contract_versions) - seen)
        if missing:
            diagnostics.append(
                Diagnostic(
                    "MANIFEST_INCOMPLETE_CONTRACT_SET",
                    _display_path(manifest.path, root),
                    "Manifest does not pin " + ", ".join(repr(ref) for ref in missing) + ".",
                )
            )

        key = manifest.identifier or str(manifest.path)
        revision_sets[key] = tuple(sorted(normalized))

    if len(revision_sets) > 1:
        distinct = set(revision_sets.values())
        if len(distinct) != 1:
            for manifest in manifests:
                diagnostics.append(
                    Diagnostic(
                        "MANIFEST_CONTRACT_SET_MISMATCH",
                        _display_path(manifest.path, root),
                        "Implementation manifests do not pin the same contract revisions.",
                    )
                )

    return diagnostics


def lint_repository(root: str | Path) -> list[Diagnostic]:
    repository_root = Path(root).resolve()
    schemas, diagnostics = _load_schemas(repository_root)
    documents, document_diagnostics = _discover_documents(repository_root)
    diagnostics.extend(document_diagnostics)
    diagnostics.extend(_schema_diagnostics(documents, schemas, repository_root))

    identifier_index, id_diagnostics = _identifier_index(documents, repository_root)
    diagnostics.extend(id_diagnostics)
    diagnostics.extend(
        _reference_diagnostics(documents, set(identifier_index), repository_root)
    )
    diagnostics.extend(_command_diagnostics(documents, repository_root))
    diagnostics.extend(_traceability_diagnostics(documents, repository_root))
    diagnostics.extend(_prohibited_term_diagnostics(repository_root))
    diagnostics.extend(_manifest_diagnostics(documents, repository_root))

    return sorted(
        diagnostics,
        key=lambda item: (str(item.path), item.code, item.message),
    )


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "repository",
        nargs="?",
        default=".",
        help="Canon Spec repository root (default: current directory)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    diagnostics = lint_repository(args.repository)
    if diagnostics:
        for diagnostic in diagnostics:
            print(f"{diagnostic.path}: {diagnostic.code}: {diagnostic.message}")
        print(f"Contract lint failed with {len(diagnostics)} diagnostic(s).")
        return 1
    print("Contract lint passed: schemas, contracts, references, coverage, producers, and manifests are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

