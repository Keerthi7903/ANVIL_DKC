'use client'

import { useState } from 'react'
import SimulateModal from './SimulateModal'

export default function Navbar() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <div className="sticky top-0 z-40 border-b border-white/10 bg-black/30 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">

          <div>
            <h1 className="text-2xl font-bold tracking-wide text-white">
              AI Team OS
            </h1>

            <p className="text-sm text-zinc-400">
              Autonomous PR Operations Platform
            </p>
          </div>

          <div className="flex items-center gap-4">

            <div className="flex items-center gap-2 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-sm text-emerald-400">
              <div className="h-2 w-2 animate-pulse rounded-full bg-emerald-400" />
              LIVE
            </div>

            <button
              onClick={() => setOpen(true)}
              className="rounded-2xl bg-gradient-to-r from-violet-600 to-fuchsia-600 px-6 py-3 font-semibold text-white transition hover:scale-105 hover:shadow-[0_0_30px_rgba(168,85,247,0.4)]"
            >
              Simulate Stale PR
            </button>

          </div>
        </div>
      </div>

      <SimulateModal
        isOpen={open}
        onClose={() => setOpen(false)}
      />
    </>
  )
}