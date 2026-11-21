export function parseUtc(value) {
  if (!value) return null
  if (value instanceof Date) return value
  const text = String(value).trim()
  if (!text) return null
  // Backend timestamps without an offset are UTC; adding Z prevents the
  // browser from interpreting them as local time (8h offset in UTC+8).
  const hasZone = /(?:[zZ]|[+-]\d{2}:?\d{2})$/.test(text)
  const date = new Date(hasZone ? text : `${text}Z`)
  return Number.isNaN(date.getTime()) ? null : date
}

export function formatLocal(value, options = {}) {
  const date = parseUtc(value)
  if (!date) return '--'
  return date.toLocaleString('zh-CN', { hour12: false, ...options })
}
