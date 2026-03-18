'use client'
import { Flame, TrendingUp } from 'lucide-react'
import type { TrendingTopic } from '@/lib/supabase'

interface TrendingBarProps {
  topics: TrendingTopic[]
  onTopicClick?: (topic: string) => void
}

export default function TrendingBar({ topics, onTopicClick }: TrendingBarProps) {
  if (!topics.length) {
    // Show placeholder when no trending topics yet
    const placeholders = ['AI & Technology', 'World Affairs', 'India News', 'Business', 'Science', 'Sports', 'Health', 'Climate']
    return (
      <div style={{ background: 'var(--bg-card)', borderBottom: '1px solid var(--border)', padding: '0.75rem 0' }}>
        <div className="page-wrapper">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', overflowX: 'auto', scrollbarWidth: 'none' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', flexShrink: 0, color: 'var(--accent)' }}>
              <Flame size={14} />
              <span style={{ fontSize: '0.7rem', fontWeight: 600, letterSpacing: '0.08em', textTransform: 'uppercase' }}>Trending</span>
            </div>
            {placeholders.map((t, i) => (
              <span key={i} style={{
                fontSize: '0.8rem', color: 'var(--text-muted)',
                background: 'var(--bg)', border: '1px solid var(--border)',
                padding: '0.25rem 0.75rem', borderRadius: '9999px', whiteSpace: 'nowrap', flexShrink: 0,
              }}>
                {t}
              </span>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div style={{ background: 'var(--bg-card)', borderBottom: '1px solid var(--border)', padding: '0.75rem 0' }}>
      <div className="page-wrapper">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', overflowX: 'auto', scrollbarWidth: 'none' }}>
          {/* Label */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', flexShrink: 0, color: 'var(--accent)' }}>
            <Flame size={14} />
            <span style={{ fontSize: '0.7rem', fontWeight: 600, letterSpacing: '0.08em', textTransform: 'uppercase' }}>Trending</span>
          </div>

          {/* Topic pills */}
          {topics.map((topic, i) => (
            <button
              key={i}
              onClick={() => onTopicClick?.(topic.topic)}
              style={{
                fontSize: '0.8rem',
                color: 'var(--text-secondary)',
                background: 'var(--bg)',
                border: '1px solid var(--border)',
                padding: '0.25rem 0.75rem',
                borderRadius: '9999px',
                whiteSpace: 'nowrap',
                flexShrink: 0,
                cursor: 'pointer',
                transition: 'all 0.2s',
                fontFamily: 'var(--font-dm)',
                display: 'flex',
                alignItems: 'center',
                gap: '0.3rem',
              }}
              onMouseEnter={e => {
                (e.currentTarget as HTMLButtonElement).style.borderColor = 'var(--accent)'
                ;(e.currentTarget as HTMLButtonElement).style.color = 'var(--accent)'
              }}
              onMouseLeave={e => {
                (e.currentTarget as HTMLButtonElement).style.borderColor = 'var(--border)'
                ;(e.currentTarget as HTMLButtonElement).style.color = 'var(--text-secondary)'
              }}
            >
              <TrendingUp size={11} />
              {topic.topic}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
