'use client'

import {
  use,
  useEffect,
  useState
} from 'react'

import Navbar from '@/components/Navbar'
import DecisionBanner from '@/components/DecisionBanner'
import ReflectionBlock from '@/components/ReflectionBlock'
import SummaryReport from '@/components/SummaryReport'
import LiveAgentTimeline from '@/components/LiveAgentTimeline'

interface Props {
  params: Promise<{
    id: string
  }>
}

export default function IncidentPage({
  params,
}: Props) {

  const resolvedParams = use(params)

  const [workflow, setWorkflow] =
    useState<any>(null)

  const [loading, setLoading] =
    useState(true)

  useEffect(() => {

    const fetchWorkflow =
      async () => {

        try {

          const response =
            await fetch(
              `http://localhost:8000/workflows/${resolvedParams.id}`
            )

          const data =
            await response.json()

          setWorkflow(data)

        } catch (error) {

          console.error(
            'Failed to fetch workflow:',
            error
          )

        } finally {

          setLoading(false)

        }
      }

    fetchWorkflow()

  }, [resolvedParams.id])

  if (loading) {

    return (
      <main className="min-h-screen flex items-center justify-center text-white text-2xl">
        Loading incident...
      </main>
    )

  }

  if (
    !workflow ||
    workflow.error
  ) {

    return (
      <main className="min-h-screen flex items-center justify-center text-red-400 text-2xl">
        Workflow not found.
      </main>
    )

  }

  const reflection =
    workflow.agent_results?.find(
      (agent: any) =>
        agent.agent_name === 'reflection'
    )

  return (
    <main className="min-h-screen">

      <Navbar />

      <section className="mx-auto max-w-7xl px-6 py-10">

        <div className="glass mb-8 rounded-3xl p-8">

          <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">

            <div>

              <p className="text-sm uppercase tracking-[0.3em] text-violet-300">
                Pull Request Incident
              </p>

              <h1 className="mt-3 text-4xl font-bold text-white">
                {workflow.title}
              </h1>

              <p className="mt-3 text-zinc-400">
                Repository:
                {' '}
                {workflow.repo}
              </p>

              <p className="mt-2 text-zinc-500">
                Author:
                {' '}
                @{workflow.author}
              </p>

            </div>

            <div className="grid grid-cols-2 gap-4 text-sm text-zinc-300">

              <div className="glass rounded-2xl p-4">

                <p className="text-zinc-500">
                  Status
                </p>

                <h3 className="mt-1 font-semibold capitalize">
                  {workflow.status}
                </h3>

              </div>

              <div className="glass rounded-2xl p-4">

                <p className="text-zinc-500">
                  Decision
                </p>

                <h3 className="mt-1 font-semibold capitalize">
                  {workflow.decision}
                </h3>

              </div>

            </div>

          </div>

        </div>

        <DecisionBanner
          decision={workflow.decision}
          summary={workflow.summary}
        />

        <div className="mt-10 grid gap-10 lg:grid-cols-[1.2fr_0.8fr]">

          <div>

            <h2 className="mb-8 text-3xl font-bold text-white">
              Agent Execution Timeline
            </h2>

            <LiveAgentTimeline
              agentResults={
                workflow.agent_results || []
              }
            />

          </div>

          <div className="space-y-8">

            <ReflectionBlock
              reflection={reflection}
            />

            <SummaryReport
              summary={workflow.summary}
              research={
                workflow.agentResults?.find(
                  (agent: any) =>
                    agent.agent_name === 'research'
                )
              }
            />

          </div>

        </div>

      </section>

    </main>
  )
}