import { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, PieChart, Pie, Legend } from 'recharts'
import { useKPIs } from '@/hooks/useKPIs'
import { ChartCard, CustomTooltip } from '@/components/ChartCard'
import { PageHeader, Loader, ErrorMsg } from './Dashboard'
import { COLORS, fmt } from '@/lib/utils'

export function Products() {
  const { data, loading, error } = useKPIs()
  const [topN, setTopN] = useState(10)

  if (loading) return <Loader />
  if (error || !data) return <ErrorMsg msg={error ?? 'Sem dados'} />

  const produtos = (data.top_produtos ?? []).slice(0, topN).map(p => ({
    ...p,
    nome: p.nome ?? `${p.categoria || 'sem_categoria'} #${p.product_id.slice(0, 6)}`,
  }))
  const categorias = (data.top_categorias ?? []).slice(0, topN)

  return (
    <div>
      <PageHeader title="Análise de Produtos" sub="Performance por produto e categoria" />

      <div className="flex items-center gap-4 mb-4">
        <span className="section-label">Exibir top</span>
        <input type="range" min={5} max={20} step={5} value={topN} onChange={e => setTopN(+e.target.value)}
          className="w-32" />
        <span className="text-sm font-bold" style={{ color:'var(--acc)' }}>{topN}</span>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <ChartCard title={`Top ${topN} Produtos por Faturamento`}>
          <ResponsiveContainer width="100%" height={Math.max(280, topN * 28)}>
            <BarChart data={produtos} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="var(--grid)" horizontal={false} />
              <XAxis type="number" tick={{ fill:'var(--sub)', fontSize:10 }} axisLine={false} tickLine={false}
                tickFormatter={v => `R$${(v/1000).toFixed(0)}k`} />
              <YAxis type="category" dataKey="nome" tick={{ fill:'var(--sub)', fontSize:9 }}
                axisLine={false} tickLine={false} width={140} />
              <Tooltip content={<CustomTooltip currency />} />
              <Bar dataKey="faturamento" name="Faturamento" radius={[0,4,4,0]}>
                {produtos.map((_, i) => <Cell key={i} fill={`rgba(92,111,245,${.45 + (i/topN)*.55})`} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title={`Top ${topN} Categorias por Faturamento`}>
          <ResponsiveContainer width="100%" height={Math.max(280, topN * 28)}>
            <BarChart data={categorias} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="var(--grid)" horizontal={false} />
              <XAxis type="number" tick={{ fill:'var(--sub)', fontSize:10 }} axisLine={false} tickLine={false}
                tickFormatter={v => `R$${(v/1000).toFixed(0)}k`} />
              <YAxis type="category" dataKey="categoria" tick={{ fill:'var(--sub)', fontSize:9 }}
                axisLine={false} tickLine={false} width={90} />
              <Tooltip content={<CustomTooltip currency />} />
              <Bar dataKey="faturamento" name="Faturamento" radius={[0,4,4,0]}>
                {categorias.map((_, i) => <Cell key={i} fill={`rgba(168,85,247,${.45 + (i/topN)*.55})`} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <ChartCard title="Distribuição de Receita">
          <ResponsiveContainer width="100%" height={320}>
            <PieChart>
              <Pie data={categorias} dataKey="faturamento" nameKey="categoria"
                innerRadius="52%" outerRadius="75%" paddingAngle={2}>
                {categorias.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip formatter={(v) => fmt.currency(v as number)} />
              <Legend wrapperStyle={{ fontSize:11, color:'var(--sub)' }} />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Volume por Categoria">
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={categorias}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--grid)" />
              <XAxis dataKey="categoria" tick={{ fill:'var(--sub)', fontSize:9 }} axisLine={false} tickLine={false} angle={-30} textAnchor="end" height={48} />
              <YAxis tick={{ fill:'var(--sub)', fontSize:10 }} axisLine={false} tickLine={false} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="quantidade" name="Unidades" fill="#06b6d4" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <ChartCard title="Dados completos por categoria">
        <div className="overflow-x-auto">
          <table className="w-full text-sm" style={{ color:'var(--text)' }}>
            <thead>
              <tr style={{ borderBottom:'1px solid var(--border)' }}>
                {['Categoria','Faturamento','Quantidade'].map(h => (
                  <th key={h} className="text-left py-2 px-3" style={{ color:'var(--sub)', fontSize:'.65rem', textTransform:'uppercase', letterSpacing:'.1em', fontWeight:700 }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {(data.top_categorias ?? []).map((r, i) => (
                <tr key={i} style={{ borderBottom:'1px solid var(--border)' }}
                  className="transition-colors hover:bg-white/5">
                  <td className="py-2 px-3" style={{ fontSize:'.84rem' }}>{r.categoria}</td>
                  <td className="py-2 px-3 font-semibold" style={{ color:'var(--acc)', fontSize:'.84rem' }}>{fmt.currency(r.faturamento)}</td>
                  <td className="py-2 px-3" style={{ fontSize:'.84rem' }}>{fmt.number(r.quantidade)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </ChartCard>
    </div>
  )
}
