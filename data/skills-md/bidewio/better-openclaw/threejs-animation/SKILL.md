---
name: threejs-animation
description: "Create, control, and optimize animations in Three.js — keyframes, skeletal rigs, morph targets, blending, procedural motion, and performance patterns for web 3D."
metadata:
  openclaw:
    emoji: "🎬"
    source: "https://github.com/CloudAI-X/threejs-skills"
---

# Three.js Animation Skill

## When to use
- Animating 3D models (walk cycles, character rigs, product reveals)
- Keyframe-based animations from Blender/Maya exported as glTF
- Procedural motion (orbiting, waving, pulsing)
- Morph target animations (facial expressions, shape morphing)

## Animation system overview
- **AnimationMixer**: Manages all animations for an object
- **AnimationClip**: Contains keyframe tracks
- **AnimationAction**: Controls playback (play, pause, blend, loop)

## Quick recipe — Play glTF animation
```js
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
const loader = new GLTFLoader();
const clock = new THREE.Clock();
let mixer;

loader.load("model.glb", (gltf) => {
  scene.add(gltf.scene);
  mixer = new THREE.AnimationMixer(gltf.scene);
  const action = mixer.clipAction(gltf.animations[0]);
  action.play();
});

function animate() {
  requestAnimationFrame(animate);
  if (mixer) mixer.update(clock.getDelta());
  renderer.render(scene, camera);
}
animate();
```

## Animation blending
```js
const idleAction = mixer.clipAction(clips.idle);
const walkAction = mixer.clipAction(clips.walk);
idleAction.play();
// Crossfade to walk
walkAction.reset().setEffectiveTimeScale(1).setEffectiveWeight(1).fadeIn(0.5).play();
idleAction.fadeOut(0.5);
```

## Morph targets
```js
mesh.morphTargetInfluences[0] = Math.sin(time) * 0.5 + 0.5;
```

## Procedural motion
```js
// Orbit
object.position.x = Math.cos(time) * radius;
object.position.z = Math.sin(time) * radius;

// Bobbing
object.position.y = Math.sin(time * 2) * 0.1;
```

## Performance tips
- Use `mixer.timeScale` to globally speed/slow animations
- Limit active AnimationActions — blend/crossfade efficiently
- Dispose mixers on route changes in SPAs

## Tips for AI Agents
- Ask for the animation format (glTF, FBX, procedural).
- Confirm loop behavior (once, loop, ping-pong).
- Check reduced motion accessibility requirements.
