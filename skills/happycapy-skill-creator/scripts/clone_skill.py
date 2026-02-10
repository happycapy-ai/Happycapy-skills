#!/usr/bin/env python3
"""
Clone skill from anthropics/skills repository
"""

import subprocess
from pathlib import Path
import shutil


def clone_skill_from_repo(skill_info: dict, workspace: Path) -> Path:
    """
    Clone a skill from anthropics/skills repository

    Args:
        skill_info: Dict with skill metadata
            {
                'name': 'pdf',
                'repo_path': 'skills/pdf'
            }
        workspace: Working directory

    Returns:
        Path to cloned skill
    """

    skill_name = skill_info['name']
    repo_url = "https://github.com/anthropics/skills.git"

    # Create workspace
    workspace.mkdir(parents=True, exist_ok=True)
    skill_path = workspace / skill_name

    # Remove if exists
    if skill_path.exists():
        shutil.rmtree(skill_path)

    print(f"   Cloning from {repo_url}...")

    try:
        # Clone entire repo to temp location
        temp_repo = workspace / "temp_skills_repo"
        if temp_repo.exists():
            shutil.rmtree(temp_repo)

        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, str(temp_repo)],
            capture_output=True,
            check=True
        )

        # Copy specific skill
        source_skill = temp_repo / "skills" / skill_name

        if source_skill.exists():
            shutil.copytree(source_skill, skill_path)
            print(f"   ✅ Cloned {skill_name}")
        else:
            # Fallback: create from template
            print(f"   ⚠️  Skill not found in repo, creating template...")
            create_template_skill(skill_path, skill_name)

        # Cleanup
        shutil.rmtree(temp_repo)

        return skill_path

    except subprocess.CalledProcessError as e:
        print(f"   ⚠️  Git clone failed: {e}")
        print(f"   Creating template skill instead...")
        create_template_skill(skill_path, skill_name)
        return skill_path


def create_template_skill(skill_path: Path, skill_name: str):
    """
    Create a template skill structure

    Used as fallback when cloning fails
    """

    skill_path.mkdir(parents=True, exist_ok=True)

    # Create directories
    (skill_path / "scripts").mkdir(exist_ok=True)
    (skill_path / "references").mkdir(exist_ok=True)
    (skill_path / "assets").mkdir(exist_ok=True)

    # Create SKILL.md
    skill_md_content = f"""---
name: {skill_name}
description: [TODO: Add description]
---

# {skill_name.title()}

## Overview

[TODO: Add overview]

## Usage

[TODO: Add usage examples]
"""

    (skill_path / "SKILL.md").write_text(skill_md_content)

    # Create example script
    script_content = f"""#!/usr/bin/env python3
\"\"\"
{skill_name} - Main script
\"\"\"

def main():
    print("Hello from {skill_name}")

if __name__ == "__main__":
    main()
"""

    script_file = skill_path / "scripts" / f"{skill_name.replace('-', '_')}.py"
    script_file.write_text(script_content)
    script_file.chmod(0o755)

    print(f"   ✅ Created template for {skill_name}")


if __name__ == "__main__":
    # Test
    from pathlib import Path

    skill_info = {
        'name': 'pdf',
        'repo_path': 'skills/pdf'
    }

    workspace = Path("./test_workspace")

    path = clone_skill_from_repo(skill_info, workspace)
    print(f"\nCloned to: {path}")
    print(f"Contents: {list(path.iterdir())}")
