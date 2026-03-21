"""
Capy Cortex v3 - Topic Detection Engine

Fast (<50ms) keyword-based topic detection for contextual rule matching.
Pure Python implementation with no external dependencies.
"""

TOPIC_KEYWORDS = {
    "git": ["git", "commit", "branch", "merge", "rebase", "clone", "push", "pull", ".git", "checkout", "stash", "cherry-pick"],
    "npm": ["npm", "yarn", "pnpm", "package.json", "node_modules", "install", "dependencies", "devdependencies"],
    "python": ["python", "pip", "venv", "requirements.txt", ".py", "pytest", "conda", "poetry"],
    "docker": ["docker", "dockerfile", "container", "image", "compose", "kubernetes", "k8s"],
    "react": ["react", "jsx", "tsx", "component", "hook", "usestate", "useeffect", "nextjs", "next.js", "vite"],
    "api": ["api", "endpoint", "rest", "graphql", "fetch", "axios", "http", "curl", "request", "response"],
    "database": ["database", "sql", "postgres", "mysql", "sqlite", "query", "migration", "schema", "supabase"],
    "testing": ["test", "spec", "jest", "mocha", "pytest", "unittest", "cypress", "playwright"],
    "build": ["build", "webpack", "vite", "rollup", "compile", "bundle", "esbuild", "turbopack"],
    "deployment": ["deploy", "ci", "cd", "github actions", "vercel", "aws", "gcloud", "cloudflare"],
    "browser-automation": ["browser", "selenium", "playwright", "puppeteer", "chromium", "screenshot", "scrape"],
    "video-generation": ["video", "remotion", "ffmpeg", "veo", "sora", "seedance", "animation", "film"],
    "skill-creation": ["skill", "skill.md", "clawhub", "claude code", "hook", "agent"],
    "security": ["security", "injection", "xss", "csrf", "auth", "token", "jwt", "oauth", "permission"],
    "instagram": ["instagram", "post", "carousel", "reel", "story", "social media", "content"],
    "email": ["email", "smtp", "inbox", "gmail", "send email", "capymail"],
    "audio": ["audio", "tts", "speech", "voice", "podcast", "music", "elevenlabs", "kokoro"],
}


def detect_topics_fast(prompt_text, file_paths=None, skill_name=None, top_k=3):
    """
    Fast keyword-based topic detection.

    Args:
        prompt_text: User's prompt text to analyze
        file_paths: Optional list of file paths being accessed
        skill_name: Optional name of the skill being used
        top_k: Number of top topics to return (default: 3)

    Returns:
        List of topic names sorted by relevance score, always includes 'universal'
    """
    # Normalize inputs to lowercase for case-insensitive matching
    prompt_lower = prompt_text.lower() if prompt_text else ""
    file_paths_lower = [fp.lower() for fp in file_paths] if file_paths else []
    skill_name_lower = skill_name.lower() if skill_name else ""

    # Score each topic
    topic_scores = {}

    for topic, keywords in TOPIC_KEYWORDS.items():
        score = 0.0

        # Check prompt text for keyword matches (+1.0 per hit)
        for keyword in keywords:
            if keyword in prompt_lower:
                score += 1.0

        # Check file paths for keyword matches (+2.0 per hit - stronger signal)
        for file_path in file_paths_lower:
            for keyword in keywords:
                if keyword in file_path:
                    score += 2.0

        # Check skill name for keyword matches (+1.5 per hit)
        if skill_name_lower:
            for keyword in keywords:
                if keyword in skill_name_lower:
                    score += 1.5

        if score > 0:
            topic_scores[topic] = score

    # Sort topics by score (descending)
    sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)

    # Take top_k topics
    top_topics = [topic for topic, score in sorted_topics[:top_k]]

    # Always include 'universal' as fallback
    if 'universal' not in top_topics:
        top_topics.append('universal')

    return top_topics


def detect_topic_for_rule(rule_content, rule_category):
    """
    Classifies a single rule into its best-matching topic.

    Args:
        rule_content: The content/text of the rule
        rule_category: The category of the rule (e.g., 'dependency_error', 'network_error')

    Returns:
        Single topic name string (best match or 'universal')
    """
    # Normalize inputs
    content_lower = rule_content.lower() if rule_content else ""
    category_lower = rule_category.lower() if rule_category else ""

    # Score each topic
    topic_scores = {}

    for topic, keywords in TOPIC_KEYWORDS.items():
        score = 0.0

        # Check rule content for keyword matches (+1.0 per hit)
        for keyword in keywords:
            if keyword in content_lower:
                score += 1.0

        # Check if category matches topic name (+0.5 bonus)
        if topic in category_lower or category_lower in topic:
            score += 0.5

        if score > 0:
            topic_scores[topic] = score

    # Return the highest scoring topic, or 'universal' if no matches
    if topic_scores:
        best_topic = max(topic_scores.items(), key=lambda x: x[1])[0]
        return best_topic
    else:
        return 'universal'
