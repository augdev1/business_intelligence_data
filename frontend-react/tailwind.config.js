/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        acc:  'var(--acc)',
        acc2: 'var(--acc2)',
      },
      backgroundImage: {
        'gradient-accent': 'linear-gradient(135deg, var(--acc), var(--acc2))',
      },
      backdropBlur: {
        xs: '4px',
      },
    },
  },
  plugins: [],
}
