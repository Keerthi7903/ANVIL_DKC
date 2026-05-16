interface Props {
  workflows: any[]
}

export default function StatsBar({
  workflows,
}: Props) {

  const total = workflows.length

  const active = workflows.filter(
    (w) => w.status === 'running'
  ).length

  const autonomous = workflows.filter(
    (w) => w.decision
  ).length

  const avgResolution = workflows.length
    ? (
        workflows.reduce(
          (acc, w) =>
            acc + (w.duration || 0),
          0
        ) / workflows.length
      ).toFixed(1)
    : '0'

  const stats = [
    {
      label: 'Total Workflows',
      value: total,
    },
    {
      label: 'Active Now',
      value: active,
    },
    {
      label: 'Autonomous Actions',
      value: autonomous,
    },
    {
      label: 'Avg Resolution',
      value: `${avgResolution}ms`,
    },
  ]

  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

      {stats.map((item) => (
        <div
          key={item.label}
          className="glass rounded-3xl p-5"
        >
          <p className="text-sm text-zinc-400">
            {item.label}
          </p>

          <h2 className="mt-3 text-4xl font-bold text-white">
            {item.value}
          </h2>
        </div>
      ))}

    </div>
  )
}