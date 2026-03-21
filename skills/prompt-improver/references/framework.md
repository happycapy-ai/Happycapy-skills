# Prompt Improvement Framework

Six principles for transforming prompts:

## 1. Clarity and Specificity

- Replace vague language with concrete terms
- Define exact output format expected
- Specify constraints, scope, boundaries
- Include examples when helpful

## 2. Task Decomposition

- Break complex requests into discrete steps
- Order steps logically with dependencies
- Identify parallel vs sequential work

## 3. Context Optimization

- Include only relevant context (remove noise)
- Front-load most important information
- Specify role/perspective to adopt
- Necessary background without over-explaining

## 4. Output Specification

- Define format explicitly (code, prose, JSON, markdown)
- Specify length/depth expectations
- Include quality criteria or acceptance standards
- Request specific structure (headers, sections, bullets)

## 5. Constraint Definition

- State what to avoid explicitly
- Define scope boundaries (what NOT to include)
- Specify technical constraints (language, framework, style)
- Set tone and audience expectations

## 6. Iteration Hooks

- Build in checkpoints for clarification
- Request reasoning/explanation when needed
- Allow for follow-up refinement

## Platform-Specific Tips

### For Claude Code / CLI
- Specify programming language and version
- Reference existing patterns in the codebase
- Include test expectations
- Define error handling requirements

### For ChatGPT / Claude.ai
- Specify depth (overview vs deep-dive)
- Request citations/sources if needed
- Define audience expertise level
- Set recency boundaries for information

### For API / Automation
- Define structured output format (JSON schema)
- Specify error handling behavior
- Include validation requirements
- Consider token limits

### For Image Generation
- Describe style, mood, lighting
- Specify composition and framing
- Include what to avoid (negative prompting)
- Reference specific artists/styles if needed

## 7. Aristotelian First Principles (Optional)

When the user requests "Aristotelian", "first principles", or "proof-based" mode, the improved prompt **instructs the receiving LLM to reason from first principles** during task execution. See references/aristotelian.md for the full methodology.

**Core idea:** Instead of just improving surface-level clarity, produce a prompt that tells the LLM to decompose the task into atomic truths, verify them, and build its entire solution deductively from those truths. The prompt-improver bakes in known context (system capabilities, tools, domain constraints) as given axioms so the LLM does not hallucinate them.

**What the improved prompt contains:**
1. **Reasoning directive** - Explicit instruction telling the LLM to reason from first principles
2. **Given axioms** - Known truths (root access, AI model, tools, domain) baked in as context
3. **Axiom discovery instructions** - Tell the LLM to find task-specific atomic truths before acting
4. **Interrogation instructions** - Tell the LLM to verify its axioms (primacy, independence, necessity, consistency)
5. **Deductive execution** - Tell the LLM to justify every action by tracing it to an axiom
6. **Verification** - Tell the LLM to check its result against its axioms when done

**Why this works for LLMs:**
- Explicit given axioms prevent hallucinated assumptions about the environment
- The reasoning directive anchors the LLM to deductive logic instead of pattern-matching
- Self-interrogation of axioms catches contradictions before they cascade
- Traceability (action -> axiom) makes errors localizable and debuggable
