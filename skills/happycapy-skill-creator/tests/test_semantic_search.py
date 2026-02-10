#!/usr/bin/env python3
"""
Test cases for semantic search issues

Bug: semantic_search.py doesn't output results properly
Solution: Fix output formatting and ensure results are returned
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


class TestSemanticSearch:
    """Test semantic search functionality"""

    def test_search_returns_results(self):
        """Test that search returns valid results"""
        from semantic_search import search_similar_skills

        results = search_similar_skills("compress PDF files")
        assert results is not None
        assert isinstance(results, list)
        assert len(results) > 0

    def test_result_structure(self):
        """Test that each result has required fields"""
        from semantic_search import search_similar_skills

        results = search_similar_skills("compress PDF files")
        if results:
            result = results[0]
            assert 'name' in result
            assert 'description' in result
            assert 'similarity' in result

    def test_similarity_scores_valid(self):
        """Test that similarity scores are between 0 and 1"""
        from semantic_search import search_similar_skills

        results = search_similar_skills("compress PDF files")
        for result in results:
            assert 0 <= result['similarity'] <= 1

    def test_results_sorted_by_relevance(self):
        """Test that results are sorted by similarity (descending)"""
        from semantic_search import search_similar_skills

        results = search_similar_skills("compress PDF files")
        if len(results) > 1:
            for i in range(len(results) - 1):
                assert results[i]['similarity'] >= results[i + 1]['similarity']


class TestKeywordFallback:
    """Test keyword matching fallback"""

    def test_keyword_matching_works_without_api(self):
        """Test that keyword matching works when API is unavailable"""
        from semantic_search import rank_skills_by_keywords

        skills = [
            {
                'name': 'pdf',
                'description': 'PDF manipulation toolkit',
                'tags': ['pdf', 'document']
            }
        ]

        results = rank_skills_by_keywords("compress PDF files", skills)
        assert len(results) > 0
        assert results[0]['similarity'] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
