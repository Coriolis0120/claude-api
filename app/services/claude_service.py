# -*- coding: utf-8 -*-
import asyncio
import os
import uuid
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class Session:
    """会话数据类"""
    id: str
    created_at: datetime
    message_count: int = 0


class ClaudeService:
    """Claude Code 服务封装"""

    def __init__(self, timeout: int = 120):
        self.timeout = timeout
        self.sessions: dict[str, Session] = {}

    def create_session(self) -> str:
        """创建新会话"""
        session_id = str(uuid.uuid4())[:8]
        self.sessions[session_id] = Session(
            id=session_id,
            created_at=datetime.now()
        )
        return session_id

    def get_or_create_session(self, session_id: Optional[str] = None) -> str:
        """获取或创建会话"""
        if session_id and session_id in self.sessions:
            return session_id
        return self.create_session()

    def list_sessions(self) -> list[Session]:
        """列出所有会话"""
        return list(self.sessions.values())

    def delete_session(self, session_id: str) -> bool:
        """删除会话"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    async def chat(self, message: str, session_id: Optional[str] = None) -> tuple[str, str]:
        """
        发送消息给 Claude 并获取回复

        Args:
            message: 用户消息
            session_id: 可选的会话 ID

        Returns:
            (response, session_id) 元组
        """
        # 获取或创建会话
        sid = self.get_or_create_session(session_id)

        # 调用 claude 命令
        try:
            # 复制环境变量，移除 CLAUDECODE 避免嵌套会话检测
            env = os.environ.copy()
            env.pop("CLAUDECODE", None)

            process = await asyncio.create_subprocess_exec(
                "claude",
                "-p",
                message,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.timeout
            )

            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                raise Exception(f"Claude command failed: {error_msg}")

            response = stdout.decode().strip()

            # 更新会话消息计数
            self.sessions[sid].message_count += 1

            return response, sid

        except asyncio.TimeoutError:
            raise Exception(f"Request timed out after {self.timeout} seconds")


# 全局服务实例
claude_service = ClaudeService()
