#!/bin/sh
# Create the default F2F bucket in MinIO.
# Run as the `createbuckets` sidecar after `minio` becomes healthy.

set -eu

ALIAS="local"
ENDPOINT="${S3_ENDPOINT:-http://minio:9000}"
ACCESS_KEY="${MINIO_ROOT_USER:-f2fminio}"
SECRET_KEY="${MINIO_ROOT_PASSWORD:-f2fminio-secret}"
BUCKET="${S3_BUCKET:-f2f-assets}"

# Retry the alias set in case MinIO's healthcheck reports ready a hair early.
i=0
until mc alias set "${ALIAS}" "${ENDPOINT}" "${ACCESS_KEY}" "${SECRET_KEY}" >/dev/null 2>&1; do
  i=$((i + 1))
  if [ "${i}" -ge 30 ]; then
    echo "minio: alias set failed after 30 retries" >&2
    exit 1
  fi
  sleep 1
done

mc mb --ignore-existing "${ALIAS}/${BUCKET}"
echo "minio: bucket '${BUCKET}' ready at ${ENDPOINT}"
