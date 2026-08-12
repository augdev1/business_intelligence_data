import { useRef, useState } from 'react'
import { Send, Trash2, ChevronDown, ChevronUp } from 'lucide-react'
import { api, type IAResponse } from '@/lib/api'
import { useTheme } from '@/context/ThemeContext'
import { PageHeader } from './Dashboard'

interface Msg {
  role: 'user' | 'assistant'
  content: string
  mode?: string
  sql?: string
  dados?: unknown[]
  reviews_evidences?: Array<{ review_id: string; score?: number; comment_text?: string; similarity_score?: number }>
  products_evidences?: Array<{ product_id: string; category_name?: string; text_content: string; similarity_score?: number }>
}

const SUGGESTIONS = [
  'O que os clientes comentam sobre os atrasos de entrega?',
  'Quais os principais elogios e opiniões nas avaliações?',
  'Produtos com melhores avaliações e maior receita',
  'Qual estado gerou maior faturamento total?',
]

function SqlExpander({ sql }: { sql: string }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="mt-2">
      <button onClick={() => setOpen(o => !o)}
        className="flex items-center gap-1 text-xs font-medium transition-colors"
        style={{ color:'var(--sub)' }}>
        {open ? <ChevronUp size={12}/> : <ChevronDown size={12}/>}
        {open ? 'Ocultar SQL' : 'Ver SQL gerado'}
      </button>
      {open && <pre className="mt-2 text-xs overflow-x-auto p-2.5 rounded bg-black/20 border border-white/10">{sql}</pre>}
    </div>
  )
}

