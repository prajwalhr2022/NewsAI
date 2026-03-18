'use client'

interface RegionToggleProps {
  isIndia: boolean
  onChange: (v: boolean) => void
}

export default function RegionToggle({ isIndia, onChange }: RegionToggleProps) {
  return (
    <div style={{ display: 'inline-flex', background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: '9999px', padding: '3px', gap: '2px' }}>
      <button
        onClick={() => onChange(false)}
        style={{
          padding: '0.35rem 1rem', borderRadius: '9999px', fontSize: '0.8rem', fontWeight: 500,
          border: 'none', cursor: 'pointer', fontFamily: 'var(--font-dm)',
          background: !isIndia ? 'var(--accent)' : 'transparent',
          color: !isIndia ? 'white' : 'var(--text-secondary)',
          transition: 'all 0.2s',
        }}
      >
        🌍 World
      </button>
      <button
        onClick={() => onChange(true)}
        style={{
          padding: '0.35rem 1rem', borderRadius: '9999px', fontSize: '0.8rem', fontWeight: 500,
          border: 'none', cursor: 'pointer', fontFamily: 'var(--font-dm)',
          background: isIndia ? 'var(--accent)' : 'transparent',
          color: isIndia ? 'white' : 'var(--text-secondary)',
          transition: 'all 0.2s',
        }}
      >
        🇮🇳 India
      </button>
    </div>
  )
}
