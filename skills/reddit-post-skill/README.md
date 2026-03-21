# Reddit Post Writer Skill

A Claude Code skill for generating authentic Reddit posts that sound human, avoid AI detection, and spark engagement across 25+ subreddits.

## Features

- Generate authentic Reddit posts that match subreddit culture
- 7-persona committee review system for quality assurance
- Configurable tool/product mentions with subtlety levels (1-10)
- **25+ subreddit-specific guidelines** covering:
  - Career & Jobs: r/jobs, r/RemoteWork, r/careerguidance, r/antiwork, r/workfromhome
  - AI & Tech: r/claude, r/AgentsOfAI, r/claudecode, r/claudeexplorers, r/aiagents, r/AI_Application, r/AIAgentsInAction, r/AiForSmallBusiness
  - Entrepreneurship: r/Entrepreneur, r/indiehackers, r/founder, r/EntrepreneurRideAlong, r/GrowMyBusiness
  - Productivity: r/Productivity, r/ProductivityApps, r/ProductivityCafe, r/nocode, r/automation
  - Lifestyle: r/digitalnomad, r/InternetIsBeautiful
- Posting strategy recommendations including timing and engagement predictions

## Installation

### For Claude Code Users

Copy the skill to your Claude Code skills directory:

```bash
# Create the skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Clone or copy this repository
git clone https://github.com/niveshdandyan/reddit-post-skill.git ~/.claude/skills/reddit-post-writer
```

### Directory Structure

```
~/.claude/skills/reddit-post-writer/
├── SKILL.md                                    # Main skill definition
└── references/
    ├── tool-mentions.md                        # Guidelines for subtle product mentions
    ├── examples.md                             # Good vs bad examples
    ├── subreddits.md                           # Core subreddit guidelines (r/jobs, r/RemoteWork, etc.)
    ├── subreddits-extended.md                  # 20+ additional subreddit analyses
    └── subreddit-analysis-claude-agentsofai.md # Deep analysis for r/claude & r/AgentsOfAI
```

## Usage

Once installed, invoke the skill in Claude Code:

```
/reddit-post-writer
```

The skill will ask for:
1. **Target Subreddit(s):** e.g., r/jobs, r/RemoteWork, r/Entrepreneur, r/claudecode
2. **Core Situation:** Brief description of the scenario
3. **Primary Goal:** Share struggle, ask for advice, vent, tell a story, or start discussion
4. **Tool/Product Mention (Optional):** Name + subtlety level 1-10

## Output Format

The skill generates:
- Ready-to-post title and body
- Posting strategy (timing, expected engagement, risks)
- Authenticity breakdown
- Comment response guide
- Committee review with 7 persona perspectives

## Committee Review System

Each generated post is reviewed by 7 simulated personas:

| Persona | Role |
|---------|------|
| Jade | Reddit veteran (400k karma) |
| Tyler | Authenticity detector |
| Marcus | Professional skeptic |
| Devon | Target audience member |
| Priya | Career/topic expert |
| Kai | BS detector |
| Jamie | Reddit mod |

## Supported Subreddits

### Career & Remote Work
- r/jobs, r/RemoteWork, r/careerguidance, r/antiwork, r/workfromhome, r/digitalnomad

### AI & Technology
- r/claude, r/AgentsOfAI, r/claudecode, r/claudeexplorers, r/aiagents
- r/AI_Application, r/AIAgentsInAction, r/AiForSmallBusiness, r/automation

### Entrepreneurship & Business
- r/Entrepreneur, r/indiehackers, r/founder, r/EntrepreneurRideAlong, r/GrowMyBusiness

### Productivity & Tools
- r/Productivity, r/ProductivityApps, r/ProductivityCafe, r/nocode, r/InternetIsBeautiful

## Iteration Commands

After receiving output, you can request:
- `alternatives` - 2-3 different versions
- `expand [section]` - Detailed analysis
- `revise [feedback]` - Adjust based on notes
- `another subreddit` - Adapt for different community
- `committee debate` - Detailed persona discussion
- `more vulnerable/less desperate/shorter/more specific` - Tone adjustments

## Core Principles

1. **Real Over Polished** - Messy, contradictory, unresolved
2. **Specific Over Generic** - One embarrassing detail > ten generic statements
3. **Struggle Over Solution** - People upvote relatability
4. **Community Voice** - Match each subreddit's culture
5. **Tools Are Never The Hero** - Mentioned once, briefly, with limitations

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

---

**Repository:** [github.com/niveshdandyan/reddit-post-skill](https://github.com/niveshdandyan/reddit-post-skill)
