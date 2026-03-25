'use client'
import { Flame, TrendingUp } from 'lucide-react'
import type { Category, TrendingTopic } from '@/lib/supabase'

const CATEGORY_EMOJIS: Record<string, string> = {
  'Politics':              '🏛️',
  'Geopolitics':           '🌏',
  'Regional Politics':     '🗳️',
  'Technology':            '💻',
  'Business & Economy':    '📈',
  'Trade & Markets':       '💹',
  'Agriculture':           '🌾',
  'Sports':                '⚽',
  'Cricket':               '🏏',
  'Science & Space':       '🚀',
  'Health & Medicine':     '🏥',
  'Entertainment':         '🎬',
  'Environment & Climate': '🌍',
  'World Affairs':         '🌐',
  'Crime & Law':           '⚖️',
  'Education':             '📚',
  'Lifestyle':             '✨',
  'Defence & Security':    '🛡️',
  'Cars & Automobiles':    '🚗',
  'Electronics & Gadgets': '📱',
}

interface CategoryBarProps {
  categories: Category[]
  activeCategory: string
  onCategoryChange: (cat: string) => void
  topics: TrendingTopic[]
  onTopicClick: (topic: string) => void
}

export default function CategoryBar({
  categories, activeCategory, onCategoryChange, topics, onTopicClick,
}: CategoryBarProps) {
  const topLevel = categories.filter(c => !c.parent_slug)

  const pillStyle = (isActive: boolean) => ({
    display: 'flex' as const, alignItems: 'center' as const, gap: '0.35rem',
    padding: '0.35rem 0.875rem',
    borderRadius: '9999px',
    fontSize: '0.8rem',
    fontWeight: isActive ? 600 : 400,
    border: isActive ? '1.5px solid var(--accent)' : '1px solid var(--border)',
    background: isActive ? 'var(--accent-soft)' : 'var(--bg-card)',
    color: isActive ? 'var(--accent)' : 'var(--text-secondary)',
    cursor: 'pointer' as const,
    whiteSpace: 'nowrap' as const,
    flexShrink: 0,
    transition: 'all 0.2s',
    fontFamily: 'var(--font-dm)',
  })

  return (
    <div style={{ borderBottom: '1px solid var(--border)', background: 'var(--bg)' }}>
      {/* Categories row */}
      <div style={{ borderBottom: '1px solid var(--border)', padding: '0.5rem 0' }}>
        <div className="page-wrapper">
          <div className="hide-scrollbar" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', overflowX: 'auto', paddingBottom: '2px' }}>
            <button style={pillStyle(activeCategory === 'all')} onClick={() => onCategoryChange('all')}>
              📰 All News
            </button>
            {topLevel.map(cat => (
              <button key={cat.slug} style={pillStyle(activeCategory === cat.name)} onClick={() => onCategoryChange(cat.name)}>
                <span style={{ fontSize: '0.85rem' }}>{CATEGORY_EMOJIS[cat.name] ?? '📄'}</span>
                {cat.name}
                <span style={{
                  fontSize: '0.65rem',
                  background: activeCategory === cat.name ? 'var(--accent)' : 'var(--border)',
                  color: activeCategory === cat.name ? 'white' : 'var(--text-muted)',
                  padding: '1px 5px', borderRadius: '9999px', marginLeft: '2px',
                }}>
                  {cat.article_count}
                </span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Trending row */}
      {topics.length > 0 && (
        <div style={{ padding: '0.4rem 0' }}>
          <div className="page-wrapper">
            <div className="hide-scrollbar" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', overflowX: 'auto' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', flexShrink: 0, color: 'var(--accent)' }}>
                <Flame size={13} />
                <span style={{ fontSize: '0.68rem', fontWeight: 600, letterSpacing: '0.08em', textTransform: 'uppercase' }}>
                  Trending
                </span>
              </div>
              {topics.map((topic, i) => (
                <button
                  key={i}
                  onClick={() => onTopicClick(topic.topic)}
                  style={{
                    display: 'flex', alignItems: 'center', gap: '0.25rem',
                    fontSize: '0.75rem', color: 'var(--text-muted)',
                    background: 'transparent', border: 'none',
                    cursor: 'pointer', whiteSpace: 'nowrap', flexShrink: 0,
                    padding: '0.2rem 0.5rem', borderRadius: '9999px',
                    transition: 'all 0.2s', fontFamily: 'var(--font-dm)',
                  }}
                  onMouseEnter={e => { (e.currentTarget as HTMLElement).style.color = 'var(--accent)'; (e.currentTarget as HTMLElement).style.background = 'var(--accent-soft)' }}
                  onMouseLeave={e => { (e.currentTarget as HTMLElement).style.color = 'var(--text-muted)'; (e.currentTarget as HTMLElement).style.background = 'transparent' }}
                >
                  <TrendingUp size={10} />
                  {topic.topic}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
