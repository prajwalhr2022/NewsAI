'use client'
import { useEffect, useState, useCallback } from 'react'
import { useTheme } from 'next-themes'
import { Search, Sun, Moon, Zap } from 'lucide-react'

const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'हिं' },
  { code: 'ta', label: 'தமி' },
  { code: 'te', label: 'తెలు' },
  { code: 'ml', label: 'മല' },
  { code: 'bn', label: 'বাং' },
  { code: 'mr', label: 'मरा' },
  { code: 'kn', label: 'ಕನ್' },
]

interface HeaderProps {
  search: string
  onSearchChange: (v: string) => void
  language: string
  onLanguageChange: (v: string) => void
}

export default function Header({ search, onSearchChange, language, onLanguageChange }: HeaderProps) {
  const { theme, setTheme, resolvedTheme } = useTheme()
  const [mounted, setMounted] = useState(false)
  const [time, setTime] = useState('')

  useEffect(() => { setMounted(true) }, [])

  useEffect(() => {
    const tick = () => {
      setTime(new Date().toLocaleTimeString('en-IN', {
        hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true,
      }))
    }
    tick()
    const id = setInterval(tick, 1000)
    return () => clearInterval(id)
  }, [])

  const toggleTheme = useCallback(() => {
    setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')
  }, [resolvedTheme, setTheme])

  return (
    <header className="header">
      <div className="page-wrapper">
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', padding: '0.75rem 0' }}>

          {/* Logo */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexShrink: 0 }}>
            <div style={{ background: 'var(--accent)', borderRadius: '8px', padding: '5px', display: 'flex' }}>
              <Zap size={18} color="white" fill="white" />
            </div>
            <span style={{ fontFamily: 'var(--font-playfair)', fontWeight: 900, fontSize: '1.375rem', color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>
              NewsAI
            </span>
            {time && (
              <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', fontVariantNumeric: 'tabular-nums', marginLeft: '0.25rem' }}>
                {time}
              </span>
            )}
          </div>

          {/* Search */}
          <div className="search-wrapper" style={{ flex: 1, maxWidth: '480px', position: 'relative' }}>
            <Search
              size={15}
              style={{ position: 'absolute', left: '0.875rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)', pointerEvents: 'none' }}
            />
            <input
              className="search-input"
              type="text"
              placeholder="Search headlines..."
              value={search}
              onChange={e => onSearchChange(e.target.value)}
            />
          </div>

          {/* Right controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginLeft: 'auto' }}>
            <select
              className="lang-select"
              value={language}
              onChange={e => onLanguageChange(e.target.value)}
              title="Select language"
            >
              {LANGUAGES.map(l => (
                <option key={l.code} value={l.code}>{l.label}</option>
              ))}
            </select>

            {mounted && (
              <button className="theme-toggle" onClick={toggleTheme} title="Toggle theme" aria-label="Toggle theme">
                {resolvedTheme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
              </button>
            )}
          </div>

        </div>
      </div>
    </header>
  )
}
