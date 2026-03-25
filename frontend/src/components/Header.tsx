'use client'
import { useEffect, useState, useCallback } from 'react'
import { useTheme } from 'next-themes'
import { Search, Sun, Moon, Zap } from 'lucide-react'

const LANGUAGES = [
  { code: 'en', label: 'EN' },
  { code: 'hi', label: 'हिं' },
  { code: 'kn', label: 'ಕನ್' },
]

interface HeaderProps {
  search: string
  onSearchChange: (v: string) => void
  language: string
  onLanguageChange: (v: string) => void
}

export default function Header({ search, onSearchChange, language, onLanguageChange }: HeaderProps) {
  const { setTheme, resolvedTheme } = useTheme()
  const [mounted, setMounted] = useState(false)
  const [time, setTime] = useState('')

  useEffect(() => { setMounted(true) }, [])

  useEffect(() => {
    const tick = () => setTime(new Date().toLocaleTimeString('en-IN', {
      hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true,
    }))
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
            <div>
              <div style={{ fontFamily: 'var(--font-playfair)', fontWeight: 900, fontSize: '1.25rem', color: 'var(--text-primary)', letterSpacing: '-0.01em', lineHeight: 1.1 }}>
                NewsAI
              </div>
              {/* <div style={{ fontSize: '0.6rem', color: 'var(--text-muted)', letterSpacing: '0.05em', textTransform: 'uppercase' }}>
                Truth · News · Insight
              </div> */}
            </div>
            {time && (
              <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginLeft: '0.5rem', fontVariantNumeric: 'tabular-nums' }}>
                {time}
              </span>
            )}
          </div>

          {/* Search */}
          <div style={{ flex: 1, maxWidth: '500px', position: 'relative' }}>
            <Search size={15} style={{ position: 'absolute', left: '0.875rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)', pointerEvents: 'none' }} />
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
            <div style={{ display: 'flex', background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: '9999px', padding: '3px', gap: '2px' }}>
              {LANGUAGES.map(l => (
                <button
                  key={l.code}
                  onClick={() => onLanguageChange(l.code)}
                  style={{
                    padding: '0.25rem 0.625rem', borderRadius: '9999px',
                    fontSize: '0.75rem', fontWeight: 500, border: 'none', cursor: 'pointer',
                    background: language === l.code ? 'var(--accent)' : 'transparent',
                    color: language === l.code ? 'white' : 'var(--text-secondary)',
                    transition: 'all 0.2s', fontFamily: 'var(--font-dm)',
                  }}
                >
                  {l.label}
                </button>
              ))}
            </div>
            {mounted && (
              <button className="theme-toggle" onClick={toggleTheme} title="Toggle theme">
                {resolvedTheme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
              </button>
            )}
          </div>

        </div>
      </div>
    </header>
  )
}
