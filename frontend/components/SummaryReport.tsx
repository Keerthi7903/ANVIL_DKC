interface Props {
  summary: string
  research?: any
}

export default function SummaryReport({
  summary,
  research,
}: Props) {

  return (
    <div className="space-y-8">

      {/* INCIDENT SUMMARY */}

      <div className="glass rounded-3xl p-6">

        <h2 className="mb-6 text-2xl font-semibold text-white">
          Incident Summary
        </h2>

        <div className="prose prose-invert max-w-none whitespace-pre-wrap text-zinc-300">

          {summary}

        </div>

      </div>

      {/* AI RESEARCH INSIGHTS */}

      {research && (

        <div className="glass rounded-3xl p-6">

          <div className="mb-6 flex items-center gap-3">

            <div className="text-2xl">
              🧠
            </div>

            <h2 className="text-2xl font-semibold text-white">
              AI Research Insights
            </h2>

          </div>

          <div className="space-y-5">

            {/* SYNTHESIS */}

            <div>

              <p className="mb-2 text-sm uppercase tracking-wide text-violet-300">
                Engineering Analysis
              </p>

              <div className="rounded-2xl border border-violet-500/20 bg-violet-500/5 p-4 text-zinc-300">

                {
                  research.findings
                    ?.synthesis
                }

              </div>

            </div>

            {/* SEARCH QUERIES */}

            {research.findings
              ?.search_queries
              ?.length > 0 && (

              <div>

                <p className="mb-3 text-sm uppercase tracking-wide text-violet-300">
                  External Research Queries
                </p>

                <div className="flex flex-wrap gap-2">

                  {research.findings
                    .search_queries
                    .map(
                      (
                        query: string,
                        index: number
                      ) => (

                        <div
                          key={index}
                          className="rounded-full border border-white/10 bg-black/20 px-4 py-2 text-sm text-zinc-300"
                        >
                          {query}
                        </div>

                      )
                    )}

                </div>

              </div>

            )}

            {/* RESEARCH RESULT COUNT */}

            <div className="flex items-center justify-between rounded-2xl border border-white/5 bg-black/20 p-4">

              <div>

                <p className="text-sm text-zinc-500">
                  External Intelligence Sources
                </p>

                <h3 className="mt-1 text-xl font-semibold text-white">

                  {
                    research.findings
                      ?.search_results
                      ?.length || 0
                  }

                </h3>

              </div>

              <div className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-4 py-2 text-sm font-medium text-emerald-400">

                Tavily Connected

              </div>

            </div>

          </div>

        </div>

      )}

    </div>
  )
}