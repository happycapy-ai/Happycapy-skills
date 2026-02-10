#!/usr/bin/env python3
"""
Check HappyCapy environment compatibility
"""

from pathlib import Path
from typing import List, Dict
import re


def check_environment_compatibility(skill_path: Path) -> List[Dict]:
    """
    Check if skill is compatible with HappyCapy environment

    Args:
        skill_path: Path to skill directory

    Returns:
        List of compatibility issues:
        [
            {
                'type': 'docker_dependency',
                'file': 'scripts/build.sh',
                'line': 10,
                'description': 'Uses Docker (not available)',
                'suggestion': 'Remove Docker or use alternative'
            },
            ...
        ]
    """

    issues = []

    # Check Python dependencies
    issues.extend(check_python_dependencies(skill_path))

    # Check for Docker usage
    issues.extend(check_docker_usage(skill_path))

    # Check for unsupported runtimes
    issues.extend(check_unsupported_runtimes(skill_path))

    # Check memory usage patterns
    issues.extend(check_memory_patterns(skill_path))

    return issues


def check_python_dependencies(skill_path: Path) -> List[Dict]:
    """Check if Python dependencies are available in HappyCapy"""

    issues = []

    # Known unavailable packages
    unavailable = {'tensorflow', 'torch', 'pytorch', 'cuda'}

    # Check requirements.txt
    req_file = skill_path / "requirements.txt"
    if req_file.exists():
        content = req_file.read_text()

        for line_num, line in enumerate(content.split('\n'), 1):
            line = line.strip().lower()

            for pkg in unavailable:
                if pkg in line and not line.startswith('#'):
                    issues.append({
                        'type': 'unavailable_dependency',
                        'file': 'requirements.txt',
                        'line': line_num,
                        'description': f'Package "{pkg}" not available in HappyCapy',
                        'suggestion': f'Remove or find alternative to {pkg}'
                    })

    return issues


def check_docker_usage(skill_path: Path) -> List[Dict]:
    """Check for Docker usage"""

    issues = []

    docker_patterns = [
        r'docker\s+run',
        r'docker\s+build',
        r'docker-compose',
        r'FROM\s+\w+',  # Dockerfile
        r'subprocess.*docker',
    ]

    # Check all code files
    for code_file in skill_path.rglob("*.py"):
        content = code_file.read_text()

        for line_num, line in enumerate(content.split('\n'), 1):
            for pattern in docker_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        'type': 'docker_dependency',
                        'file': str(code_file.relative_to(skill_path)),
                        'line': line_num,
                        'description': 'Uses Docker (not available in HappyCapy)',
                        'suggestion': 'Rewrite to run natively without Docker'
                    })
                    break

    # Check for Dockerfile
    if (skill_path / "Dockerfile").exists():
        issues.append({
            'type': 'docker_dependency',
            'file': 'Dockerfile',
            'line': 1,
            'description': 'Dockerfile present (Docker not available)',
            'suggestion': 'Remove Dockerfile and run natively'
        })

    return issues


def check_unsupported_runtimes(skill_path: Path) -> List[Dict]:
    """Check for unsupported runtime dependencies"""

    issues = []

    # Unsupported in HappyCapy
    unsupported = {
        'java': ['java', 'javac', 'jar'],
        'ruby': ['ruby', 'gem'],
        'go': ['go run', 'go build'],
    }

    for code_file in skill_path.rglob("*.py"):
        content = code_file.read_text()

        for runtime, commands in unsupported.items():
            for cmd in commands:
                if cmd in content.lower():
                    issues.append({
                        'type': 'unsupported_runtime',
                        'file': str(code_file.relative_to(skill_path)),
                        'line': 0,
                        'description': f'Uses {runtime} (not available)',
                        'suggestion': f'Rewrite without {runtime} dependency'
                    })
                    break

    return issues


def check_memory_patterns(skill_path: Path) -> List[Dict]:
    """Check for potentially memory-intensive patterns"""

    issues = []

    memory_patterns = [
        (r'\.read\(\)', 'Reading entire file into memory'),
        (r'pd\.read_csv.*chunksize', 'Not using chunked reading'),
    ]

    for code_file in skill_path.rglob("*.py"):
        content = code_file.read_text()

        # Simple heuristic: if file is large and reads all at once
        if '.read()' in content and 'chunk' not in content.lower():
            issues.append({
                'type': 'memory_concern',
                'file': str(code_file.relative_to(skill_path)),
                'line': 0,
                'description': 'May load large files entirely into memory',
                'suggestion': 'Consider streaming or chunked processing for large files'
            })

    return issues


if __name__ == "__main__":
    # Test
    import sys
    from pathlib import Path

    if len(sys.argv) > 1:
        skill_path = Path(sys.argv[1])
    else:
        print("Usage: python check_compatibility.py <skill_path>")
        sys.exit(1)

    print(f"Checking compatibility: {skill_path}\n")

    issues = check_environment_compatibility(skill_path)

    if issues:
        print(f"Found {len(issues)} issues:\n")
        for issue in issues:
            print(f"❌ {issue['type']}: {issue['file']}")
            print(f"   {issue['description']}")
            print(f"   💡 {issue['suggestion']}\n")
    else:
        print("✅ No compatibility issues found")
