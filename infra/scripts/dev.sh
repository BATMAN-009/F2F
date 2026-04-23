#!/usr/bin/env bash
# F2F dev helper (bash) — thin wrapper around docker compose.
# Usage:
#   ./infra/scripts/dev.sh up           # start stack (detached)
#   ./infra/scripts/dev.sh down         # stop stack
#   ./infra/scripts/dev.sh logs [svc]   # tail logs, optionally a single service
#   ./infra/scripts/dev.sh migrate      # run `alembic upgrade head` inside api
#   ./infra/scripts/dev.sh shell [svc]  # open a shell inside a service (default: api)

set -euo pipefail

CMD="${1:-up}"
SVC="${2:-}"

# Run commands from the repo root (parent of infra/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}/../.."

case "${CMD}" in
  up)
    docker compose up -d --build
    ;;
  down)
    docker compose down
    ;;
  logs)
    if [ -n "${SVC}" ]; then docker compose logs -f "${SVC}"; else docker compose logs -f; fi
    ;;
  migrate)
    docker compose exec api alembic upgrade head
    ;;
  shell)
    docker compose exec "${SVC:-api}" /bin/bash
    ;;
  *)
    echo "Unknown command: ${CMD}. Expected: up | down | logs | migrate | shell" >&2
    exit 2
    ;;
esac