function RagEvidencesDisplay({
  reviews,
  products
}: {
  reviews?: Array<{ review_id: string; score?: number; comment_text?: string; similarity_score?: number }>
  products?: Array<{ product_id: string; category_name?: string; text_content: string; similarity_score?: number }>
}) {
  const [open, setOpen] = useState(true)
  if ((!reviews || reviews.length === 0) && (!products || products.length === 0)) return null

  return (
    <div className="mt-3 pt-3 border-t border-white/10">
      <button onClick={() => setOpen(o => !o)}
        className="flex items-center gap-1.5 text-xs font-semibold text-teal-400 mb-2">
        {open ? <ChevronUp size={12}/> : <ChevronDown size={12}/>}
        🎯 Evidências Recuperadas por RAG Vetorial (pgvector)
      </button>

      {open && (
        <div className="space-y-2 mt-2">
          {reviews && reviews.length > 0 && (
            <div className="space-y-1.5">
              <span className="text-[11px] uppercase tracking-wider font-bold text-amber-300">💬 Avaliações de Clientes (Reviews)</span>
              <div className="grid gap-1.5">
                {reviews.map((r, idx) => (
                  <div key={idx} className="p-2 rounded-lg text-xs bg-white/5 border border-white/10">
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-semibold text-amber-400">Nota: {r.score ?? 5}/5 ⭐</span>
                      {r.similarity_score && (
                        <span className="text-[10px] opacity-70">Similaridade: {(r.similarity_score * 100).toFixed(1)}%</span>
                      )}
                    </div>
                    <p className="italic text-gray-300">"{r.comment_text || 'Sem texto de comentário'}"</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {products && products.length > 0 && (
            <div className="space-y-1.5 mt-2">
              <span className="text-[11px] uppercase tracking-wider font-bold text-indigo-300">📦 Catálogo de Produtos</span>
              <div className="grid gap-1.5">
                {products.map((p, idx) => (
                  <div key={idx} className="p-2 rounded-lg text-xs bg-white/5 border border-white/10">
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-semibold text-indigo-300">{p.category_name || p.product_id}</span>
                      {p.similarity_score && (
                        <span className="text-[10px] opacity-70">Match Vetorial: {(p.similarity_score * 100).toFixed(1)}%</span>
                      )}
                    </div>
                    <p className="text-gray-300">{p.text_content}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function FormatMessage({ text }: { text: string }) {
  const { theme } = useTheme()
  const isTurquoise = theme === 'light'
  const lines = text.split('\n')
  return (
    <div className="space-y-1 text-sm leading-relaxed" style={{ color: 'var(--text)' }}>
      {lines.map((line, lineIdx) => {
        let cleanLine = line
        let isBullet = false

        if (line.trim().startsWith('* ')) {
          cleanLine = line.trim().replace(/^\*\s+/, '• ')
          isBullet = true
        } else if (line.trim().startsWith('- ')) {
          cleanLine = line.trim().replace(/^-\s+/, '• ')
          isBullet = true
        }

        const parts = cleanLine.split(/\*\*([^*]+)\*\*/g)

        return (
          <div key={lineIdx} className={`${isBullet ? 'pl-4 py-0.5' : ''}`}>
            {parts.map((part, partIdx) => {
              if (partIdx % 2 === 1) {
                return (
                  <strong key={partIdx} className="font-semibold text-indigo-400" style={{ color: isTurquoise ? '#0d9488' : '#a5b4fc' }}>
                    {part}
                  </strong>
                )
              }
              return part
            })}
          </div>
        )
      })}
    </div>
  )
}

export function AIAssistant() {
  const { theme } = useTheme()
  const isTurquoise = theme === 'light'
  const [msgs, setMsgs] = useState<Msg[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const textRef = useRef<HTMLTextAreaElement>(null)
  const bottomRef = useRef<HTMLDivElement>(null)

  const send = async (q: string) => {
    if (!q.trim() || loading) return
    const question = q.trim()
    setMsgs(m => [...m, { role: 'user', content: question }])
    setInput('')
    setLoading(true)
    try {
      const res: IAResponse = await api.askIA(question)
      if (res.sucesso) {
        setMsgs(m => [
          ...m,
          {
            role: 'assistant',
            content: res.resposta,
            mode: res.mode,
            sql: res.sql,
            dados: res.dados,
            reviews_evidences: res.reviews_evidences,
            products_evidences: res.products_evidences,
          },
        ])
      } else {
        setMsgs(m => [...m, { role: 'assistant', content: res.resposta || 'Erro ao processar.' }])
      }
    } catch {
      setMsgs(m => [...m, { role: 'assistant', content: 'Erro de conexão. Verifique se a API está rodando.' }])
    } finally {
      setLoading(false)
      setTimeout(() => bottomRef.current?.scrollIntoView({ behavior: 'smooth' }), 100)
    }
  }

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send(input)
    }
  }

  return (
    <div>
      <PageHeader title="Assistente RAG & BI" sub="Consultas Híbridas RAG (Text-to-SQL + Busca Vetorial em Reviews & Produtos via pgvector)" />

      {/* Suggestion chips */}
      <div className="flex flex-wrap gap-2 mb-5">
        {SUGGESTIONS.map(s => (
          <button key={s} className="chip-btn" onClick={() => send(s)}>{s}</button>
        ))}
      </div>

      {/* Messages */}
      <div className="flex flex-col gap-3 mb-4 min-h-[120px]" style={{ maxHeight: 520, overflowY: 'auto' }}>
        {msgs.length === 0 && (
          <div className="glass-card rounded-xl p-5 text-center" style={{ color: 'var(--sub)' }}>
            <div className="text-3xl mb-2">🧠</div>
            <p className="text-sm font-semibold">Assistente RAG Híbrido Ativo</p>
            <p className="text-xs opacity-75 mt-1">Pergunte sobre faturamento, produtos ou análises de sentimentos dos comentários dos clientes.</p>
          </div>
        )}

        {msgs.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] ${m.role === 'assistant' ? 'w-full' : ''}`}>
              {m.role === 'user' ? (
                <div className="rounded-[14px] rounded-tr-sm px-4 py-2.5 text-sm font-medium"
                  style={{ background: isTurquoise ? 'linear-gradient(135deg,#2dd4bf,#0d9488)' : 'linear-gradient(135deg,#6366f1,#8b5cf6)', color: '#fff' }}>
                  {m.content}
                </div>
              ) : (
                <div className="glass-card rounded-[14px] rounded-tl-sm px-4 py-3 text-sm leading-relaxed"
                  style={{ color: 'var(--text)' }}>
                  <div className="flex items-center justify-between mb-2 pb-1 border-b border-white/10" style={{ color: 'var(--sub)', fontSize: '.7rem' }}>
                    <div className="flex items-center gap-1.5">
                      <span>⚡</span> <span className="font-semibold uppercase tracking-wide">Assistente RAG Híbrido</span>
                    </div>
                    {m.mode && (
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-teal-500/20 text-teal-300 border border-teal-500/30">
                        {m.mode === 'vector_rag' ? 'RAG Vetorial' : m.mode === 'hybrid' ? 'RAG Híbrido' : 'SQL Analytics'}
                      </span>
                    )}
                  </div>
                  <FormatMessage text={m.content} />
                  <RagEvidencesDisplay reviews={m.reviews_evidences} products={m.products_evidences} />
                  {m.sql && <SqlExpander sql={m.sql} />}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="glass-card rounded-[14px] rounded-tl-sm px-4 py-3 max-w-[60%]">
            <div className="flex items-center gap-2" style={{ color: 'var(--sub)', fontSize: '.82rem' }}>
              <div className="flex gap-1">
                {[0, 1, 2].map(i => (
                  <div key={i} className="w-1.5 h-1.5 rounded-full animate-bounce"
                    style={{ background: isTurquoise ? '#2dd4bf' : '#6366f1', animationDelay: `${i * .15}s` }} />
                ))}
              </div>
              Buscando evidências vetoriais & gerando respostas...
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="glass-card rounded-[16px] p-3 flex gap-3 items-end">
        <textarea
          ref={textRef}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKey}
          placeholder="Faça uma pergunta RAG sobre faturamento ou reviews dos clientes..."
          className="chat-input flex-1"
          rows={1}
          style={{ minHeight: 44, maxHeight: 120, resize: 'none' }}
        />
        <button onClick={() => send(input)} disabled={loading || !input.trim()}
          className="flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center transition-all"
          style={{
            background: input.trim() && !loading ? (isTurquoise ? 'linear-gradient(135deg,#2dd4bf,#0d9488)' : 'linear-gradient(135deg,#6366f1,#8b5cf6)') : 'var(--border)',
            cursor: input.trim() && !loading ? 'pointer' : 'not-allowed',
          }}>
          <Send size={15} color="white" />
        </button>
      </div>

      {msgs.length > 0 && (
        <div className="flex justify-end mt-3">
          <button onClick={() => setMsgs([])}
            className="flex items-center gap-1.5 text-xs font-medium transition-colors hover:opacity-80"
            style={{ color: 'var(--sub)' }}>
            <Trash2 size={12} /> Limpar conversa
          </button>
        </div>
      )}
    </div>
  )
}

