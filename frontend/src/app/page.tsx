'use client'
import { useState, useEffect, useCallback, useRef } from 'react'
import {
  supabase, getArticles, getCategories, getTrendingTopics,
  type Article, type Category, type TrendingTopic,
} from '@/lib/supabase'

import Header      from '@/components/Header'
import TrendingBar from '@/components/TrendingBar'
import CategoryBar from '@/components/CategoryBar'
import RegionToggle from '@/components/RegionToggle'
import NewsGrid    from '@/components/NewsGrid'

export default function HomePage() {
  const [articles,   setArticles]   = useState<Article[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [topics,     setTopics]     = useState<TrendingTopic[]>([])
  const [loading,    setLoading]    = useState(true)

  const [search,           setSearch]           = useState('')
  const [language,         setLanguage]         = useState('en')
  const [isIndia,          setIsIndia]          = useState(false)
  const [activeCategory,   setActiveCategory]   = useState('all')

  const [newCount,  setNewCount]  = useState(0)
  const [showBadge, setShowBadge] = useState(false)
  const badgeTimer = useRef<ReturnType<typeof setTimeout> | null>(null)

  // ── Translation cache ─────────────────────────────────────
  // articleId → { hi: {title, summary}, kn: {title, summary} }
  const [translationCache, setTranslationCache] = useState<
    Record<string, Record<string, { title: string; summary: string }>>
  >({})
  const [translating, setTranslating] = useState(false)

  // ── Load articles ─────────────────────────────────────────
  const loadArticles = useCallback(async () => {
    setLoading(true)
    const data = await getArticles({
      category:    activeCategory === 'all' ? undefined : activeCategory,
      isIndia,
      search:      search || undefined,
      limit:       60,
    })
    setArticles(data)
    setLoading(false)
  }, [activeCategory, isIndia, search])

  const loadMeta = useCallback(async () => {
    const [cats, tops] = await Promise.all([getCategories(), getTrendingTopics()])
    setCategories(cats)
    setTopics(tops)
  }, [])

  useEffect(() => { loadMeta() }, [loadMeta])
  useEffect(() => { loadArticles() }, [loadArticles])

  // ── Search debounce ───────────────────────────────────────
  const searchRef = useRef(search)
  searchRef.current = search
  useEffect(() => {
    const id = setTimeout(loadArticles, 350)
    return () => clearTimeout(id)
  }, [search]) // eslint-disable-line

  // ── Translation ───────────────────────────────────────────
  useEffect(() => {
    if (language === 'en' || articles.length === 0) return

    const untranslated = articles.filter(a => {
      // Already in Supabase cache
      if (a.translations?.[language]) return false
      // Already in local cache
      if (translationCache[a.id]?.[language]) return false
      return true
    })

    if (untranslated.length === 0) return

    // Translate up to 10 articles at a time to avoid rate limits
    const batch = untranslated.slice(0, 10)
    setTranslating(true)

    Promise.all(
      batch.map(async (article) => {
        try {
          const res = await fetch('/api/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              articleId:           article.id,
              title:               article.title,
              summary:             article.summary ?? '',
              targetLang:          language,
              currentTranslations: article.translations ?? {},
            }),
          })
          if (!res.ok) return null
          const data = await res.json()
          return { id: article.id, translation: data.translation }
        } catch {
          return null
        }
      })
    ).then(results => {
      const newCache: Record<string, Record<string, { title: string; summary: string }>> = { ...translationCache }
      results.forEach(r => {
        if (r?.translation) {
          newCache[r.id] = { ...(newCache[r.id] ?? {}), [language]: r.translation }
        }
      })
      setTranslationCache(newCache)
      setTranslating(false)
    })
  }, [language, articles]) // eslint-disable-line

  // ── Merge translations into articles ──────────────────────
  const displayArticles = articles.map(article => {
    if (language === 'en') return article
    // Check Supabase cache first, then local cache
    const trans = article.translations?.[language] ?? translationCache[article.id]?.[language]
    if (!trans) return article
    return { ...article, title: trans.title, summary: trans.summary }
  })

  // ── Supabase Realtime ─────────────────────────────────────
  useEffect(() => {
    const channel = supabase
      .channel('realtime-articles')
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'articles' }, payload => {
        const a = payload.new as Article
        const matchesIndia = a.is_india_focused === isIndia
        const matchesCat   = activeCategory === 'all' || a.category === activeCategory
        if (matchesIndia && matchesCat) {
          setNewCount(c => c + 1)
          setShowBadge(true)
          if (badgeTimer.current) clearTimeout(badgeTimer.current)
          badgeTimer.current = setTimeout(() => { setShowBadge(false); setNewCount(0) }, 5000)
        }
      })
      .subscribe()
    return () => { supabase.removeChannel(channel) }
  }, [isIndia, activeCategory])

  // ── Handlers ──────────────────────────────────────────────
  const handleTopicClick = (topic: string) => {
    setSearch(topic)
    setActiveCategory('all')
  }

  const handleRegionChange = (india: boolean) => {
    setIsIndia(india)
    setActiveCategory('all')
    setSearch('')
  }

  const handleBadgeClick = () => {
    setShowBadge(false)
    setNewCount(0)
    loadArticles()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  // ── Render ────────────────────────────────────────────────
  return (
    <>
      <Header
        search={search}
        onSearchChange={setSearch}
        language={language}
        onLanguageChange={lang => { setLanguage(lang); setTranslationCache({}) }}
      />

      {/* Trending bar */}
      <TrendingBar topics={topics} onTopicClick={handleTopicClick} />

      {/* Category bar */}
      <CategoryBar
        categories={categories}
        activeCategory={activeCategory}
        onCategoryChange={setActiveCategory}
      />

      {/* New articles badge */}
      {showBadge && newCount > 0 && (
        <div className="new-articles-badge" onClick={handleBadgeClick}>
          ↑ {newCount} new article{newCount > 1 ? 's' : ''} — click to refresh
        </div>
      )}

      {/* Translation indicator */}
      {translating && language !== 'en' && (
        <div style={{
          textAlign: 'center', padding: '0.5rem',
          fontSize: '0.75rem', color: 'var(--text-muted)',
          background: 'var(--accent-soft)',
        }}>
          Translating articles to {language === 'hi' ? 'Hindi' : 'Kannada'}...
        </div>
      )}

      <main className="page-wrapper" style={{ paddingTop: '1.25rem', paddingBottom: '3rem' }}>
        {/* Region + article count row */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '0.75rem' }}>
          <RegionToggle isIndia={isIndia} onChange={handleRegionChange} />
          {!loading && (
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              {displayArticles.length} articles · updates every 30 min
            </span>
          )}
        </div>

        {/* Full width news grid */}
        <NewsGrid
          articles={displayArticles}
          loading={loading}
          activeCategory={activeCategory}
          language={language}
        />
      </main>
    </>
  )
}
