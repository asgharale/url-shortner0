<script setup lang="ts">
useHead({
  htmlAttrs: { lang: 'fa',
    dir:"rtl"
   }
})
// ---------------------------------------------------------------------------
// 👉 EDIT THIS: where "Claim Offer" sends the visitor once they've won.
const FALLBACK_CLAIM_URL = 'https://smart-locker.ir'
const claimUrl = ref(FALLBACK_CLAIM_URL)

onMounted(async () => {
  try {
    const data = await $fetch('/api/wheel/redirect/')
    if (data?.url) claimUrl.value = data.url
  } catch (e) {
    console.error('Could not fetch wheel redirect URL, using fallback:', e)
  }
})
// ---------------------------------------------------------------------------

type Prize = {
  label: string
  sub: string
  fill: string
  weight: number
}

const prizes: Prize[] = [
  { label: '666 شیبا',    sub: 'code',    fill: 'var(--pink)',  weight: 18 },
  { label: '0.005 اتریوم',  sub: 'code',    fill: 'var(--teal)',  weight: 16 },
  { label: '0.00008 \nبیتکوین',    sub: 'code',    fill: 'var(--pink)',  weight: 12 },
  { label: '100 سوت طلا',  sub: '0.1 gr gold', fill: 'var(--gold)', weight: 8 },
  { label: '5٪ تخفیف\n خرید طلا',    sub: 'code',    fill: 'var(--teal)',  weight: 8 },
  { label: 'پوچ',  sub: 'code',    fill: 'var(--pink)',  weight: 14 },
  { label: '8٪ تخفیف\n خرید طلا',    sub: 'code',    fill: 'var(--teal)',  weight: 16 },
  { label: '500 سوت طلا',    sub: '0.5 gr gold', fill: 'var(--gold)',  weight: 8 }
]

const segAngle = 360 / prizes.length
const radius = 150
const center = 160

function polar(angleDeg: number, r: number) {
  const rad = ((angleDeg - 90) * Math.PI) / 180
  return { x: center + r * Math.cos(rad), y: center + r * Math.sin(rad) }
}

function segmentPath(index: number) {
  const start = index * segAngle
  const end = start + segAngle
  const p1 = polar(start, radius)
  const p2 = polar(end, radius)
  const largeArc = segAngle > 180 ? 1 : 0
  return `M ${center} ${center} L ${p1.x.toFixed(2)} ${p1.y.toFixed(2)} A ${radius} ${radius} 0 ${largeArc} 1 ${p2.x.toFixed(2)} ${p2.y.toFixed(2)} Z`
}

function labelTransform(index: number) {
  const mid = index * segAngle + segAngle / 2

  const r = radius - 42

  const rad = ((mid - 90) * Math.PI) / 180

  const x = center + Math.cos(rad) * r
  const y = center + Math.sin(rad) * r

  return [
    `translate(${x} ${y})`,
    `rotate(${mid + 90})`
  ].join(" ")
}

const rotation = ref(0)
const spinning = ref(false)
const resultIndex = ref<number | null>(null)
const showCard = ref(false)
const pointerHit = ref(false)
const confettiPieces = ref<{ id: number; left: number; color: string; delay: number; duration: number; drift: number; rot: number }[]>([])
let confettiSeq = 0

const wheelStyle = computed(() => ({
  transform: `rotate(${rotation.value}deg)`
}))

function pickWeightedIndex() {
  const total = prizes.reduce((sum, p) => sum + p.weight, 0)
  let r = Math.random() * total
  for (let i = 0; i < prizes.length; i++) {
    r -= prizes[i].weight
    if (r <= 0) return i
  }
  return prizes.length - 1
}

function launchConfetti() {
  const colors = ['var(--gold)', 'var(--pink)', 'var(--teal)', 'var(--cream)']
  const pieces = []
  for (let i = 0; i < 46; i++) {
    pieces.push({
      id: confettiSeq++,
      left: Math.random() * 100,
      color: colors[i % colors.length],
      delay: Math.random() * 0.25,
      duration: 1.6 + Math.random() * 1.1,
      drift: (Math.random() - 0.5) * 140,
      rot: 360 + Math.random() * 720
    })
  }
  confettiPieces.value = pieces
  setTimeout(() => {
    confettiPieces.value = []
  }, 3200)
}

