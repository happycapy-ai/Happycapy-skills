# Office Status UI

HappyCapy 办公室状态可视化 - 实时显示 AI 助手的工作状态

## Preview

启动一个像素风格的虚拟办公室，水豚角色会根据 AI 的实时操作在不同区域移动。

## Features

- **豪华像素办公室** - 游戏风格 + CAD 平面图布局
- **实时状态显示** - 水豚跟随 AI 操作移动
- **多区域映射**:
  - 图书区 - 读取/搜索文件
  - CEO办公桌 - 编写/编辑代码
  - 服务器机房 - 执行命令/任务
  - 休息沙发区 - 空闲待命

## Usage

在任何工作区中说：

```
/office
```

或者：

```
启动办公室
办公室状态
```

## How It Works

1. 首次使用时从 GitHub 克隆仓库
2. 启动 Flask 后端服务器
3. 导出端口提供预览 URL
4. 实时轮询状态并更新水豚位置

## Screenshots

水豚在豪华像素办公室中根据 AI 操作实时移动：
- 读取文件时 → 移动到图书区
- 编写代码时 → 移动到办公桌
- 执行命令时 → 移动到服务器机房
- 空闲时 → 回到休息沙发区

## Repository

https://github.com/AchengBusiness/happycapy-office-ui

## Author

AchengBusiness
