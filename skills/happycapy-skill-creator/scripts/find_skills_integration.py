#!/usr/bin/env python3
"""
Integration with find-skills

Checks if a perfect match already exists in installed skills
"""

import subprocess
import json
from typing import Optional, Dict


def find_existing_skill(user_requirement: str) -> Optional[Dict]:
    """
    Search for existing skills using find-skills

    Args:
        user_requirement: User's description

    Returns:
        Skill info if found, None otherwise
        {
            'name': 'pdf',
            'description': '...',
            'perfect_match': True/False
        }
    """

    try:
        # Try to use find-skills if available
        # This would integrate with the actual find-skills tool

        # For now, simple check in installed skills
        installed = get_installed_skills()

        # Use LLM to check if any installed skill matches perfectly
        for skill in installed:
            if is_perfect_match(user_requirement, skill):
                skill['perfect_match'] = True
                return skill

        return None

    except Exception as e:
        print(f"⚠️  find-skills integration failed: {e}")
        return None


def get_installed_skills() -> list:
    """
    Get list of installed skills

    Checks ~/.claude/skills/ directory
    """

    import os
    from pathlib import Path

    skills_dir = Path.home() / '.claude' / 'skills'

    if not skills_dir.exists():
        return []

    installed = []
    for skill_path in skills_dir.iterdir():
        if skill_path.is_dir():
            skill_md = skill_path / 'SKILL.md'
            if skill_md.exists():
                # Parse SKILL.md
                info = parse_skill_md(skill_md)
                if info:
                    installed.append(info)

    return installed


def parse_skill_md(skill_md_path) -> Optional[Dict]:
    """
    Parse SKILL.md to extract name and description

    Args:
        skill_md_path: Path to SKILL.md

    Returns:
        {
            'name': 'pdf',
            'description': '...',
            'path': '/path/to/skill'
        }
    """

    try:
        content = skill_md_path.read_text()

        # Extract YAML frontmatter
        import re
        frontmatter_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)

        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)

            # Simple YAML parsing
            name_match = re.search(r'name:\s*(.+)', frontmatter)
            desc_match = re.search(r'description:\s*(.+)', frontmatter)

            if name_match and desc_match:
                return {
                    'name': name_match.group(1).strip(),
                    'description': desc_match.group(1).strip(),
                    'path': str(skill_md_path.parent)
                }

    except Exception as e:
        print(f"⚠️  Failed to parse {skill_md_path}: {e}")

    return None


def is_perfect_match(requirement: str, skill: Dict) -> bool:
    """
    Check if a skill perfectly matches the requirement

    Uses simple heuristics - in real implementation, use LLM
    """

    req_lower = requirement.lower()
    desc_lower = skill['description'].lower()

    # Check if key words from requirement are in description
    key_words = [w for w in req_lower.split() if len(w) > 3]

    matches = sum(1 for word in key_words if word in desc_lower)

    # Perfect match if > 70% of key words match
    threshold = len(key_words) * 0.7

    return matches >= threshold


if __name__ == "__main__":
    # Test
    import sys

    if len(sys.argv) > 1:
        requirement = sys.argv[1]
    else:
        requirement = "I need to manipulate PDF files"

    print(f"Searching for existing skill: {requirement}\n")

    result = find_existing_skill(requirement)

    if result:
        if result.get('perfect_match'):
            print(f"✅ Perfect match found: {result['name']}")
        else:
            print(f"✅ Partial match found: {result['name']}")
        print(f"   Description: {result['description']}")
    else:
        print("❌ No existing skill found")
