# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

This repo uses `docs/decisions/` instead of `docs/adr/` as its decision-record
convention — already established before these skills were installed. Read
`docs/decisions/` wherever the upstream skill instructions say `docs/adr/`.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root, if it exists.
- **`docs/decisions/`**: cross-domain / architecture decisions that apply to the whole project. Read entries here before working in any area.
- **Tier-specific decisions**, if the area you're working in falls under one of these tiers:
  - `docs/core/decisions/` — core regulation layer (rules shared by every project type)
  - `docs/platform/decisions/` — platform (web/backend feature) specific decisions
  - `docs/game/decisions/` — game (slot game) specific decisions

If any of these don't exist yet, **proceed silently**. Don't flag their absence; don't suggest creating them upfront.

## File structure (actual, as of this setup)

```
/
├── CLAUDE.md
├── docs/
│   ├── decisions/           ← cross-domain / architecture decisions
│   ├── core/
│   │   ├── SOP.md
│   │   └── decisions/       ← core-tier decisions
│   ├── platform/
│   │   ├── examples/
│   │   └── decisions/       ← platform-tier decisions
│   ├── game/
│   │   ├── examples/
│   │   └── decisions/       ← game-tier decisions
│   ├── agents/               ← this skill's output (issue-tracker.md, triage-labels.md, domain.md)
│   └── SOP-分享版.html       ← merged single-file share version
```

This is effectively a multi-context layout (root decisions + one decisions/ per tier), but named `decisions/` rather than `adr/`, and tiers rather than `src/<context>/`.

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md` if one exists. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal: either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag decision-record conflicts

If your output contradicts an existing decision record, surface it explicitly rather than silently overriding:

> _Contradicts docs/decisions/0002-core-plus-extension-architecture.md, but worth reopening because…_
