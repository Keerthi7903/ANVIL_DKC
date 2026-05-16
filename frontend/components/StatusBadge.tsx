interface Props {
  status: string
}

export default function StatusBadge({ status }: Props) {
  const styles: Record<string, string> = {
    running:
      'bg-amber-500/15 text-amber-300 border border-amber-500/30 animate-pulse',
    completed:
      'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30',
    failed:
      'bg-red-500/15 text-red-300 border border-red-500/30',
    pending:
      'bg-zinc-500/15 text-zinc-300 border border-zinc-500/30',
  }

  return (
    <div
      className={`w-fit rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wider ${styles[status]}`}
    >
      {status}
    </div>
  )
}