<script setup lang="ts">
const config = useRuntimeConfig();

const DOMAINS = ["mini2.ir", "tny2.ir"];

const url = ref("");
const shortUrl = ref("");
const originalUrl = ref("");
const error = ref("");
const loading = ref(false);
const copied = ref(false);

// Default to whichever domain the page is actually being viewed from,
// falling back to the first option if it's not one of the three (e.g. localhost)
const selectedDomain = ref(DOMAINS[0]);
onMounted(() => {
  const host = window.location.hostname.replace(/^www\./, "");
  if (DOMAINS.includes(host)) {
    selectedDomain.value = host;
  }
});

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
      { method: "POST", body: { url: trimmed, domain: selectedDomain.value } }
    );
    shortUrl.value = data.short_url;
    originalUrl.value = data.original_url;
    url.value = "";
  } catch (e: any) {
    console.error("shorten failed:", e);
    if (e?.data?.url) {
      error.value = "آدرس وارد شده معتبر نیست. حتماً با http:// یا https:// شروع بشه.";
    } else if (e?.data?.domain) {
      error.value = "دامنه انتخاب‌شده معتبر نیست.";
    } else if (e?.status) {
      error.value = `مشکلی در سرور پیش اومد (کد ${e.status}). دوباره امتحان کن.`;
    } else {
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
        <span class="logo">🔗 لینکو</span>
        <span class="tagline">لینک‌های کوتاه، ساده و سریع</span>
      </header>

      <div class="card">
        <h1>کوتاه کردن لینک</h1>
        <p class="subtitle">آدرس طولانی رو وارد کن، دامنه دلخواه رو انتخاب کن، لینک کوتاه بگیر.</p>

        <div class="domain-tabs" dir="ltr">
          <button
            v-for="d in DOMAINS"
            :key="d"
            type="button"
            class="domain-tab"
            :class="{ active: selectedDomain === d }"
            @click="selectedDomain = d"
          >
            {{ d }}
          </button>
        </div>

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

      <footer class="footer">mini2.ir · tny2.ir</footer>
    </div>
  </div>
</template>