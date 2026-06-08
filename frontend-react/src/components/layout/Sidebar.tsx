import { NavLink } from 'react-router-dom'
import { LayoutDashboard, Package, MapPin, Bot, Sun, Moon } from 'lucide-react'
import { useTheme } from '@/context/ThemeContext'

const NAV = [
  { to: '/',          icon: LayoutDashboard, label: 'Visão Executiva' },
  { to: '/produtos',  icon: Package,         label: 'Produtos' },
  { to: '/clientes',  icon: MapPin,          label: 'Clientes e Geo' },
  { to: '/assistente',icon: Bot,             label: 'Assistente IA' },
]

function NavIcon({ color, children }: { color: string; children: React.ReactNode }) {
  return (
    <div className="flex-shrink-0 w-7 h-7 rounded-[8px] flex items-center justify-center text-sm"
      style={{ background: color }}>
      {children}
    </div>
  )
}

const NAV_ICONS = [
  'linear-gradient(135deg,#5c6ff5,#a855f7)',
  'linear-gradient(135deg,#06b6d4,#0891b2)',
  'linear-gradient(135deg,#10b981,#059669)',
  'linear-gradient(135deg,#f59e0b,#d97706)',
]

export function Sidebar() {
  const { theme, toggle } = useTheme()
  const today = new Date().toLocaleDateString('pt-BR', { weekday:'short', day:'2-digit', month:'2-digit', year:'numeric' })

  return (
    <aside className="sidebar fixed left-0 top-0 h-screen w-[258px] flex flex-col z-50 overflow-y-auto overflow-x-hidden">

      {/* Logo */}
      <div className="px-3 pt-5 pb-2">
        <div className="flex items-center gap-2.5 mb-5">
          <div className="w-9 h-9 flex-shrink-0 rounded-[10px] flex items-center justify-center text-lg"
            style={{ background:'linear-gradient(135deg,#5c6ff5,#a855f7)', boxShadow:'0 4px 16px rgba(92,111,245,.45)' }}>
            📊
          </div>
          <div>
            <div className="text-white font-bold text-[.9rem] tracking-tight">Olist Analytics</div>
            <div className="text-[.57rem] uppercase tracking-[.1em] mt-px" style={{ color:'rgba(255,255,255,.3)' }}>
              Business Intelligence
            </div>
          </div>
        </div>

        {/* User card */}
        <div className="flex items-center gap-2.5 rounded-xl p-3 mb-5"
          style={{ background:'rgba(255,255,255,.05)', border:'1px solid rgba(255,255,255,.07)' }}>
          <div className="w-8 h-8 flex-shrink-0 rounded-full flex items-center justify-center text-sm"
            style={{ background:'linear-gradient(135deg,#5c6ff5,#a855f7)' }}>👤</div>
          <div className="flex-1 min-w-0">
            <div className="text-[#e2e8f0] text-[.78rem] font-semibold">Bem-vindo!</div>
            <div className="text-[.62rem] mt-px truncate" style={{ color:'rgba(255,255,255,.28)' }}>{today}</div>
          </div>
          <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ background:'#10b981', boxShadow:'0 0 6px #10b98177' }} />
        </div>

        {/* Nav label */}
        <p className="text-[.57rem] font-bold uppercase tracking-[.16em] px-0.5 mb-1.5"
          style={{ color:'rgba(255,255,255,.22)' }}>Páginas</p>
      </div>

      {/* Nav */}
      <nav className="px-3 flex-1">
        {NAV.map(({ to, icon: Icon, label }, i) => (
          <NavLink key={to} to={to} end={to === '/'}
            className={({ isActive }) => `nav-item mb-0.5 ${isActive ? 'active' : ''}`}>
            <NavIcon color={NAV_ICONS[i]}>
              <Icon size={13} color="white" />
            </NavIcon>
            {label}
          </NavLink>
        ))}

      </nav>

      {/* Bottom */}
      <div className="px-3 pb-4 mt-auto">
        {/* Theme toggle */}
        <button onClick={toggle}
          className="w-full flex items-center justify-center gap-2 rounded-full py-1.5 text-[.76rem] font-medium transition-all mb-3"
          style={{ background:'rgba(255,255,255,.05)', border:'1px solid rgba(255,255,255,.09)', color:'rgba(255,255,255,.7)' }}
          onMouseEnter={e=>{(e.target as HTMLElement).style.background='rgba(255,255,255,.11)'}}
          onMouseLeave={e=>{(e.target as HTMLElement).style.background='rgba(255,255,255,.05)'}}>
          {theme === 'dark' ? <Sun size={13}/> : <Moon size={13}/>}
          {theme === 'dark' ? 'Modo Claro' : 'Modo Escuro'}
        </button>

        {/* Help card */}
        <div className="rounded-[14px] p-4 relative overflow-hidden"
          style={{ background:'linear-gradient(135deg,rgba(92,111,245,.6),rgba(168,85,247,.55))', border:'1px solid rgba(92,111,245,.35)' }}>
          <div className="absolute -top-4 -right-4 w-16 h-16 rounded-full" style={{ background:'rgba(255,255,255,.06)' }} />
          <div className="absolute -bottom-6 -left-2 w-14 h-14 rounded-full" style={{ background:'rgba(255,255,255,.04)' }} />
          <div className="relative">
            <div className="text-base mb-1">💡</div>
            <div className="text-white text-[.76rem] font-bold mb-1">Precisa de ajuda?</div>
            <div className="text-[.67rem] leading-[1.4] mb-2.5" style={{ color:'rgba(255,255,255,.6)' }}>
              Use o Assistente IA para consultar os dados
            </div>
            <NavLink to="/assistente"
              className="block text-center text-white text-[.66rem] font-bold py-1.5 rounded-[8px] tracking-[.06em]"
              style={{ background:'rgba(255,255,255,.18)', border:'1px solid rgba(255,255,255,.22)' }}>
              ASSISTENTE IA →
            </NavLink>
          </div>
        </div>

        <p className="text-center text-[.57rem] mt-2" style={{ color:'rgba(255,255,255,.16)' }}>
          v2.0 · Olist E-Commerce
        </p>
      </div>
    </aside>
  )
}
