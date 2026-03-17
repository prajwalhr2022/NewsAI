'use client'
import { Flame } from 'lucide-react'
import type { TrendingTopic } from '@/lib/supabase'

interface TrendingBarProps {
  topics: TrendingTopic[]
}

export default function TrendingBar({ topics }: TrendingBarProps) {
  if (!topics.length) return null

  // Duplicate topics for seamless infinite loop
  const doubled = [...topics, ...topics]

  return (
    <div className="trending-bar" style={{ display: 'flex', alignItems: 'center', height: '36px', overflow: 'hidden' }}>
      {/* Label */}
      <div className="trending-bar-label" style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', height: '100%' }}>
        <Flame size={12} />
        <span>Trending</span>
      </div>

      {/* Ticker */}
      <div style={{ flex: 1, overflow: 'hidden', position: 'relative' }}>
        <div className="ticker-track">
          {doubled.map((topic, i) => (
            <span key={i} className="ticker-item">
              {topic.topic}
              {topic.article_count > 1 && (
                <span style={{ opacity: 0.5, fontSize: '0.7rem', marginLeft: '0.2rem' }}>
                  ({topic.article_count})
                </span>
              )}
              <span style={{ margin: '0 1.5rem', opacity: 0.25 }}>•</span>
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}
