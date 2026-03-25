'use client'
import { useState, useRef } from 'react'
import Image from 'next/image'
import { ExternalLink, CheckCircle, AlertTriangle, Clock, ChevronDown, ChevronUp } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'
import type { Article } from '@/lib/supabase'

interface ArticleCardProps {
  article: Article
  hero?: boolean
  language?: string
}

function VerificationBadge({ status }: { status: Article['verification_status'] }) {
  if (status === 'confirmed') return (
    <span className="verification-badge verified"><CheckCircle size={10} /> Confirmed</span>
  )
  if (status === 'flagged') return (
    <span className="verification-badge flagged"><AlertTriangle size={10} /> Flagged</span>
  )
  return (
    <span className="verification-badge unverified"><Clock size={10} /> Unverified</span>
  )
}

function timeAgo(dateStr: string | null): string {
  if (!dateStr) return ''
  try {
    const d = new Date(dateStr)
    if (isNaN(d.getTime())) return ''
    return formatDistanceToNow(d, { addSuffix: true })
  } catch { return '' }
}

function isLongSummary(text: string): boolean {
  return text.length > 180
}

export default function ArticleCard({ article, hero = false, language = 'en' }: ArticleCardProps) {
  const [expanded,     setExpanded]     = useState(false)
  const [imgError,     setImgError]     = useState(false)
  const clickTimer = useRef<ReturnType<typeof setTimeout> | null>(null)

  const translation = language !== 'en' ? article.translations?.[language] : null
  const title   = translation?.title   ?? article.title
  const summary = translation?.summary ?? article.summary ?? ''

  const dateStr = article.published_at ?? article.fetched_at
  const hasImage = article.image_url && !imgError
  const longSummary = isLongSummary(summary)

  // Single click = expand summary / go to source if hero
  // Double click on title = go to source
  const handleCardClick = (e: React.MouseEvent) => {
    // If clicking the external link icon, always go to source
    if ((e.target as HTMLElement).closest('.go-to-source')) {
      window.open(article.source_url, '_blank', 'noopener,noreferrer')
      return
    }

    if (hero) {
      // Hero: single click goes to source
      window.open(article.source_url, '_blank', 'noopener,noreferrer')
      return
    }

    // Regular card: single click expands summary
    if (longSummary && !expanded) {
      setExpanded(true)
      return
    }
    if (expanded) {
      setExpanded(false)
      return
    }
    // Short summary: go to source
    window.open(article.source_url, '_blank', 'noopener,noreferrer')
  }

  const handleTitleDoubleClick = (e: React.MouseEvent) => {
    e.stopPropagation()
    window.open(article.source_url, '_blank', 'noopener,noreferrer')
  }

  const handleExternalClick = (e: React.MouseEvent) => {
    e.stopPropagation()
    window.open(article.source_url, '_blank', 'noopener,noreferrer')
  }

  return (
    <article
      className={`article-card ${hero ? 'hero' : ''}`}
      onClick={handleCardClick}
      role="article"
      tabIndex={0}
      onKeyDown={e => e.key === 'Enter' && handleCardClick(e as any)}
      style={{ cursor: 'pointer', animationFillMode: 'forwards' }}
    >
      {/* Image */}
      {hasImage && (
        <div style={{
          position: 'relative', flexShrink: 0,
          ...(hero
            ? { width: '42%', minHeight: '220px' }
            : { width: '100%', height: '160px' }),
        }}>
          <Image
            src={article.image_url!}
            alt={title}
            fill
            style={{ objectFit: 'cover' }}
            unoptimized
            onError={() => setImgError(true)}
          />
        </div>
      )}

      {/* Body */}
      <div className="card-body">
        {/* Badges */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', flexWrap: 'wrap' }}>
          {article.category && (
            <span className="card-badge">
              {article.category}
              {article.subcategory && (
                <span style={{ opacity: 0.7 }}> · {article.subcategory}</span>
              )}
            </span>
          )}
          <VerificationBadge status={article.verification_status} />
          {article.source_count > 1 && (
            <span className="source-count-badge">📡 {article.source_count} sources</span>
          )}
        </div>

        {/* Title — double click goes to source */}
        <h2
          className="card-title"
          style={{ fontSize: hero ? '1.375rem' : '1rem' }}
          onDoubleClick={handleTitleDoubleClick}
          title="Double-click to open article"
        >
          {title}
        </h2>

        {/* Summary */}
        {summary && (
          <div style={{ position: 'relative' }}>
            <p
              className="card-summary"
              style={{
                WebkitLineClamp: expanded ? 'unset' : (hero ? 'unset' : 3),
                display: '-webkit-box',
                WebkitBoxOrient: 'vertical',
                overflow: expanded || hero ? 'visible' : 'hidden',
                fontSize: '0.875rem',
                color: 'var(--text-secondary)',
                lineHeight: 1.55,
              }}
            >
              {summary}
            </p>
            {/* Expand/collapse button for long summaries */}
            {!hero && longSummary && (
              <button
                onClick={e => { e.stopPropagation(); setExpanded(!expanded) }}
                style={{
                  display: 'flex', alignItems: 'center', gap: '0.2rem',
                  fontSize: '0.72rem', color: 'var(--accent)',
                  background: 'none', border: 'none', cursor: 'pointer',
                  padding: '0.25rem 0', marginTop: '0.2rem',
                  fontFamily: 'var(--font-dm)', fontWeight: 500,
                }}
              >
                {expanded
                  ? <><ChevronUp size={12} /> Show less</>
                  : <><ChevronDown size={12} /> Read more</>
                }
              </button>
            )}
          </div>
        )}

        {/* Tags (hero only) */}
        {hero && article.tags?.length > 0 && (
          <div className="card-tags">
            {article.tags.slice(0, 5).map(tag => (
              <span key={tag} className="card-tag">#{tag}</span>
            ))}
          </div>
        )}

        {/* Meta */}
        <div className="card-meta">
          <span className="card-source">{article.source_name}</span>
          <span>{timeAgo(dateStr)}</span>
          <button
            className="go-to-source"
            onClick={handleExternalClick}
            title="Open article"
            style={{
              marginLeft: 'auto', background: 'none', border: 'none',
              cursor: 'pointer', color: 'var(--text-muted)', display: 'flex',
              padding: '2px',
            }}
          >
            <ExternalLink size={13} />
          </button>
        </div>

        {/* Hint text for interaction */}
        {!hero && !expanded && longSummary && (
          <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginTop: '0.1rem', fontStyle: 'italic' }}>
            Click to read summary · Double-click title to open article
          </div>
        )}
      </div>
    </article>
  )
}
