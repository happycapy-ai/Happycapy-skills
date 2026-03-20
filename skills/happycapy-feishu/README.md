# happycapy-feishu

让 Claude 直接操作飞书——发消息、写文档、管理多维表格，一句话搞定。

Connect Claude to Feishu (Lark) via MCP — send messages, read/write docs, manage Bitable, all in one conversation.

---

## 功能 / Features

| 类别 | 工具 |
|------|------|
| 即时通讯 / IM | 发送消息、回复消息、创建群组、搜索会话 |
| 多维表格 / Bitable | 创建表格、增删改查记录、管理字段 |
| 文档 / Docx | 读取文档内容、追加内容 |
| 知识库 / Wiki | 搜索节点 |
| 通讯录 / Contact | 按手机号/邮件查找用户 |

---

## 安装 / Installation

```bash
# 将 skill 文件夹复制到 Claude Code skills 目录
# Copy the skill folder to your Claude Code skills directory
cp -r happycapy-feishu ~/.claude/skills/
```

需要 HappyCapy + Claude Code 环境。/ Requires HappyCapy + Claude Code.

---

## 使用 / Usage

直接对 Claude 说 / Just tell Claude:

> 安装飞书 MCP

> connect feishu

Claude 会引导你完成飞书应用创建和 OAuth 授权，全程只需：
1. 提供 App ID 和 App Secret
2. 点一个飞书授权链接，把浏览器地址栏的 URL 发回来

Claude will guide you through Feishu app setup and OAuth authorization. You only need to:
1. Provide your App ID and App Secret
2. Click the Feishu auth link, then paste the callback URL back

---

## 前提条件 / Prerequisites

- [飞书](https://www.feishu.cn) 账号及自建应用凭证（App ID + App Secret）
- [Feishu](https://www.larksuite.com) account with a self-built app (App ID + App Secret)

如何创建飞书应用，安装后告诉 Claude "安装飞书 MCP" 即可获得引导。

For app creation instructions, just say "安装飞书 MCP" to Claude after installing the skill.

---

## License

MIT © HappyCapy Team
