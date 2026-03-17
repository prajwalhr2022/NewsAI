/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        serif:  ['var(--font-playfair)', 'Georgia', 'serif'],
        sans:   ['var(--font-dm-sans)',  'system-ui', 'sans-serif'],
      },
      colors: {
        // Light theme
        ink:      '#1a1410',
        paper:    '#f5f0e8',
        accent:   '#c8401a',
        // Dark theme
        void:     '#0d0d0f',
        snow:     '#f0ede8',
        fire:     '#e85d2a',
      },
      animation: {
        'fade-in':    'fadeIn 0.4s ease forwards',
        'slide-down': 'slideDown 0.3s ease forwards',
        'ticker':     'ticker 40s linear infinite',
      },
      keyframes: {
        fadeIn:    { from: { opacity: 0, transform: 'translateY(6px)' }, to: { opacity: 1, transform: 'translateY(0)' } },
        slideDown: { from: { opacity: 0, transform: 'translateY(-8px)' }, to: { opacity: 1, transform: 'translateY(0)' } },
        ticker:    { from: { transform: 'translateX(0)' }, to: { transform: 'translateX(-50%)' } },
      },
    },
  },
  plugins: [],
}