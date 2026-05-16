'use client'

import { motion } from 'framer-motion'

const events = [
  {
    icon: '🧠',
    text: 'Planner agent initialized',
    color: 'text-violet-300',
  },
  {
    icon: '⚠️',
    text: 'CI failure detected in workflow',
    color: 'text-amber-300',
  },
  {
    icon: '🔍',
    text: 'Research agent queried Tavily',
    color: 'text-cyan-300',
  },
  {
    icon: '✅',
    text: 'Reviewer assigned successfully',
    color: 'text-emerald-300',
  },
  {
    icon: '📢',
    text: 'Discord escalation dispatched',
    color: 'text-pink-300',
  },
]

export default function LiveEventFeed() {
  return (
    <motion.div
      initial={{ opacity: 0, x: 40 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5 }}
      className="glass fixed bottom-6 right-6 z-40 w-[340px] rounded-3xl p-5"
    >
      <div className="mb-5 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-white">
            Live Events
          </h2>

          <p className="text-sm text-zinc-400">
            Autonomous workflow activity
          </p>
        </div>

        <div className="h-3 w-3 animate-pulse rounded-full bg-emerald-400" />
      </div>

      <div className="space-y-3">

        {events.map((event, index) => (
          <motion.div
            key={event.text}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              delay: index * 0.2,
            }}
            className="rounded-2xl border border-white/5 bg-white/[0.03] p-3"
          >
            <div className="flex items-start gap-3">

              <div className="text-xl">
                {event.icon}
              </div>

              <div>
                <p className={`text-sm font-medium ${event.color}`}>
                  {event.text}
                </p>

                <p className="mt-1 text-xs text-zinc-500">
                  just now
                </p>
              </div>

            </div>
          </motion.div>
        ))}

      </div>
    </motion.div>
  )
}