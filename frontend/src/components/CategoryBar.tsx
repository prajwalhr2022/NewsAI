'use client'
import type { Category } from '@/lib/supabase'

const CATEGORY_EMOJIS: Record<string, string> = {
  'Politics':              '🏛️',
  'Technology':            '💻',
  'Business & Economy':    '📈',
  'Sports':                '⚽',
  'Science & Space':       '🚀',
  'Health & Medicine':     '🏥',
  'Entertainment':         '🎬',
  'Environment & Climate': '🌍',
  'World Affairs':         '🌐',
  'Crime & Law':           '⚖️',
  'Education':             '📚',
  'Lifestyle':             '✨',
  'Defence & Security':    '🛡️',
}

interface CategoryBarProps {
  categories: Category[]
  activeCategory: string
  onCategoryChange: (cat: string) => void
}

export default function CategoryBar({ categories, activeCategory, onCategoryChange }: CategoryBarProps) {
  const topLevel = categories.filter(c => !c.parent_slug)

  return (
    <div style={{ borderBottom: '1px solid var(--border)', padding: '0.625rem 0', background: 'var(--bg)' }}>
      <div className="page-wrapper">
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          overflowX: 'auto',
          scrollbarWidth: 'none',
          paddingBottom: '2px',
        }}>

          {/* All News pill */}
          <button
            onClick={() => onCategoryChange('all')}
            style={{
              display: 'flex', alignItems: 'center', gap: '0.35rem',
              padding: '0.35rem 0.875rem',
              borderRadius: '9999px',
              fontSize: '0.8rem',
              fontWeight: activeCategory === 'all' ? 600 : 400,
              border: activeCategory === 'all' ? '1.5px solid var(--accent)' : '1px solid var(--border)',
              background: activeCategory === 'all' ? 'var(--accent-soft)' : 'var(--bg-card)',
              color: activeCategory === 'all' ? 'var(--accent)' : 'var(--text-secondary)',
              cursor: 'pointer',
              whiteSpace: 'nowrap',
              flexShrink: 0,
              transition: 'all 0.2s',
              fontFamily: 'var(--font-dm)',
            }}
          >
            📰 All News
          </button>

          {/* Dynamic category pills */}
          {topLevel.map(cat => {
            const isActive = activeCategory === cat.name
            return (
              <button
                key={cat.slug}
                onClick={() => onCategoryChange(cat.name)}
                style={{
                  display: 'flex', alignItems: 'center', gap: '0.35rem',
                  padding: '0.35rem 0.875rem',
                  borderRadius: '9999px',
                  fontSize: '0.8rem',
                  fontWeight: isActive ? 600 : 400,
                  border: isActive ? '1.5px solid var(--accent)' : '1px solid var(--border)',
                  background: isActive ? 'var(--accent-soft)' : 'var(--bg-card)',
                  color: isActive ? 'var(--accent)' : 'var(--text-secondary)',
                  cursor: 'pointer',
                  whiteSpace: 'nowrap',
                  flexShrink: 0,
                  transition: 'all 0.2s',
                  fontFamily: 'var(--font-dm)',
                }}
              >
                <span style={{ fontSize: '0.85rem' }}>{CATEGORY_EMOJIS[cat.name] ?? '📄'}</span>
                {cat.name}
                <span style={{
                  fontSize: '0.65rem',
                  background: isActive ? 'var(--accent)' : 'var(--border)',
                  color: isActive ? 'white' : 'var(--text-muted)',
                  padding: '1px 5px',
                  borderRadius: '9999px',
                  marginLeft: '2px',
                }}>
                  {cat.article_count}
                </span>
              </button>
            )
          })}
        </div>
      </div>
    </div>
  )
}
