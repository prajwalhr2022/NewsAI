'use client'
import { useState, useEffect, useCallback, useRef } from 'react'
import {
  supabase,
  getArticles,
  getCategories,
  getTrendingTopics,
  type Article,
  type Category,
  type TrendingTopic,
} from '@/lib/supabase'

import Header       from '@/components/Header'
import TrendingBar  from '@/components/TrendingBar'
import RegionToggle from '@/components/RegionToggle'
import Sidebar      from '@/components/Sidebar'
import NewsGrid     from '@/components/NewsGrid'

export default function HomePage() {
  // ── State ───────────────────────────────────────────────────
  const [articles,    setArticles]    = useState<Article[]>([])
  const [categories,  setCategories]  = useState<Category[]>([])
  const [topics,      setTopics]      = useState<TrendingTopic[]>([])
  const [loading,     setLoading]     = useState(true)

  const [search,      setSearch]      = useState('')
  const [language,    setLanguage]    = useState('en')
  const [isIndia,     setIsIndia]     = useState(false)
  const [activeCategory,    setActiveCategory]    = useState('all')
  const [activeSubcategory, setActiveSubcategory] = useState('')

  const [newCount,    setNewCount]    = useState(0)
  const [showBadge,   setShowBadge]   = useState(false)
  const badgeTimer = useRef<ReturnType<typeof setTimeout> | null>(null)

  // ── Load data ───────────────────────────────────────────────
  const loadArticles = useCallback(async () => {
    setLoading(true)
    const data = await getArticles({
      category:    activeCategory === 'all' ? undefined : activeCategory,
      subcategory: activeSubcategory || undefined,
      isIndia,
      search:      search || undefined,
      limit:       60,
    })
    setArticles(data)
    setLoading(false)
  }, [activeCategory, activeSubcategory, isIndia, search])

  const loadMeta = useCallback(async () => {
    const [cats, tops] = await Promise.all([getCategories(), getTrendingTopics()])
    setCategories(cats)
    setTopics(tops)
  }, [])

  useEffect(() => { loadMeta() }, [loadMeta])
  useEffect(() => { loadArticles() }, [loadArticles])

  // ── Supabase Realtime ───────────────────────────────────────
  useEffect(() => {
    const channel = supabase
      .channel('realtime-articles')
      .on(
        'postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'articles' },
        (payload) => {
          const newArticle = payload.new as Article

          // Only show badge if matches current filters
          const matchesIndia    = newArticle.is_india_focused === isIndia
          const matchesCategory = activeCategory === 'all' || newArticle.category === activeCategory

          if (matchesIndia && matchesCategory) {
            setNewCount(c => c + 1)
            setShowBadge(true)

            // Auto-hide badge after 5s
            if (badgeTimer.current) clearTimeout(badgeTimer.current)
            badgeTimer.current = setTimeout(() => {
              setShowBadge(false)
              setNewCount(0)
            }, 5000)
          }
        }
      )
      .subscribe()

    return () => { supabase.removeChannel(channel) }
  }, [isIndia, activeCategory])

  // ── Handlers ────────────────────────────────────────────────
  const handleCategoryChange = (cat: string, sub?: string) => {
    setActiveCategory(cat)
    setActiveSubcategory(sub ?? '')
  }

  const handleBadgeClick = () => {
    setShowBadge(false)
    setNewCount(0)
    loadArticles()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const handleRegionChange = (india: boolean) => {
    setIsIndia(india)
    setActiveCategory('all')
    setActiveSubcategory('')
  }

  // ── Search debounce ─────────────────────────────────────────
  useEffect(() => {
    const id = setTimeout(() => { loadArticles() }, 350)
    return () => clearTimeout(id)
  }, [search]) // eslint-disable-line react-hooks/exhaustive-deps
  // (loadArticles is stable enough; we only want to debounce on search changes)

  // ── Render ──────────────────────────────────────────────────
  return (
    <>
      <Header
        search={search}
        onSearchChange={setSearch}
        language={language}
        onLanguageChange={setLanguage}
      />

      <TrendingBar topics={topics} />

      {/* New articles badge */}
      {showBadge && newCount > 0 && (
        <div className="new-articles-badge" onClick={handleBadgeClick}>
          ↑ {newCount} new article{newCount > 1 ? 's' : ''} — click to refresh
        </div>
      )}

      <main className="page-wrapper" style={{ paddingTop: '1.5rem', paddingBottom: '3rem' }}>
        {/* Region toggle */}
        <div style={{ marginBottom: '1.25rem' }}>
          <RegionToggle isIndia={isIndia} onChange={handleRegionChange} />
        </div>

        {/* Main layout */}
        <div style={{ display: 'flex', gap: '1.75rem', alignItems: 'flex-start' }}>
          <Sidebar
            categories={categories}
            activeCategory={activeCategory}
            activeSubcategory={activeSubcategory}
            onCategoryChange={handleCategoryChange}
          />
          <NewsGrid
            articles={articles}
            loading={loading}
            activeCategory={activeCategory}
            language={language}
          />
        </div>
      </main>
    </>
  )
}
