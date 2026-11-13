import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: ['class'],
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        background: '#F5F7FA',
        surface: {
          DEFAULT: '#FFFFFF',
          subtle: '#F8FAFC',
          muted: '#F1F5F9',
        },
        brand: {
          primary: '#173B63',
          'primary-hover': '#102D4D',
          'primary-subtle': '#E8EFF7',
          accent: '#12665C',
          'accent-hover': '#0C4A43',
          'accent-subtle': '#E6F3F1',
        },
        text: {
          foreground: '#172B42',
          muted: '#475569',
          disabled: '#94A3B8',
          inverse: '#FFFFFF',
        },
        border: {
          DEFAULT: '#DCE3EB',
          subtle: '#E2E8F0',
          input: '#64748B',
          focus: '#1D4ED8',
        },
        semantic: {
          'success-fg': '#166534',
          'success-bg': '#EAF6EE',
          'success-border': '#BBF7D0',
          'warning-fg': '#8A570C',
          'warning-bg': '#FFF4DE',
          'warning-border': '#FED7AA',
          'danger-fg': '#991B1B',
          'danger-bg': '#FDECEC',
          'danger-border': '#FECACA',
          'info-fg': '#173B63',
          'info-bg': '#E8EFF7',
          'info-border': '#BFDBFE',
        },
      },
      borderRadius: {
        sm: '4px',
        input: '6px',
        button: '8px',
        card: '10px',
        panel: '12px',
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        tabular: ['Inter', 'SF Pro Text', 'tabular-nums', 'sans-serif'],
      },
      boxShadow: {
        sm: '0 1px 2px 0 rgba(15, 23, 42, 0.05)',
        md: '0 4px 6px -1px rgba(15, 23, 42, 0.08), 0 2px 4px -2px rgba(15, 23, 42, 0.04)',
        lg: '0 10px 15px -3px rgba(15, 23, 42, 0.1), 0 4px 6px -4px rgba(15, 23, 42, 0.05)',
      },
    },
  },
  plugins: [],
};

export default config;
