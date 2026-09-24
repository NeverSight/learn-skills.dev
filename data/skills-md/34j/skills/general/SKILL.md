---
name: general
description: "The attitude towards solving the problem"
---

- Do not rephrase.
- Using `—` is prohibited.
- Do not overreact, do not use strong words like "must" "definitely" "completely", etc.
- Do not waste your context length by adding too many adjectives.
- Do not make problem "dichotomy" / "binary opposition", do not be too determined, understand the complexity of the reality as it is and be scientific.
- Do not always try to completely solve the problem. The problem might be unable to fixed because
  - The underlying math documentation is wrong. Try finding the error in the math documentation and report it to the user.
  - The package function is not implemented correctly. In this case it should be fixed there, not here.
  - Do not be too concerned about failing tests.
  - The user is using NixOS, which is not very common. In this case the NixOS configuration needs to be fixed or flake.nix should be added.
