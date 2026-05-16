interface Props {
  reflection: any
}

export default function ReflectionBlock({
  reflection,
}: Props) {

  return (
    <div className="glass rounded-3xl p-6">

      <div className="mb-6 flex items-center gap-3">

        <div className="text-2xl">
          🔍
        </div>

        <h2 className="text-2xl font-semibold text-white">
          Reflection
        </h2>

      </div>

      <div className="space-y-6 text-zinc-300">

        <div>

          <h3 className="mb-2 font-medium text-violet-300">
            Contradictions
          </h3>

          <p>
            {
              reflection?.findings
                ?.contradictions ||
              'None detected.'
            }
          </p>

        </div>

        <div>

          <h3 className="mb-2 font-medium text-violet-300">
            Missing Information
          </h3>

          <p>
            {
              reflection?.findings
                ?.missing_info ||
              'No missing data.'
            }
          </p>

        </div>

        <div>

          <h3 className="mb-2 font-medium text-violet-300">
            Confidence
          </h3>

          <div className="inline-flex rounded-full border border-emerald-500/30 bg-emerald-500/10 px-4 py-2 font-semibold text-emerald-400">

            {
              reflection?.findings
                ?.confidence ||
              'UNKNOWN'
            }

          </div>

        </div>

        <div>

          <h3 className="mb-2 font-medium text-violet-300">
            Confidence Reasoning
          </h3>

          <p>
            {
              reflection?.findings
                ?.confidence_reasoning ||
              'No reasoning available.'
            }
          </p>

        </div>

      </div>
    </div>
  )
}