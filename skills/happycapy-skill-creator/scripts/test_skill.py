#!/usr/bin/env python3
"""
Basic skill testing
"""

from pathlib import Path


def test_skill_basic(skill_path: Path) -> dict:
    """
    Run basic tests on skill

    Args:
        skill_path: Path to skill

    Returns:
        {'success': True/False, 'error': None or error message}
    """

    try:
        # Check structure
        required = ['SKILL.md', 'scripts']

        for item in required:
            if not (skill_path / item).exists():
                return {
                    'success': False,
                    'error': f'Missing required: {item}'
                }

        # Try to import Python scripts
        scripts_dir = skill_path / 'scripts'

        if scripts_dir.exists():
            for script in scripts_dir.glob('*.py'):
                # Basic syntax check
                content = script.read_text()

                try:
                    compile(content, str(script), 'exec')
                except SyntaxError as e:
                    return {
                        'success': False,
                        'error': f'Syntax error in {script.name}: {e}'
                    }

        return {'success': True, 'error': None}

    except Exception as e:
        return {'success': False, 'error': str(e)}
