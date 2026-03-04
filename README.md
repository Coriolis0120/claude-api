# Claude Code Web API

将 Claude Code 封装为 Web API 服务，通过 SSH 隧道安全访问。

## 快速开始

### 1. 安装依赖

```bash
cd /root/myFiles/claude-api
pip install -r requirements.txt
```

### 2. 启动服务（服务器端）

```bash
./run.sh
```

### 3. 建立 SSH 隧道（Windows 端）

```powershell
# 复制 connect.ps1 到 Windows 主机
# 运行：
.\connect.ps1 -Server user@服务器IP

# 或手动执行：
ssh -L 8000:127.0.0.1:8000 user@服务器IP -N
```

### 4. 访问

- Web 界面: http://localhost:8000
- API 文档: http://localhost:8000/docs

## API 接口

### POST /api/chat

发送消息给 Claude。

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好", "session_id": "可选"}'
```

响应:
```json
{
  "response": "你好！有什么可以帮你的吗？",
  "session_id": "abc12345"
}
```

### GET /api/sessions

列出所有会话。

### DELETE /api/sessions/{session_id}

删除指定会话。

## 架构

```
Windows 主机              服务器
┌──────────────┐        ┌──────────────┐
│ 浏览器       │        │              │
│ localhost:8000 │─SSH──▶│ 127.0.0.1:8000 │
└──────────────┘  隧道  │    ↓         │
                       │ Claude API   │
                       └──────────────┘
```

## 配置

环境变量:
- `HOST`: 监听地址，默认 127.0.0.1
- `PORT`: 监听端口，默认 8000
