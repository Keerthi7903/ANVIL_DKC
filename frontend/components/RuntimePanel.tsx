'use client'

import { motion, AnimatePresence } from 'framer-motion'

interface Props {
  open: boolean
  onClose: () => void
}

const logs = [
  '[Planner] Evaluating stale PR conditions...',
  '[Priority] Calculating urgency score...',
  '[Research] Tavily search initialized...',
  '[Reflection] Confidence score HIGH...',
  '[Notification] GitHub reviewer assignment...',
]

export default function RuntimePanel({
  open,
  onClose,
}: Props) {
  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ x: -420, opacity: 0 }}
          animate={{ x: 0, opacity: 150 }}
          exit={{ x: -420, opacity: 0 }}
          transition={{
            duration: 0.35,
            ease: 'easeOut',
          }}
          className="fixed left-20 top-1/2 z-50 w-[420px] -translate-y-1/2"
        >
          <div className="overflow-hidden rounded-3xl border border-violet-500/20 bg-[#0B0714]/95 backdrop-blur-2xl shadow-[0_0_60px_rgba(168,85,247,0.22)]">

            {/* HEADER */}
            <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">

              <div>
                <h2 className="text-lg font-semibold text-white">
                  AI Runtime
                </h2>

                <p className="text-sm text-zinc-400">
                  Autonomous agent execution logs
                </p>
              </div>

              <button
                onClick={onClose}
                className="flex h-10 w-10 items-center justify-center rounded-xl border border-white/10 text-zinc-400 transition hover:border-violet-500/30 hover:text-white"
              >
                ✕
              </button>

            </div>

            {/* LOGS */}
            <div className="space-y-3 p-5">

              {logs.map((log, index) => (
                <motion.div
                  key={log}
                  initial={{ opacity: 10, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{
                    delay: index * 0.2,
                  }}
                  className="flex items-center gap-3 rounded-2xl border border-white/5 bg-white/[0.03] p-3"
                >

                  <div className="h-2 w-2 animate-pulse rounded-full bg-emerald-400" />

                  <span className="font-mono text-sm text-emerald-300">
                    {log}
                  </span>

                </motion.div>
              ))}

            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}