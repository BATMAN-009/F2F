# F2F Worker

Celery worker. Runs Blender headless for format conversion (from Feature 10).

```bash
uv sync
uv run celery -A worker.celery_app worker -l INFO
uv run pytest
```
