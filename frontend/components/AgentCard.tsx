'use client'

import { motion } from 'framer-motion'
import StatusBadge from './StatusBadge'

interface Props {
  agent: {
    name: string
    description: string
    confidence: number
    duration: string
  }

  status: 'pending' | 'running' | 'completed'
}

export default function AgentCard({
  agent,
  status,
}: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -30 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{
        duration: 0.5,
      }}
    >
      <div className="relative pl-10">

        {/* TIMELINE */}
        <div className="absolute left-0 top-0 h-full w-px bg-gradient-to-b from-violet-500 to-transparent" />

        {/* GLOW NODE */}
        <motion.div
          animate={{
            boxShadow:
              status === 'running'
                ? [
                    '0 0 0px rgba(168,85,247,0)',
                    '0 0 25px rgba(168,85,247,0.8)',
                    '0 0 0px rgba(168,85,247,0)',
                  ]
                : '0 0 0px rgba(168,85,247,0)',
          }}
          transition={{
            repeat: Infinity,
            duration: 1.8,
          }}
          className={`absolute left-[-7px] top-6 h-4 w-4 rounded-full border-2 bg-black ${
            status === 'completed'
              ? 'border-emerald-400'
              : status === 'running'
              ? 'border-violet-400'
              : 'border-zinc-600'
          }`}
        />

        <div className="glass rounded-3xl p-6 transition duration-300 hover:border-violet-500/30 hover:shadow-[0_0_30px_rgba(168,85,247,0.12)]">

          <div className="flex items-start justify-between">

            <div>
              <h3 className="text-xl font-semibold text-white">
                {agent.name}
              </h3>

              <p className="mt-1 text-zinc-400">
                {agent.description}
              </p>
            </div>

            <StatusBadge status={status} />

          </div>

          {/* AI THINKING STATE */}
          {status === 'running' && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-4 flex items-center gap-2 text-sm text-violet-300"
            >
              <div className="flex gap-1">
                <motion.div
                  animate={{ opacity: [0.3, 1, 0.3] }}
                  transition={{
                    repeat: Infinity,
                    duration: 1,
                  }}
                  className="h-2 w-2 rounded-full bg-violet-400"
                />

                <motion.div
                  animate={{ opacity: [0.3, 1, 0.3] }}
                  transition={{
                    repeat: Infinity,
                    duration: 1,
                    delay: 0.2,
                  }}
                  className="h-2 w-2 rounded-full bg-violet-400"
                />

                <motion.div
                  animate={{ opacity: [0.3, 1, 0.3] }}
                  transition={{
                    repeat: Infinity,
                    duration: 1,
                    delay: 0.4,
                  }}
                  className="h-2 w-2 rounded-full bg-violet-400"
                />
              </div>

              AI agent executing...
            </motion.div>
          )}

          {/* CONFIDENCE */}
          <div className="mt-6">

            <div className="mb-2 flex justify-between text-sm">
              <span className="text-zinc-400">
                Confidence
              </span>

              <span className="text-white">
                {Math.round(agent.confidence * 100)}%
              </span>
            </div>

            <div className="h-3 overflow-hidden rounded-full bg-zinc-800">

              <motion.div
                initial={{ width: 0 }}
                animate={{
                  width:
                    status === 'pending'
                      ? '0%'
                      : `${agent.confidence * 100}%`,
                }}
                transition={{
                  duration: 1,
                  ease: 'easeOut',
                }}
                className={`h-full rounded-full ${
                  status === 'completed'
                    ? 'bg-gradient-to-r from-emerald-500 to-green-400'
                    : 'bg-gradient-to-r from-violet-500 to-fuchsia-400'
                }`}
              />

            </div>
          </div>

          <div className="mt-5 text-sm text-zinc-500">
            Duration:
            {' '}
            {status === 'pending'
              ? '--'
              : agent.duration}
          </div>

        </div>
      </div>
    </motion.div>
  )
}