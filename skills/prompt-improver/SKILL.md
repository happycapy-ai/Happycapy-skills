---
name: prompt-improver
description: Optimize prompts for better AI responses. Use when user asks to improve a prompt, refine a prompt, make a prompt better, optimize prompting, review their prompt, or says "/improve-prompt". Transforms vague requests into clear, specific, actionable prompts.
---

# Prompt Improver

Transform vague prompts into clear, specific, actionable ones for better AI responses.

## Workflow

1. **Gather context** - Use AskUserQuestion to clarify:
   - Target platform (Claude Code, ChatGPT, API, image gen)
   - Priority (accuracy, speed, depth, creativity)
   - Missing context (technical stack, constraints, examples)

2. **Analyze** - Identify what's unclear, missing, or ambiguous

3. **Improve** - Apply the framework (see references/framework.md)

4. **Present** - Show improved prompt with key changes explained

5. **Refine** - Ask if user wants adjustments

## AskUserQuestion Templates

**Initial clarification:**
```
questions:
  - header: "Platform"
    question: "What will you use this prompt for?"
    options:
      - label: "Claude Code"
        description: "Coding, file ops, terminal"
      - label: "ChatGPT/Claude.ai"
        description: "General conversation"
      - label: "API/Automation"
        description: "Programmatic use"
      - label: "Image gen"
        description: "DALL-E, Midjourney, etc."
  - header: "Priority"
    question: "What matters most?"
    options:
      - label: "Accuracy"
        description: "Correctness is critical"
      - label: "Speed"
        description: "Quick, concise"
      - label: "Depth"
        description: "Comprehensive"
      - label: "Creativity"
        description: "Novel approaches"
```

**Post-improvement:**
```
header: "Refine"
question: "Adjust the improved prompt?"
options:
  - label: "Looks good"
    description: "Use as-is"
  - label: "More specific"
    description: "Add constraints"
  - label: "More concise"
    description: "Shorten"
  - label: "Different focus"
    description: "Change emphasis"
```

## Output Format

```markdown
## Analysis
[Brief issues/opportunities]

## Improved Prompt
[Ready-to-use prompt]

## Key Changes
- [Change]: [Why]
```

## Quick Mode

If user says "quick improve", skip questions and make reasonable assumptions. Note assumptions made.

## Aristotelian Mode (First Principles)

Activated when user says "Aristotelian", "first principles", or "proof-based". Instead of the standard framework, produce a prompt that **instructs the receiving LLM to reason from first principles** when executing the task.

The prompt-improver does NOT do the Aristotelian reasoning itself. It crafts a prompt that tells the LLM to:

1. **Gather context from user** - Ask what system capabilities, tools, and constraints exist. Bake known context (root access, AI model, available tools, domain) directly into the prompt as given axioms.

2. **Embed the reasoning directive** - The improved prompt tells the LLM to:
   - Identify the atomic, irreducible truths of the task before acting
   - Interrogate each truth: "Can this be decomposed further? If removed, does the task break? Does it contradict anything?"
   - Discard anything that is not strictly necessary
   - Build the solution deductively, where every action traces to a stated axiom
   - Verify the result against the axioms at the end

3. **Structure the output prompt** with these sections:
   ```
   REASONING DIRECTIVE: [Instruct the LLM to use first-principles reasoning]
   GIVEN AXIOMS: [Known truths about system, capabilities, domain -- baked in]
   TASK: [What to accomplish]
   METHOD: [Tell LLM to discover task-specific axioms, interrogate them, then build deductively]
   VERIFICATION: [Tell LLM to check its result against its axioms]
   ```

**Output format for Aristotelian mode:**
```markdown
## Analysis
[What context was embedded and why]

## Improved Prompt (Aristotelian)
[The complete prompt with reasoning directive, given axioms, task, method, and verification]

## What This Prompt Does
- Tells the LLM to [specific reasoning behavior]
- Bakes in [specific context] so the LLM does not hallucinate it
```

See references/aristotelian.md for the full methodology and prompt structure.

## References

- **Framework details**: See references/framework.md for the 6-principle improvement framework
- **Aristotelian mode**: See references/aristotelian.md for the proof-based first principles methodology
- **Examples**: See references/examples.md for before/after transformations
- **Anti-patterns**: See references/anti-patterns.md for common issues to fix
