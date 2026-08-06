interface Props {
  icon:   string
  label:  string
  value:  string
  delta?: string
  color?: string
}

export function KPICard({ icon, label, value, delta, color = '#10b981' }: Props) {
  return (
    <div className="glass-card glass-hover kpi-shimmer rounded-[18px] p-5 relative overflow-hidden cursor-pointer"
      style={{ borderTop: `3px solid ${color}` }}>
      <div className="flex items-center justify-between mb-3">
        <div className="w-10 h-10 rounded-[12px] flex items-center justify-center text-xl"
          style={{ background: `${color}20`, border: `1px solid ${color}40` }}>
          {icon}
        </div>
        <div className="w-2.5 h-2.5 rounded-full" style={{ background: color, boxShadow: `0 0 10px ${color}` }} />
      </div>
      <div className="section-label mb-1">{label}</div>
      <div style={{ color: 'var(--text)', fontSize: '1.78rem', fontWeight: 800, lineHeight: 1.05, letterSpacing: '-0.025em' }}>
        {value}
      </div>
      {delta && (
        <div style={{ color: color, fontSize: '.72rem', fontWeight: 600, marginTop: '.4rem' }}>
          {delta}
        </div>
      )}
    </div>
  )
}
