interface Props {
  decision: string
  summary: string
}

export default function DecisionBanner({
  decision,
  summary,
}: Props) {

  return (
    <div className="overflow-hidden rounded-3xl border border-violet-500/20 bg-gradient-to-r from-violet-700/20 to-fuchsia-700/10 p-8">

      <p className="text-sm uppercase tracking-[0.3em] text-violet-300">
        System Decision
      </p>

      <h1 className="mt-3 text-4xl font-bold text-white">
        {decision?.replaceAll(
          '_',
          ' '
        ).toUpperCase()}
      </h1>

      <p className="mt-4 max-w-3xl text-zinc-300">
        {summary}
      </p>

    </div>
  )
}