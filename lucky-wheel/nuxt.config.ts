export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  app: {
    head: {
      title: 'Spin & Win',
      meta: [
        { name: 'description', content: 'Spin the wheel for a chance to win a prize.' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ],
      link: [
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&family=Inter:wght@400;500;600;700&display=swap'
        }
      ]
    }
  },
  css: ['~/assets/css/main.css'],
  vite: {
    server: {
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:8085',
          changeOrigin: true,
        },
      },
    },
  },
})