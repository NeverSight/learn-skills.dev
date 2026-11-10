---
name: howler-js
description: Guides the agent through Howler.js audio integration for Webflow sites — playback, spatial audio, mute controls, and Barba cleanup. Activates when the task involves sound, audio, or music.
---

<objective>
Integrate Howler.js audio into Webflow projects with proper autoplay handling, accessibility controls, format fallbacks, and Barba.js cleanup.
</objective>

<quick_start>
CDN:
```html
<script src="https://cdn.jsdelivr.net/npm/howler@2/dist/howler.min.js"></script>
```

Basic sound setup:
```js
const AudioManager = (() => {
  let bgMusic, sfxPool;

  function init() {
    bgMusic = new Howl({
      src: ['/audio/ambient.webm', '/audio/ambient.mp3'],
      loop: true,
      volume: 0,
      autoplay: false,
    });

    sfxPool = {
      click: new Howl({ src: ['/audio/click.webm', '/audio/click.mp3'], volume: 0.6 }),
      hover: new Howl({ src: ['/audio/hover.webm', '/audio/hover.mp3'], volume: 0.3 }),
    };
  }

  function playBg() {
    bgMusic.play();
    bgMusic.fade(0, 0.4, 1000);
  }

  function pauseBg() {
    bgMusic.fade(0.4, 0, 500);
    setTimeout(() => bgMusic.pause(), 500);
  }

  function playSfx(name) {
    sfxPool[name]?.play();
  }

  function destroy() {
    bgMusic?.unload();
    Object.values(sfxPool || {}).forEach(s => s.unload());
  }

  return { init, playBg, pauseBg, playSfx, destroy };
})();
```
</quick_start>

<common_patterns>
Mute/unmute toggle:
```js
let muted = false;

muteBtn.addEventListener('click', () => {
  muted = !muted;
  Howler.mute(muted);
  muteBtn.setAttribute('aria-pressed', muted);
  muteBtn.textContent = muted ? 'Unmute' : 'Mute';
});
```

Web Audio policy (autoplay):
Browsers block autoplay audio without user interaction.
```js
document.addEventListener('click', () => {
  if (Howler.ctx.state === 'suspended') {
    Howler.ctx.resume().then(() => AudioManager.playBg());
  }
}, { once: true });
```

Spatial audio (3D):
```js
const sound = new Howl({
  src: ['/audio/wind.webm'],
  loop: true,
  pannerAttr: { panningModel: 'HRTF', refDistance: 1, rolloffFactor: 1 },
});
sound.pos(x, y, z);
Howler.pos(listenerX, listenerY, listenerZ);
```

Barba cleanup:
```js
barba.hooks.before(() => {
  AudioManager.pauseBg();
});
barba.hooks.after(() => {
  // Re-init or resume as appropriate for the new page
});
AudioManager.destroy();
```
</common_patterns>

<anti_patterns>
- Never autoplay audio without user consent
- Always provide both WebM (Opus) and MP3 for compatibility — WebM is smaller/better, MP3 is Safari fallback
- Always provide a visible mute/unmute control
- Use `aria-pressed` on toggle buttons and indicate audio state visually
</anti_patterns>

<success_criteria>
- Audio plays only after user interaction (autoplay policy satisfied)
- Mute/unmute toggle works with correct `aria-pressed` state
- Both WebM and MP3 formats provided for cross-browser support
- `AudioManager.destroy()` called on Barba leave to prevent memory leaks
- No audio continues playing after page transition
</success_criteria>