function spin() {
  if (spinning.value) return
  spinning.value = true
  showCard.value = false
  resultIndex.value = null

  const targetIndex = pickWeightedIndex()
  const targetCenter = targetIndex * segAngle + segAngle / 2
  const normalizedTarget = (360 - targetCenter) % 360
  const extraSpins = 6 + Math.floor(Math.random() * 3)

  const baseline = Math.ceil((rotation.value + 1) / 360) * 360
  rotation.value = baseline + extraSpins * 360 + normalizedTarget

  window.setTimeout(() => {
    spinning.value = false
    resultIndex.value = targetIndex
    pointerHit.value = true
    launchConfetti()
    window.setTimeout(() => { pointerHit.value = false }, 420)
    window.setTimeout(() => { showCard.value = true }, 200)
  }, 4200)
}

const result = computed(() => (resultIndex.value !== null ? prizes[resultIndex.value] : null))
const isWin = computed(() => result.value?.label !== 'TRY AGAIN')

function spinAgain() {
  showCard.value = false
  resultIndex.value = null
}
</script>

<template>
  <div class="wheel-scene">
    <div class="confetti-layer" aria-hidden="true">
      <span
        v-for="piece in confettiPieces"
        :key="piece.id"
        class="confetti-piece"
        :style="{
          left: piece.left + '%',
          background: piece.color,
          animationDelay: piece.delay + 's',
          animationDuration: piece.duration + 's',
          '--drift': piece.drift + 'px',
          '--rot': piece.rot + 'deg'
        }"
      />
    </div>

    <div class="wheel-wrap">
      <div class="pointer" :class="{ hit: pointerHit }" aria-hidden="true">
        <svg viewBox="0 0 40 46" width="40" height="46">
          <path d="M20 46 L2 10 A18 18 0 0 1 38 10 Z" fill="var(--gold-bright)" stroke="var(--ink-900)" stroke-width="2" />
        </svg>
      </div>

      <div class="wheel-rim">
        <svg
          class="wheel-svg"
          :class="{ spinning }"
          :style="wheelStyle"
          viewBox="0 0 320 320"
          width="320"
          height="320"
        >
          <circle :cx="center" :cy="center" :r="radius + 4" fill="var(--ink-900)" />
          <g v-for="(p, i) in prizes" :key="p.label">
            <path :d="segmentPath(i)" :fill="p.fill" stroke="var(--ink-900)" stroke-width="2" />
            <text
              :transform="labelTransform(i)"
              x="0"
              y="0"
              text-anchor="middle"
              dominant-baseline="middle"
              class="segment-label"
            >
              <tspan
                v-for="(line,index) in p.label.split('\n')"
                :key="index"
                x="0"
                :dy="index===0?0:18"
              >
                {{ line }}
              </tspan>
            </text>

          </g>
          <circle :cx="center" :cy="center" r="12" fill="var(--ink-900)" />
        </svg>

        <button
          class="hub"
          type="button"
          :disabled="spinning"
          :aria-label="spinning ? 'Spinning' : 'Spin the wheel'"
          @click="spin"
        >
          {{ spinning ? '···' : 'بچرخونش' }}
        </button>
      </div>
    </div>

    <Transition name="ticket">
      <div v-if="showCard && result" class="result-card" role="status">
        <div class="ticket-notch left" />
        <div class="ticket-notch right" />
        <p class="eyebrow">{{ isWin ? 'جایزت در اومد:' : 'So close' }}</p>
        <h3 class="prize-name">{{ result.label }}</h3>

        <template v-if="isWin">
          <p class="prize-copy">
            برای دریافت جایزه وارد وبسایت شو قبل اینکه منقضی شه
          </p>
          <a
            class="claim-btn"
            :href="claimUrl"
            target="_blank"
            rel="noopener noreferrer"
          >
            دریافت جایزه
          </a>
          <button class="text-btn" type="button" @click="spinAgain">دوباره بچرخون</button>
        </template>

        <template v-else>
          <p class="prize-copy">ای وای پوچ اومد</p>
          <button class="claim-btn secondary" type="button" @click="spinAgain">دوباره بچرخون</button>
        </template>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.wheel-scene {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2.5rem;
  width: 100%;
}

.wheel-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pointer {
  position: absolute;
  top: -14px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 3;
  filter: drop-shadow(0 3px 4px rgba(0, 0, 0, 0.4));
  transition: transform 0.15s ease;
}

.pointer.hit {
  animation: pointer-wobble 0.42s ease;
}

@keyframes pointer-wobble {
  0% { transform: translateX(-50%) rotate(0deg); }
  30% { transform: translateX(-50%) rotate(-16deg); }
  60% { transform: translateX(-50%) rotate(10deg); }
  100% { transform: translateX(-50%) rotate(0deg); }
}

