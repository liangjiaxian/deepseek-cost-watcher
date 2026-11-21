const STORAGE_KEY = 'dsm_auth'

export function getSession() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null')
    if (!saved || !saved.token || !saved.exp || saved.exp <= Date.now()) {
      if (saved) localStorage.removeItem(STORAGE_KEY)
      return null
    }
    return saved
  } catch {
    localStorage.removeItem(STORAGE_KEY)
    return null
  }
}

export function getToken() {
  return getSession()?.token || ''
}

export function isAuthenticated() {
  return !!getSession()
}

export function setSession(token, expiresAt) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({ token, exp: expiresAt }))
}

export function clearSession() {
  localStorage.removeItem(STORAGE_KEY)
}

export const logout = clearSession
