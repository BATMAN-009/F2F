"""Smoke task dispatch endpoints."""

from __future__ import annotations

from typing import Any

from celery.result import AsyncResult
from fastapi import APIRouter

from app.celery_app import celery_app

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/ping")
def dispatch_ping() -> dict[str, str]:
    result = celery_app.send_task("tasks.ping")
    return {"task_id": result.id}


@router.get("/ping/{task_id}")
def get_ping(task_id: str) -> dict[str, Any]:
    result = AsyncResult(task_id, app=celery_app)
    payload: dict[str, Any] = {"task_id": task_id, "status": result.status}
    if result.ready():
        payload["result"] = result.result if result.successful() else str(result.result)
    return payload
