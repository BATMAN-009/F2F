"""Celery client used by the API to dispatch tasks to the worker pool."""

from __future__ import annotations

from celery import Celery

from app.config import get_settings

_settings = get_settings()

celery_app = Celery(
    "f2f",
    broker=_settings.redis_url,
    backend=_settings.redis_url,
)
celery_app.conf.task_default_queue = "f2f"
