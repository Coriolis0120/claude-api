# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    SessionListResponse,
    SessionInfo,
    DeleteSessionResponse,
    ErrorResponse
)
from app.services.claude_service import claude_service

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse, responses={500: {"model": ErrorResponse}})
async def chat(request: ChatRequest):
    """
    发送消息给 Claude

    - **message**: 要发送的消息内容
    - **session_id**: 可选的会话 ID，用于多轮对话
    """
    try:
        response, session_id = await claude_service.chat(
            message=request.message,
            session_id=request.session_id
        )
        return ChatResponse(response=response, session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions():
    """列出所有会话"""
    sessions = claude_service.list_sessions()
    return SessionListResponse(
        sessions=[
            SessionInfo(
                id=s.id,
                created_at=s.created_at,
                message_count=s.message_count
            )
            for s in sessions
        ]
    )


@router.delete("/sessions/{session_id}", response_model=DeleteSessionResponse)
async def delete_session(session_id: str):
    """删除指定会话"""
    success = claude_service.delete_session(session_id)
    return DeleteSessionResponse(success=success)
