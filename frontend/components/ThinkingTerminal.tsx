'use client'

import { motion } from 'framer-motion'

const logs = [
  '[Planner] Evaluating stale PR conditions...',
  '[Priority] Calculating urgency score...',
  '[Research] Tavily search initialized...',
  '[Reflection] Confidence score HIGH...',
  '[Notification] GitHub reviewer assignment...',
]

export default function ThinkingTerminal() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="glass fixed bottom-6 left-6 z-40 w-[420px] overflow-hidden rounded-3xl"
    >

      {/* HEADER */}
      <div className="flex items-center gap-2 border-b border-white/10 px-5 py-3">

        <div className="h-3 w-3 rounded-full bg-red-400" />
        <div className="h-3 w-3 rounded-full bg-yellow-400" />
        <div className="h-3 w-3 rounded-full bg-emerald-400" />

        <div className="ml-3 text-sm font-medium text-zinc-400">
          AI Agent Runtime
        </div>
      </div>

      {/* TERMINAL */}
      <div className="space-y-3 p-5 font-mono text-sm">

        {logs.map((log, index) => (
          <motion.div
            key={log}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{
              delay: index * 0.6,
            }}
            className="flex items-center gap-3"
          >

            <div className="h-2 w-2 animate-pulse rounded-full bg-emerald-400" />

            <span className="text-emerald-300">
              {log}
            </span>

          </motion.div>
        ))}

        <motion.div
          animate={{
            opacity: [0, 1, 0],
          }}
          transition={{
            repeat: Infinity,
            duration: 1,
          }}
          className="text-violet-400"
        >
          ▋
        </motion.div>

      </div>
    </motion.div>
  )
}