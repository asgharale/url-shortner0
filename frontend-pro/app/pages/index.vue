<script setup lang="ts">
const config = useRuntimeConfig();

const url = ref("");
const shortUrls = ref<string[]>([]);
const originalUrl = ref("");
const error = ref("");
const loading = ref(false);
const copiedIndex = ref<number | null>(null);

async function shorten() {
  error.value = "";
  shortUrls.value = [];

  const trimmed = url.value.trim();
  if (!trimmed) {
    error.value = "یه آدرس وارد کن.";
    return;
  }

  loading.value = true;
  try {
    const data = await $fetch<{ short_urls: string[]; original_url: string }>(
      `${config.public.apiBase}/pro/shorten/`,
      { method: "POST", body: { url: trimmed } }
    );
    shortUrls.value = data.short_urls;
    originalUrl.value = data.original_url;
    url.value = "";
  } catch (e: any) {
    if (e?.data?.url) {
      error.value = "آدرس معتبر نیست. با http:// یا https:// شروعش کن.";
    } else if (e?.status) {
      error.value = `خطای سرور (کد ${e.status}). دوباره امتحان کن.`;
    } else {
      error.value = "اتصال برقرار نشد. اینترنتت رو چک کن.";
    }
  } finally {
    loading.value = false;
  }
}

async function copyLink(link: string, i: number) {
  await navigator.clipboard.writeText(link);
  copiedIndex.value = i;
  setTimeout(() => (copiedIndex.value = null), 1400);
}
</script>

<template>
  <div class="page">
    <nav class="topbar">
      <span class="brand">پرولینک</span>
      <span class="tag">یک لینک، چند دامنه</span>
    </nav>

    <main class="hero">
      <h1>کوتاه کردن لینک</h1>
      <p class="lede">آدرس رو وارد کن؛ همزمان روی همه دامنه‌ها لینک کوتاه بگیر.</p>

      <form class="form" dir="ltr" @submit.prevent="shorten">
        <input v-model="url" type="text" inputmode="url" autocomplete="off" :disabled="loading" />
        <button type="submit" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          {{ loading ? "..." : "کوتاه کن" }}
        </button>
      </form>

      <p v-if="error" class="error">{{ error }}</p>

      <transition name="fade">
        <div v-if="shortUrls.length" class="results">
          <p class="original-hint" dir="ltr">{{ originalUrl }}</p>
          <div class="card" v-for="(link, i) in shortUrls" :key="link">
            <a :href="link" target="_blank" rel="noopener" dir="ltr" class="link-text">{{ link }}</a>
            <div class="card-actions">
              <button class="btn-flat" @click="copyLink(link, i)">
                {{ copiedIndex === i ? "کپی شد ✓" : "کپی" }}
              </button>
              <a class="btn-flat" :href="link" target="_blank" rel="noopener">باز کن</a>
            </div>
          </div>
        </div>
      </transition>
    </main>

    <footer class="footer">sml2.ir · shrtlnk.ir · linksml.ir · kootaher.ir</footer>
  </div>
</template>