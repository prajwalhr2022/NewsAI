'use client'
import ArticleCard from './ArticleCard'
import type { Article } from '@/lib/supabase'

interface NewsGridProps {
  articles: Article[]
  loading: boolean
  activeCategory: string
  language: string
}

function SkeletonCard({ hero }: { hero?: boolean }) {
  return (
    <div className={`article-card ${hero ? 'hero' : ''}`} style={{ pointerEvents: 'none' }}>
      {hero ? (
        <>
          <div className="skeleton" style={{ width: '45%', minHeight: '220px' }} />
          <div className="card-body" style={{ gap: '0.75rem' }}>
            <div className="skeleton" style={{ height: '20px', width: '40%' }} />
            <div className="skeleton" style={{ height: '28px', width: '90%' }} />
            <div className="skeleton" style={{ height: '16px', width: '100%' }} />
            <div className="skeleton" style={{ height: '16px', width: '80%' }} />
            <div className="skeleton" style={{ height: '16px', width: '60%', marginTop: 'auto' }} />
          </div>
        </>
      ) : (
        <>
          <div className="skeleton" style={{ height: '160px', width: '100%' }} />
          <div className="card-body" style={{ gap: '0.625rem' }}>
            <div className="skeleton" style={{ height: '16px', width: '35%' }} />
            <div className="skeleton" style={{ height: '20px', width: '95%' }} />
            <div className="skeleton" style={{ height: '14px', width: '100%' }} />
            <div className="skeleton" style={{ height: '14px', width: '70%' }} />
            <div className="skeleton" style={{ height: '12px', width: '45%', marginTop: 'auto' }} />
          </div>
        </>
      )}
    </div>
  )
}

export default function NewsGrid({ articles, loading, activeCategory, language }: NewsGridProps) {
  const heading = activeCategory === 'all' ? 'Latest News' : activeCategory

  if (loading) {
    return (
      <div style={{ flex: 1, minWidth: 0 }}>
        {/* Section heading skeleton */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.25rem' }}>
          <div className="skeleton" style={{ height: '24px', width: '180px' }} />
          <div className="live-dot" />
        </div>
        {/* Hero skeleton */}
        <div style={{ marginBottom: '1.25rem' }}>
          <SkeletonCard hero />
        </div>
        {/* Grid skeleton */}
        <div className="news-grid">
          {Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)}
        </div>
      </div>
    )
  }

  if (!articles.length) {
    return (
      <div style={{ flex: 1, minWidth: 0 }}>
        <div className="empty-state">
          <span style={{ fontSize: '3rem' }}>📭</span>
          <h3 style={{ fontFamily: 'var(--font-playfair)', fontSize: '1.25rem', color: 'var(--text-primary)' }}>
            No articles found
          </h3>
          <p style={{ fontSize: '0.875rem' }}>
            Try a different category or check back soon — the crawler runs every 5 minutes.
          </p>
        </div>
      </div>
    )
  }

  const [heroArticle, ...restArticles] = articles

  return (
    <div style={{ flex: 1, minWidth: 0 }}>
      {/* Section heading */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '1.25rem' }}>
        <h1 style={{
          fontFamily: 'var(--font-playfair)',
          fontSize: '1.375rem',
          fontWeight: 700,
          color: 'var(--text-primary)',
          margin: 0,
        }}>
          {heading}
        </h1>
        <div className="live-dot" title="Live updates" />
        <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', fontWeight: 500 }}>LIVE</span>
        <span style={{ marginLeft: 'auto', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          {articles.length} articles
        </span>
      </div>

      {/* Hero card */}
      <div style={{ marginBottom: '1.25rem' }}>
        <ArticleCard article={heroArticle} hero language={language} />
      </div>

      {/* Grid */}
      {restArticles.length > 0 && (
        <div className="news-grid">
          {restArticles.map(article => (
            <ArticleCard key={article.id} article={article} language={language} />
          ))}
        </div>
      )}
    </div>
  )
}
