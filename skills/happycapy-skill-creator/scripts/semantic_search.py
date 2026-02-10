#!/usr/bin/env python3
"""
Semantic Search for Anthropic Skills

Uses LLM to understand user intent and find most relevant skills
from github.com/anthropics/skills repository
"""

import os
import json
from typing import List, Dict


def search_similar_skills(user_requirement: str) -> List[Dict]:
    """
    Search for similar skills using semantic understanding

    Args:
        user_requirement: User's description of what they need

    Returns:
        List of similar skills, sorted by relevance
        [
            {
                'name': 'pdf',
                'description': 'PDF manipulation...',
                'similarity': 0.95,
                'language': 'python',
                'repo_path': 'skills/pdf'
            },
            ...
        ]
    """

    # Get available skills (this would fetch from anthropics/skills repo)
    available_skills = get_available_skills()

    # Use LLM to rank skills by relevance
    ranked_skills = rank_skills_by_llm(user_requirement, available_skills)

    return ranked_skills


def get_available_skills() -> List[Dict]:
    """
    Get list of available skills from anthropics/skills

    In real implementation, this would:
    1. Clone/fetch the anthropics/skills repo
    2. Parse all SKILL.md files
    3. Extract metadata

    For now, return mock data
    """

    # Mock data - in real implementation, fetch from GitHub
    mock_skills = [
        {
            'name': 'pdf',
            'description': 'Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms.',
            'language': 'python',
            'repo_path': 'skills/pdf',
            'stars': 150,
            'tags': ['pdf', 'document', 'processing']
        },
        {
            'name': 'docx',
            'description': 'Document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction.',
            'language': 'python',
            'repo_path': 'skills/docx',
            'stars': 120,
            'tags': ['word', 'document', 'office']
        },
        {
            'name': 'image-enhancer',
            'description': 'Improves the quality of images, especially screenshots, by enhancing resolution, sharpness, and clarity.',
            'language': 'python',
            'repo_path': 'skills/image-enhancer',
            'stars': 80,
            'tags': ['image', 'enhancement', 'quality']
        },
        {
            'name': 'video-frames',
            'description': 'Extract frames or short clips from videos using ffmpeg.',
            'language': 'python',
            'repo_path': 'skills/video-frames',
            'stars': 60,
            'tags': ['video', 'ffmpeg', 'frames']
        }
    ]

    return mock_skills


def rank_skills_by_llm(requirement: str, skills: List[Dict]) -> List[Dict]:
    """
    Use LLM to rank skills by relevance to user requirement

    This is where we leverage Claude's semantic understanding
    """

    # Check if we have AI Gateway API available
    api_key = os.environ.get('AI_GATEWAY_API_KEY')

    if not api_key:
        # Fallback to keyword matching
        return rank_skills_by_keywords(requirement, skills)

    # Use LLM for semantic ranking via AI Gateway
    try:
        from ai_gateway import create_client
        client = create_client()

        # Build prompt
        skills_desc = "\n".join([
            f"{i+1}. {s['name']}: {s['description']}"
            for i, s in enumerate(skills)
        ])

        prompt = f"""User needs: "{requirement}"

Available skills:
{skills_desc}

Task: Rank these skills by relevance to the user's need. Consider:
- Semantic similarity (not just keywords)
- What the user is trying to accomplish
- Which skill provides the closest functionality

Return ONLY a JSON array of skill names in order of relevance, with similarity scores (0-1):
[
  {{"name": "pdf", "similarity": 0.95}},
  {{"name": "docx", "similarity": 0.3}},
  ...
]"""

        result_text = client.simple_prompt(
            prompt=prompt,
            max_tokens=1000,
            temperature=0.3  # Lower temperature for consistent JSON output
        )

        # Extract JSON
        import re
        json_match = re.search(r'\[.*\]', result_text, re.DOTALL)
        if json_match:
            rankings = json.loads(json_match.group())

            # Merge with original skill data
            ranked_skills = []
            for rank in rankings:
                skill = next((s for s in skills if s['name'] == rank['name']), None)
                if skill:
                    skill['similarity'] = rank['similarity']
                    ranked_skills.append(skill)

            return ranked_skills

    except Exception as e:
        print(f"⚠️  LLM ranking failed: {e}")
        print("   Falling back to keyword matching...")

    # Fallback
    return rank_skills_by_keywords(requirement, skills)


def rank_skills_by_keywords(requirement: str, skills: List[Dict]) -> List[Dict]:
    """
    Fallback: Simple keyword matching

    Args:
        requirement: User requirement
        skills: List of available skills

    Returns:
        Skills ranked by keyword overlap
    """

    req_words = set(requirement.lower().split())

    for skill in skills:
        # Count keyword matches
        desc_words = set(skill['description'].lower().split())
        tag_words = set(skill.get('tags', []))

        overlap = len(req_words & (desc_words | tag_words))
        skill['similarity'] = overlap / max(len(req_words), 1)

    # Sort by similarity
    ranked = sorted(skills, key=lambda s: s['similarity'], reverse=True)

    return ranked


if __name__ == "__main__":
    # Test
    import sys

    if len(sys.argv) > 1:
        requirement = sys.argv[1]
    else:
        requirement = "I need to compress PDF files"

    print(f"Searching for: {requirement}\n")

    results = search_similar_skills(requirement)

    print("Results:")
    for i, skill in enumerate(results[:3], 1):
        print(f"{i}. {skill['name']} ({skill['similarity']:.0%} match)")
        print(f"   {skill['description'][:80]}...")
        print()
