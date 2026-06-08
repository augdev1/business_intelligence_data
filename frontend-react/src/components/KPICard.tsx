interface Props {
  icon:   string
  label:  string
  value:  string
  delta?: string
}

export function KPICard({ icon, label, value, delta }: Props) {
  return (
    <div className="glass-card glass-hover kpi-shimmer rounded-[18px] p-5 relative overflow-hidden cursor-pointer">
      <div className="kpi-accent rounded-b-[18px]" />
      <div className="text-2xl mb-2.5">{icon}</div>
      <div className="section-label mb-1">{label}</div>
      <div style={{ color: 'var(--text)', fontSize: '1.78rem', fontWeight: 800, lineHeight: 1.05, letterSpacing: '-0.025em' }}>
        {value}
      </div>
      {delta && (
        <div style={{ color: 'var(--sub)', fontSize: '.7rem', fontWeight: 500, marginTop: '.3rem' }}>
          {delta}
        </div>
      )}
    </div>
  )
}
