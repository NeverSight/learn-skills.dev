---
name: extreme-motion-design
description: Cria vídeos de motion design de nível de estúdio por código (Remotion/React), com trilha licenciada, SFX sincronizados, voz opcional (ElevenLabs ou modelo TTS local escolhido pelo hardware) e gates automáticos de lint e QA antes da entrega. Use quando pedirem motion design, motion graphics, vídeo animado, explainer, vídeo de produto ou lançamento, reel ou TikTok animado, tipografia cinética, logo animado, animação de UI, loop, narração ou voiceover para vídeo, ou técnicas como keyframing, zoom in e zoom out, motion smooth, morphing, rigging, frame a frame, cel animation, stop motion, rotoscopia, motion tracking, match moving, compositing, motion 3D, speed ramp, match cut, overshoot, parallax e transições. Also for animated video, kinetic typography, product launch video, explainer with voiceover, text to speech narration.
license: MIT
compatibility: Node 18+, Python 3.10+ (uv recomendado) e ffmpeg. Remotion é gratuito para indivíduos e empresas de até 3 pessoas; acima disso exige Company License. Rede opcional (trilha online, voz por API, download de modelos de voz, leitura de site para a marca, acervo de imagem e vídeo livres). Voz local funciona em CPU; modelos maiores pedem GPU.
metadata:
  version: "2.0.0"
  author: "Isaac Mello"
---

# Motion Design

Produz vídeo de motion design por código, com áudio e verificação. O agente não enxerga o vídeo enquanto escreve código: por isso o fluxo declara a direção antes de animar (`direction.json`), mede antes de renderizar (`lint.py`), mede o texto nos frames (`layout.py`), mede se a peça tem direção própria ou caiu no quadro padrão do modelo (`design.py`), passa por um revisor que não escreveu o código e só entrega depois de um gate numérico (`qa.py`). Com um vídeo de referência do usuário, a estrutura dele vira medida e a peça nova ganha uma nota de fidelidade (`reference.py`).

Caminhos são relativos à pasta desta skill (`<skill>`). Scripts com dependências declaram tudo inline (PEP 723): rode com `uv run <skill>/scripts/x.py`. `voice.py`, `lint.py` e `gl.py` usam só a biblioteca padrão e rodam com `python3`; `stills.cjs` e `render.cjs` rodam com `node` na pasta do projeto.

## Fluxo obrigatório

1. **Brief em 5 linhas**: objetivo, público, formato (16:9, 9:16, 1:1), duração, tom e marca. Se faltar formato ou duração, assuma 16:9, 30 fps, 15 a 30 s, e diga o que assumiu.
2. **Marca**: se existe site, repositório ou screenshot do produto, rode `uv run <skill>/scripts/brand.py` e use o `brand.json` que ele escreve (cores, fontes, logo, com a origem de cada valor). Se já existe uma pasta `brand/` de um vídeo anterior, reuse. Sem nenhuma fonte, peça as cores e a fonte ao usuário; não invente marca. Detalhes em `references/brand.md`.
3. **Pergunta de voz (sempre)**: rode `python3 <skill>/scripts/voice.py` e faça ao usuário a pergunta que ele imprime, com as três opções: **sem voz**, **voz com ElevenLabs** ou **voz local**. Use a ferramenta de pergunta do agente quando existir e espere a resposta. Não escolha pelo usuário. Só dispense quando o pedido já respondeu com todas as letras. Detalhes em `references/narration.md`.
4. **Projeto**: copie `<skill>/assets/template/` para a pasta do vídeo, renomeie `gitignore` para `.gitignore`, copie o `brand.json` para `public/` e rode `npm install`. Mapa em `references/template.md`.
5. **Direção (antes de qualquer cena)**: leia `references/design.md`, `references/direction.md` e `references/doctrine.md`. Se o usuário entregou um vídeo de referência, rode antes `reference.py analyze` e siga `references/reference.md`. Monte de 2 a 3 direções diferentes (as fichas do fim de `design.md` ou derivadas do assunto; nunca a combinação padrão de condensada gigante, quase preto com um acento e mono no canto), um styleframe de cada, junte com `contact_sheet.py --images` e mostre ao usuário para ele escolher. Grave a escolha em `direction.json` (conceito, lei visual, motivo, e para cada cena: layout, entrada e herói). Se o pedido delegou a escolha com todas as letras, escolha você, grave `"approved_by": "agent"` e diga isso na entrega.
6. **Roteiro e partitura**: escreva `roteiro.json` (cenas, falas, marcas nomeadas, SFX). `uv run <skill>/scripts/score.py --dry` diz quantos caracteres pagos serão gastos; informe o número e espere o sim antes de `--yes`. O script gera a voz frase a frase, a partitura (`public/timeline.json`) e as marcas (`public/cues.json`). O áudio é o relógio: o visual se ajusta a ele. Nenhuma cena guarda número de frame escrito à mão. Formato em `references/score.md`.
7. **Trilha e SFX**: `music.py` (Incompetech, depois Openverse, depois geração local), `beats.py` quando o corte for na batida. Todo arquivo baixado entra em `credits.json`. Detalhes em `references/audio.md`.
   **Aprovação do áudio (com voz)**: rode `mix.py` e entregue `public/audio/mix.wav` para o usuário ouvir antes de animar. Pedido que muda só a voz refaz `score.py` e `mix.py` e volta para o usuário ouvir, sem render e sem folha de contato.
