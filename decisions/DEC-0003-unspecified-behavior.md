---
schema_version: "1.0"
kind: decision
id: DEC-0003
version: "1.0.0"
status: draft
title: Unspecified behavior must not be inferred
problem: An AI Coding Agent or implementer can turn an unstated assumption into persistent business behavior.
background: Technology defaults and plausible domain conventions are not evidence of a reviewed business rule.
decision: Adopt constitution/ambiguity-policy.md as the sole normative handling policy for undefined or conflicting behavior.
rejected_options:
  - Allow each implementation to choose a reasonable default.
  - Record assumptions only in implementation comments.
consequences:
  - Some draft implementation tasks remain blocked until a human answers their clarification requests.
  - Cross-language implementations cannot drift through different implicit defaults.
revisit_when:
  - A governed extension mechanism can express implementation discretion without changing observable business behavior.
contract_refs: []
---

# Unspecified behavior must not be inferred

The operative policy is [the Ambiguity Policy](../constitution/ambiguity-policy.md). This decision record preserves why guessing is not an acceptable delivery shortcut.
