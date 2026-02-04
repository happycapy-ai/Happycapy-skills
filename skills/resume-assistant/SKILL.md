---
name: resume-assistant
description: 智能简历助手,通过五个AI代理提供全流程求职支持:(1)故事挖掘-发现经历亮点;(2)职位推荐-匹配合适岗位;(3)简历优化-针对JD定制内容;(4)模拟面试-实战演练与反馈;(5)能力提升-差距分析与计划。适用于简历创建、优化、面试准备、职业规划等求职相关任务。
---

# 简历助手

智能简历创建与优化系统，通过五个专业代理为学生提供全方位求职支持。

## ⚠️ 重要使用规则

生成简历文件（PDF/DOCX/HTML）时**必须使用** `scripts/` 目录下的脚本，严禁自行编写替代代码。如脚本失败，应解决环境问题而非绕过。

### 环境配置

首次使用前必须配置环境，否则脚本会失败。详见 `references/troubleshooting.md`。

```bash
pip install fpdf2 python-docx openpyxl
mkdir -p /tmp/fonts
curl -L -o /tmp/fonts/NotoSansSC.ttf \
  "https://github.com/notofonts/noto-cjk/raw/main/Sans/Variable/TTF/Subset/NotoSansSC-VF.ttf"
```

---

## 代理概览

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           简历助手系统                                    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                │
│  │ 1.故事挖掘   │───→│ 2.职位推荐   │───→│ 3.简历优化   │                │
│  │   代理       │    │   代理       │    │   代理       │                │
│  └──────────────┘    └──────────────┘    └──────────────┘                │
│         │                   │                   │                        │
│         │                   ↓                   ↓                        │
│         │            ┌──────────────┐    ┌──────────────┐                │
│         │            │ 5.能力提升   │    │ 4.模拟面试   │                │
│         │            │   代理       │    │   代理       │                │
│         │            └──────────────┘    └──────────────┘                │
│         │                   │                   │                        │
│         │                   ↓                   ↓                        │
│         │            [制定提升计划]       [反向优化简历]                  │
│         │                   │                   │                        │
│         └───────────────────┴───────────────────┘                        │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 代理1：故事挖掘代理

**触发词**：帮我挖掘经历、我不知道写什么、我没什么经历

**目标**：通过引导式对话，帮学生发现被忽略的有价值经历

**工作方式**：
1. 建立信任，降低学生压力
2. 多维度提问（学业、实践、社团、个人项目、生活挑战）
3. 用STAR框架深挖每个经历
4. 提炼可迁移技能

**输出**：《经历档案》，包含核心经历、潜在亮点、可迁移技能清单

**详细指南**：见 `references/agent-story-mining.md`

---

## 代理2：职位推荐代理

**触发词**：不知道找什么工作、适合什么岗位、职业方向

**目标**：基于学生背景和兴趣，推荐合适的职位方向

**工作方式**：
1. 收集学生档案、专业背景、兴趣偏好、硬性限制
2. 从技能匹配度、兴趣契合度、发展潜力三个维度评估
3. 按匹配度分级推荐（强烈推荐、值得考虑、拓展方向）

**输出**：《职位推荐报告》，每个推荐包含：适合原因、典型公司、技能差距、入门建议

**详细指南**：见 `references/agent-job-recommendation.md`

---

## 代理3：简历优化代理

**触发词**：优化简历、根据JD改简历、投这个岗位

**目标**：根据目标岗位JD，针对性优化简历内容

**工作方式**：
1. 解析JD提取关键要求和关键词
2. 匹配分析学生经历与JD要求
3. 重写经历描述，融入关键词，量化成果
4. 优化ATS通过率

**输出**：《简历优化报告》+ 标准JSON格式简历（供后续脚本使用）

**详细指南**：见 `references/agent-resume-optimization.md`

---

## 代理4：模拟面试代理

**触发词**：模拟面试、面试准备、帮我练习面试

**目标**：基于简历提问，评估回答，反向优化简历

**面试模式**：常规面试、压力面试、针对性训练

**工作方式**：
1. 开场自我介绍
2. 针对简历各部分深挖细节
3. STAR框架行为面试问题
4. 评估回答质量，识别简历弱点

