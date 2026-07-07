<script setup lang="ts">
const config = useRuntimeConfig();

const url = ref("");
const shortUrl = ref("");
const originalUrl = ref("");
const error = ref("");
const loading = ref(false);
const copied = ref(false);

async function shorten() {
  error.value = "";
  shortUrl.value = "";
  copied.value = false;

  const trimmed = url.value.trim();
  if (!trimmed) {
    error.value = "لطفاً یک آدرس وارد کن.";
    return;
  }

  loading.value = true;
  try {
    const data = await $fetch<{ short_url: string; original_url: string }>(
      `${config.public.apiBase}/shorten/`,
      { method: "POST", body: { url: trimmed } }
    );
    shortUrl.value = data.short_url;
    originalUrl.value = data.original_url;
    url.value = "";
  } catch (e: any) {
    console.error("shorten failed:", e);

    if (e?.data?.url) {
      // Real validation error from the backend
      error.value = "آدرس وارد شده معتبر نیست. حتماً با http:// یا https:// شروع بشه.";
    } else if (e?.status) {
      // Backend responded, but with an unexpected error code
      error.value = `مشکلی در سرور پیش اومد (کد ${e.status}). دوباره امتحان کن.`;
    } else {
      // Request never got a response at all — network/CORS/connection issue
      error.value = "اتصال به سرور برقرار نشد. اتصال اینترنت یا وضعیت سرویس رو چک کن.";
    }
  } finally {
    loading.value = false;
  }
}

async function copyLink() {
  await navigator.clipboard.writeText(shortUrl.value);
  copied.value = true;
  setTimeout(() => (copied.value = false), 1500);
}
</script>

<template>
  <div class="page">
    <div class="wrap">
      <header class="brand">
        <span class="logo">کوتاه<b>ر</b></span>
        <span class="tagline">لینک‌های کوتاه، ساده و سریع</span>
      </header>

      <div class="card">
        <h1>کوتاه کردن لینک</h1>
        <p class="subtitle">آدرس طولانی رو وارد کن، یه لینک کوتاه برای اشتراک‌گذاری بگیر.</p>

        <form class="form" @submit.prevent="shorten">
          <input
            v-model="url"
            type="text"
            dir="ltr"
            inputmode="url"
            autocomplete="off"
            :disabled="loading"
          />
          <button type="submit" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? "در حال کوتاه‌سازی…" : "کوتاه کن" }}
          </button>
        </form>

        <p v-if="error" class="error">{{ error }}</p>

        <transition name="fade">
          <div v-if="shortUrl" class="result">
            <div class="result-row">
              <a :href="shortUrl" target="_blank" rel="noopener" dir="ltr" class="short-link">{{ shortUrl }}</a>
              <div class="result-actions">
                <button class="icon-btn" @click="copyLink">
                  {{ copied ? "کپی شد ✓" : "کپی" }}
                </button>
                <a class="icon-btn" :href="shortUrl" target="_blank" rel="noopener">باز کن</a>
              </div>
            </div>
            <p class="original-hint" dir="ltr">→ {{ originalUrl }}</p>
          </div>
        </transition>
      </div>

      <footer class="footer">kootaher.ir</footer>
    </div>
  </div>
</template>