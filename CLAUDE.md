# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个将 Claude Code CLI 封装为 Web API 的 FastAPI 服务。通过 SSH 隧道安全访问。

## 常用命令

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
./run.sh

# 或直接使用 uvicorn
uvicorn app.main:app --host 127.0.0.1 --port 8000

# 环境变量配置
HOST=127.0.0.1 PORT=8000 ./run.sh
```

## 架构

```
app/
├── main.py              # FastAPI 应用入口，配置 CORS、静态文件、路由
├── routes/
│   └── chat.py          # API 路由：/api/chat, /api/sessions
├── services/
│   └── claude_service.py # 核心服务：调用 claude CLI 命令
└── models/
    └── schemas.py       # Pydantic 请求/响应模型
static/
└── index.html           # Web 聊天界面
```

## 核心实现要点

### Claude CLI 调用
`claude_service.py` 通过 `asyncio.create_subprocess_exec` 调用 `claude -p <message>` 命令。关键：必须移除 `CLAUDECODE` 环境变量以避免嵌套会话检测：

```python
env = os.environ.copy()
env.pop("CLAUDECODE", None)
```

### 会话管理
会话存储在内存字典中（`self.sessions`），每个会话包含 id、创建时间和消息计数。注意：当前实现重启后会话数据会丢失。

### API 端点
- `POST /api/chat` - 发送消息，可选 `session_id` 用于多轮对话
- `GET /api/sessions` - 列出所有会话
- `DELETE /api/sessions/{session_id}` - 删除会话
- `GET /health` - 健康检查
- `GET /docs` - FastAPI 自动生成的 API 文档

## 默认配置

- 监听地址: `127.0.0.1:8000`
- 请求超时: 120 秒