**输出**：面试反馈 + 简历修改建议 + 更新版简历

**详细指南**：见 `references/agent-mock-interview.md`

---

## 代理5：能力提升代理

**触发词**：我想冲这个岗位、能力不够怎么办、怎么提升、差距分析

**目标**：分析与目标岗位的差距，制定具体可执行的提升计划

**差距分类**：
- A类硬伤（学历、年限）→ 诚实告知，建议备选
- B类可补（技能、项目经验）→ 制定学习计划
- C类易补（工具使用、面试技巧）→ 短期突击

**工作方式**：
1. 诊断差距并评估可行性
2. 制定分阶段提升计划
3. 推荐学习资源和项目实践
4. 设定里程碑检查点

**输出**：《能力提升规划报告》（JSON格式，可生成Excel追踪表）

**详细指南**：见 `references/agent-growth-planning.md`

---

## 快速入口

| 用户需求 | 使用代理 |
|---------|---------|
| "我不知道简历写什么" | 代理1 → 代理3 |
| "不知道找什么工作" | 代理1 → 代理2 |
| "帮我优化这份简历" | 代理3 |
| "我要投XX岗位" | 代理3（需要JD） |
| "帮我准备面试" | 代理4 |
| "我想冲XX岗位但能力不够" | 代理5 |
| "完整求职辅导" | 代理1 → 代理2 → 代理5 → 代理3 → 代理4 |

---

## 输出文件生成

代理完成后，使用以下脚本生成最终文件。**必须使用提供的脚本**，不得自行实现。

### 网页简历（推荐）⭐

```bash
python scripts/current/create_web_resume.py --data resume_data.json --output resume.html
```

现代响应式设计，支持深色模式，适合在线分享和投递互联网公司。

### PDF简历

```bash
python scripts/current/create_pdf_resume.py --data resume_data.json --output resume.pdf
```

正式投递、打印、邮件附件。需要先配置字体（见环境配置）。

### DOCX简历

```bash
python scripts/current/create_docx_resume.py output.docx --data resume_data.json
```

需要继续编辑或传统企业投递。

### Excel能力提升追踪表

```bash
python scripts/current/create_growth_tracker.py --plan growth_plan.json --output tracker.xlsx
```

包含每周任务清单、进度追踪、里程碑检查。

---

## 数据格式

代理3和代理5会自动生成标准JSON格式数据。

**简历数据**：`resume_data.json` - 包含个人信息、教育、项目、经验、技能等

**能力提升计划**：`growth_plan.json` - 包含目标岗位、阶段计划、任务、资源等

详细格式说明见 `references/data-formats.md`，示例文件见 `examples/` 目录。

---

## 故障排查

遇到问题时，查阅 `references/troubleshooting.md` 获取解决方案。

常见问题：
- PDF生成失败 → 检查字体文件
- 脚本找不到 → 检查工作目录
- JSON格式错误 → 参考示例文件
- 依赖包缺失 → 安装所需包

---

## 参考资源

### 代理详细指南
- `references/agent-story-mining.md` - 故事挖掘代理完整流程
- `references/agent-job-recommendation.md` - 职位推荐代理匹配算法
- `references/agent-resume-optimization.md` - 简历优化代理优化原则
- `references/agent-mock-interview.md` - 模拟面试代理提问技巧
- `references/agent-growth-planning.md` - 能力提升代理规划方法

### 写作与参考
- `references/writing-guide.md` - 简历写作指南
- `references/industry-keywords.md` - 行业关键词参考

### 技术文档
- `references/troubleshooting.md` - 故障排查完整指南
- `references/data-formats.md` - JSON数据格式详细说明

### 示例文件
- `examples/resume_data_example.json` - 简历数据标准格式
- `examples/fresh_graduate_example.json` - 应届生简历示例
- `examples/experienced_example.json` - 有经验求职者示例
- `examples/growth_plan_example.json` - 能力提升计划示例
- `examples/USAGE_GUIDE.md` - 使用指南

### 资源文件
- `assets/templates/*.html` - 简历HTML模板（用于输出，不加载到上下文）
- `scripts/current/*.py` - 简历生成脚本（可执行，必要时可读取）
