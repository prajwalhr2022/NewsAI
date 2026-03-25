'use client'
import { TrendingUp, TrendingDown, Minus, RefreshCw } from 'lucide-react'
import type { Predictions, PredictionItem } from '@/lib/supabase'
import { formatDistanceToNow } from 'date-fns'

interface PredictionsProps {
  predictions: Predictions | null
}

const ASSETS = [
  { key: 'gold',          label: 'Gold',           emoji: '🥇' },
  { key: 'silver',        label: 'Silver',         emoji: '🥈' },
  { key: 'oil',           label: 'Crude Oil',      emoji: '🛢️' },
  { key: 'global_stocks', label: 'Global Markets', emoji: '🌐' },
  { key: 'india_stocks',  label: 'India Markets',  emoji: '🇮🇳' },
]

function DirectionIcon({ direction }: { direction: PredictionItem['direction'] }) {
  if (direction === 'up')       return <TrendingUp size={16} className="prediction-up" />
  if (direction === 'down')     return <TrendingDown size={16} className="prediction-down" />
  return <Minus size={16} className="prediction-side" />
}

function ConfidencePill({ confidence }: { confidence: PredictionItem['confidence'] }) {
  const colors: Record<string, string> = {
    high:   'background: rgba(34,197,94,0.12); color: #16a34a',
    medium: 'background: rgba(251,191,36,0.12); color: #b45309',
    low:    'background: rgba(107,114,128,0.12); color: #6b7280',
  }
  return (
    <span style={{
      fontSize: '0.65rem', fontWeight: 600,
      padding: '1px 6px', borderRadius: '9999px',
      textTransform: 'uppercase', letterSpacing: '0.05em',
      // FIX 1: Removed extra parenthesis around Object.fromEntries
      ...Object.fromEntries(colors[confidence].split(';').map(s => {
        const [k, v] = s.split(':').map(x => x.trim())
        return [k === 'background' ? 'background' : 'color', v]
      })),
    }}>
      {confidence}
    </span>
  )
}

export default function PredictionsSection({ predictions }: PredictionsProps) {
  return (
    <section style={{ marginBottom: '2rem' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
        <h2 style={{
          fontFamily: 'var(--font-playfair)', fontSize: '1.25rem',
          fontWeight: 700, color: 'var(--text-primary)', margin: 0,
        }}>
          📊 Market Predictions
        </h2>
        {/* FIX 2: Removed duplicate color property */}
        <span style={{ fontSize: '0.7rem', background: 'var(--accent-soft)', color: 'var(--accent)', padding: '2px 8px', borderRadius: '9999px', fontWeight: 500 }}>
          1-Week Outlook
        </span>
        {predictions?.generated_at && (
          <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
            <RefreshCw size={10} />
            Updated {formatDistanceToNow(new Date(predictions.generated_at), { addSuffix: true })}
          </span>
        )}
      </div>

      {!predictions ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '0.875rem' }}>
          {ASSETS.map(a => (
            <div key={a.key} className="prediction-card">
              <div className="skeleton" style={{ height: '16px', width: '60%' }} />
              <div className="skeleton" style={{ height: '24px', width: '40%' }} />
              <div className="skeleton" style={{ height: '14px', width: '90%' }} />
            </div>
          ))}
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '0.875rem' }}>
          {ASSETS.map(asset => {
            const item = predictions[asset.key as keyof Predictions] as PredictionItem
            if (!item?.direction) return null
            return (
              <div key={asset.key} className="prediction-card">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ fontSize: '1.1rem' }}>{asset.emoji}</span>
                  <span style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                    {asset.label}
                  </span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <DirectionIcon direction={item.direction} />
                  <span style={{
                    fontSize: '1rem', fontWeight: 700,
                    color: item.direction === 'up' ? 'var(--verified)' : item.direction === 'down' ? '#ef4444' : 'var(--text-muted)',
                    textTransform: 'capitalize',
                  }}>
                    {item.direction}
                  </span>
                  <ConfidencePill confidence={item.confidence} />
                </div>
                <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', margin: 0, lineHeight: 1.4 }}>
                  {item.reason}
                </p>
              </div>
            )
          })}
        </div>
      )}

      <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '0.75rem', fontStyle: 'italic' }}>
        ⚠️ AI-generated predictions based on news analysis. Not financial advice.
      </p>
    </section>
  )
}