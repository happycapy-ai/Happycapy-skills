#!/usr/bin/env python3
"""
Auto-fix compatibility issues using LLM
"""

import os
from pathlib import Path
from typing import List, Dict


def fix_compatibility_issues(skill_path: Path, issues: List[Dict]):
    """
    Automatically fix compatibility issues using LLM

    Args:
        skill_path: Path to skill
        issues: List of compatibility issues from check_compatibility
    """

    api_key = os.environ.get('ANTHROPIC_API_KEY') or os.environ.get('AI_GATEWAY_API_KEY')

    if not api_key:
        print("      ⚠️  No API key, manual fixes required")
        return

    try:
        from ai_gateway import create_client
        client = create_client()

        for issue in issues:
            print(f"      Fixing: {issue['type']} in {issue['file']}...")

            if issue['type'] == 'docker_dependency':
                fix_docker_issue(client, skill_path, issue)
            elif issue['type'] == 'unavailable_dependency':
                fix_dependency_issue(client, skill_path, issue)
            elif issue['type'] == 'unsupported_runtime':
                fix_runtime_issue(client, skill_path, issue)
            elif issue['type'] == 'memory_concern':
                fix_memory_issue(client, skill_path, issue)

    except Exception as e:
        print(f"      ⚠️  Auto-fix failed: {e}")


def fix_docker_issue(client, skill_path: Path, issue: Dict):
    """Fix Docker dependencies"""

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

    fixed_code_text = client.simple_prompt(
        prompt=prompt,
        max_tokens=3000,
        temperature=0.3
    )

    fixed_code = extract_code_from_response(fixed_code_text)

    if fixed_code:
        file_path.write_text(fixed_code)
        print(f"         ✅ Fixed Docker issue in {issue['file']}")


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
        print(f"         ✅ Removed unavailable dependencies")


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
        print(f"         ✅ Fixed runtime issue in {issue['file']}")


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
        print(f"         ✅ Optimized memory usage in {issue['file']}")


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
    print("Auto-fix utility for HappyCapy compatibility")
    print("This is typically called from create_skill.py")
