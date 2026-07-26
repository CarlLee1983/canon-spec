# Ambiguity Policy

## Normative

An author, implementer, reviewer, or AI Coding Agent that encounters undefined, contradictory, or multiply interpretable behavior MUST:

1. stop relying on the uncertain behavior;
2. create or cite a Specification Clarification Request under `clarifications/`;
3. list the affected contract and scenario identifiers;
4. state the competing interpretations without selecting one; and
5. identify whether the question blocks promotion to `candidate` or only a later scope expansion.

Undefined behavior MUST NOT be encoded as a default value, implicit branch, undocumented error, silent fallback, or example-only rule. A draft contract MAY remain lint-valid while carrying an explicit clarification, but an unresolved blocking clarification MUST prevent promotion to `candidate`.

## Explanatory

Clarification requests preserve uncertainty as visible work instead of turning an implementer's guess into accidental policy.

