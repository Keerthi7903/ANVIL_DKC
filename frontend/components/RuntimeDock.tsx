'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import RuntimePanel from './RuntimePanel'

export default function RuntimeDock() {
  const [open, setOpen] = useState(false)

  return (
    <>
      {/* FLOATING MINI DOCK */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="fixed bottom-6 left-6 z-40"
      >
        <button
          onClick={() => setOpen(true)}
          className="group glass flex h-14 w-14 items-center justify-center rounded-2xl border border-violet-500/10 bg-white/[0.03] text-xl transition hover:border-violet-500/40 hover:bg-violet-500/10 hover:shadow-[0_0_20px_rgba(168,85,247,0.2)]"
        >
          <div className="transition group-hover:scale-110">
            ⚡
          </div>
        </button>
      </motion.div>

      {/* PANEL */}
      <RuntimePanel
        open={open}
        onClose={() => setOpen(false)}
      />
    </>
  )
}