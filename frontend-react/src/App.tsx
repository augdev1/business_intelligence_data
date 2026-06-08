import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from '@/context/ThemeContext'
import { Layout } from '@/components/layout/Layout'
import { Dashboard } from '@/pages/Dashboard'
import { Products } from '@/pages/Products'
import { Customers } from '@/pages/Customers'
import { AIAssistant } from '@/pages/AIAssistant'

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route index          element={<Dashboard />} />
            <Route path="produtos"   element={<Products />} />
            <Route path="clientes"   element={<Customers />} />
            <Route path="assistente" element={<AIAssistant />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  )
}
