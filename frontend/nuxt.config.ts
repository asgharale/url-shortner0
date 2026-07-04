export default defineNuxtConfig({
  compatibilityDate: "2026-06-01",
  devtools: { enabled: true },

  css: ["~/assets/css/main.css"],

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "/api",
    },
  },

  // In dev, proxy /api calls to Django running on 8085
  vite: {
    server: {
      proxy: {
        "/api": {
          target: "http://127.0.0.1:8085",
          changeOrigin: true,
        },
      },
    },
  },

  // `nuxt generate` outputs static files Django (WhiteNoise) can serve directly
  nitro: {
    output: {
      publicDir: "../dist",
    },
  },
});