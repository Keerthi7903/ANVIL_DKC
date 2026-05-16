'use client'

import { motion } from 'framer-motion'

export default function AnimatedBackground() {
  return (
    <div className="pointer-events-none fixed inset-0 overflow-hidden">

      {/* TOP LEFT GLOW */}
      <motion.div
        animate={{
          x: [0, 40, 0],
          y: [0, 20, 0],
        }}
        transition={{
          duration: 12,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
        className="absolute left-[-10%] top-[-10%] h-[500px] w-[500px] rounded-full bg-violet-700/20 blur-3xl"
      />

      {/* BOTTOM RIGHT GLOW */}
      <motion.div
        animate={{
          x: [0, -30, 0],
          y: [0, -20, 0],
        }}
        transition={{
          duration: 15,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
        className="absolute bottom-[-10%] right-[-10%] h-[450px] w-[450px] rounded-full bg-fuchsia-700/10 blur-3xl"
      />

      {/* CENTER LIGHT */}
      <motion.div
        animate={{
          opacity: [0.15, 0.25, 0.15],
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
        }}
        className="absolute left-1/2 top-1/3 h-[350px] w-[350px] -translate-x-1/2 rounded-full bg-violet-500/10 blur-3xl"
      />

      {/* GRID OVERLAY */}
      <div
        className="absolute inset-0 opacity-[0.04]"
        style={{
          backgroundImage: `
            linear-gradient(rgba(255,255,255,0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.08) 1px, transparent 1px)
          `,
          backgroundSize: '80px 80px',
        }}
      />
    </div>
  )
}