import { useEffect, useState } from 'react'
import { api, type KPIData } from '@/lib/api'

export function useKPIs() {
  const [data,    setData]    = useState<KPIData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState<string | null>(null)

  useEffect(() => {
    let alive = true
    setLoading(true)
    api.getKPIs()
      .then(d  => { if (alive) { setData(d); setError(null) } })
      .catch(e => { if (alive) setError(e.message) })
      .finally(()=> { if (alive) setLoading(false) })
    return () => { alive = false }
  }, [])

  return { data, loading, error }
}