8. **Cenas**: `<Scene id>` e `useScene(id).at('marca')` dão o tempo; `theme.ts` dá cor e fonte; `useFormat()` dá a escala e a área segura. Procure primeiro um bloco pronto em `references/blocks.md`; só depois componha com as primitivas. Leia só a referência da técnica que for usar (roteador abaixo).
9. **Lint (antes de todo render)**: `python3 <skill>/scripts/lint.py` na pasta do projeto. Corrija todo FAIL; avalie cada WARN.
10. **Dailies**: `node <skill>/scripts/stills.cjs <Composição>` renderiza início, meio e fim de cada cena em um processo só e mede o texto de cada frame. `uv run <skill>/scripts/layout.py out/stills --timeline public/timeline.json` reprova texto cortado, sobreposto, pequeno, sem contraste ou fora da área segura, e avisa cenas com a mesma composição. `uv run <skill>/scripts/design.py out/stills --timeline public/timeline.json` conta os sinais do quadro padrão do modelo: com o veredito "padrão do modelo", volte à direção antes de polir. `contact_sheet.py --stills out/stills` monta a folha. OLHE a imagem, revise com o checklist de `references/qa.md`, corrija e repita até não haver FIX. Nunca chame `remotion still` em laço.
11. **Revisor independente**: entregue a folha de contato e o brief a um subagente de contexto limpo com o texto de `references/critic.md`. Quem escreveu a cena não aprova a cena. Sem subagente disponível, diga na entrega que não houve revisão independente.
12. **Mixagem, render, entrega e gate**:
    ```bash
    uv run <skill>/scripts/mix.py public/timeline.json
    python3 <skill>/scripts/gl.py Showcase                      # uma vez por projeto: mede o backend gráfico
    node <skill>/scripts/render.cjs Showcase                    # ou --formats reels,square,youtube
    uv run <skill>/scripts/deliver.py out/render.mp4 -o out/final.mp4
    uv run <skill>/scripts/qa.py out/final.mp4 --profile youtube --timeline public/timeline.json --stills out/stills
    uv run <skill>/scripts/contact_sheet.py out/final.mp4 --timeline public/timeline.json -o out/sheet.png
    ```
    Com vídeo de referência, feche com `reference.py compare reference/reference.json out/final.mp4 --timeline public/timeline.json` e informe a nota.
    Correção depois do render: `render.cjs Showcase --scene <id>` refaz só aquela cena e remonta o master. O render completo tem orçamento (`budget.full_renders`, padrão 4) e o script recusa quando estoura. Só entregue com `qa.py` sem FAIL.
13. **Entrega honesta**: o MP4, a folha de contato, o texto de créditos e uma lista do que ficou em WARN, de quem aprovou a direção, de todo recurso que caiu em alternativa (voz, trilha, formato, cena simplificada) e do que não foi verificado.

## Regras inegociáveis

