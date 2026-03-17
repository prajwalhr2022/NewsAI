'use client'
import { useState } from 'react'
import { ChevronDown, ChevronRight } from 'lucide-react'
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

interface SidebarProps {
  categories: Category[]
  activeCategory: string
  activeSubcategory: string
  onCategoryChange: (cat: string, sub?: string) => void
}

export default function Sidebar({ categories, activeCategory, activeSubcategory, onCategoryChange }: SidebarProps) {
  const [expanded, setExpanded] = useState<Set<string>>(new Set())

  const topLevel = categories.filter(c => !c.parent_slug)
  const getSubcats = (slug: string) => categories.filter(c => c.parent_slug === slug && c.article_count >= 2)

  const toggleExpand = (slug: string, e: React.MouseEvent) => {
    e.stopPropagation()
    setExpanded(prev => {
      const next = new Set(prev)
      next.has(slug) ? next.delete(slug) : next.add(slug)
      return next
    })
  }

  return (
    <aside className="sidebar">
      <div className="sidebar-heading">Categories</div>

      {/* All News */}
      <button
        className={`cat-btn ${activeCategory === 'all' ? 'active' : ''}`}
        onClick={() => onCategoryChange('all')}
      >
        <span>📰</span>
        <span>All News</span>
        <span className="cat-count" style={{ marginLeft: 'auto' }}></span>
      </button>

      {/* Dynamic categories */}
      {topLevel.map(cat => {
        const subcats = getSubcats(cat.slug)
        const isExpanded = expanded.has(cat.slug)
        const isActive = activeCategory === cat.name

        return (
          <div key={cat.slug}>
            <button
              className={`cat-btn ${isActive ? 'active' : ''}`}
              onClick={() => onCategoryChange(cat.name)}
            >
              <span>{CATEGORY_EMOJIS[cat.name] ?? '📄'}</span>
              <span style={{ flex: 1, textAlign: 'left' }}>{cat.name}</span>
              <span className="cat-count">{cat.article_count}</span>
              {subcats.length > 0 && (
                <span
                  onClick={e => toggleExpand(cat.slug, e)}
                  style={{ padding: '2px', color: 'var(--text-muted)', display: 'flex' }}
                >
                  {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                </span>
              )}
            </button>

            {/* Subcategories */}
            {isExpanded && subcats.map(sub => (
              <button
                key={sub.slug}
                className={`subcat-btn ${activeSubcategory === sub.name ? 'active' : ''}`}
                onClick={() => onCategoryChange(cat.name, sub.name)}
              >
                {sub.name}
                <span style={{ float: 'right', fontSize: '0.68rem', color: 'var(--text-muted)' }}>
                  {sub.article_count}
                </span>
              </button>
            ))}
          </div>
        )
      })}
    </aside>
  )
}
