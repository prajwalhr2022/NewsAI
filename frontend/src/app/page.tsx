'use client'
import { useState, useEffect, useCallback, useRef } from 'react'
import {
  supabase, getArticles, getTopArticles, getCategories,
  getTrendingTopics, getPredictions,
  type Article, type Category, type TrendingTopic, type Predictions,
} from '@/lib/supabase'

import Header             from '@/components/Header'
import CategoryBar        from '@/components/CategoryBar'
import RegionToggle       from '@/components/RegionToggle'
import NewsGrid           from '@/components/NewsGrid'
import PredictionsSection from '@/components/PredictionsSection'

const PAGE_SIZE = 100

export default function HomePage() {
  const [articles,    setArticles]    = useState<Article[]>([])
  const [topArticles, setTopArticles] = useState<Article[]>([])
  const [categories,  setCategories]  = useState<Category[]>([])
  const [topics,      setTopics]      = useState<TrendingTopic[]>([])
  const [predictions, setPredictions] = useState<Predictions | null>(null)
  const [loading,     setLoading]     = useState(true)
  const [loadingMore, setLoadingMore] = useState(false)
  const [hasMore,     setHasMore]     = useState(false)
  const [offset,      setOffset]      = useState(0)

  const [search,         setSearch]         = useState('')
  const [language,       setLanguage]       = useState('en')
  const [isIndia,        setIsIndia]        = useState(false)
  const [activeCategory, setActiveCategory] = useState('all')

  const [newCount,  setNewCount]  = useState(0)
  const [showBadge, setShowBadge] = useState(false)
  const badgeTimer = useRef<ReturnType<typeof setTimeout> | null>(null)

  const [translationCache, setTranslationCache] = useState<
    Record<string, Record<string, { title: string; summary: string }>>
  >({})
  const [translating, setTranslating] = useState(false)

  const isSearching = search.trim().length > 0

  // ── Load first page ───────────────────────────────────────
  const loadArticles = useCallback(async () => {
    setLoading(true)
    setOffset(0)

    const filters = {
      category: activeCategory === 'all' ? undefined : activeCategory,
      isIndia,
      search:   search || undefined,
      limit:    PAGE_SIZE,
      offset:   0,
    }

    const [data, top] = await Promise.all([
      getArticles(filters),
      getTopArticles({ category: filters.category, isIndia, limit: 6 }),
    ])

    setArticles(data)
    setTopArticles(top)
    setHasMore(data.length === PAGE_SIZE)
    setLoading(false)
  }, [activeCategory, isIndia, search])

  // ── Load more (pagination) ────────────────────────────────
  const handleLoadMore = async () => {
    setLoadingMore(true)
    const nextOffset = offset + PAGE_SIZE
    const more = await getArticles({
      category: activeCategory === 'all' ? undefined : activeCategory,
      isIndia,
      search:   search || undefined,
      limit:    PAGE_SIZE,
      offset:   nextOffset,
    })
    setArticles(prev => [...prev, ...more])
    setOffset(nextOffset)
    setHasMore(more.length === PAGE_SIZE)
    setLoadingMore(false)
  }

  // ── Load metadata ─────────────────────────────────────────
  const loadMeta = useCallback(async () => {
    const [cats, tops, preds] = await Promise.all([
      getCategories(), getTrendingTopics(), getPredictions(),
    ])
    setCategories(cats)
    setTopics(tops)
    setPredictions(preds)
  }, [])

  useEffect(() => { loadMeta() }, [loadMeta])
  useEffect(() => { loadArticles() }, [loadArticles])

  // Debounce search
  useEffect(() => {
    const id = setTimeout(loadArticles, 400)
    return () => clearTimeout(id)
  }, [search]) // eslint-disable-line

  // ── Translation ───────────────────────────────────────────
  useEffect(() => {
    if (language === 'en' || articles.length === 0) return
    const untranslated = articles.filter(a =>
      !a.translations?.[language] && !translationCache[a.id]?.[language]
    ).slice(0, 10)
    if (!untranslated.length) return

    setTranslating(true)
    Promise.all(untranslated.map(async article => {
      try {
        const res = await fetch('/api/translate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            articleId: article.id, title: article.title,
            summary: article.summary ?? '', targetLang: language,
            currentTranslations: article.translations ?? {},
          }),
        })
        if (!res.ok) return null
        const data = await res.json()
        return { id: article.id, translation: data.translation }
      } catch { return null }
    })).then(results => {
      const newCache = { ...translationCache }
      results.forEach(r => {
        if (r?.translation) newCache[r.id] = { ...(newCache[r.id] ?? {}), [language]: r.translation }
      })
      setTranslationCache(newCache)
      setTranslating(false)
    })
  }, [language, articles]) // eslint-disable-line

  // Merge translations
  const applyTranslations = (list: Article[]) => list.map(article => {
    if (language === 'en') return article
    const trans = article.translations?.[language] ?? translationCache[article.id]?.[language]
    if (!trans) return article
    return { ...article, title: trans.title, summary: trans.summary }
  })

  // ── Realtime ──────────────────────────────────────────────
  useEffect(() => {
    const channel = supabase
      .channel('realtime-articles')
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'articles' }, payload => {
        const a = payload.new as Article
        if (a.is_india_focused === isIndia && (activeCategory === 'all' || a.category === activeCategory)) {
          setNewCount(c => c + 1)
          setShowBadge(true)
          if (badgeTimer.current) clearTimeout(badgeTimer.current)
          badgeTimer.current = setTimeout(() => { setShowBadge(false); setNewCount(0) }, 5000)
        }
      })
      .subscribe()
    return () => { supabase.removeChannel(channel) }
  }, [isIndia, activeCategory])

  const handleRegionChange = (india: boolean) => {
    setIsIndia(india)
    setActiveCategory('all')
    setSearch('')
  }

  const handleBadgeClick = () => {
    setShowBadge(false); setNewCount(0)
    loadArticles()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const displayArticles    = applyTranslations(articles)
  const displayTopArticles = applyTranslations(topArticles)

  // ── Render ────────────────────────────────────────────────
  return (
    <>
      <Header
        search={search}
        onSearchChange={setSearch}
        language={language}
        onLanguageChange={lang => { setLanguage(lang); setTranslationCache({}) }}
      />

      <CategoryBar
        categories={categories}
        activeCategory={activeCategory}
        onCategoryChange={cat => { setActiveCategory(cat); setSearch('') }}
        topics={topics}
        onTopicClick={t => { setSearch(t); setActiveCategory('all') }}
      />

      {showBadge && newCount > 0 && (
        <div className="new-articles-badge" onClick={handleBadgeClick}>
          ↑ {newCount} new article{newCount > 1 ? 's' : ''} — click to refresh
        </div>
      )}

      {translating && language !== 'en' && (
        <div style={{ textAlign: 'center', padding: '0.4rem', fontSize: '0.75rem', color: 'var(--accent)', background: 'var(--accent-soft)' }}>
          Translating to {language === 'hi' ? 'Hindi' : 'Kannada'}...
        </div>
      )}

      <main className="page-wrapper" style={{ paddingTop: '1.25rem', paddingBottom: '3rem' }}>

        {/* Region toggle */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '0.75rem' }}>
          <RegionToggle isIndia={isIndia} onChange={handleRegionChange} />
          {!loading && (
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              {displayArticles.length}{hasMore ? '+' : ''} articles · updates every 20 min
            </span>
          )}
        </div>

        {/* Top stories — hide when searching */}
        {!loading && !isSearching && displayTopArticles.length > 0 && (
          <section style={{ marginBottom: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '1rem' }}>
              <h2 style={{ fontFamily: 'var(--font-playfair)', fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', margin: 0 }}>
                🔥 Top Stories
              </h2>
              <span style={{ fontSize: '0.7rem', background: 'var(--accent-soft)', color: 'var(--accent)', padding: '2px 8px', borderRadius: '9999px', fontWeight: 500 }}>
                Multiple sources
              </span>
            </div>
            <div className="news-grid">
              {displayTopArticles.map(article => (
                <TopStoryCard key={article.id} article={article} />
              ))}
            </div>
          </section>
        )}

        {/* Predictions — hide when searching */}
        {!isSearching && <PredictionsSection predictions={predictions} />}

        {/* Main news feed */}
        <NewsGrid
          articles={displayArticles}
          loading={loading}
          activeCategory={activeCategory}
          language={language}
          isSearching={isSearching}
          onLoadMore={handleLoadMore}
          hasMore={hasMore}
          loadingMore={loadingMore}
        />

      </main>
    </>
  )
}

function TopStoryCard({ article }: { article: Article }) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div
      className="article-card"
      style={{ borderLeft: '3px solid var(--accent)', cursor: 'pointer' }}
      onClick={() => {
        if (article.summary && article.summary.length > 120 && !expanded) {
          setExpanded(true)
        } else {
          window.open(article.source_url, '_blank', 'noopener,noreferrer')
        }
      }}
    >
      <div className="card-body">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', flexWrap: 'wrap' }}>
          {article.category && <span className="card-badge">{article.category}</span>}
          <span className="source-count-badge">📡 {article.source_count} sources</span>
          {article.verification_status === 'confirmed' && (
            <span className="verification-badge verified">✓ Confirmed</span>
          )}
        </div>
        <h3 className="card-title" style={{ fontSize: '0.9rem' }}
          onDoubleClick={e => { e.stopPropagation(); window.open(article.source_url, '_blank') }}>
          {article.title}
        </h3>
        {article.summary && (
          <p className="card-summary" style={{
            fontSize: '0.8rem',
            WebkitLineClamp: expanded ? 'unset' : 2,
            display: '-webkit-box', WebkitBoxOrient: 'vertical',
            overflow: expanded ? 'visible' : 'hidden',
          }}>
            {article.summary}
          </p>
        )}
        <div className="card-meta">
          <span className="card-source">{article.source_name}</span>
          <button
            onClick={e => { e.stopPropagation(); window.open(article.source_url, '_blank') }}
            style={{ marginLeft: 'auto', background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)', display: 'flex', padding: '2px' }}
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
          </button>
        </div>
      </div>
    </div>
  )
}