.wheel-rim {
  position: relative;
  padding: 14px;
  border-radius: 50%;
  background: linear-gradient(155deg, var(--gold-bright), var(--gold) 55%, #b5810a);
  box-shadow:
    0 18px 40px -12px rgba(0, 0, 0, 0.55),
    inset 0 0 0 3px rgba(0, 0, 0, 0.15);
}

.wheel-svg {
  display: block;
  border-radius: 50%;
  background: var(--ink-900);
}

.wheel-svg.spinning {
  transition: transform 4.2s cubic-bezier(0.12, 0.67, 0.1, 1);
}
.wheel-svg:not(.spinning) {
  transition: transform 4.2s cubic-bezier(0.12, 0.67, 0.1, 1);
}

.segment-label {
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 700;

  text-anchor: middle;
  dominant-baseline: middle;

  direction: rtl;
  unicode-bidi: plaintext;
}
.segment-label.on-dark {
  fill: var(--cream);
}

.hub {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 74px;
  height: 74px;
  border-radius: 50%;
  border: 3px solid var(--ink-900);
  background: radial-gradient(circle at 35% 30%, var(--gold-bright), var(--gold) 70%);
  color: var(--ink-900);
  font-family: var(--font-display);
  font-weight: 800;
  font-size: 1rem;
  letter-spacing: 0.06em;
  cursor: pointer;
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.4);
  z-index: 2;
}
.hub:hover:not(:disabled) {
  filter: brightness(1.05);
}
.hub:disabled {
  cursor: not-allowed;
  opacity: 0.85;
}
.hub:focus-visible {
  outline: 3px solid var(--teal);
  outline-offset: 3px;
}

.confetti-layer {
  position: absolute;
  inset: -40px -20px auto -20px;
  height: 0;
  overflow: visible;
  pointer-events: none;
  z-index: 4;
}
.confetti-piece {
  position: absolute;
  top: -10px;
  width: 9px;
  height: 14px;
  border-radius: 2px;
  animation-name: confetti-fall;
  animation-timing-function: ease-in;
  animation-fill-mode: forwards;
}
@keyframes confetti-fall {
  0% { transform: translate(0, 0) rotate(0deg); opacity: 1; }
  100% { transform: translate(var(--drift), 340px) rotate(var(--rot)); opacity: 0; }
}

.result-card {
  position: relative;
  width: min(360px, 100%);
  background: var(--ink-700);
  border-radius: 18px;
  padding: 1.75rem 1.75rem 2rem;
  text-align: center;
  box-shadow: 0 20px 50px -18px rgba(0, 0, 0, 0.6);
  border: 1px dashed rgba(242, 183, 5, 0.5);
}
.ticket-notch {
  position: absolute;
  top: 50%;
  width: 24px;
  height: 24px;
  background: var(--ink-800);
  border-radius: 50%;
  transform: translateY(-50%);
}
.ticket-notch.left { left: -12px; }
.ticket-notch.right { right: -12px; }

.eyebrow {
  margin: 0 0 0.35rem;
  font-size: 0.75rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--cream-dim);
}
.prize-name {
  margin: 0 0 0.75rem;
  font-family: var(--font-display);
  font-size: 2rem;
  color: var(--gold-bright);
}
.prize-copy {
  margin: 0 0 1.25rem;
  color: var(--cream-dim);
  line-height: 1.5;
  font-size: 0.95rem;
}
.claim-btn {
  display: inline-block;
  width: 100%;
  padding: 0.85rem 1rem;
  border-radius: 10px;
  background: linear-gradient(180deg, var(--gold-bright), var(--gold));
  color: var(--ink-900);
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 1.05rem;
  text-decoration: none;
  border: none;
  cursor: pointer;
  box-shadow: 0 8px 18px -6px rgba(242, 183, 5, 0.55);
}
.claim-btn:hover {
  filter: brightness(1.04);
}
.claim-btn.secondary {
  background: transparent;
  border: 1.5px solid var(--cream-dim);
  color: var(--cream);
  box-shadow: none;
}
.text-btn {
  margin-top: 0.9rem;
  background: none;
  border: none;
  color: var(--cream-dim);
  font-size: 0.85rem;
  text-decoration: underline;
  cursor: pointer;
}

.ticket-enter-active {
  transition: transform 0.45s cubic-bezier(0.2, 0.7, 0.2, 1), opacity 0.45s ease;
}
.ticket-leave-active {
  transition: transform 0.25s ease, opacity 0.25s ease;
}
.ticket-enter-from,
.ticket-leave-to {
  transform: translateY(24px);
  opacity: 0;
}

@media (max-width: 420px) {
  .wheel-svg { width: 260px; height: 260px; }
  .wheel-rim { padding: 10px; }
}
</style>
