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
    error.value = "Please enter a URL first.";
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
    error.value = e?.data?.url?.[0] || "That doesn't look like a valid URL.";
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
    <div class="card">
      <h1>koota<b>her</b>.ir</h1>
      <p class="subtitle">Paste a long URL, get a short one to share.</p>

      <form class="form" @submit.prevent="shorten">
        <input v-model="url" type="text" placeholder="https://example.com/a/long/url" :disabled="loading" />
        <button type="submit" :disabled="loading">{{ loading ? "Shortening…" : "Shorten" }}</button>
      </form>

      <p v-if="error" class="error">{{ error }}</p>

      <div v-if="shortUrl" class="result">
        <a :href="shortUrl" target="_blank">{{ shortUrl }}</a>
        <button @click="copyLink">{{ copied ? "Copied!" : "Copy" }}</button>
      </div>
    </div>
  </div>
</template>