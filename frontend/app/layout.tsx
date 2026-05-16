import './globals.css'
import type { Metadata } from 'next'
import AnimatedBackground from '@/components/AnimatedBackground'
import RuntimeDock from '@/components/RuntimeDock'


export const metadata: Metadata = {
  title: 'AI Team OS',
  description: 'Autonomous PR Operations Platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-[#07070A] text-white antialiased">

        <AnimatedBackground />

        <RuntimeDock />

        <div className="relative z-10">
          {children}
        </div>
      </body>
    </html>
  )
}