- Todo estado visual deriva de `useCurrentFrame()`. Proibido: transição ou animação CSS, classes `animate-*`, `setTimeout`, `Date.now()`, `Math.random()` (use `random(seed)`), `useFrame()` do React Three Fiber. Senão o render pisca ou diverge do preview. `lint.py` reprova.
- Curvas e springs só dos tokens de `src/lib/motion.ts`: entrada `enter` ou `sharp`, saída `exit`, mudança de posição ou forma `move`, zoom out e reveal `settle`, herói da cena `easeX.emphasized`, `linear` só para rotação contínua e loops. Nunca `bounce` ou `elastic`. Overshoot é um só (`easeX.overshoot` ou `springs.snappy`) e só no elemento em foco. `interpolate()` sem `easing` é linear: use `tween()` ou `keys()`.
- Tempo vem da partitura, cor vem do tema. Cena não escreve frame nem hex soltos: `useScene(id).at('marca')` e `C.*`.
- Cada cena tem layout, entrada e herói próprios, declarados em `direction.json`. Cenas vizinhas não repetem o par layout e entrada. Um motivo visual atravessa a peça; ele não vira o mesmo cartão em todas as cenas.
- Imagem real só de acervo com licença conferida (`stock.py`) ou do usuário. Sem rosto reconhecível, marca ou obra recente de terceiro em peça comercial.
- De uma referência reproduza estrutura, ritmo e técnica. Nunca frame, asset, logo, texto, trilha ou voz dela.
- Uma ação primária por vez; secundárias de até 30% da amplitude e ambiente de até 5%. Stagger total até 500 ms. Saída dura cerca de 75% da entrada. Primeira animação começa 0,1 a 0,3 s depois do corte. Depois de cada chegada, hold de 0,4 a 0,8 s; pausa de 0,3 a 0,75 s antes do clímax.
- Texto fica na tela pelo menos 1,5 s + 0,3 s por palavra e no máximo 17 caracteres por segundo em pt-BR. No máximo 2 linhas de 32 a 42 caracteres.
- Safe area: ação dentro de 90% do quadro, texto dentro de 80%. Em 9:16 (1080x1920), texto entre y 360 e 1420. Letra de 28 px ou mais no lado menor de 1080. Texto ornamental que sangra do quadro de propósito leva `data-decor`.
- Motion blur só em 1 a 3 batidas rápidas por vídeo, nunca em texto que precisa ser lido.
- Nada com cara de gerado por IA: sem gradiente roxo de tela cheia, sem tudo entrando com fade, sem glow genérico, sem emoji, sem tudo centralizado. Uma cor de acento, contraste WCAG AA.
- Nenhum número, logo ou fato inventado na tela. Dado do usuário ou com fonte.
- Trilha só com licença `cc0`, `pdm` ou `by` (ou gerada). Nunca `nd`, `sa`, `nc`, sampling+ ou licença desconhecida.
- Chave de API nunca entra no chat, em comando, em log ou em arquivo versionado. O usuário grava no `.env` do projeto.

## Roteador de técnicas

