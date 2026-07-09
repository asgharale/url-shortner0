export default defineNuxtConfig({
  compatibilityDate: "2026-06-01",
  devtools: { enabled: true },

  app: {
    head: {
      htmlAttrs: { lang: "en" },
      title: "Prolink — Short Links, Done Right",
      meta: [
        { name: "description", content: "Enterprise-grade link shortening." },
      ],
    },
  },

  css: ["~/assets/css/main.css"],

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "/api",
    },
  },

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
});