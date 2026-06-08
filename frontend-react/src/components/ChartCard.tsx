interface Props {
  title:    string
  children: React.ReactNode
  className?: string
}

export function ChartCard({ title, children, className = '' }: Props) {
  return (
    <div className={`glass-card glass-hover rounded-[18px] p-4 ${className}`}>
      <p className="section-label mb-3">{title}</p>
      {children}
    </div>
  )
}

export function CustomTooltip({ active, payload, label, currency = false }: {
  active?: boolean; payload?: { name: string; value: number; color: string }[]; label?: string; currency?: boolean
}) {
  if (!active || !payload?.length) return null
  return (
    <div className="glass-card rounded-xl p-3 text-xs" style={{ minWidth: 140 }}>
      {label && <p style={{ color: 'var(--text)', fontWeight: 600, marginBottom: 4 }}>{label}</p>}
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.color }}>
          {p.name}: {currency ? `R$ ${p.value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}` : p.value.toLocaleString('pt-BR')}
        </p>
      ))}
    </div>
  )
}
