# Anti-Patterns to Fix

Common prompt issues and their fixes:

| Problem | Fix |
|---------|-----|
| "Make it better" | Define specific quality criteria |
| "Do everything" | Prioritize and scope explicitly |
| "You know what I mean" | State assumptions explicitly |
| "Be creative" | Provide constraints that enable creativity |
| "ASAP" | Remove time pressure (doesn't help AI) |
| Emotional language | Replace with objective requirements |
| Multiple unrelated asks | Split into separate focused prompts |
| Wall of text | Structure with headers and bullets |
| No success criteria | Define what "done" looks like |
| Assumed context | State all necessary background |

## Red Flags to Watch For

**Vagueness indicators:**
- "some", "a few", "maybe"
- "good", "better", "nice"
- "whatever works"
- "you decide"

**Scope creep indicators:**
- "also", "and while you're at it"
- "everything related to"
- "all the things"

**Missing specificity:**
- No output format mentioned
- No constraints defined
- No success criteria
- No audience specified

## Transformation Patterns

**Vague → Specific:**
- "help me" → "write/explain/fix/analyze [specific thing]"
- "improve this" → "optimize for [metric], by [method]"
- "make it work" → "ensure [specific behavior] when [condition]"

**Implicit → Explicit:**
- Unstated format → "Output as [format]"
- Assumed audience → "For [audience type]"
- Unclear scope → "Only include/exclude [boundaries]"
