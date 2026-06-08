import { useRef, useState } from 'react'
import { Send, Trash2, ChevronDown, ChevronUp } from 'lucide-react'
import { api, type IAResponse } from '@/lib/api'
import { PageHeader } from './Dashboard'

interface Msg { role: 'user'|'assistant'; content: string; sql?: string; dados?: unknown[] }

const SUGGESTIONS = [
  'Qual estado gerou mais receita?',
  'Top 5 categorias?',
  'Produto mais vendido?',
  'Método de pagamento mais usado?',
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
      {open && <pre className="mt-2 text-xs overflow-x-auto">{sql}</pre>}
    </div>
  )
}

export function AIAssistant() {
  const [msgs,    setMsgs]    = useState<Msg[]>([])
  const [input,   setInput]   = useState('')
  const [loading, setLoading] = useState(false)
  const textRef = useRef<HTMLTextAreaElement>(null)
  const bottomRef = useRef<HTMLDivElement>(null)

  const send = async (q: string) => {
    if (!q.trim() || loading) return
    const question = q.trim()
    setMsgs(m => [...m, { role:'user', content: question }])
    setInput('')
    setLoading(true)
    try {
      const res: IAResponse = await api.askIA(question)
      if (res.sucesso) {
        setMsgs(m => [...m, { role:'assistant', content: res.resposta, sql: res.sql, dados: res.dados }])
      } else {
        setMsgs(m => [...m, { role:'assistant', content: res.resposta || 'Erro ao processar.' }])
      }
    } catch {
      setMsgs(m => [...m, { role:'assistant', content: 'Erro de conexão. Verifique se a API está rodando.' }])
    } finally {
      setLoading(false)
      setTimeout(() => bottomRef.current?.scrollIntoView({ behavior:'smooth' }), 100)
    }
  }

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(input) }
  }

  return (
    <div>
      <PageHeader title="Assistente de Dados" sub="Perguntas em linguagem natural sobre o dataset Olist" />

      {/* Suggestion chips */}
      <div className="flex flex-wrap gap-2 mb-5">
        {SUGGESTIONS.map(s => (
          <button key={s} className="chip-btn" onClick={() => send(s)}>{s}</button>
        ))}
      </div>

      {/* Messages */}
      <div className="flex flex-col gap-3 mb-4 min-h-[120px]" style={{ maxHeight: 480, overflowY:'auto' }}>
        {msgs.length === 0 && (
          <div className="glass-card rounded-xl p-5 text-center" style={{ color:'var(--sub)' }}>
            <div className="text-3xl mb-2">🤖</div>
            <p className="text-sm">Faça uma pergunta sobre os dados do Olist E-Commerce</p>
          </div>
        )}

        {msgs.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[82%] ${m.role === 'assistant' ? 'w-full' : ''}`}>
              {m.role === 'user' ? (
                <div className="rounded-[14px] rounded-tr-sm px-4 py-2.5 text-sm font-medium"
                  style={{ background:'linear-gradient(135deg,var(--acc),var(--acc2))', color:'#fff' }}>
                  {m.content}
                </div>
              ) : (
                <div className="glass-card rounded-[14px] rounded-tl-sm px-4 py-3 text-sm leading-relaxed"
                  style={{ color:'var(--text)' }}>
                  <div className="flex items-center gap-1.5 mb-2" style={{ color:'var(--sub)', fontSize:'.7rem' }}>
                    <span>🤖</span> <span className="font-semibold uppercase tracking-wide">Assistente IA</span>
                  </div>
                  <p style={{ whiteSpace:'pre-wrap', margin:0 }}>{m.content}</p>
                  {m.sql && <SqlExpander sql={m.sql} />}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="glass-card rounded-[14px] rounded-tl-sm px-4 py-3 max-w-[60%]">
            <div className="flex items-center gap-2" style={{ color:'var(--sub)', fontSize:'.82rem' }}>
              <div className="flex gap-1">
                {[0,1,2].map(i => (
                  <div key={i} className="w-1.5 h-1.5 rounded-full animate-bounce"
                    style={{ background:'var(--acc)', animationDelay:`${i*.15}s` }} />
                ))}
              </div>
              Analisando dados...
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
          placeholder="Faça uma pergunta sobre os dados Olist... (Enter para enviar)"
          className="chat-input flex-1"
          rows={1}
          style={{ minHeight:44, maxHeight:120, resize:'none' }}
        />
        <button onClick={() => send(input)} disabled={loading || !input.trim()}
          className="flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center transition-all"
          style={{
            background: input.trim() && !loading ? 'linear-gradient(135deg,var(--acc),var(--acc2))' : 'var(--border)',
            cursor: input.trim() && !loading ? 'pointer' : 'not-allowed',
          }}>
          <Send size={15} color="white" />
        </button>
      </div>

      {msgs.length > 0 && (
        <div className="flex justify-end mt-3">
          <button onClick={() => setMsgs([])}
            className="flex items-center gap-1.5 text-xs font-medium transition-colors hover:opacity-80"
            style={{ color:'var(--sub)' }}>
            <Trash2 size={12} /> Limpar conversa
          </button>
        </div>
      )}
    </div>
  )
}
