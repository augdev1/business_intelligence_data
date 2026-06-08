'use client'
import { useState, useRef, useEffect } from 'react'
import { motion, useReducedMotion } from 'framer-motion'
import { TIER_COLORS } from '@/lib/utils'

interface Tier { label: string; threshold: number; color: string; size: number }

const TIERS: Tier[] = [
  { label: 'R$10K',  threshold: 10_000,     color: TIER_COLORS[0], size: 12 },
  { label: 'R$100K', threshold: 100_000,    color: TIER_COLORS[1], size: 14 },
  { label: 'R$1M',   threshold: 1_000_000,  color: TIER_COLORS[2], size: 16 },
  { label: 'R$10M+', threshold: 10_000_000, color: TIER_COLORS[3], size: 18 },
]

function OrbitalDots({ color, radius = 18 }: { color: string; radius?: number }) {
  const shouldReduce = useReducedMotion()
  return (
    <>
      {Array.from({ length: 8 }, (_, i) => {
        const angle = (i / 8) * 2 * Math.PI
        const x = Math.cos(angle) * radius - 2
        const y = Math.sin(angle) * radius - 2
        return (
          <motion.div
            key={i}
            className="absolute w-1 h-1 rounded-full"
            style={{ backgroundColor: color, left: '50%', top: '50%' }}
            initial={{ opacity: 0, scale: .3, x, y }}
            animate={{ opacity: 1, scale: 1,  x, y }}
            transition={{ duration: shouldReduce ? .1 : .5, delay: shouldReduce ? 0 : i * .04,
              type: 'spring', stiffness: 400, damping: 25 }}
          />
        )
      })}
    </>
  )
}

export function GradientSelector({ currentValue }: { currentValue: number }) {
  const reached    = TIERS.filter(t => currentValue >= t.threshold).length
  const containerRef = useRef<HTMLDivElement>(null)
  const circleRefs   = useRef<(HTMLDivElement | null)[]>([])
  const [gradPos, setGradPos] = useState<{ x: number; y: number } | null>(null)

  useEffect(() => {
    const idx = reached - 1
    if (idx >= 0 && circleRefs.current[idx] && containerRef.current) {
      const cr = circleRefs.current[idx]!.getBoundingClientRect()
      const pr = containerRef.current.getBoundingClientRect()
      setGradPos({ x: cr.left + cr.width / 2 - pr.left, y: cr.top + cr.height / 2 - pr.top })
    } else {
      setGradPos(null)
    }
  }, [reached])

  const pct = Math.round((reached / TIERS.length) * 100)

  return (
    <div ref={containerRef}
      className="glass-card rounded-[18px] p-5 mb-4 relative overflow-hidden">
      {gradPos && (
        <div className="absolute inset-0 pointer-events-none"
          style={{ background: `radial-gradient(circle at ${gradPos.x}px ${gradPos.y + 300}px, ${TIERS[reached-1]?.color}18 0%, transparent 65%)` }} />
      )}

      <div className="flex justify-between items-baseline mb-4 relative">
        <p className="section-label">Tiers de Receita</p>
        <span className="text-[.64rem] font-bold px-2.5 py-0.5 rounded-full text-white"
          style={{ background: 'linear-gradient(135deg,var(--acc),var(--acc2))' }}>
          {reached}/{TIERS.length} ALCANÇADOS
        </span>
      </div>

      <div className="gs-track flex items-center justify-center gap-0 mb-3">
        {TIERS.map((t, i) => {
          const active = i < reached
          return (
            <div key={t.label} className="flex items-center gap-0">
              <div ref={el => { circleRefs.current[i] = el }}
                className="relative flex-shrink-0 rounded-full transition-all duration-300"
                style={{
                  width: t.size, height: t.size,
                  background: active ? t.color : '#1e2860',
                  boxShadow: active ? `0 0 18px ${t.color}55, 0 0 38px ${t.color}28` : 'none',
                }}>
                {active && <OrbitalDots color={t.color} radius={t.size + 6} />}
              </div>
              {i < TIERS.length - 1 && (
                <div className="rounded-full flex-1 mx-1"
                  style={{
                    height: 2 + i,
                    minWidth: 36, maxWidth: 68,
                    background: i < reached - 1
                      ? `linear-gradient(90deg,${t.color},${TIERS[i+1].color})`
                      : '#1e2860',
                  }} />
              )}
            </div>
          )
        })}
      </div>

      <div className="flex">
        {TIERS.map((t, i) => (
          <div key={t.label} className="flex-1 text-center"
            style={{ fontSize: '.67rem', fontWeight: 700, letterSpacing: '.04em',
              color: i < reached ? t.color : '#2a3870' }}>
            {t.label}
          </div>
        ))}
      </div>

      <div className="mt-3 h-[3px] rounded-full overflow-hidden"
        style={{ background: 'rgba(255,255,255,.06)' }}>
        <motion.div className="h-full rounded-full"
          style={{ background: `linear-gradient(90deg,${TIER_COLORS[0]},${TIER_COLORS[3]})` }}
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: .8, ease: 'easeOut' }} />
      </div>
    </div>
  )
}
