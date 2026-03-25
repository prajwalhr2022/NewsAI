'use client'
import { useState } from 'react'
import ArticleCard from './ArticleCard'
import type { Article } from '@/lib/supabase'

interface NewsGridProps {
  articles: Article[]
  loading: boolean
  activeCategory: string
  language: string
  isSearching?: boolean
  onLoadMore?: () => void
  hasMore?: boolean
  loadingMore?: boolean
}

function SkeletonCard({ hero }: { hero?: boolean }) {
  return (
    <div className={`article-card ${hero ? 'hero' : ''}`} style={{ pointerEvents: 'none' }}>
      {hero ? (
        <>
          <div className="skeleton" style={{ width: '42%', minHeight: '220px' }} />
          <div className="card-body" style={{ gap: '0.75rem' }}>
            <div className="skeleton" style={{ height: '18px', width: '40%' }} />
            <div className="skeleton" style={{ height: '26px', width: '90%' }} />
            <div className="skeleton" style={{ height: '15px', width: '100%' }} />
            <div className="skeleton" style={{ height: '15px', width: '75%' }} />
            <div className="skeleton" style={{ height: '15px', width: '55%' }} />
          </div>
        </>
      ) : (
        <>
          <div className="skeleton" style={{ height: '160px', width: '100%' }} />
          <div className="card-body" style={{ gap: '0.625rem' }}>
            <div className="skeleton" style={{ height: '15px', width: '35%' }} />
            <div className="skeleton" style={{ height: '19px', width: '95%' }} />
            <div className="skeleton" style={{ height: '13px', width: '100%' }} />
            <div className="skeleton" style={{ height: '13px', width: '80%' }} />
            <div className="skeleton" style={{ height: '13px', width: '60%' }} />
          </div>
        </>
      )}
    </div>
  )
}

export default function NewsGrid({
  articles, loading, activeCategory, language,
  isSearching, onLoadMore, hasMore, loadingMore,
}: NewsGridProps) {
  const heading = activeCategory === 'all' ? 'Latest News' : activeCategory

  if (loading) {
    return (
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.25rem' }}>
          <div className="skeleton" style={{ height: '24px', width: '160px' }} />
          <div className="live-dot" />
        </div>
        <div style={{ marginBottom: '1.25rem' }}><SkeletonCard hero /></div>
        <div className="news-grid">
          {Array.from({ length: 9 }).map((_, i) => <SkeletonCard key={i} />)}
        </div>
      </div>
    )
  }

  if (!articles.length) {
    return (
      <div className="empty-state">
        <span style={{ fontSize: '3rem' }}>📭</span>
        <h3 style={{ fontFamily: 'var(--font-playfair)', fontSize: '1.25rem', color: 'var(--text-primary)' }}>
          {isSearching ? 'No articles found for this search' : 'No articles yet'}
        </h3>
        <p style={{ fontSize: '0.875rem' }}>
          {isSearching
            ? 'Try different keywords or browse categories above.'
            : 'The crawler runs every 20 minutes — check back soon.'}
        </p>
      </div>
    )
  }

  const [heroArticle, ...restArticles] = articles

  return (
    <div>
      {/* Section heading */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '1.25rem', flexWrap: 'wrap' }}>
        <h2 style={{
          fontFamily: 'var(--font-playfair)', fontSize: '1.25rem',
          fontWeight: 700, color: 'var(--text-primary)', margin: 0,
        }}>
          {isSearching ? `Search results` : heading}
        </h2>
        <div className="live-dot" />
        <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', fontWeight: 500 }}>
          {isSearching ? '' : 'LIVE'}
        </span>
        <span style={{ marginLeft: 'auto', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          {articles.length} articles{hasMore ? '+' : ''}
        </span>
      </div>

      {/* Hero */}
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

      {/* Load more button */}
      {hasMore && onLoadMore && (
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '2rem' }}>
          <button
            onClick={onLoadMore}
            disabled={loadingMore}
            style={{
              padding: '0.75rem 2rem',
              borderRadius: '9999px',
              border: '1.5px solid var(--accent)',
              background: 'transparent',
              color: 'var(--accent)',
              fontSize: '0.875rem',
              fontWeight: 600,
              cursor: loadingMore ? 'not-allowed' : 'pointer',
              fontFamily: 'var(--font-dm)',
              transition: 'all 0.2s',
              opacity: loadingMore ? 0.6 : 1,
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
            }}
          >
            {loadingMore ? (
              <>
                <span style={{ display: 'inline-block', width: '14px', height: '14px', border: '2px solid var(--accent)', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />
                Loading older articles...
              </>
            ) : (
              '↓ Load more articles'
            )}
          </button>
        </div>
      )}

      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  )
}
