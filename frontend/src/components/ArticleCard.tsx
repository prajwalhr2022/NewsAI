'use client'
import Image from 'next/image'
import { ExternalLink, CheckCircle, AlertTriangle, Clock } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'
import type { Article } from '@/lib/supabase'

interface ArticleCardProps {
  article: Article
  hero?: boolean
  language?: string
}

function VerificationBadge({ status }: { status: Article['verification_status'] }) {
  if (status === 'confirmed') return (
    <span className="verification-badge verified">
      <CheckCircle size={10} /> Verified
    </span>
  )
  if (status === 'flagged') return (
    <span className="verification-badge flagged">
      <AlertTriangle size={10} /> Flagged
    </span>
  )
  return (
    <span className="verification-badge unverified">
      <Clock size={10} /> Unverified
    </span>
  )
}

function timeAgo(dateStr: string | null): string {
  if (!dateStr) return ''
  try {
    return formatDistanceToNow(new Date(dateStr), { addSuffix: true })
  } catch {
    return ''
  }
}

export default function ArticleCard({ article, hero = false, language = 'en' }: ArticleCardProps) {
  // Use translation if available and non-English
  const translation = language !== 'en' ? article.translations?.[language] : null
  const title   = translation?.title   ?? article.title
  const summary = translation?.summary ?? article.summary ?? ''

  const dateStr = article.published_at ?? article.fetched_at

  const handleClick = () => {
    window.open(article.source_url, '_blank', 'noopener,noreferrer')
  }

  return (
    <article
      className={`article-card ${hero ? 'hero' : ''} animate-fade-in`}
      onClick={handleClick}
      role="article"
      tabIndex={0}
      onKeyDown={e => e.key === 'Enter' && handleClick()}
    >
      {/* Image */}
      {article.image_url && (
        <div style={{ position: 'relative', flexShrink: 0, ...(hero ? { width: '45%' } : { width: '100%', height: '160px' }) }}>
          <Image
            src={article.image_url}
            alt={title}
            fill
            style={{ objectFit: 'cover' }}
            unoptimized
            onError={e => { (e.target as HTMLImageElement).style.display = 'none' }}
          />
        </div>
      )}

      {/* Body */}
      <div className="card-body">
        {/* Badges row */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', flexWrap: 'wrap' }}>
          {article.category && (
            <span className="card-badge">
              {article.category}
              {article.subcategory && <span style={{ opacity: 0.7 }}>· {article.subcategory}</span>}
            </span>
          )}
          <VerificationBadge status={article.verification_status} />
          {article.source_count > 1 && (
            <span className="source-count-badge">{article.source_count} sources</span>
          )}
        </div>

        {/* Title */}
        <h2
          className="card-title"
          style={{ fontSize: hero ? '1.375rem' : '1rem' }}
        >
          {title}
        </h2>

        {/* Summary */}
        {summary && (
          <p className="card-summary">{summary}</p>
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
          <ExternalLink size={12} style={{ marginLeft: 'auto', color: 'var(--text-muted)', flexShrink: 0 }} />
        </div>
      </div>
    </article>
  )
}
