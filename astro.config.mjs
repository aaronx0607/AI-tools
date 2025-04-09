import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import react from '@astrojs/react';

export default defineConfig({
  site: 'https://aitools-directory.com',
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
    react()
  ],
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es', 'fr', 'zh'],
    routing: {
      prefixDefaultLocale: false
    }
  }
});