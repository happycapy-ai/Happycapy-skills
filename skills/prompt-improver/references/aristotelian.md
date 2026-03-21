# Aristotelian First Principles Mode

A prompt design methodology that instructs the **receiving LLM** to reason from first principles when executing a task. Rooted in Aristotle's *Posterior Analytics*. Activated only when the user explicitly requests "Aristotelian reasoning" or "first principles mode".

## Core Concept

The prompt-improver does NOT perform Aristotelian reasoning itself. Instead, it produces an **improved prompt that tells the LLM to use Aristotelian reasoning on the task**. The output prompt instructs the AI to:

1. Identify the atomic, irreducible truths relevant to the task
2. Interrogate those truths to confirm they are genuinely foundational
3. Build its entire solution deductively from those verified foundations
4. Trace every decision back to a specific axiom

## How the Prompt-Improver Prepares the Prompt

Before generating the Aristotelian prompt, the improver gathers context to bake into it:

**Context to embed in the prompt (not for the improver to investigate itself):**
- Known system capabilities (e.g., root/sudo access, OS, installed tools)
- AI model being used and its strengths (e.g., Claude Opus 4.6, large context window)
- Available tools and integrations the LLM can call
- Domain constraints from the user (language, framework, project conventions)

This context becomes the **given truths** the LLM will use as its starting axioms.

## The Aristotelian Prompt Structure

The improved prompt instructs the LLM to follow this reasoning methodology:

### Part 1: Reasoning Directive

Tell the LLM to work from first principles:
```
Before taking any action, reason from first principles. Identify the fundamental,
irreducible truths relevant to this task. Do not assume anything that cannot be
traced back to a verified ground truth. Build your approach step by step, where
each step is justified by either a foundational truth or a prior verified step.
```

### Part 2: Given Axioms (Baked-In Context)

Provide the known truths so the LLM does not have to guess or hallucinate them:
```
The following are established ground truths for this task:
- [System capability: e.g., "You have root access on a Linux environment"]
- [Model capability: e.g., "You can read, write, and execute files via Bash"]
- [Domain truth: e.g., "This is a Python 3.11 project using FastAPI"]
- [Constraint: e.g., "No external API calls are allowed"]
```

### Part 3: Axiom Discovery Instruction

Tell the LLM to find additional axioms specific to the task before acting:
```
Before proceeding, identify the atomic truths of this specific task:
1. What must be true for this task to succeed? (necessary conditions)
2. What, if false, would make the task impossible? (critical dependencies)
3. Are any of these derived from something more basic? If so, go deeper.
4. State each axiom in one sentence. Discard anything that is not strictly necessary.
```

### Part 4: Axiom Interrogation Instruction

Tell the LLM to verify its own axioms before building on them:
```
For each axiom you identified, ask yourself:
- "Why is this true?" -- if the answer is "because of X", then X is more fundamental
- "If this were false, what breaks?" -- if nothing breaks, discard it
- "Does this contradict any other axiom?" -- resolve before continuing
Only proceed once your axioms are non-contradictory, independent, and necessary.
```

### Part 5: Deductive Task Execution

Tell the LLM to execute the task as a logical proof:
```
Now execute the task. For each action you take:
- State which axiom or prior step justifies it
- If you cannot justify an action from your axioms, stop and identify what is missing
- After completion, verify your result against your axioms -- does it satisfy them all?
```

## Verification Tests for Axioms

The improved prompt should instruct the LLM to apply these tests (from Aristotle's framework):

| Test | The LLM asks itself | Action if fails |
|------|---------------------|-----------------|
| **Primacy** | "Can this be derived from something more basic?" | Decompose further |
| **Independence** | "Does this depend on another axiom?" | Mark the dependency chain |
| **Necessity** | "If I remove this, does the task become impossible?" | Keep only if yes |
| **Consistency** | "Does this contradict anything else I hold true?" | Resolve the contradiction |
| **Non-Contradiction** | "Am I assuming X and not-X simultaneously?" | Eliminate one |

## Key Aristotelian Principles to Embed

These principles should be woven into the improved prompt's reasoning instructions:

1. **Non-Contradiction**: The LLM must not hold two contradictory premises simultaneously
2. **Excluded Middle**: Each claim about the task is either true or false -- no "maybe" allowed during axiom establishment
3. **Sufficient Reason**: Every action in the solution must trace to a stated axiom
4. **Causal Priority**: The LLM should explain *why* it does something (the axiom), not just *what* it does

## Why This Works for LLMs

Embedding first-principles reasoning instructions in prompts works because:

- **Reduces hallucination**: The LLM is explicitly told to only build on stated truths, not invent premises
- **Improves chain-of-thought**: Each deductive step is a natural reasoning unit the attention mechanism can track
- **Enables self-correction**: If the LLM's output contradicts a stated axiom, it has a reference point to catch the error
- **Structures attention**: The hierarchical axiom-then-deduction structure helps the model focus on relevant context per step
- **Prevents drift**: Without first principles, LLMs tend to drift toward "most likely" patterns from training; axioms anchor the reasoning to the specific task

## When to Use This Mode

- Tasks where precision and correctness matter more than speed
- Complex multi-step work where a wrong foundation cascades into failure
- When the user wants the LLM to show its reasoning and justify every decision
- Infrastructure, deployment, security, or data integrity tasks
- When the user explicitly says "Aristotelian", "first principles", or "proof-based"

## When NOT to Use This Mode

- Simple prompt improvements (use the standard framework)
- Creative/open-ended tasks where rigid logical structure over-constrains
- Quick mode requests
