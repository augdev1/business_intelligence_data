import { useEffect, useState } from 'react'
import { api, type KPIData } from '@/lib/api'

let cachedKPIs: KPIData | null = null

export function useKPIs() {
  const [data,    setData]    = useState<KPIData | null>(cachedKPIs)
  const [loading, setLoading] = useState<boolean>(!cachedKPIs)
  const [error,   setError]   = useState<string | null>(null)

  useEffect(() => {
    let alive = true
    if (!cachedKPIs) {
      setLoading(true)
    }
    api.getKPIs()
      .then(d => {
        cachedKPIs = d
        if (alive) {
          setData(d)
          setError(null)
        }
      })
      .catch(e => {
        if (alive && !cachedKPIs) setError(e.message)
      })
      .finally(() => {
        if (alive) setLoading(false)
      })
    return () => {
      alive = false
    }
  }, [])

  return { data, loading, error }
}
