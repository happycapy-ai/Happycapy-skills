---
name: office-status-ui
description: HappyCapy 办公室状态可视化 - 启动像素风格虚拟办公室，水豚角色实时显示 AI 工作状态。Use when the user says /office, 启动办公室, 办公室状态, or wants to visualize AI working status.
tools: Bash, Read, Write
---

# Office Status UI Skill

启动 HappyCapy 豪华像素办公室，实时可视化 AI 助手的工作状态。水豚角色会根据操作在不同区域移动。

## When to Use

- 用户说 `/office` 或 `启动办公室`
- 用户想要可视化 AI 工作状态
- 用户想要一个有趣的状态监控界面

## 状态映射

| 操作类型 | 状态 | 水豚位置 |
|---------|------|---------|
| Read/Glob/Grep/WebFetch | researching | 图书区 |
| Write/Edit | writing | CEO办公桌 |
| Bash/Task | executing | 服务器机房 |
| 空闲 | idle | 休息沙发区 |

## 执行步骤

### 步骤 1: 克隆仓库（如果不存在）

```bash
OFFICE_DIR="$HOME/.claude/office-ui"
if [ ! -d "$OFFICE_DIR" ]; then
  echo "正在下载办公室 UI..."
  git clone https://github.com/AchengBusiness/happycapy-office-ui.git "$OFFICE_DIR"
fi
```

### 步骤 2: 启动服务器

```bash
# 停止旧进程
lsof -ti:18791 | xargs kill -9 2>/dev/null || true
sleep 1

# 启动服务器
cd "$HOME/.claude/office-ui/backend"
nohup python app.py > /dev/null 2>&1 &
sleep 2

# 验证
curl -s localhost:18791/health
```

### 步骤 3: 导出端口

```bash
/app/export-port.sh 18791
```

### 步骤 4: 返回结果

告诉用户：
1. 预览 URL
2. 状态映射说明
3. 保持页面打开观察水豚移动

## 实时状态更新

在后续操作中，可选择性调用状态更新：

```bash
$HOME/.claude/office-ui/update_status.sh <工具名> <描述>
```

例如：
- `update_status.sh Read "正在读取配置文件"`
- `update_status.sh Write "正在编写新功能"`
- `update_status.sh Bash "正在执行测试"`

## 示例响应

```
办公室 UI 已启动！

预览地址: https://18791-xxx-preview.happycapy.ai

水豚状态映射：
- 读取/搜索文件 → 图书区
- 编写/编辑代码 → CEO办公桌
- 执行命令/任务 → 服务器机房
- 空闲/思考 → 休息沙发区

保持页面打开，水豚会跟着我的操作实时移动！
```

## 关闭办公室

```bash
lsof -ti:18791 | xargs kill -9 2>/dev/null
echo "办公室已关闭"
```

## GitHub 仓库

https://github.com/AchengBusiness/happycapy-office-ui
