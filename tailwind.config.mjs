/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
          950: '#020617',
        }
      },
      typography: (theme) => ({
        invert: {
          css: {
            '--tw-prose-body': theme('colors.dark[300]'),
            '--tw-prose-headings': theme('colors.dark[50]'),
            '--tw-prose-lead': theme('colors.dark[300]'),
            '--tw-prose-links': theme('colors.indigo[400]'),
            '--tw-prose-bold': theme('colors.dark[50]'),
            '--tw-prose-counters': theme('colors.dark[400]'),
            '--tw-prose-bullets': theme('colors.dark[400]'),
            '--tw-prose-hr': theme('colors.dark[700]'),
            '--tw-prose-quotes': theme('colors.dark[100]'),
            '--tw-prose-quote-borders': theme('colors.dark[700]'),
            '--tw-prose-captions': theme('colors.dark[400]'),
            '--tw-prose-code': theme('colors.dark[50]'),
            '--tw-prose-pre-code': theme('colors.dark[50]'),
            '--tw-prose-pre-bg': theme('colors.dark[800]'),
            '--tw-prose-th-borders': theme('colors.dark[700]'),
            '--tw-prose-td-borders': theme('colors.dark[700]'),
          },
        },
      }),
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}