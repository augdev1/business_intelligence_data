import { Outlet } from 'react-router-dom'
import { Sidebar } from './Sidebar'

export function Layout() {
  return (
    <div style={{ background: 'var(--bg)', minHeight: '100vh', position: 'relative', overflowX: 'hidden' }}>
      {/* Background radial glowing effects matching premium dark theme */}
      <div 
        className="absolute top-[10%] left-[20%] w-[500px] h-[500px] rounded-full pointer-events-none opacity-30 blur-[100px] z-0"
        style={{ background: 'radial-gradient(circle, var(--glow-1) 0%, transparent 70%)' }} 
      />
      <div 
        className="absolute bottom-[20%] right-[10%] w-[600px] h-[600px] rounded-full pointer-events-none opacity-20 blur-[120px] z-0"
        style={{ background: 'radial-gradient(circle, var(--glow-2) 0%, transparent 70%)' }} 
      />

      <Sidebar />
      
      <main style={{ marginLeft: 258, padding: '1.5rem 2rem 2.5rem', minHeight: '100vh', position: 'relative', zIndex: 1 }}>
        <Outlet />
      </main>
    </div>
  )
}
