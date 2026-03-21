# Contract Template

Copy and fill in this template before spawning any worker agents.

---

# === SHARED CONTRACT: [Project Name] ===

> Generated: [Date]
> Agents: [Number]
> Task: [Brief description]

## 1. Module Manifest

| Module | File(s) | Responsibility | Agent |
|---|---|---|---|
| [module-name] | [filename.ext] | [1-sentence purpose] | Agent-[N] |
| [module-name] | [filename.ext] | [1-sentence purpose] | Agent-[N] |
| [module-name] | [filename.ext] | [1-sentence purpose] | Agent-[N] |

## 2. Interface Definitions

### [module-name].[ext]

```
[Exact function/class signatures with parameter names, types, and return types]
[Include docstring format]
```

### [module-name].[ext]

```
[Exact function/class signatures]
```

## 3. Shared Types

```
[All data structures shared across modules]
[Exact field names and types]
[Constants and enums]
```

## 4. Style Guide

**Naming:**
- Functions: [convention, e.g., snake_case]
- Classes: [convention, e.g., PascalCase]
- Constants: [convention, e.g., UPPER_SNAKE_CASE]
- Private: [convention, e.g., prefix with _]

**Formatting:**
- Indentation: [N] spaces
- Max line length: [N] characters
- Blank lines: [rules]

**Documentation:**
- Docstring style: [Google/NumPy/Sphinx/JSDoc]
- Required on: [all public functions/classes]

**Error Handling:**
- Exception types: [list specific types]
- Logging: [convention]

**Imports:**
- Order: [stdlib, third-party, local]
- Style: [from X import Y / import X]

## 5. Dependency Map

```
[module-a] (no dependencies)
    |
[module-b] (depends on: module-a)
    |
[module-c] (depends on: module-a, module-b)
```

**Rules:**
- [module-a] NEVER imports from other local modules
- [module-b] MAY import from [module-a] ONLY
- NO circular imports

## 6. Section Boundaries

**Agent-1 ([module-name]):**
- OWNS: [list of files]
- MUST IMPLEMENT: [list of functions/classes]
- MUST USE: [types from shared types]
- MUST NOT: [constraints]
- OUTPUT: [deliverable format]

**Agent-2 ([module-name]):**
- OWNS: [list of files]
- MUST IMPLEMENT: [list of functions/classes]
- IMPORTS FROM Agent-1: [exact names]
- MUST NOT: [constraints]
- OUTPUT: [deliverable format]

---

## Quality Checklist

Before distributing this contract, verify:

- [ ] Every exported name is spelled out exactly
- [ ] Every cross-module import has a matching export
- [ ] Style guide uses specific rules, not vague principles
- [ ] Shared types have exact field names and types
- [ ] No ambiguity -- an agent reading only this contract can produce correct code
- [ ] Dependency map has no circular references
- [ ] Section boundaries are clear and non-overlapping
