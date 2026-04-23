"""Smoke ping task — verifies worker liveness and Blender availability."""

from __future__ import annotations

import shutil
import subprocess

from worker.celery_app import app


def _blender_version() -> str:
    blender = shutil.which("blender")
    if blender is None:
        return "blender: unavailable"
    try:
        result = subprocess.run(
            [blender, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        first_line = (result.stdout or result.stderr or "").splitlines()[:1]
        return first_line[0].strip() if first_line else "blender: unknown"
    except (subprocess.TimeoutExpired, OSError):
        return "blender: error"


@app.task(name="tasks.ping")
def ping() -> str:
    return f"pong | {_blender_version()}"
