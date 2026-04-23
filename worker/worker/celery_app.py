"""Celery worker app — registered tasks live under worker.tasks."""

from __future__ import annotations

from celery import Celery

from worker.config import get_settings

_settings = get_settings()

app = Celery(
    "f2f",
    broker=_settings.redis_url,
    backend=_settings.redis_url,
    include=["worker.tasks.ping"],
)
app.conf.task_default_queue = "f2f"
