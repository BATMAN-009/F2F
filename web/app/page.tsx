import HealthBadge from '@/components/HealthBadge';

export default function Page() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 p-8">
      <h1 className="text-4xl font-semibold tracking-tight">F2F</h1>
      <p className="text-neutral-400">Idea → physical product</p>
      <HealthBadge />
    </main>
  );
}
