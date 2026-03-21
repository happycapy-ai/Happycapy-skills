# Before/After Examples

## Example 1: Vague to Specific

**Before:**
> help me write some code

**After (given: Python, validation task):**
> Write a Python function that validates email addresses. Requirements:
> - Accept a string input, return boolean
> - Check for valid format (user@domain.tld)
> - Handle edge cases (empty string, missing @, etc.)
> - Include docstring with examples
> - No external dependencies

## Example 2: Adding Structure

**Before:**
> explain how authentication works in my app

**After (given: new developer audience, walkthrough depth):**
> Explain the authentication flow in this codebase. Include:
> 1. Entry points (login endpoints)
> 2. Token generation and validation logic
> 3. Session management approach
> 4. Key files involved with line references
> Format as a numbered walkthrough a new developer could follow.

## Example 3: Constraining Scope

**Before:**
> fix the bugs

**After (given: type errors, single file):**
> Fix the TypeScript type errors in src/components/UserForm.tsx. Constraints:
> - Only address type errors (no refactoring)
> - Preserve existing behavior
> - Use existing type definitions where available
> - Run `npm run typecheck` to verify fixes

## Example 4: Research Task

**Before:**
> tell me about kubernetes

**After (given: practical focus, intermediate audience):**
> Explain Kubernetes core concepts for a developer who knows Docker but is new to orchestration. Cover:
> 1. Pods, Services, Deployments - what each does
> 2. How traffic routing works
> 3. Basic kubectl commands for debugging
> Keep explanations practical with examples, not theoretical.

## Example 5: Creative Task

**Before:**
> write a blog post about AI

**After (given: technical audience, engaging tone):**
> Write a 800-word blog post about practical AI applications in software development. Requirements:
> - Target audience: developers exploring AI tools
> - Tone: conversational but technically accurate
> - Include 3 concrete examples with code snippets
> - Avoid hype, focus on real productivity gains
> - End with actionable next steps

## Example 6: Aristotelian Mode (First Principles / Proof-Based)

**Before:**
> deploy my app to production

**After (Aristotelian mode, given: Claude Code agent with root access, Node.js project):**

> **Reasoning Directive:**
> Before taking any action, reason from first principles. Identify the fundamental,
> irreducible truths relevant to this deployment. Do not assume anything that cannot
> be traced to a verified ground truth. Build your approach step by step, where each
> step is justified by a foundational truth or a prior verified step.
>
> **Given Axioms (established context):**
> - You have root access on a Linux environment with Bash
> - You are Claude Opus 4.6 with Read, Write, Edit, and Bash tools available
> - This is a Next.js project (verify via package.json before assuming version)
> - The user's goal is a running production server returning HTTP 200
>
> **Task:**
> Deploy this application to production.
>
> **Method:**
> 1. Before acting, identify the atomic truths of this deployment:
>    - What must exist for the build to succeed? (dependencies, env vars, config)
>    - What must be true for the server to start? (port available, build output exists)
>    - For each truth: ask "is this derived from something more basic?" -- if yes, go deeper
>    - Discard anything not strictly necessary for deployment
> 2. Interrogate your axioms: do any contradict each other? Are any redundant?
> 3. Execute each deployment step, stating which axiom justifies it
> 4. If any step fails, trace back to identify which axiom was violated
>
> **Verification:**
> After deployment, check your result against every axiom. Does the running server
> satisfy all the ground truths you established? If not, identify the gap.
