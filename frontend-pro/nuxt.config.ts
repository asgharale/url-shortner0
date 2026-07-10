export default defineNuxtConfig({
  compatibilityDate: "2026-06-01",
  devtools: { enabled: true },

  app: {
    head: {
      htmlAttrs: { lang: "fa", dir: "rtl" },
      title: "پرولینک — کوتاه‌کننده لینک حرفه‌ای",
      meta: [{ name: "description", content: "لینکت رو کوتاه کن، روی چند دامنه همزمان داشته باش." }],
    },
  },

  css: ["~/assets/css/main.css"],

  runtimeConfig: {
    public: { apiBase: process.env.NUXT_PUBLIC_API_BASE || "/api" },
  },

  vite: {
    server: {
      proxy: { "/api": { target: "http://127.0.0.1:8085", changeOrigin: true } },
    },
  },
});