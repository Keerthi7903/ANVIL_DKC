'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import StatusBadge from './StatusBadge'

interface Props {
  workflow: any
}

export default function WorkflowCard({
  workflow,
}: Props) {

  const prStateColor =
    workflow.pr_state === 'merged'
      ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
      : workflow.pr_state === 'open'
      ? 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30'
      : workflow.pr_state === 'closed'
      ? 'bg-red-500/20 text-red-400 border-red-500/30'
      : 'bg-violet-500/20 text-violet-300 border-violet-500/30'

  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.5,
        ease: 'easeOut',
      }}
      whileHover={{
        y: -8,
        scale: 1.01,
      }}
    >
      <Link href={`/incident/${workflow.id}`}>

        <div className="group glass relative overflow-hidden rounded-3xl p-6 transition duration-300 hover:border-violet-500/40 hover:shadow-[0_0_40px_rgba(168,85,247,0.18)]">

          <div className="absolute right-0 top-0 h-40 w-40 rounded-full bg-violet-600/10 blur-3xl transition duration-500 group-hover:bg-violet-500/20" />

          <div className="relative z-10 flex items-start justify-between">

            <div>

              <h2 className="text-lg font-semibold text-white">
                {workflow.title}
              </h2>

              <p className="mt-1 text-sm text-zinc-400">
                {workflow.repo}
              </p>

            </div>

            <div className="flex flex-col items-end gap-2">

              {/* AI WORKFLOW STATUS */}
              <StatusBadge
                status={workflow.status}
              />

              {/* REAL PR LIFECYCLE */}
              <div
                className={`rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-wide ${prStateColor}`}
              >
                {workflow.pr_state || 'open'}
              </div>

            </div>

          </div>

          <div className="mt-6">

            <p className="text-sm text-zinc-500">
              Decision
            </p>

            <p className="mt-1 font-medium text-violet-300">
              {workflow.decision}
            </p>

          </div>

          <div className="mt-6 space-y-2">

            {workflow.agentResults?.map(
              (agent: any) => (

                <div
                  key={agent.agent_name}
                  className="rounded-2xl border border-white/5 bg-black/20 p-3"
                >

                  <div className="flex items-center justify-between">

                    <h3 className="font-medium text-white">
                      {agent.agent_name}
                    </h3>

                    <span className="text-xs text-violet-400">
                      {agent.status}
                    </span>

                  </div>

                  <div className="mt-2 flex items-center justify-between text-sm text-zinc-400">

                    <span>
                      Confidence:
                      {' '}
                      {agent.confidence}
                    </span>

                    <span>
                      {agent.duration_ms}ms
                    </span>

                  </div>

                </div>

              )
            )}

          </div>

          <div className="mt-6 flex items-center justify-between text-sm text-zinc-500">

            <span>
              {workflow.time}
            </span>

            <span className="text-violet-400 transition group-hover:translate-x-1">
              View Details →
            </span>

          </div>

        </div>

      </Link>
    </motion.div>
  )
}