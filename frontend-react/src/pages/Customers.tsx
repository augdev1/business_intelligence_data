import { useMemo, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts'
import { useKPIs } from '@/hooks/useKPIs'
import { KPICard } from '@/components/KPICard'
import { ChartCard, CustomTooltip } from '@/components/ChartCard'
import { PageHeader, Loader, ErrorMsg } from './Dashboard'
import { COLORS, fmt } from '@/lib/utils'

export function Customers() {
  const { data, loading, error } = useKPIs()
  const [selectedStates, setSelectedStates] = useState<string[]>([])

  const allStates = useMemo(() =>
    [...new Set((data?.pedidos_por_estado ?? []).map(r => r.estado))].sort()
  , [data])

  const active = selectedStates.length ? selectedStates : allStates

  const toggleState = (s: string) =>
    setSelectedStates(prev => prev.includes(s) ? prev.filter(x => x !== s) : [...prev, s])

  if (loading) return <Loader />
  if (error || !data) return <ErrorMsg msg={error ?? 'Sem dados'} />

  const c   = data.clientes_unicos
  const p   = data.numero_pedidos
  const t   = data.ticket_medio
  const ppc = c > 0 ? p / c : 0

  const pedidos  = (data.pedidos_por_estado  ?? []).filter(r => active.includes(r.estado))
  const receitas = (data.receita_por_estado  ?? []).filter(r => active.includes(r.estado))
  const payments = data.metodos_pagamento ?? []
  const totalPay = payments.reduce((s, r) => s + r.valor_total, 0)

  return (
    <div>
      <PageHeader title="Clientes e Geografia" sub="Distribuição geográfica e comportamento de compra" />

      <div className="grid grid-cols-4 gap-4 mb-4">
        <KPICard icon="👥" label="Clientes Únicos"  value={fmt.number(c)}          delta="Total cadastrado" />
        <KPICard icon="🛒" label="Pedidos Totais"   value={fmt.number(p)}          delta="Volume completo" />
        <KPICard icon="📈" label="Pedidos/Cliente"  value={ppc.toFixed(2)}         delta="Frequência média" />
        <KPICard icon="💳" label="Ticket Médio"     value={fmt.currency(t)}        delta="Por pedido" />
      </div>

      {/* State filter chips */}
      {allStates.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          <button className="chip-btn" style={selectedStates.length === 0 ? { borderColor:'var(--acc)', color:'var(--acc)', background:'rgba(92,111,245,.12)' } : {}}
            onClick={() => setSelectedStates([])}>
            Todos
          </button>
          {allStates.map(s => (
            <button key={s} className="chip-btn"
              style={active.includes(s) && selectedStates.length > 0
                ? { borderColor:'var(--acc)', color:'var(--acc)', background:'rgba(92,111,245,.12)' } : {}}
              onClick={() => toggleState(s)}>
              {s}
            </button>
          ))}
        </div>
      )}

      <div className="grid grid-cols-2 gap-4 mb-4">
        <ChartCard title="Pedidos por Estado">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={pedidos}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--grid)" />
              <XAxis dataKey="estado" tick={{ fill:'var(--sub)', fontSize:10 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill:'var(--sub)', fontSize:10 }} axisLine={false} tickLine={false} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="quantidade" name="Pedidos" fill="var(--acc)" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Receita por Estado">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={receitas}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--grid)" />
              <XAxis dataKey="estado" tick={{ fill:'var(--sub)', fontSize:10 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill:'var(--sub)', fontSize:10 }} axisLine={false} tickLine={false}
                tickFormatter={v => `R$${(v/1000).toFixed(0)}k`} />
              <Tooltip content={<CustomTooltip currency />} />
              <Bar dataKey="receita" name="Receita" fill="var(--acc2)" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      {payments.length > 0 && (
        <div className="glass-card rounded-[18px] p-5">
          <p className="section-label mb-4">Métodos de Pagamento</p>
          <div className="grid grid-cols-2 gap-6">
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie data={payments} dataKey="valor_total" nameKey="tipo"
                  innerRadius="50%" outerRadius="72%" paddingAngle={2}>
                  {payments.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip formatter={(v: number) => fmt.currency(v)} />
                <Legend wrapperStyle={{ fontSize:11, color:'var(--sub)' }} />
              </PieChart>
            </ResponsiveContainer>
            <div className="flex flex-col justify-center gap-2">
              {[...payments].sort((a,b) => b.valor_total - a.valor_total).map((r, i) => (
                <div key={i} className="pay-row">
                  <div className="flex items-center gap-2">
                    <div className="w-2.5 h-2.5 rounded-full flex-shrink-0"
                      style={{ background: COLORS[i % COLORS.length] }} />
                    <span style={{ color:'var(--text)', fontSize:'.82rem', fontWeight:500 }}>
                      {r.tipo.replace(/_/g,' ').replace(/\b\w/g, c => c.toUpperCase())}
                    </span>
                  </div>
                  <div className="flex items-baseline gap-1.5">
                    <span style={{ color:'var(--acc)', fontWeight:700, fontSize:'.88rem' }}>
                      {fmt.currency(r.valor_total)}
                    </span>
                    <span style={{ color:'var(--sub)', fontSize:'.72rem' }}>
                      {fmt.pct(totalPay > 0 ? r.valor_total / totalPay * 100 : 0)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
