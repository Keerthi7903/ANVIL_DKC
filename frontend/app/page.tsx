'use client'

import { useEffect, useState } from 'react'

import Navbar from '@/components/Navbar'
import StatsBar from '@/components/StatsBar'
import WorkflowCard from '@/components/WorkflowCard'

export default function HomePage() {

  const [workflows, setWorkflows] =
    useState<any[]>([])

  const fetchWorkflows = async () => {

    try {

      const response = await fetch(
        'http://localhost:8000/workflows'
      )

      const data = await response.json()

      const formatted = data.map(
        (workflow: any) => ({

          id: workflow.workflow_id,

          title:
            workflow.title,

          repo:
            workflow.repo,

          status:
            workflow.status,

          pr_state:
            workflow.pr_state,

          decision:
            workflow.decision,

          time:
            workflow.created_at,

          summary:
            workflow.summary,

          confidence:
            workflow.confidence,
        })
      )

      setWorkflows(formatted)

    } catch (error) {

      console.error(
        'Failed to fetch workflows:',
        error
      )

    }
  }

  useEffect(() => {

    fetchWorkflows()

    // AUTO REFRESH EVERY 5s
    const interval = setInterval(
      fetchWorkflows,
      5000
    )

    return () =>
      clearInterval(interval)

  }, [])

  return (
    <main className="min-h-screen">

      <Navbar />

      <section className="mx-auto max-w-7xl px-6 py-10">

        <div className="mb-10">

          <h1 className="text-5xl font-bold leading-tight text-white">
            Autonomous PR Intelligence
          </h1>

          <p className="mt-4 max-w-2xl text-lg text-zinc-400">
            AI Team OS monitors stale pull requests,
            coordinates multiple autonomous agents,
            and takes action without human intervention.
          </p>

        </div>

        <StatsBar workflows={workflows} />

        <div className="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-3">

          {workflows.map((workflow) => (

            <WorkflowCard
              key={workflow.id}
              workflow={workflow}
            />

          ))}

        </div>

      </section>

    </main>
  )
}