/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        bg: 'var(--color-bg)',
        surface: {
          DEFAULT: 'var(--color-surface)',
          hover: 'var(--color-surface-hover)',
          raised: 'var(--color-surface-raised)',
          border: 'var(--color-border)',
        },
        'border-subtle': 'var(--color-border-subtle)',
        hairline: 'var(--color-hairline)',
        kicker: 'var(--color-kicker)',
        translucent: 'var(--color-bg-blur)',
        'success-subtle': 'var(--color-success-subtle)',
        'neutral-subtle': 'var(--color-neutral-subtle)',
        'on-brand': 'var(--color-on-brand)',
        text: {
          primary: 'var(--color-text-primary)',
          secondary: 'var(--color-text-secondary)',
          tertiary: 'var(--color-text-tertiary)',
          disabled: 'var(--color-text-tertiary)',
        },
        brand: {
          DEFAULT: 'var(--color-brand)',
          hover: 'var(--color-brand-hover)',
          subtle: 'var(--color-brand-subtle)',
        },
        success: 'var(--color-success)',
        warning: 'var(--color-warning)',
        danger: 'var(--color-danger)',
        chart: {
          1: 'var(--color-chart-1)',
          2: 'var(--color-chart-2)',
          3: 'var(--color-chart-3)',
          4: 'var(--color-chart-4)',
          5: 'var(--color-chart-5)',
          6: 'var(--color-chart-6)',
          7: 'var(--color-chart-7)',
        },
      },
      fontFamily: {
        mono: ['Roboto Mono', 'JetBrains Mono', 'Fira Code', 'SF Mono', 'ui-monospace', 'monospace'],
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'system-ui', 'sans-serif'],
        display: ['Lora', 'Georgia', 'Times New Roman', 'serif'],
      },
      spacing: {
        '18': '4.5rem',
      },
      borderRadius: {
        // Bifrost: sharp corners throughout (--radius: 0px)
        sm: '0px',
        md: '0px',
        lg: '0px',
        xl: '0px',
      },
    },
  },
  plugins: [],
}
