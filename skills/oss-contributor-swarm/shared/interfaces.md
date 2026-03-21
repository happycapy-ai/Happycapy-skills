# Shared Interfaces

This document defines the data contracts between agents in the OSS Contributor Swarm.

## Agent Communication Flow

```
Agent 1 (Scout)     → current-issue.json      → Agent 2 (Analyst)
Agent 2 (Analyst)   → issue-analysis.json     → Agent 3 (Explorer)
Agent 3 (Explorer)  → codebase-map.json       → Agents 4, 5, 6
Agent 4 (Coder)     → code-changes.json       → Agent 7 (PR)
Agent 5 (Tester)    → test-changes.json       → Agent 7 (PR)
Agent 6 (Docs)      → docs-changes.json       → Agent 7 (PR)
Agent 7 (PR)        → pr-created.json         → Agent 8 (Reviews)
Agent 8 (Reviews)   → review-activity.json    → Orchestrator
```

---

## Interface Definitions

### 1. current-issue.json (Agent 1 → Agent 2)

```typescript
interface CurrentIssue {
  agent: "agent-1-scout";
  timestamp: string; // ISO 8601
  status: "completed" | "failed";
  selected_issue: {
    url: string;
    title: string;
    body: string;
    labels: string[];
    repository: {
      owner: string;
      name: string;
      url: string;
      language: string;
      stars: number;
      license: string;
    };
    comments_count: number;
    created_at: string;
    difficulty_estimate: "trivial" | "easy" | "medium";
    type: "documentation" | "bug-fix" | "feature" | "test" | "refactor";
  };
  alternatives: Array<{
    url: string;
    title: string;
    reason_not_selected: string;
  }>;
  search_stats: {
    total_searched: number;
    filtered_out: number;
    candidates_found: number;
  };
}
```

### 2. issue-analysis.json (Agent 2 → Agent 3)

```typescript
interface IssueAnalysis {
  agent: "agent-2-analyst";
  timestamp: string;
  status: "completed" | "failed";
  issue_url: string;
  analysis: {
    summary: string;
    type: "documentation" | "bug-fix" | "feature" | "test" | "refactor";
    complexity: "trivial" | "easy" | "medium";
    estimated_loc_change: number;
    breaking_change: boolean;
    requirements: string[];
    files_to_modify: Array<{
      path: string;
      change_type: "create" | "edit" | "delete";
      description: string;
    }>;
    tests_required: boolean;
    docs_update_required: boolean;
  };
  repository_context: {
    contributing_guidelines: string;
    pr_template_exists: boolean;
    code_style: string;
    branch_naming: string;
    commit_convention: string;
  };
  implementation_plan: {
    steps: string[];
    estimated_time: string;
    risk_level: "low" | "medium" | "high";
  };
  warnings: string[];
  blockers: string[];
}
```

### 3. codebase-map.json (Agent 3 → Agents 4, 5, 6)

```typescript
interface CodebaseMap {
  agent: "agent-3-explorer";
  timestamp: string;
  status: "completed" | "failed";
  repository: {
    owner: string;
    name: string;
    local_path: string;
    branch: string;
    default_branch: string;
  };
  structure: {
    framework: string;
    language: string;
    package_manager: string;
    monorepo: boolean;
    source_dir: string;
    test_dir: string;
    docs_dir: string;
  };
  relevant_files: {
    to_modify: Array<{
      path: string;
      purpose: string;
      line_numbers?: number[];
      content_preview?: string;
    }>;
    to_reference: Array<{
      path: string;
      purpose: string;
    }>;
    tests: string[];
    docs: string[];
  };
  code_style: {
    indent: string;
    quotes: "single" | "double";
    semicolons: boolean;
    trailing_comma: string;
    line_length: number;
    formatter: string;
    linter: string;
  };
  build_commands: {
    install: string;
    build: string;
    test: string;
    lint: string;
  };
  insights: {
    patterns_observed: string[];
    potential_gotchas: string[];
  };
}
```

### 4. code-changes.json (Agent 4 → Agent 7)

```typescript
interface CodeChanges {
  agent: "agent-4-coder";
  timestamp: string;
  status: "completed" | "failed";
  branch: string;
  changes: Array<{
    file: string;
    action: "created" | "modified" | "deleted";
    diff: string;
    lines_changed: {
      added: number;
      removed: number;
    };
    description: string;
  }>;
  validation: {
    lint_passed: boolean;
    typecheck_passed: boolean;
    build_passed: boolean;
    tests_passed: boolean;
    errors: string[];
  };
  summary: {
    total_files_changed: number;
    total_additions: number;
    total_deletions: number;
  };
  commit_ready: boolean;
  suggested_commit_message: string;
}
```

