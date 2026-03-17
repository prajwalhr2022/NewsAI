'use client'

interface RegionToggleProps {
  isIndia: boolean
  onChange: (v: boolean) => void
}

export default function RegionToggle({ isIndia, onChange }: RegionToggleProps) {
  return (
    <div className="region-toggle">
      <button className={`region-btn ${!isIndia ? 'active' : ''}`} onClick={() => onChange(false)}>
        🌍 World News
      </button>
      <button className={`region-btn ${isIndia ? 'active' : ''}`} onClick={() => onChange(true)}>
        🇮🇳 India News
      </button>
    </div>
  )
}
