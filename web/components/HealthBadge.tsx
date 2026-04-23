'use client';

import { useEffect, useState } from 'react';
import { apiFetch } from '@/lib/api';

type Health = { status: string; db: string; redis: string; version: string };

export default function HealthBadge() {
  const [health, setHealth] = useState<Health | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    apiFetch<Health>('/healthz')
      .then((data) => {
        if (!cancelled) setHealth(data);
      })
      .catch((e: Error) => {
        if (!cancelled) setError(e.message);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (error) {
    return (
      <div className="flex items-center gap-2 rounded border border-red-500 px-3 py-2">
        <span className="h-2 w-2 rounded-full bg-red-500" />
        <span>API unreachable: {error}</span>
      </div>
    );
  }

  if (!health) {
    return (
      <div className="flex items-center gap-2 rounded border border-neutral-700 px-3 py-2">
        <span className="h-2 w-2 animate-pulse rounded-full bg-neutral-500" />
        <span>Checking…</span>
      </div>
    );
  }

  const ok = health.status === 'ok';
  return (
    <div
      className={`flex items-center gap-2 rounded border px-3 py-2 ${
        ok ? 'border-green-500' : 'border-yellow-500'
      }`}
    >
      <span className={`h-2 w-2 rounded-full ${ok ? 'bg-green-500' : 'bg-yellow-500'}`} />
      <span>
        api {health.status} · db {health.db} · redis {health.redis} · v{health.version}
      </span>
    </div>
  );
}
