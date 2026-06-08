import { useMemo, useState } from 'react'
import {
  AreaChart, Area, BarChart, Bar, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts'
import { useKPIs } from '@/hooks/useKPIs'
import { KPICard } from '@/components/KPICard'
import { ChartCard, CustomTooltip } from '@/components/ChartCard'
import { GradientSelector } from '@/components/GradientSelector'
import { fmt } from '@/lib/utils'

export function Dashboard() {
  const { data, loading, error } = useKPIs()
  const [inicio, setInicio] = useState('')
  const [fim,    setFim]    = useState('')

  const periodos = useMemo(() => {
    if (!data?.receita_por_mes) return []
    return [...new Set(
      data.receita_por_mes.map(d => `${d.ano}-${String(d.mes).padStart(2,'0')}`)
    )].sort()
  }, [data])

  const dfMes = useMemo(() => {
    if (!data?.receita_por_mes) return []
    const rows = data.receita_por_mes.map(d => ({
      periodo: `${d.ano}-${String(d.mes).padStart(2,'0')}`,
      receita: d.receita,
    })).sort((a,b) => a.periodo.localeCompare(b.periodo))
    const ini = inicio || periodos[0] || ''
    const fi  = fim    || periodos[periodos.length-1] || ''
    return rows.filter(r => r.periodo >= ini && r.periodo <= fi)
  }, [data, inicio, fim, periodos])

  const dfAcum = useMemo(() => {
    let acc = 0
    return dfMes.map(r => ({ ...r, acumulado: (acc += r.receita) }))
  }, [dfMes])

  if (loading) return <Loader />
  if (error || !data) return <ErrorMsg msg={error ?? 'Sem dados'} />

  return (
    <div>
      <PageHeader title="Visão Executiva" sub="Métricas gerais do e-commerce Olist" />

      <div className="grid grid-cols-4 gap-4 mb-4">
        <KPICard icon="💰" label="Receita Total"    value={fmt.currency(data.receita_total)}  delta="Dataset completo" />
        <KPICard icon="🛒" label="Total de Pedidos" value={fmt.number(data.numero_pedidos)}   delta="Pedidos realizados" />
        <KPICard icon="👥" label="Clientes Únicos"  value={fmt.number(data.clientes_unicos)}  delta="Cadastros únicos" />
        <KPICard icon="🎯" label="Ticket Médio"     value={fmt.currency(data.ticket_medio)}   delta="Por pedido" />
      </div>

      <GradientSelector currentValue={data.receita_total} />

      {/* Period filter */}
      {periodos.length > 1 && (
        <div className="flex items-center gap-3 mb-4">
          <label className="section-label">De</label>
          <select value={inicio || periodos[0]} onChange={e => setInicio(e.target.value)}>
            {periodos.map(p => <option key={p}>{p}</option>)}
          </select>
          <label className="section-label">Até</label>
          <select value={fim || periodos[periodos.length-1]} onChange={e => setFim(e.target.value)}>
            {periodos.map(p => <option key={p}>{p}</option>)}
          </select>
        </div>
      )}

      <div className="grid grid-cols-2 gap-4 mb-4">
        <ChartCard title="Receita por Mês">
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={dfMes}>
              <defs>
                <linearGradient id="accGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%"  stopColor="#5c6ff5" stopOpacity={.35}/>
                  <stop offset="95%" stopColor="#5c6ff5" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--grid)" />
              <XAxis dataKey="periodo" tick={{ fill:'var(--sub)', fontSize:11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill:'var(--sub)', fontSize:11 }} axisLine={false} tickLine={false}
                tickFormatter={v => `R$${(v/1000).toFixed(0)}k`} />
              <Tooltip content={<CustomTooltip currency />} />
              <Area type="monotone" dataKey="receita" name="Receita"
                stroke="#5c6ff5" strokeWidth={2.5} fill="url(#accGrad)" dot={{ fill:'#5c6ff5', r:4, strokeWidth:2, stroke:'var(--solid)' }} />
            </AreaChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Receita por Estado">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data.receita_por_estado}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--grid)" />
              <XAxis dataKey="estado" tick={{ fill:'var(--sub)', fontSize:10 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill:'var(--sub)', fontSize:10 }} axisLine={false} tickLine={false}
                tickFormatter={v => `R$${(v/1000).toFixed(0)}k`} />
              <Tooltip content={<CustomTooltip currency />} />
              <Bar dataKey="receita" name="Receita" fill="#5c6ff5" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <ChartCard title="Evolução Acumulada">
        <ResponsiveContainer width="100%" height={280}>
          <AreaChart data={dfAcum}>
            <defs>
              <linearGradient id="acc2Grad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%"  stopColor="#a855f7" stopOpacity={.3}/>
                <stop offset="95%" stopColor="#a855f7" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="acc1Grad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%"  stopColor="#5c6ff5" stopOpacity={.18}/>
                <stop offset="95%" stopColor="#5c6ff5" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--grid)" />
            <XAxis dataKey="periodo" tick={{ fill:'var(--sub)', fontSize:10 }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fill:'var(--sub)', fontSize:10 }} axisLine={false} tickLine={false}
              tickFormatter={v => `R$${(v/1000).toFixed(0)}k`} />
            <Tooltip content={<CustomTooltip currency />} />
            <Legend wrapperStyle={{ fontSize:12, color:'var(--sub)' }} />
            <Area type="monotone" dataKey="receita"   name="Mensal"     stroke="#a855f7" strokeWidth={2} fill="url(#acc2Grad)" strokeDasharray="5 3" />
            <Area type="monotone" dataKey="acumulado" name="Acumulado"  stroke="#5c6ff5" strokeWidth={2.5} fill="url(#acc1Grad)" />
          </AreaChart>
        </ResponsiveContainer>
      </ChartCard>
    </div>
  )
}

function PageHeader({ title, sub }: { title: string; sub?: string }) {
  return (
    <div className="mb-5">
      <h1 style={{ color:'var(--text)', fontSize:'1.5rem', fontWeight:800, margin:0, letterSpacing:'-.025em' }}>{title}</h1>
      {sub && <p style={{ color:'var(--sub)', fontSize:'.84rem', marginTop:'.12rem' }}>{sub}</p>}
    </div>
  )
}

function Loader() {
  return (
    <div className="flex items-center justify-center h-64">
      <div className="w-8 h-8 rounded-full border-2 border-t-transparent animate-spin"
        style={{ borderColor:'var(--border)', borderTopColor:'var(--acc)' }} />
    </div>
  )
}

function ErrorMsg({ msg }: { msg: string }) {
  return (
    <div className="glass-card rounded-xl p-4 text-center" style={{ color:'#ef4444' }}>
      ⚠️ {msg} — verifique se a API está rodando em localhost:8000
    </div>
  )
}

export { PageHeader, Loader, ErrorMsg }
