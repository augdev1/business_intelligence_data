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
  active?: boolean; payload?: { name: string; value: number; color: string; payload?: any }[]; label?: string; currency?: boolean
}) {
  if (!active || !payload?.length) return null
  const extra = payload[0]?.payload
  return (
    <div className="glass-card rounded-xl p-3 text-xs" style={{ minWidth: 140 }}>
      {label && <p style={{ color: 'var(--text)', fontWeight: 600, marginBottom: 4 }}>{label}</p>}
      {extra?.categoria && (
        <p style={{ color: 'var(--sub)', fontSize: '0.72rem', marginBottom: 6 }}>
          Categoria: <span className="font-medium text-emerald-400">{extra.categoria}</span>
        </p>
      )}
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.color }}>
          {p.name}: {currency ? `R$ ${p.value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}` : p.value.toLocaleString('pt-BR')}
        </p>
      ))}
    </div>
  )
}
