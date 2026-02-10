#!/usr/bin/env python3
"""
Package skill into .skill file
"""

import zipfile
from pathlib import Path


def package_skill(skill_path: Path, skill_name: str) -> Path:
    """
    Package skill into distributable .skill file

    Args:
        skill_path: Path to skill directory
        skill_name: Name for the skill

    Returns:
        Path to .skill file
    """

    output_dir = Path("./outputs")
    output_dir.mkdir(exist_ok=True)

    skill_file = output_dir / f"{skill_name}.skill"

    # Create zip file with .skill extension
    with zipfile.ZipFile(skill_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all files
        for file_path in skill_path.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(skill_path.parent)
                zipf.write(file_path, arcname)

    return skill_file


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 2:
        skill_path = Path(sys.argv[1])
        skill_name = sys.argv[2]

        output = package_skill(skill_path, skill_name)
        print(f"✅ Packaged: {output}")
    else:
        print("Usage: python package_skill.py <skill_path> <skill_name>")
