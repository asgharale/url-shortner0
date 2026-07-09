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
    error.value = "Enter a URL first.";
    return;
  }

  loading.value = true;
  try {
    const data = await $fetch<{ short_url: string; original_url: string }>(
      `${config.public.apiBase}/pro/shorten/`,
      { method: "POST", body: { url: trimmed } }
    );
    shortUrl.value = data.short_url;
    originalUrl.value = data.original_url;
    url.value = "";
  } catch (e: any) {
    if (e?.data?.url) {
      error.value = "That doesn't look like a valid URL. Include http:// or https://";
    } else if (e?.status) {
      error.value = `Server error (${e.status}). Please try again.`;
    } else {
      error.value = "Couldn't reach the server. Check your connection.";
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
    <nav class="topnav">
      <span class="brand">
        <svg class="mark" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 12h6m-3-3v6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
          <circle cx="12" cy="12" r="9.25" stroke="currentColor" stroke-width="1.5"/>
        </svg>
        Prolink
      </span>
      <span class="topnav-tag">links, minimal</span>
    </nav>

    <main class="hero">
      <h1>Shorten a link.</h1>
      <p class="lede">Paste a URL. Get something shorter. Ship it.</p>

      <form class="form" @submit.prevent="shorten">
        <input
          v-model="url"
          type="text"
          inputmode="url"
          autocomplete="off"
          placeholder="e.g. "
          :disabled="loading"
        />
        <button type="submit" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          {{ loading ? "Shortening" : "Shorten" }}
        </button>
      </form>

      <p v-if="error" class="error">{{ error }}</p>

      <transition name="fade">
        <div v-if="shortUrl" class="result">
          <div class="result-row">
            <a :href="shortUrl" target="_blank" rel="noopener" class="short-link">{{ shortUrl }}</a>
            <div class="result-actions">
              <button class="btn-ghost" @click="copyLink">{{ copied ? "Copied" : "Copy" }}</button>
              <a class="btn-ghost" :href="shortUrl" target="_blank" rel="noopener">Open</a>
            </div>
          </div>
          <p class="original-hint">{{ originalUrl }}</p>
        </div>
      </transition>
    </main>

    <footer class="footer">Prolink</footer>
  </div>
</template>