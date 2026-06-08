import { Outlet } from 'react-router-dom'
import { Sidebar } from './Sidebar'

export function Layout() {
  return (
    <div style={{ background: 'var(--bg)', minHeight: '100vh' }}>
      <Sidebar />
      <main style={{ marginLeft: 258, padding: '1.5rem 2rem 2.5rem', minHeight: '100vh' }}>
        <Outlet />
      </main>
    </div>
  )
}
