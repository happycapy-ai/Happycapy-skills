#!/usr/bin/env python3
"""
Integrate new features into skill using LLM fine-tuning
"""

import os
from pathlib import Path
from typing import Dict


def integrate_and_adapt(
    skill_path: Path,
    feature_name: str,
    implementation: Dict,
    user_requirement: str
):
    """
    Integrate a new feature into existing skill with LLM fine-tuning

    Args:
        skill_path: Path to skill directory
        feature_name: Name of feature to add (e.g., "compress")
        implementation: Dict with implementation code/info
        user_requirement: Original user requirement for context
    """

    print(f"      Analyzing existing skill structure...")

    # Read existing skill code
    existing_code = read_skill_code(skill_path)

    # Get API key
    api_key = os.environ.get('ANTHROPIC_API_KEY') or os.environ.get('AI_GATEWAY_API_KEY')

    if not api_key:
        print("      ⚠️  No API key found, using template integration...")
        integrate_with_template(skill_path, feature_name, implementation)
        return

    # Use LLM to integrate via AI Gateway
    try:
        from ai_gateway import create_client
        client = create_client()

        prompt = build_integration_prompt(
            existing_code,
            feature_name,
            implementation,
            user_requirement
        )

        print(f"      Generating integrated code with GPT-4...")

        integrated_code = client.simple_prompt(
            prompt=prompt,
            max_tokens=4000,
            temperature=0.5
        )

        # Save integrated code
        save_integrated_code(skill_path, feature_name, integrated_code)

        print(f"      ✅ Feature integrated successfully")

    except Exception as e:
        print(f"      ⚠️  LLM integration failed: {e}")
        print(f"      Using template integration...")
        integrate_with_template(skill_path, feature_name, implementation)


def build_integration_prompt(
    existing_code: str,
    feature_name: str,
    implementation: Dict,
    user_requirement: str
) -> str:
    """
    Build prompt for LLM to integrate feature
    """

    prompt = f"""You are integrating a new feature into an existing skill.

USER REQUIREMENT: {user_requirement}

EXISTING SKILL STRUCTURE:
{existing_code}

NEW FEATURE TO ADD: {feature_name}

REFERENCE IMPLEMENTATION:
{implementation.get('code', 'No reference code provided')}

TASK:
1. Add the new feature ({feature_name}) to the existing skill
2. Match the existing code style and patterns
3. Ensure compatibility with HappyCapy environment:
   - Python 3.11 or Node.js 24
   - No Docker dependencies
   - Memory usage < 2GB
   - Use standard libraries when possible
4. Keep dependencies minimal
5. Follow the skill's existing structure (scripts/, references/, assets/)

OUTPUT:
Provide the new/modified files needed. Format as:

```filename: scripts/feature_name.py
[code here]
```

```filename: SKILL.md
[updated SKILL.md with feature documented]
```

Focus on creating clean, working code that integrates seamlessly."""

    return prompt


def read_skill_code(skill_path: Path) -> str:
    """
    Read existing skill code for context

    Returns:
        String summary of skill structure and key files
    """

    structure = []

    # Read SKILL.md
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text()
        structure.append(f"=== SKILL.md ===\n{content[:1000]}...\n")

    # List scripts
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists():
        structure.append(f"\n=== scripts/ ===")
        for script in scripts_dir.glob("*.py"):
            structure.append(f"- {script.name}")
            # Include first 500 chars of each script
            content = script.read_text()
            structure.append(f"  Preview: {content[:500]}...\n")

    return "\n".join(structure)


def save_integrated_code(skill_path: Path, feature_name: str, integrated_code: str):
    """
    Parse and save the integrated code from LLM response
    """

    import re

    # Extract code blocks
    pattern = r'```filename:\s*([^\n]+)\n(.*?)```'
    matches = re.findall(pattern, integrated_code, re.DOTALL)

    for filename, code in matches:
        filename = filename.strip()
        file_path = skill_path / filename

        # Create parent directories
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Save file
        file_path.write_text(code)

        # Make scripts executable
        if file_path.suffix == '.py' and 'scripts' in str(file_path):
            file_path.chmod(0o755)

        print(f"      ✅ Saved: {filename}")


def integrate_with_template(skill_path: Path, feature_name: str, implementation: Dict):
    """
    Fallback: Integrate using template (no LLM)
    """

    # Create a simple template file
    script_path = skill_path / "scripts" / f"{feature_name}.py"

    template_code = f"""#!/usr/bin/env python3
\"\"\"
{feature_name.title()} functionality

Added by HappyCapy Skill Creator
\"\"\"

def {feature_name}(input_file, output_file=None):
    \"\"\"
    {feature_name.title()} operation

    Args:
        input_file: Input file path
        output_file: Output file path (optional)

    Returns:
        Path to output file
    \"\"\"

    # TODO: Implement {feature_name} logic
    # Reference implementation:
    # {implementation.get('description', 'No description')}

    print(f"Processing {{input_file}}...")

    # Placeholder implementation
    if output_file is None:
        output_file = input_file.replace('.', f'_{feature_name}.')

    # Add actual implementation here

    return output_file


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        result = {feature_name}(sys.argv[1])
        print(f"Output: {{result}}")
    else:
        print("Usage: python {feature_name}.py <input_file>")
"""

    script_path.write_text(template_code)
    script_path.chmod(0o755)

    print(f"      ✅ Created template: {script_path.name}")

    # Update SKILL.md
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text()

        # Add feature to SKILL.md
        addition = f"\n\n## {feature_name.title()}\n\nNew feature added by HappyCapy Skill Creator.\n\nUsage:\n```bash\npython scripts/{feature_name}.py <input>\n```\n"

        skill_md.write_text(content + addition)


if __name__ == "__main__":
    # Test
    from pathlib import Path

    skill_path = Path("./test_skill")
    skill_path.mkdir(exist_ok=True)
    (skill_path / "scripts").mkdir(exist_ok=True)

    (skill_path / "SKILL.md").write_text("# Test Skill\n\nExisting skill")

    implementation = {
        'code': 'def compress(): pass',
        'description': 'Compresses files'
    }

    integrate_and_adapt(skill_path, "compress", implementation, "compress PDFs")

    print(f"\nGenerated files:")
    for f in skill_path.rglob("*"):
        if f.is_file():
            print(f"  - {f.relative_to(skill_path)}")