### 5. test-changes.json (Agent 5 → Agent 7)

```typescript
interface TestChanges {
  agent: "agent-5-tester";
  timestamp: string;
  status: "completed" | "failed";
  tests_required: boolean;
  reason: string;
  test_files: Array<{
    path: string;
    action: "created" | "modified";
    tests_added: Array<{
      name: string;
      type: "unit" | "integration" | "e2e";
      covers: string;
    }>;
  }>;
  validation: {
    existing_tests_pass: boolean;
    new_tests_pass: boolean;
    coverage_before: string;
    coverage_after: string;
  };
  summary: {
    tests_added: number;
    tests_modified: number;
    total_test_files: number;
  };
}
```

### 6. docs-changes.json (Agent 6 → Agent 7)

```typescript
interface DocsChanges {
  agent: "agent-6-docs";
  timestamp: string;
  status: "completed" | "failed";
  docs_required: boolean;
  reason: string;
  doc_files: Array<{
    path: string;
    action: "created" | "modified";
    sections_updated: Array<{
      heading: string;
      change: string;
    }>;
  }>;
  validation: {
    links_valid: boolean;
    examples_tested: boolean;
    spelling_checked: boolean;
  };
  summary: {
    files_updated: number;
    sections_added: number;
    sections_modified: number;
  };
}
```

### 7. pr-created.json (Agent 7 → Agent 8)

```typescript
interface PRCreated {
  agent: "agent-7-pr";
  timestamp: string;
  status: "completed" | "failed";
  pr: {
    url: string;
    number: number;
    title: string;
    branch: string;
    base: string;
    state: "open" | "draft";
    draft: boolean;
  };
  commits: Array<{
    sha: string;
    message: string;
    files_changed: number;
  }>;
  issue_linked: {
    number: number;
    url: string;
    auto_close: boolean;
  };
  ci_status: {
    checks_started: boolean;
    initial_status: "pending" | "success" | "failure";
  };
  summary: {
    files_in_pr: number;
    additions: number;
    deletions: number;
    commits: number;
  };
}
```

### 8. review-activity.json (Agent 8 → Orchestrator)

```typescript
interface ReviewActivity {
  agent: "agent-8-reviews";
  timestamp: string;
  status: "monitoring" | "completed" | "failed";
  pr: {
    url: string;
    number: number;
    state: "open" | "merged" | "closed";
  };
  activity: Array<{
    timestamp: string;
    type: "review_received" | "changes_made" | "comment_replied" | "ci_status_change";
    details: object;
  }>;
  ci_history: Array<{
    timestamp: string;
    status: "pending" | "success" | "failure";
    checks_passed: number;
    checks_failed: number;
  }>;
  current_status: {
    reviews_received: number;
    approvals: number;
    changes_requested: number;
    comments_pending: number;
    ci_status: "pending" | "success" | "failure";
  };
  final_outcome: {
    result: "merged" | "closed" | "abandoned" | "escalated" | null;
    timestamp: string | null;
    merged_by: string | null;
    merge_commit: string | null;
  } | null;
}
```

---

## Status File

### swarm-status.json

```typescript
interface SwarmStatus {
  swarm_id: string;
  cycle: number;
  started_at: string;
  current_phase: "idle" | "discovery" | "analysis" | "exploration" |
                 "development" | "pr_creation" | "review_monitoring";
  agents: {
    [key: string]: {
      status: "idle" | "running" | "completed" | "failed" | "waiting";
      last_run: string | null;
    };
  };
  current_issue: string | null;
  current_pr: string | null;
  stats: {
    cycles_completed: number;
    prs_created: number;
    prs_merged: number;
    issues_contributed: string[];
  };
}
```

---

## Validation Rules

All JSON files must:
1. Be valid JSON (parseable by `jq`)
2. Include `agent` field identifying the source
3. Include `timestamp` in ISO 8601 format
4. Include `status` field (`completed` or `failed`)
5. Be written atomically (write to .tmp then rename)

## Error Handling

If any agent fails:
1. Set `status: "failed"` in output file
2. Include error details in `errors` array
3. Orchestrator will read status and decide on retry/abort
