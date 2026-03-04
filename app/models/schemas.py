# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """聊天响应模型"""
    response: str
    session_id: str


class SessionInfo(BaseModel):
    """会话信息模型"""
    id: str
    created_at: datetime
    message_count: int


class SessionListResponse(BaseModel):
    """会话列表响应"""
    sessions: list[SessionInfo]


class DeleteSessionResponse(BaseModel):
    """删除会话响应"""
    success: bool


class ErrorResponse(BaseModel):
    """错误响应"""
    error: str
