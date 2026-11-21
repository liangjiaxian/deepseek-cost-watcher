export const APP_TIME_ZONE = 'Asia/Shanghai'

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
  return date.toLocaleString('zh-CN', { timeZone: APP_TIME_ZONE, hour12: false, ...options })
}

function beijingParts(date = new Date()) {
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: APP_TIME_ZONE,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).formatToParts(date)
  const get = (type) => parts.find(p => p.type === type)?.value
  return { year: Number(get('year')), month: Number(get('month')), day: Number(get('day')) }
}

export function beijingTodayISO() {
  const { year, month, day } = beijingParts()
  return `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`
}

export function beijingMonthISO() {
  const { year, month } = beijingParts()
  return `${year}-${String(month).padStart(2, '0')}`
}

export function beijingISOWeek(date = new Date()) {
  const { year, month, day } = beijingParts(date)
  const target = new Date(Date.UTC(year, month - 1, day))
  const dayNum = target.getUTCDay() || 7
  target.setUTCDate(target.getUTCDate() + 4 - dayNum)
  const isoYear = target.getUTCFullYear()
  const yearStart = new Date(Date.UTC(isoYear, 0, 1))
  const week = Math.ceil((((target - yearStart) / 86400000) + 1) / 7)
  return { year: isoYear, week }
}
