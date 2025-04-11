import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import react from '@astrojs/react';
import robotsTxt from 'astro-robots-txt';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  site: 'https://bestfreeai.net',
  integrations: [
    tailwind(),
    sitemap({
      i18n: {
        defaultLocale: 'en',
        locales: {
          en: 'en-US',
          es: 'es-ES',
          fr: 'fr-FR',
          zh: 'zh-CN'
        }
      }
    }),
    react(),
    robotsTxt()
  ],
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es', 'fr', 'zh'],
    routing: {
      prefixDefaultLocale: false
    }
  },
  vite: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        '@components': path.resolve(__dirname, './src/components'),
        '@layouts': path.resolve(__dirname, './src/layouts'),
        '@content': path.resolve(__dirname, './src/content'),
        '@i18n': path.resolve(__dirname, './src/i18n'),
        '@utils': path.resolve(__dirname, './src/utils')
      }
    }
  }
});