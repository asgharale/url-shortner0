<script setup lang="ts">

</script>

<template>
  <div class="page">
    <div class="atmosphere" aria-hidden="true">
      <span v-for="n in 24" :key="n" class="spark" :style="{
        left: (n * 4.3) % 100 + '%',
        top: (n * 7.1) % 100 + '%',
        animationDelay: (n % 6) * 0.5 + 's'
      }" />
    </div>

    <main class="content">
      <p class="kicker">گردونه رو بچرخون</p>
      <h1>به گردونه بده<br />یک دور</h1>
      <p class="lede">
        بچرخون و جایزتو بگیر
      </p>

      <LuckyWheel />

      <br>
      <p class="channel-text">
        برای شرکت در گردونه های روزانه بعدی در
        <a
          href="https://eitaa.com/Geymat_onliin1"
          target="_blank"
          rel="noopener noreferrer"
          class="channel-link"
        >
          کانال ایتا
        </a>
        عضو بشین
      </p>

      <p class="fine-print">
        هر کاربر میتونه یک بار جایزه دریافت کنه!
      </p>
    </main>

    <footer class="foot">
      <span>&copy; {{ new Date().getFullYear() }} Spin &amp; Win</span>
    </footer>
  </div>
</template>

<style scoped>
.page {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: hidden;
  background:
    radial-gradient(60% 50% at 50% 28%, rgba(242, 183, 5, 0.14), transparent 70%),
    radial-gradient(80% 60% at 50% 100%, rgba(46, 230, 214, 0.08), transparent 70%),
    var(--ink-800);
}

.atmosphere {
  position: absolute;
  inset: 0;
  pointer-events: none;
}
.spark {
  position: absolute;
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: var(--cream);
  opacity: 0.35;
  animation: twinkle 3.2s ease-in-out infinite;
}
@keyframes twinkle {
  0%, 100% { opacity: 0.1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.6); }
}

.content {
  position: relative;
  z-index: 1;
  max-width: 560px;
  width: 100%;
  padding: 3.5rem 1.5rem 2.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.kicker {
  margin: 0 0 0.75rem;
  font-size: 0.85rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--teal);
  font-weight: 600;
}

h1 {
  margin: 0 0 1rem;
  font-family: var(--font-display);
  font-weight: 800;
  font-size: clamp(2.2rem, 6vw, 3.1rem);
  line-height: 1.05;
  color: var(--cream);
}

.lede {
  margin: 0 0 2.75rem;
  max-width: 40ch;
  color: var(--cream-dim);
  font-size: 1.02rem;
  line-height: 1.55;
}

.fine-print {
  margin: 2.5rem 0 0;
  font-size: 0.78rem;
  color: rgba(207, 196, 232, 0.6);
  max-width: 38ch;
}

.foot {
  position: relative;
  z-index: 1;
  padding: 1.5rem;
  font-size: 0.78rem;
  color: rgba(207, 196, 232, 0.5);
}
.channel-text {
  margin-top: 1rem;
  font-size: 1rem;
  color: var(--cream);
  font-weight: 500;
  line-height: 1.8;
}
.channel-link::after {
  content: "↗";
  margin-right: 0.35rem;
  font-size: 0.9em;
}
.channel-link {
  display: inline-block;
  background: linear-gradient(135deg, #f2b705, #ffcf33);
  color: #111;
  padding: 0.55rem 1rem;
  border-radius: 999px;
  font-weight: 700;
  text-decoration: none;
  margin: 0 0.25rem;
  box-shadow: 0 6px 18px rgba(242, 183, 5, 0.35);
}

.channel-link:hover {
  transform: translateY(-2px);
}
</style>
