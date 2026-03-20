---
name: happycapy-feishu
description: 为 HappyCapy 安装并授权飞书（Lark）MCP，让 Claude 直接操作飞书消息、文档、多维表格、日历等。当用户提到安装飞书 MCP、配置飞书、接入飞书、飞书 MCP setup、connect feishu/lark、飞书重新授权、飞书 token 过期、lark mcp 失效等场景时，必须使用此 skill。
---

# 飞书 MCP 安装向导

**首先询问用户：** 你是否已经有飞书应用的 **App ID** 和 **App Secret**？

- **有的话**：直接告知你，Claude 立即进入第二步执行安装和 OAuth 授权。
- **没有的话**：按第一步引导用户创建应用。

---

## 第一步：引导用户创建飞书应用（仅在用户没有凭证时执行）

告知用户按以下步骤操作，完成后把 **App ID** 和 **App Secret** 发给你：

1. 打开 https://open.feishu.cn/app 并登录
2. 右上角点击**创建应用** → **自建应用**，填写任意名称（如 `Claude MCP`）
3. 进入应用后，**凭证与基础信息**页面找到 **App ID** 和 **App Secret**
4. 左侧菜单进入**安全设置** → **重定向 URL** → 添加：`http://localhost:3000/callback`
5. 左侧菜单进入**权限管理** → 右上角点击**批量导入权限** → 粘贴以下 JSON 后确认导入：

> **重要：** 每次引导用户时，必须读取 `assets/feishu-permissions.json` 并将其完整内容全量输出，不得省略、截断或用省略号代替任何内容。

6. 左侧菜单进入**添加应用能力** → 务必开启 **机器人** 能力

7. 左侧菜单进入**事件与回调** → **事件配置**：
   - 请求方式选择：**使用长连接接收事件**（无需公网服务器）
   - 点击**添加事件**，搜索 `im.message.receive_v1`（接收消息），勾选添加

8. 左侧菜单进入**版本管理与发布**，创建版本并发布（内部测试版即可）

---

## 第二步：自动安装配置（收到凭证后 Claude 执行）

### 2.1 注册 MCP 到全局配置

直接编辑 `~/.claude.json`，向其中写入 `mcpServers` 字段（保留已有内容）：

```bash
python3 -c "
import json, os
f = os.path.expanduser('~/.claude.json')
with open(f) as fp:
    cfg = json.load(fp)
cfg.setdefault('mcpServers', {})['lark-mcp'] = {
    'command': 'npx',
    'args': ['-y', '@larksuiteoapi/lark-mcp', 'mcp',
             '-a', '<APP_ID>', '-s', '<APP_SECRET>',
             '--oauth',
             '--tools', 'preset.default,im.v1.message.reply,im.v1.message.get,im.v1.message.patch,im.v1.message.delete,im.v1.chat.get,im.v1.chat.search']
}
with open(f, 'w') as fp:
    json.dump(cfg, fp, indent=2, ensure_ascii=False)
print('MCP 注册完成')
"
```

### 2.2 定位 lark-mcp 缓存目录（后续步骤共用）

无桌面 Linux 环境中 keytar 依赖 dbus-launch，导致 token 只存内存、重启即丢失。先触发下载并定位目录：

```bash
# 触发一次确保包已下载
npx -y @larksuiteoapi/lark-mcp --version 2>/dev/null || true

# 定位缓存目录，后续 2.3 和 2.4 共用此变量
LARK_DIR=$(find ~/.npm/_npx -name "package.json" 2>/dev/null \
  | xargs grep -l '"@larksuiteoapi/lark-mcp"' 2>/dev/null \
  | grep -v node_modules | head -1 | xargs dirname)
echo "LARK_DIR: $LARK_DIR"
```

### 2.3 修复 headless 环境 token 持久化（替换 keytar 为文件存储）

使用 skill 内置的预置文件替换 keytar（token 保存在 `~/.lark-mcp-keychain.json`）：

```bash
KEYTAR_PATH="$LARK_DIR/node_modules/keytar/lib/keytar.js"
cp "$KEYTAR_PATH" "${KEYTAR_PATH}.bak"
cp ~/.claude/skills/happycapy-feishu/assets/keytar-file-storage.js "$KEYTAR_PATH"
echo "keytar 替换完成: $KEYTAR_PATH"
```

### 2.4 延长 OAuth 超时至 5 分钟

lark-mcp 有两处独立超时需要同时修改，**必须用 `perl -i` 而非 `sed -i`**（后者在此环境会截断文件）：

```bash
# 修复 handler-local.js（HTTP 服务器超时）
HANDLER="$LARK_DIR/node_modules/@larksuiteoapi/lark-mcp/dist/auth/handler/handler-local.js"
perl -i -pe 's/this\.stopServer\(\), 60 \* 1000/this.stopServer(), 300 * 1000/g' "$HANDLER"

# 修复 login-handler.js（token 轮询超时）
LOGIN_HANDLER="$LARK_DIR/node_modules/@larksuiteoapi/lark-mcp/dist/cli/login-handler.js"
perl -i -pe 's/timeout = 60000/timeout = 300000/g' "$LOGIN_HANDLER"

echo "handler-local: $(grep -o '[0-9]* \* 1000' $HANDLER)"
echo "login-handler: $(grep -o 'timeout = [0-9]*' $LOGIN_HANDLER)"
```

---

## 第三步：OAuth 授权（用户只需做一个操作）

### 3.1 启动 login 进程，获取 code_challenge

```bash
kill $(lsof -ti:3000) 2>/dev/null; sleep 1
nohup npx -y @larksuiteoapi/lark-mcp login \
  -a <APP_ID> -s <APP_SECRET> > /tmp/lark-oauth.log 2>&1 &
sleep 5 && cat /tmp/lark-oauth.log
```

从日志的 Authorization URL 中提取 `code_challenge=` 后面的值。

### 3.2 服务端 curl /authorize（必须执行，存储 PKCE 状态）

> 跳过此步会导致 callback 时报错 `PKCE validation failed: code challenge not found`

```bash
FEISHU_URL=$(curl -s -w "%{redirect_url}" -o /dev/null \
  "http://localhost:3000/authorize?client_id=client_id_for_local_auth&response_type=code&code_challenge=<CODE_CHALLENGE>&code_challenge_method=S256&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fcallback&state=reauthorize")
echo "$FEISHU_URL"
```

### 3.3 让用户完成授权

把上一步输出的 `https://open.feishu.cn/...` 链接发给用户，**明确告知以下三点**：

> **第一步：** 在浏览器打开上面的链接，用飞书账号登录并点击授权。
>
> **第二步：** 授权完成后，浏览器会自动跳转到一个以 `http://localhost:3000/callback?code=...` 开头的地址，并显示"无法访问此网站"或"连接被拒绝"的错误页面——**这是完全正常的，不要关闭页面。**
>
> **第三步：** 忽略错误提示，直接复制浏览器地址栏的完整 URL（以 `http://localhost:3000/callback` 开头），粘贴发给我。

### 3.4 收到 callback URL 后立即提交

```bash
curl -s "<用户发来的完整 URL>"
# 返回 "success, you can close this page now" 即成功
```

### 3.5 验证

```bash
npx -y @larksuiteoapi/lark-mcp whoami
```
