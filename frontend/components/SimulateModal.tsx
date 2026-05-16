'use client'

import { motion, AnimatePresence } from 'framer-motion'

interface Props {
  isOpen: boolean
  onClose: () => void
}

const scenarios = [
  {
    title: 'No Reviewers',
    description:
      'PR open for 72h with zero reviewers assigned.',
    icon: '👥',
  },
  {
    title: 'CI Failing',
    description:
      'Broken CI pipeline with inactive reviewers.',
    icon: '⚠️',
  },
  {
    title: 'Repeat Offender',
    description:
      'Author has multiple stale PR incidents.',
    icon: '🧠',
  },
]

export default function SimulateModal({
  isOpen,
  onClose,
}: Props) {

  const triggerWorkflow = async (
    scenario: string
  ) => {

    try {

      const response = await fetch(
        'http://localhost:8000/simulate/stale-pr',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            scenario,
          }),
        }
      )

      const data = await response.json()

      console.log('WORKFLOW RESULT:')
      console.log(data)

      // SEND TO DASHBOARD
      window.dispatchEvent(
        new CustomEvent(
          'workflow-complete',
          {
            detail: data,
          }
        )
      )

      onClose()

    } catch (error) {

      console.error(error)

      alert('Failed to trigger workflow.')

    }
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* BACKDROP */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm"
          />

          {/* MODAL */}
          <motion.div
            initial={{
              opacity: 0,
              scale: 0.9,
              y: 40,
            }}
            animate={{
              opacity: 1,
              scale: 1,
              y: 0,
            }}
            exit={{
              opacity: 0,
              scale: 0.95,
              y: 20,
            }}
            transition={{
              duration: 0.3,
            }}
            className="fixed left-1/2 top-1/2 z-50 w-[92%] max-w-2xl -translate-x-1/2 -translate-y-1/2"
          >
            <div className="glass rounded-[32px] border border-violet-500/20 p-8 shadow-[0_0_60px_rgba(168,85,247,0.18)]">

              <div className="mb-8">

                <h2 className="text-4xl font-bold text-white">
                  Simulate Stale PR
                </h2>

                <p className="mt-3 text-zinc-400">
                  Trigger an autonomous AI workflow scenario.
                </p>

              </div>

              <div className="space-y-4">

                {scenarios.map((scenario) => (

                  <motion.button
                    key={scenario.title}
                    whileHover={{
                      scale: 1.02,
                    }}
                    whileTap={{
                      scale: 0.98,
                    }}
                    onClick={() =>
                      triggerWorkflow(
                        scenario.title
                      )
                    }
                    className="group glass w-full rounded-3xl border border-white/5 p-5 text-left transition hover:border-violet-500/30 hover:bg-violet-500/5"
                  >

                    <div className="flex items-start gap-4">

                      <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-violet-500/10 text-2xl">
                        {scenario.icon}
                      </div>

                      <div>

                        <h3 className="text-xl font-semibold text-white">
                          {scenario.title}
                        </h3>

                        <p className="mt-2 text-zinc-400">
                          {scenario.description}
                        </p>

                      </div>

                    </div>

                  </motion.button>

                ))}

              </div>

              <button
                onClick={onClose}
                className="mt-8 w-full rounded-2xl border border-white/10 py-3 text-zinc-300 transition hover:border-violet-500/30 hover:text-white"
              >
                Cancel
              </button>

            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}