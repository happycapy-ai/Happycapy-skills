# Film Creator | AI 电影制作助手

**AI-powered film creation assistant that transforms a single sentence or image into a complete 30-second cinematic film**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node Version](https://img.shields.io/badge/node-%3E%3D24.0.0-brightgreen)](https://nodejs.org/)

**[English](#english) | [中文](#中文)**

---

<h2 id="english">🇬🇧 English</h2>

## What is Film Creator?

Film Creator is an **end-to-end AI film production assistant** that transforms your ideas into professional films:

1. **Takes your concept** - Text prompt or image
2. **Generates screenplay** - Professional 5-scene structure with camera directions
3. **Creates video scenes** - High-quality AI-generated video for each scene
4. **Assembles the film** - Combines scenes into a polished 30-second film

### Perfect For

- 🎥 Social media content creators
- 📱 Marketing professionals
- 🎬 Filmmakers and storytellers
- 🤖 AI enthusiasts
- ⚡ Anyone who wants to create videos quickly

## Features

### Film Production Pipeline

1. **Creative Analysis**
   - Analyzes text prompt or image
   - Extracts core creative elements
   - Determines genre, mood, and style

2. **Screenplay Generation**
   - Professional 5-scene structure
   - Three-act narrative arc
   - Camera directions and shot descriptions
   - Scene transitions and visual continuity

3. **Video Production**
   - Multi-scene generation
   - Cinematic quality with AI models
   - Smart prompting for video generation
   - Visual consistency across scenes

4. **Film Assembly**
   - Seamless scene stitching with FFmpeg
   - Smooth transitions
   - Precise 30-second duration
   - Quality preservation

### Technical Features

- 🎭 **Professional Screenplay** - 5-scene structure with detailed camera work
- 🎥 **Multi-Model Support** - Google Veo, OpenAI Sora, BytePlus Seedance
- 🎨 **Style Control** - Specify genre, mood, and visual style
- 📐 **Flexible Aspect Ratios** - 16:9, 9:16, 1:1, and custom
- 🖼️ **Image Input** - Use images as creative inspiration
- 🎬 **Automatic Assembly** - FFmpeg-powered scene combination

## Installation

### Prerequisites

- Node.js 24+ (pre-installed in HappyCapy)
- FFmpeg (pre-installed in HappyCapy)
- AI_GATEWAY_API_KEY environment variable

### Option 1: From Skills Collection

```bash
git clone https://github.com/Y1fe1-Yang/Happycapy-skills.git
cp -r Happycapy-skills/skills/film-creator ~/.claude/skills/
```

### Option 2: From Original Repository

```bash
git clone https://github.com/Y1fe1-Yang/film-creator-skill.git
cd film-creator-skill
npm install @ffmpeg-installer/ffmpeg @ffprobe-installer/ffprobe fluent-ffmpeg
```

## Quick Start

### Basic Usage

```bash
# Create a film from text
node scripts/create_film.js "A lonely robot discovers the last flower on Earth"

# Create vertical video for social media
node scripts/create_film.js "A street dancer performs in the rain" --aspect-ratio "9:16"

# Use premium model
node scripts/create_film.js "A cyberpunk detective story" --model "openai/sora-2-pro"
```

### With Claude Code

After installation, simply ask:

```
"Create a film about a time traveler"
"Generate a 30-second movie from this idea"
"Make a cinematic video about space exploration"
"创作一部关于未来城市的电影"
```

## Supported Models

| Model | Best For | Duration per Scene |
|-------|----------|-------------------|
| `google/veo-3.1-generate-preview` | Balanced quality and reliability (Recommended) | 5-6 seconds |
| `openai/sora-2` | Cinematic quality with complex scenes | 4-6 seconds |
| `openai/sora-2-pro` | Professional-grade cinematic output | 4-6 seconds |
| `byteplus/seedance-1-0-pro` | Flexible aspect ratios | 5-6 seconds |

## Use Cases

### Content Creation
- **Social Media**: Quick 30-second stories for Instagram, TikTok, YouTube Shorts
- **Marketing**: Product demos, brand stories, promotional videos
- **Education**: Visual storytelling for teaching concepts

### Creative Projects
- **Film Concepts**: Rapid prototyping of film ideas
- **Storyboarding**: Visual proof-of-concepts
- **AI Art**: Experimental video art projects

### Professional Work
- **Pitch Videos**: Quick concept videos for presentations
- **Ad Campaigns**: Test different creative directions
- **Content Strategy**: Rapid A/B testing of video concepts

## Documentation

- **Full Documentation**: [GitHub Repository](https://github.com/Y1fe1-Yang/film-creator-skill)
- **Complete Guide**: [SKILL.md](https://github.com/Y1fe1-Yang/film-creator-skill/blob/main/SKILL.md)
- **Usage Examples**: [examples.md](https://github.com/Y1fe1-Yang/film-creator-skill/blob/main/references/examples.md)

## Version

**Current**: v1.0.0

## Links

- **Repository**: https://github.com/Y1fe1-Yang/film-creator-skill
- **Issues**: https://github.com/Y1fe1-Yang/film-creator-skill/issues

---

<h2 id="中文">🇨🇳 中文</h2>

## 简介

Film Creator 是一个**端到端的 AI 电影制作助手**，将你的想法转化为专业影片：

1. **输入概念** - 文字描述或图片
2. **生成剧本** - 专业的 5 场景结构和镜头指导
3. **创建视频场景** - 为每个场景生成高质量 AI 视频
4. **组装电影** - 将场景组合成精美的 30 秒影片

### 适用人群

- 🎥 社交媒体内容创作者
- 📱 营销专业人士
- 🎬 电影制作人和故事讲述者
- 🤖 AI 爱好者
- ⚡ 任何想快速创建视频的人

## 功能特性

### 电影制作流程

1. **创意分析**
   - 分析文字提示或图片
   - 提取核心创意元素
   - 确定类型、情绪和风格

2. **剧本生成**
   - 专业的 5 场景结构
   - 三幕式叙事弧线
   - 镜头指导和拍摄描述
   - 场景过渡和视觉连续性

3. **视频制作**
   - 多场景生成
   - AI 模型打造电影级质量
   - 智能视频生成提示
   - 场景间视觉一致性

4. **电影组装**
   - 使用 FFmpeg 无缝拼接场景
   - 流畅过渡
   - 精确 30 秒时长
   - 保持画质

### 技术特性

- 🎭 **专业剧本** - 5 场景结构，详细镜头设计
- 🎥 **多模型支持** - Google Veo、OpenAI Sora、BytePlus Seedance
- 🎨 **风格控制** - 指定类型、情绪和视觉风格
- 📐 **灵活宽高比** - 16:9、9:16、1:1 及自定义
- 🖼️ **图片输入** - 使用图片作为创意灵感
- 🎬 **自动组装** - FFmpeg 驱动的场景组合

## 安装

### 前置要求

- Node.js 24+（HappyCapy 已预装）
- FFmpeg（HappyCapy 已预装）
- AI_GATEWAY_API_KEY 环境变量

### 方式 1: 从技能集合安装

```bash
git clone https://github.com/Y1fe1-Yang/Happycapy-skills.git
cp -r Happycapy-skills/skills/film-creator ~/.claude/skills/
```

### 方式 2: 从原始仓库安装

```bash
git clone https://github.com/Y1fe1-Yang/film-creator-skill.git
cd film-creator-skill
npm install @ffmpeg-installer/ffmpeg @ffprobe-installer/ffprobe fluent-ffmpeg
```

## 快速开始

### 基础用法

```bash
# 从文字创建电影
node scripts/create_film.js "一个孤独的机器人发现了地球上最后一朵花"

# 创建社交媒体竖屏视频
node scripts/create_film.js "一个街舞者在雨中表演" --aspect-ratio "9:16"

# 使用高级模型
node scripts/create_film.js "一个赛博朋克侦探故事" --model "openai/sora-2-pro"
```

### 与 Claude Code 配合

安装后，直接询问：

```
"创作一部关于时间旅行者的电影"
"生成一个 30 秒的太空探索影片"
"Make a film about a lonely robot"
```

## 支持的模型

| 模型 | 适用场景 | 每场景时长 |
|------|----------|-----------|
| `google/veo-3.1-generate-preview` | 质量与可靠性平衡（推荐） | 5-6 秒 |
| `openai/sora-2` | 复杂场景的电影级质量 | 4-6 秒 |
| `openai/sora-2-pro` | 专业级电影输出 | 4-6 秒 |
| `byteplus/seedance-1-0-pro` | 灵活的宽高比 | 5-6 秒 |

## 使用场景

### 内容创作
- **社交媒体**: Instagram、TikTok、YouTube Shorts 的 30 秒快速故事
- **营销**: 产品演示、品牌故事、宣传视频
- **教育**: 概念教学的视觉叙事

### 创意项目
- **电影概念**: 快速原型化电影想法
- **故事板**: 视觉概念验证
- **AI 艺术**: 实验性视频艺术项目

### 专业工作
- **宣传视频**: 演示用快速概念视频
- **广告活动**: 测试不同创意方向
- **内容策略**: 视频概念的快速 A/B 测试

## 文档

- **完整文档**: [GitHub 仓库](https://github.com/Y1fe1-Yang/film-creator-skill)
- **完整指南**: [SKILL.md](https://github.com/Y1fe1-Yang/film-creator-skill/blob/main/SKILL.md)
- **使用示例**: [examples.md](https://github.com/Y1fe1-Yang/film-creator-skill/blob/main/references/examples.md)
- **中文指南**: [USAGE_GUIDE.md](https://github.com/Y1fe1-Yang/film-creator-skill/blob/main/USAGE_GUIDE.md)

## 版本

**当前版本**: v1.0.0

## 链接

- **仓库**: https://github.com/Y1fe1-Yang/film-creator-skill
- **Issues**: https://github.com/Y1fe1-Yang/film-creator-skill/issues

---

## License

MIT License - See repository for details.

## Contributing

Contributions welcome! See [GitHub](https://github.com/Y1fe1-Yang/film-creator-skill) for guidelines.

---

**Made with ❤️ for storytellers and creators**
