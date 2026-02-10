#!/usr/bin/env python3
"""
HappyCapy Skill Creator - Main Entry Point

Creates new skills by:
1. Searching for similar existing skills
2. Cloning and adapting them
3. Adding new features with LLM
4. Auto-fixing compatibility issues
5. Testing and packaging

Usage:
    python create_skill.py "I need to compress PDF files"
"""

import sys
import os
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from semantic_search import search_similar_skills
from find_skills_integration import find_existing_skill
from clone_skill import clone_skill_from_repo
from search_implementation import search_feature_implementation
from integrate_feature import integrate_and_adapt
from check_compatibility import check_environment_compatibility
from auto_fix import fix_compatibility_issues
from test_skill import test_skill_basic
from package_skill import package_skill


class SkillCreator:
    """HappyCapy Skill Creator"""

    def __init__(self):
        self.workspace = Path("./workspace")
        self.workspace.mkdir(exist_ok=True)

    def create_skill(self, user_requirement: str, skill_name: str = None):
        """
        Main workflow to create a skill

        Args:
            user_requirement: User's description of what they need

        Returns:
            Path to packaged .skill file
        """

        print("🚀 HappyCapy Skill Creator")
        print("=" * 60)
        print(f"Requirement: {user_requirement}\n")

        # Step 1: Check if perfect match exists
        print("Step 1: Searching for existing skills...")
        existing = find_existing_skill(user_requirement)

        if existing and existing.get('perfect_match'):
            print(f"✅ Found perfect match: {existing['name']}")
            print(f"   You can install it directly with: /install {existing['name']}")
            return None

        # Step 2: Semantic search for similar skill
        print("\nStep 2: Searching for similar skills to adapt...")
        similar_skills = search_similar_skills(user_requirement)

        if not similar_skills:
            print("❌ No similar skills found. Creating from scratch...")
            return self._create_from_scratch(user_requirement)

        base_skill = similar_skills[0]
        print(f"✅ Found base skill: {base_skill['name']}")
        print(f"   Similarity: {base_skill['similarity']:.0%}")
        print(f"   Description: {base_skill['description'][:100]}...")

        # Step 3: Clone base skill
        print(f"\nStep 3: Cloning {base_skill['name']}...")
        skill_path = clone_skill_from_repo(base_skill, self.workspace)
        print(f"✅ Cloned to: {skill_path}")

        # Step 4: Identify new feature needed
        print("\nStep 4: Identifying new features to add...")
        new_features = self._extract_new_features(user_requirement, base_skill)
        print(f"✅ Features to add: {', '.join(new_features)}")

        # Step 5: Search for implementations
        print("\nStep 5: Searching for feature implementations...")
        implementations = {}
        for feature in new_features:
            impl = search_feature_implementation(feature, base_skill['language'])
            if impl:
                implementations[feature] = impl
                print(f"✅ Found implementation for: {feature}")

        # Step 6: Integrate features with LLM
        print("\nStep 6: Integrating features (LLM fine-tuning)...")
        for feature, impl in implementations.items():
            print(f"   Integrating {feature}...")
            integrate_and_adapt(skill_path, feature, impl, user_requirement)
        print("✅ Features integrated")

        # Step 7: Check compatibility
        print("\nStep 7: Checking HappyCapy compatibility...")
        issues = check_environment_compatibility(skill_path)

        if issues:
            print(f"⚠️  Found {len(issues)} compatibility issues:")
            for issue in issues:
                print(f"   - {issue['type']}: {issue['description']}")

            # Step 8: Auto-fix issues
            print("\nStep 8: Auto-fixing compatibility issues...")
            fix_compatibility_issues(skill_path, issues)
            print("✅ Issues fixed")

            # Re-check
            remaining = check_environment_compatibility(skill_path)
            if remaining:
                print(f"⚠️  {len(remaining)} issues remain (manual review needed)")
        else:
            print("✅ All checks passed")

        # Step 9: Test
        print("\nStep 9: Testing skill...")
        test_result = test_skill_basic(skill_path)
        if test_result['success']:
            print("✅ Tests passed")
        else:
            print(f"⚠️  Tests failed: {test_result['error']}")

        # Step 10: Get user name
        print("\nStep 10: Naming your skill...")
        if not skill_name:
            default_name = self._suggest_name(user_requirement)
            try:
                skill_name = input(f"Skill name [{default_name}]: ").strip() or default_name
            except EOFError:
                # Non-interactive environment
                skill_name = default_name
                print(f"Using default name: {skill_name}")

        # Step 11: Package
        print(f"\nStep 11: Packaging {skill_name}...")
        output_path = package_skill(skill_path, skill_name)

        print("\n" + "=" * 60)
        print(f"🎉 Skill created successfully!")
        print(f"📦 Location: {output_path}")
        print(f"💡 Install with: /install {output_path}")

        return output_path

    def _extract_new_features(self, requirement: str, base_skill: dict) -> list:
        """Extract what new features are needed beyond base skill"""
        # Simple keyword extraction for now
        # In real implementation, use LLM to understand the diff

        requirement_lower = requirement.lower()
        base_desc_lower = base_skill['description'].lower()

        # Find keywords in requirement not in base description
        req_words = set(requirement_lower.split())
        base_words = set(base_desc_lower.split())

        new_words = req_words - base_words - {'i', 'need', 'to', 'a', 'the', 'and', 'or'}

        return list(new_words)[:3]  # Top 3 features

    def _suggest_name(self, requirement: str) -> str:
        """Suggest a skill name based on requirement"""
        # Simple version: take key words
        words = requirement.lower().split()
        key_words = [w for w in words if w not in ['i', 'need', 'to', 'a', 'the']]
        return '-'.join(key_words[:3]) + '-skill'

    def _create_from_scratch(self, requirement: str):
        """Fallback: create from scratch (simplified)"""
        print("Creating from scratch is not implemented yet.")
        print("Please try with a requirement that has similar existing skills.")
        return None


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Create HappyCapy skills automatically",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_skill.py "I need to compress PDF files"
  python create_skill.py "Extract video frames" --name video-extractor
        """
    )

    parser.add_argument(
        "requirement",
        help="Description of what you need the skill to do"
    )
    parser.add_argument(
        "--name",
        help="Skill name (skip interactive prompt)"
    )

    args = parser.parse_args()

    creator = SkillCreator()
    creator.create_skill(args.requirement, skill_name=args.name)


if __name__ == "__main__":
    main()
