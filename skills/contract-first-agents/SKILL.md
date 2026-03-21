---
name: contract-first-agents
description: "Contract-First Map-Reduce coordination protocol for native TeamCreate multi-agent teams. Wraps TeamCreate, Task (teammates), SendMessage with an upfront shared contract phase that eliminates 75% of integration errors. Based on 400+ experiment research proving 52.5% quality improvement over naive coordination."
version: 1.0.0
author: HappyCapy Research
triggers:
  - contract first agents
  - contract first team
  - coordinated agents
  - multi agent contract
  - team with contract
  - optimal team coordination
  - contract-first
---

# Contract-First Map-Reduce Agent Coordination

> Wraps native TeamCreate/Task/SendMessage with a proven 4-phase protocol
> that eliminates 75% of integration errors in multi-agent tasks.

## Research Basis

Based on 400+ controlled experiments comparing 7 coordination strategies:
- **Naive multi-agent**: 0.571 composite quality score
- **Contract-First Map-Reduce**: 0.871 composite quality score (+52.5%)
- The contract alone accounts for the ENTIRE quality improvement
- Validated across 2-64 agent configurations

## The Protocol

### Phase 1: CONTRACT GENERATION (Team Lead, ~5% of time)

Before spawning ANY worker agent, the team lead MUST create a Contract Document.

**The Contract Document must contain:**

```markdown
# === SHARED CONTRACT: [Project Name] ===

## 1. MODULE MANIFEST
For EVERY module/section an agent will produce:
- Exact filename
- Purpose (1 sentence)
- ALL exported names (exact spelling, exact case)

## 2. INTERFACE DEFINITIONS
For EVERY cross-module reference:
- Exact function/class name
- Exact parameter names and types
- Exact return type
- Source module -> consuming module(s)

## 3. SHARED TYPES
For EVERY data structure shared across modules:
- Exact field names and types
- Validation rules
- Serialization format

## 4. STYLE GUIDE
- Naming: snake_case for functions/variables, PascalCase for classes
- Indentation: [N] spaces
- Docstrings: [Google/NumPy/Sphinx] style on all public functions/classes
- Error handling: exact exception types
- Import convention: "from module import Name"
- Language-specific conventions

## 5. DEPENDENCY MAP
- Which modules import from which
- Execution order constraints (if any)
- Shared state / global configuration

## 6. SECTION BOUNDARIES
For EACH section assigned to an agent:
- What it must produce (exact deliverables)
- What it imports from other sections (exact names)
- What it exports for other sections (exact names)
- How it connects to adjacent sections (transitions, API calls, imports)
```

**Contract Quality Checklist:**
- [ ] Every exported name is spelled out exactly
- [ ] Every cross-module import has a matching export
- [ ] Style guide is specific (not "be consistent" but "use snake_case")
- [ ] Shared types have exact field names and types
- [ ] No ambiguity - an agent reading only the contract can produce correct code

### Phase 2: PARALLEL EXECUTION (Worker Agents)

Spawn worker agents using the Task tool with `team_name` parameter. Each worker's prompt MUST include:

```
[FULL CONTRACT TEXT - every worker gets the COMPLETE contract]

---

YOUR ASSIGNMENT: [Specific section/module]

You are Agent [N] of [Total]. You are producing [section name].

CRITICAL INSTRUCTIONS:
1. Follow the contract EXACTLY. Do not deviate from specified names, types, or conventions.
2. Your section will be merged with outputs from other agents working in parallel.
3. Use ONLY the exported names specified in the contract when referencing other modules.
4. Do NOT rename, reorganize, or "improve" the interface - follow the contract.
5. Write your output to: [exact file path]
```

**Spawn all workers in parallel** using a single message with multiple Task tool calls.

### Phase 3: AUTOMATED VALIDATION (Team Lead or Script)

After all workers complete, the team lead validates the merged output:

```python
# Validation checks (in priority order):
1. Syntax validity    - Can the output be parsed? (ast.parse, eslint --no-fix, etc.)
2. Import resolution  - Do all imports match actual exports?
3. Name consistency   - Is the naming convention uniform throughout?
4. Completeness       - Are all contracted exports present?
5. Style consistency  - Indent, docstrings, error handling patterns
6. Cross-references   - Do function calls use correct signatures?
```

Save validation results. If all pass -> done. If issues found -> Phase 4.

### Phase 4: TARGETED FIX (Fixer Agent, only if needed)

Spawn ONE fixer agent that receives:
- The merged output
- The specific validation errors (exact line numbers, exact issues)
- The original contract

**The fixer ONLY fixes the specific issues found. It does NOT regenerate or restructure.**

## Implementation with Native Tools

```python
# Step 1: Create team
TeamCreate(team_name="my-project", description="Building X with contract-first protocol")

# Step 2: Team lead generates the contract
# Save contract to a shared file: ~/.claude/teams/{team-name}/contract.md

# Step 3: Spawn workers with full contract in their prompts
Task(
    name="worker-auth",
    team_name="my-project",
    subagent_type="general-purpose",
    prompt=f"""
    {FULL_CONTRACT_TEXT}

    YOUR ASSIGNMENT: auth module
    Write to: /workspace/project/auth.py
    Follow the contract exactly.
    """
)
# ... spawn all workers in parallel

# Step 4: After workers complete, validate
# Team lead reads all output files and runs validation checks

# Step 5: If issues found, spawn fixer
Task(
    name="fixer",
    team_name="my-project",
    subagent_type="general-purpose",
    prompt=f"""
    Fix these specific issues in the merged output:
    {VALIDATION_ERRORS}

    Original contract: {CONTRACT}
    Do NOT restructure. Only fix the specific issues listed.
    """
)

# Step 6: Cleanup
SendMessage(type="shutdown_request", recipient="worker-auth")
# ... shutdown all workers
TeamDelete()
```

## When to Use This Protocol

**ALWAYS use for:**
- Any task requiring 3+ agents
- Tasks producing code that must interoperate
- Large document generation (multiple sections that reference each other)
- Any task where agents produce outputs that will be merged

**SKIP the contract for:**
- Completely independent tasks (no cross-references)
- Single-agent tasks
- Research/exploration tasks (no integration needed)

## Key Principles

1. **The contract IS the coordination** - review phases add <5% value if contract is good
2. **Every agent gets the FULL contract** - not just their section's part
3. **Specific beats general** - "use snake_case" beats "be consistent"
4. **Parallel beats sequential** - contract enables parallel work; pipelines sacrifice speed for marginal gain
5. **Targeted fixes beat regeneration** - fix specific issues, don't redo entire sections
6. **10+ agents need validation** - probability of ANY error increases with agent count