| Técnica | Referência | Primitiva ou script |
|---|---|---|
| Gráfico, contador, moldura de aparelho, legenda, janela de código, cursor, lower third, logo sting | `references/blocks.md` | `src/blocks/*` |
| Keyframing, motion smooth, easing, springs | `references/techniques-motion.md` | `keys()`, `tween()`, `pop()`, `springs` |
| Zoom in, zoom out, push-in, pan, whip pan, parallax, câmera na mão | `references/techniques-motion.md` | `<Camera>`, `<Layer depth>`, `wiggle()` |
| Motion graphics (formas, linhas, dados, logo) | `references/techniques-motion.md` | `shapes.ts`, `strokeDashoffset`, `@remotion/shapes` |
| Kinetic typography | `references/techniques-motion.md` | `<KineticWords words={WORDS}>` |
| Morphing | `references/techniques-motion.md` | `morphPath()` (flubber) |
| Seamless loop | `references/techniques-motion.md` | `loopPhase()`, `loopNoise()`, `qa.py --loop` |
| UX/UI motion e microinterações | `references/techniques-motion.md` | `springs.snappy`, cursor em arco, ripple |
| Antecipação, overshoot, follow-through, squash e stretch, smear | `references/techniques-advanced.md` | `anticipate()`, `easeX`, `lag()`, `squash()`, `smear()` |
| Cascata, speed ramp, time remap, curva de velocidade | `references/techniques-advanced.md` | `cascade()`, `timeRemap()`, `velocity()` |
| Match cut, morph cut, corte invisível, J-cut e L-cut, íris, transição por forma e líquida | `references/techniques-advanced.md` | `<IrisReveal>`, `<GooeyFilter>`, `@remotion/transitions` |
| Mattes, trim paths, repeater, baseline reveal, contador, eco, shine, look de lente | `references/techniques-advanced.md` | `<MaskReveal>`, `ticker()`, `<Echo>`, `<Shine>`, `<Grain>` |
| Frame a frame, cel animation, stop motion | `references/techniques-character.md` | `stepped()`, `<BoilFilter>`, `jitter()` |
| Rigging, IK, lip sync | `references/techniques-character.md` | `twoBoneIK()`, `fabrik()`, `forwardKinematics()`, `visemeFor()` |
| Motion 3D | `references/techniques-3d-compositing.md` | `@remotion/three` + `<ThreeCanvas>` |
| Compositing, vídeo filmado como camada | `references/techniques-3d-compositing.md` | blend modes, máscaras, `<Grain>`, chroma key |
| Foto e vídeo reais livres, Ken Burns, parallax 2.5D de foto, duotone, vídeo dentro da letra | `references/stock.md` e `references/design.md` (seção 6) | `scripts/stock.py` |
| Reproduzir a estrutura de um vídeo de referência | `references/reference.md` | `scripts/reference.py` |
| Motion tracking, gráfico preso a rosto ou mão | `references/techniques-3d-compositing.md` | `scripts/track.py` (`--point`, `--face`, `--hand`) + `<Tracked>` |
| Match moving | `references/techniques-3d-compositing.md` | `track.py --quad` + `<CornerPin>`, `scripts/matchmove.py` |
| Rotoscopia | `references/techniques-3d-compositing.md` | `scripts/roto.py` (PNG com alfa ou contornos SVG) |

Design do quadro e seis direções de arte (`references/design.md`), direção e contrato (`references/direction.md`), modo referência (`references/reference.md`), acervo livre (`references/stock.md`), roteiro e partitura (`references/score.md`), marca (`references/brand.md`), blocos (`references/blocks.md`), voz (`references/narration.md`), áudio (`references/audio.md`), QA, orçamento e entrega (`references/qa.md`), revisor (`references/critic.md`), doutrina de movimento (`references/doctrine.md`), mapa do template (`references/template.md`).

## Comandos de voz e áudio

```bash
python3 <skill>/scripts/voice.py                                   # mede o hardware e monta a pergunta de voz
python3 <skill>/scripts/voice.py --check-key                       # valida a chave da ElevenLabs sem gastar
python3 <skill>/scripts/voice.py --audition "Primeira frase." -o out/vozes   # mesma frase em cada voz local
uv run <skill>/scripts/score.py --dry                               # custo e o que seria gerado, sem gastar
uv run <skill>/scripts/score.py --yes                               # voz frase a frase + partitura + marcas
uv run <skill>/scripts/align.py public/audio/narration.wav roteiro.txt    # tempos por palavra para qualquer WAV
uv run <skill>/scripts/align.py filmagem.mp4 --transcribe -o public/audio/fala   # fala de uma filmagem, sem roteiro
uv run <skill>/scripts/tts.py --normalize-only "Plano de R$ 49,90 às 14h30 com IA"                  # confira a pronúncia
uv run <skill>/scripts/music.py incompetech --feel calm --bpm 70-110 --min-sec 60 -o public/audio/music.mp3
uv run <skill>/scripts/music.py generate --sec 30 --bpm 84 --mood calm -o public/audio/music.wav    # offline
uv run <skill>/scripts/beats.py public/audio/music.mp3 --fps 30                                   # cortes na batida
uv run <skill>/scripts/sfx.py --all public/audio/sfx                                              # whoosh, pop, click...
```

## Quando parar e perguntar

- A pergunta de voz do passo 3 e a escolha da direção do passo 5.
- Logo, marca, número ou depoimento que o usuário não forneceu.
- Antes de gastar em API paga (voz, música): diga o número do `score.py --dry` e espere o sim.
- Trilha com licença diferente de cc0, pdm ou by.
- Orçamento de render completo estourado: diga o que falta conferir e por que os stills não bastam.
- Empresa do usuário com mais de 3 pessoas usando Remotion: avise da Company License.
