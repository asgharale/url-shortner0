export default defineNuxtConfig({
  compatibilityDate: "2026-06-01",
  devtools: { enabled: true },

  app: {
    head: {
      htmlAttrs: { lang: "fa", dir: "rtl" },
      title: "کوتاه‌کننده لینک",
      meta: [
        { name: "description", content: "لینک بلندت رو کوتاه کن و راحت به اشتراک بذار." },
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

  nitro: {
    output: {
      publicDir: "../dist",
    },
  },
});