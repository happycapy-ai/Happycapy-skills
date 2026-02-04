# Resume Assistant | 简历助手

**智能简历助手，通过五个专业 AI 代理提供全流程求职支持**

[![GitHub release](https://img.shields.io/github/v/release/Y1fe1-Yang/resume-assistant-skill?style=flat-square)](https://github.com/Y1fe1-Yang/resume-assistant-skill/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**[中文](#中文) | [English](#english)**

---

<h2 id="中文">🇨🇳 中文</h2>

## 简介

智能简历助手，通过**五个专业 AI 代理**提供从经历挖掘、职位推荐、简历优化、模拟面试到能力提升的全流程求职支持。

### 五个 AI 代理

1. **🔍 故事挖掘代理**
   - 引导式对话发现被忽略的有价值经历
   - 用 STAR 框架深挖每个经历
   - 提炼可迁移技能清单

2. **💼 职位推荐代理**
   - 基于背景和兴趣推荐职位方向
   - 从技能匹配度、兴趣契合度、发展潜力评估
   - 提供典型公司、技能差距、入门建议

3. **📝 简历优化代理**
   - 根据目标岗位 JD 针对性优化简历
   - 融入关键词，量化成果
   - 优化 ATS 通过率

4. **🎭 模拟面试代理**
   - 模拟真实面试场景（行为面试、技术面试、压力面试）
   - 提供详细反馈并反向优化简历
   - 沉浸式对话体验

5. **📈 能力提升代理**
   - 分析技能差距，制定可执行提升计划
   - 按优先级排序（高/中/低）
   - 提供具体资源和里程碑

### 输出格式

- **📄 PDF** - 专业格式，适合正式投递
- **📝 DOCX** - 可编辑格式，便于修改
- **🌐 HTML** - 现代响应式设计，支持深色模式
- **📊 Excel** - 能力提升追踪表

## 安装

### 方式 1: 下载 Release（推荐）

```bash
# 下载最新版本
curl -L -O https://github.com/Y1fe1-Yang/resume-assistant-skill/releases/latest/download/resume-assistant-skill.skill

# 安装技能包
/install resume-assistant-skill.skill

# 安装 Python 依赖
pip install fpdf2 python-docx openpyxl
```

**✅ 中文字体已内置** - PDF 生成开箱即用！

### 方式 2: 从技能集合安装

```bash
git clone https://github.com/Y1fe1-Yang/Happycapy-skills.git
cp -r Happycapy-skills/skills/resume-assistant ~/.claude/skills/
```

## 快速开始

安装后，直接与 Claude Code 对话：

```
"帮我写简历"                # 创建简历
"优化这份简历"              # 优化现有简历
"根据这个 JD 优化简历"      # 针对 JD 优化
"模拟面试"                  # 面试练习
"职业规划"                  # 职业规划
"我想冲 XX 岗位但能力不够"   # 技能差距分析
```

## 使用场景

### 1. 零经验学生
- **痛点**: "我没有实习经历，简历只能写校园经历，怕 HR 看不上"
- **解决**: 故事挖掘代理帮你发现社团活动、课程项目中的可迁移技能

### 2. 迷茫求职者
- **痛点**: "不知道自己适合什么工作，投简历很盲目"
- **解决**: 职位推荐代理基于背景推荐适合方向

### 3. 海投无回应
- **痛点**: "海投了 100 份简历，只收到 3 个面试"
- **解决**: 简历优化代理针对每个 JD 定制简历，提升匹配度

### 4. 面试紧张
- **痛点**: "一面试就紧张，脑子一片空白"
- **解决**: 模拟面试代理多轮练习，提前熟悉问题

### 5. 能力不足
- **痛点**: "看到心仪岗位，但技能差距太大不敢投"
- **解决**: 能力提升代理制定 3 个月提升计划

## 特性

### 工作流程
```
1. 故事挖掘 → 发现经历亮点
2. 职位推荐 → 找到方向
3. 简历优化 → 针对 JD 定制
4. 模拟面试 → 实战演练
5. 能力提升 → 差距分析与计划
```

### 核心优势
- ✅ **五代理协作**: 覆盖求职全流程
- ✅ **多格式输出**: PDF/DOCX/HTML/Excel
- ✅ **中文优化**: 内置字体，无需配置
- ✅ **实战导向**: 基于真实场景设计
- ✅ **渐进式引导**: 降低学生压力

## 文档

- **完整文档**: [GitHub 仓库](https://github.com/Y1fe1-Yang/resume-assistant-skill)
- **使用指南**: [README.md](https://github.com/Y1fe1-Yang/resume-assistant-skill/blob/main/README.md)
- **代理详解**: `references/` 目录
- **示例输出**: `examples/` 目录

## 版本

**当前版本**: v1.0.0

## 链接

- **仓库**: https://github.com/Y1fe1-Yang/resume-assistant-skill
- **Releases**: https://github.com/Y1fe1-Yang/resume-assistant-skill/releases
- **Issues**: https://github.com/Y1fe1-Yang/resume-assistant-skill/issues

---

<h2 id="english">🇬🇧 English</h2>

## Overview

Intelligent resume assistant powered by **five specialized AI agents** providing end-to-end job search support - from experience mining, job recommendations, resume optimization, mock interviews, to skill development.

### Five AI Agents

1. **🔍 Story Mining Agent**
   - Guided conversation to uncover overlooked valuable experiences
   - Deep dive with STAR framework
   - Extract transferable skills

2. **💼 Job Recommendation Agent**
   - Recommend positions based on background and interests
   - Evaluate from skill match, interest alignment, growth potential
   - Provide company suggestions, skill gaps, entry tips

3. **📝 Resume Optimization Agent**
   - Tailor resume to target job descriptions
   - Integrate keywords and quantify achievements
   - Optimize ATS pass rate

4. **🎭 Mock Interview Agent**
   - Simulate real interview scenarios (behavioral, technical, stress)
   - Provide detailed feedback and reverse-optimize resume
   - Immersive conversational experience

5. **📈 Skill Development Agent**
   - Analyze skill gaps and create actionable improvement plans
   - Prioritize by importance (high/medium/low)
   - Provide specific resources and milestones

### Output Formats

- **📄 PDF** - Professional format for formal applications
- **📝 DOCX** - Editable format for further modifications
- **🌐 HTML** - Modern responsive design with dark mode
- **📊 Excel** - Skill tracking sheet with milestones

## Installation

### Option 1: Download Release (Recommended)

```bash
# Download latest version
curl -L -O https://github.com/Y1fe1-Yang/resume-assistant-skill/releases/latest/download/resume-assistant-skill.skill

# Install skill
/install resume-assistant-skill.skill

# Install Python dependencies
pip install fpdf2 python-docx openpyxl
```

**✅ Chinese fonts included** - PDF generation works out of the box!

### Option 2: Install from Collection

```bash
git clone https://github.com/Y1fe1-Yang/Happycapy-skills.git
cp -r Happycapy-skills/skills/resume-assistant ~/.claude/skills/
```

## Quick Start

After installation, simply chat with Claude Code:

```
"Help me write a resume"           # Create resume
"Optimize this resume"             # Optimize existing resume
"Optimize for this JD"             # Tailor to job description
"Mock interview"                   # Practice interview
"Career planning"                  # Career guidance
"I want to apply for X but lack skills"  # Skill gap analysis
```

## Use Cases

### 1. Students with No Experience
- **Pain**: "No internship experience, only campus activities"
- **Solution**: Story Mining Agent uncovers transferable skills from clubs and projects

### 2. Confused Job Seekers
- **Pain**: "Don't know what job suits me"
- **Solution**: Job Recommendation Agent suggests suitable directions

### 3. Low Response Rate
- **Pain**: "100 applications, only 3 interviews"
- **Solution**: Resume Optimization Agent customizes each application

### 4. Interview Anxiety
- **Pain**: "Get nervous during interviews"
- **Solution**: Mock Interview Agent provides practice rounds

### 5. Skill Gaps
- **Pain**: "Dream job requires skills I don't have"
- **Solution**: Skill Development Agent creates 3-month improvement plan

## Features

### Workflow
```
1. Story Mining → Discover highlights
2. Job Recommendation → Find direction
3. Resume Optimization → Tailor to JD
4. Mock Interview → Practice
5. Skill Development → Gap analysis & plan
```

### Core Strengths
- ✅ **Five-Agent Collaboration**: Complete job search coverage
- ✅ **Multiple Formats**: PDF/DOCX/HTML/Excel
- ✅ **Chinese Optimized**: Built-in fonts, no configuration needed
- ✅ **Practice-Oriented**: Designed for real scenarios
- ✅ **Progressive Guidance**: Reduces candidate stress

## Documentation

- **Full Documentation**: [GitHub Repository](https://github.com/Y1fe1-Yang/resume-assistant-skill)
- **User Guide**: [README.md](https://github.com/Y1fe1-Yang/resume-assistant-skill/blob/main/README.md)
- **Agent Details**: `references/` directory
- **Example Outputs**: `examples/` directory

## Version

**Current**: v1.0.0

## Links

- **Repository**: https://github.com/Y1fe1-Yang/resume-assistant-skill
- **Releases**: https://github.com/Y1fe1-Yang/resume-assistant-skill/releases
- **Issues**: https://github.com/Y1fe1-Yang/resume-assistant-skill/issues

---

## License

MIT License - See repository for details.

## Contributing

Contributions welcome! See [CONTRIBUTING.md](https://github.com/Y1fe1-Yang/resume-assistant-skill/blob/main/CONTRIBUTING.md) for guidelines.

---

**Made with ❤️ for job seekers**
