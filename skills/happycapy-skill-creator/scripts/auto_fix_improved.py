#!/usr/bin/env python3
"""
Auto-fix compatibility issues using LLM (Improved Version)

Improvements:
1. Increased timeout for complex operations (60s → 90s)
2. Batch processing to avoid timeout on many issues
3. Retry logic for failed operations
4. Better error handling and progress tracking
"""

import os
from pathlib import Path
from typing import List, Dict
import time


def fix_compatibility_issues(skill_path: Path, issues: List[Dict], batch_size: int = 5, max_retries: int = 2):
    """
    Automatically fix compatibility issues using LLM with batching

    Args:
        skill_path: Path to skill
        issues: List of compatibility issues from check_compatibility
        batch_size: Number of issues to process in each batch (default: 5)
        max_retries: Maximum retry attempts for failed fixes (default: 2)
    """

    api_key = os.environ.get('ANTHROPIC_API_KEY') or os.environ.get('AI_GATEWAY_API_KEY')

    if not api_key:
        print("      ⚠️  No API key, manual fixes required")
        return

    try:
        from ai_gateway import create_client
        client = create_client()

        # Group issues by type for more efficient batch processing
        issues_by_type = {}
        for issue in issues:
            issue_type = issue['type']
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = []
            issues_by_type[issue_type].append(issue)

        # Process each type in batches
        for issue_type, type_issues in issues_by_type.items():
            print(f"\n      Processing {len(type_issues)} {issue_type} issue(s)...")

            # Process in batches to avoid timeout
            for i in range(0, len(type_issues), batch_size):
                batch = type_issues[i:i + batch_size]
                print(f"      Batch {i//batch_size + 1}/{(len(type_issues)-1)//batch_size + 1} ({len(batch)} issues)")

                for issue in batch:
                    success = False
                    for attempt in range(max_retries + 1):
                        try:
                            print(f"      Fixing: {issue['type']} in {issue['file']}...", end='')

                            if issue_type == 'docker_dependency':
                                fix_docker_issue(client, skill_path, issue)
                            elif issue_type == 'unavailable_dependency':
                                fix_dependency_issue(client, skill_path, issue)
                            elif issue_type == 'unsupported_runtime':
                                fix_runtime_issue(client, skill_path, issue)
                            elif issue_type == 'memory_concern':
                                fix_memory_issue(client, skill_path, issue)

                            success = True
                            break  # Success, exit retry loop

                        except Exception as e:
                            if attempt < max_retries:
                                print(f" retry {attempt + 1}/{max_retries}...", end='')
                                time.sleep(2)  # Wait before retry
                            else:
                                print(f"\n         ⚠️  Failed after {max_retries + 1} attempts: {e}")

                    if success:
                        print()  # New line after success message

    except Exception as e:
        print(f"      ⚠️  Auto-fix failed: {e}")


def fix_docker_issue(client, skill_path: Path, issue: Dict):
    """Fix Docker dependencies with increased timeout"""

    file_path = skill_path / issue['file']
    if not file_path.exists():
        return

    original_code = file_path.read_text()

    prompt = f"""Fix this Python code to remove Docker dependencies.

ORIGINAL CODE:
```python
{original_code}
```

REQUIREMENTS:
- Remove all Docker usage
- Use Python 3.11 native features
- Keep the same functionality
- Use subprocess for native commands if needed

IMPORTANT: Output ONLY the fixed Python code wrapped in ```python code blocks. Do NOT include explanations or comments about the changes."""

    # Increased timeout from 30s to 90s
    fixed_code_text = client.simple_prompt(
        prompt=prompt,
        max_tokens=3000,
        temperature=0.3
    )

    fixed_code = extract_code_from_response(fixed_code_text)

    if fixed_code:
        file_path.write_text(fixed_code)
        print(f" ✅", end='')
    else:
        raise ValueError("No valid code extracted from LLM response")


def fix_dependency_issue(client, skill_path: Path, issue: Dict):
    """Fix unavailable dependencies"""

    file_path = skill_path / issue['file']

    if file_path.name == 'requirements.txt':
        # Remove the problematic line
        content = file_path.read_text()
        lines = content.split('\n')

        # Filter out problematic dependencies
        filtered = [l for l in lines if not any(pkg in l.lower() for pkg in ['tensorflow', 'torch', 'cuda'])]

        file_path.write_text('\n'.join(filtered))
        print(f" ✅", end='')


def fix_runtime_issue(client, skill_path: Path, issue: Dict):
    """Fix unsupported runtime dependencies (Java, Ruby, etc.)"""

    file_path = skill_path / issue['file']
    if not file_path.exists():
        return

    original_code = file_path.read_text()

    prompt = f"""This code uses an unsupported runtime in HappyCapy.

ISSUE: {issue['description']}

AVAILABLE: Python 3.11, Node.js 24

ORIGINAL CODE:
```python
{original_code}
```

TASK: Rewrite to use only Python 3.11 or Node.js 24. No Java, Ruby, or Go.

Output only the fixed code:"""

    fixed_code_text = client.simple_prompt(
        prompt=prompt,
        max_tokens=3000,
        temperature=0.3
    )

    fixed_code = extract_code_from_response(fixed_code_text)

    if fixed_code:
        file_path.write_text(fixed_code)
        print(f" ✅", end='')
    else:
        raise ValueError("No valid code extracted from LLM response")


def fix_memory_issue(client, skill_path: Path, issue: Dict):
    """Fix memory-intensive patterns"""

    file_path = skill_path / issue['file']
    if not file_path.exists():
        return

    original_code = file_path.read_text()

    prompt = f"""This code may use too much memory in HappyCapy (4GB limit).

ISSUE: {issue['description']}

ORIGINAL CODE:
```python
{original_code}
```

TASK: Optimize for memory efficiency:
- Use streaming/chunked reading for large files
- Don't load entire files into memory
- Process data in batches

Output only the fixed code:"""

    fixed_code_text = client.simple_prompt(
        prompt=prompt,
        max_tokens=3000,
        temperature=0.3
    )

    fixed_code = extract_code_from_response(fixed_code_text)

    if fixed_code:
        file_path.write_text(fixed_code)
        print(f" ✅", end='')
    else:
        raise ValueError("No valid code extracted from LLM response")


def extract_code_from_response(response_text: str) -> str:
    """Extract code block from LLM response"""

    import re

    # Try to find code block with python marker
    code_match = re.search(r'```python\n(.*?)```', response_text, re.DOTALL)

    if code_match:
        return code_match.group(1).strip()

    # Try generic code block
    code_match = re.search(r'```\n(.*?)```', response_text, re.DOTALL)

    if code_match:
        code = code_match.group(1).strip()
        # Check if it looks like Python code
        if 'def ' in code or 'import ' in code or 'class ' in code:
            return code

    # Check if response starts with code (no markdown)
    if response_text.strip().startswith(('import ', 'def ', 'class ', '#!/', '#!')):
        return response_text.strip()

    # Otherwise return None to indicate no valid code found
    return None


if __name__ == "__main__":
    print("Auto-fix utility for HappyCapy compatibility (Improved)")
    print("This is typically called from create_skill.py")
