---
name: aula-interativa
description: Produz aulas guiadas em HTML sobre qualquer assunto — telas curtas com pouco texto, um botão Continuar, mocks realistas da ferramenta ou situação, diagramas animados e prática com feedback — e as revisa quadro a quadro via Playwright. Use quando o usuário quiser aprender nesse formato ou transformar material em uma aula interativa. Pergunta apenas idioma, assunto e profundidade ou quantidade de telas; executa pesquisa, roteiro, design, motion, captura, correção e entrega com os recursos incluídos.
---

# Aula interativa

Uma entrada simples deve acionar uma produção completa: uma aula que a pessoa **quer** seguir, em que sempre sabe o que olhar, o que ler e onde clicar, e ao fim consegue aplicar o conceito. Correção de conteúdo e determinismo são obrigatórios, mas não bastam: uma tela feia, cheia de texto ou confusa é um defeito com a mesma prioridade de um erro factual.

## Entrada: somente três perguntas

Reutilize respostas explícitas do pedido e da conversa. Não pergunte novamente o que já foi respondido. Se faltar idioma, pergunte-o antes das demais perguntas e traduza o restante para a resposta escolhida.

1. **Qual idioma? / Which language?** Português, English, Español ou outro.
2. **O que você quer aprender hoje?** Aceite tema, problema, pergunta, ferramenta ou material.
3. **Qual profundidade?** 1 — pouca, 2 — média, 3 — muita. Aceite também uma quantidade exata de telas.

| Escolha | Escopo | Telas curtas (faixa usual) |
|---|---|---|
| 1 | Um mecanismo central, um caso real, uma aplicação | 10–14 |
| 2 | Mecanismo, variações, caso real resolvido, duas práticas | 18–26 |
| 3 | Mecanismos internos, limites, operação, transferência | 30–40 |

Cada tela tem uma ideia. Profundidade vem de mais telas e passos e, quando o assunto pede, de um bloco de aprofundamento bem composto; nunca de telas desarrumadas. Respeite uma quantidade exata. Profundidade não é conhecimento prévio. Se o usuário delegar, use 2. Não acrescente questionário de estética, plataforma ou áudio. Não execute a entrada quando a tarefa for editar esta skill.

## Leia antes de começar

| Quando | Recurso | Resultado |
|---|---|---|
| **Sempre, primeiro** | [Experiência do aluno](references/00-experiencia-do-aluno.md) | Contrato de navegação, texto calmo (uma voz tipográfica), tipos de tela, composição |
| **Sempre, antes do brief** | [Arco da aula](references/10-arco-da-aula.md) | As 7 decisões e os 8 movimentos de uma aula impecável |
| **Sempre, antes do roteiro** | [Escrita](references/11-escrita.md) | Títulos, frases de passo, termos, feedback |
| **Sempre, em cada portão** | [Qualidade e portões](references/12-qualidade-e-portoes.md) | Rubrica 1–5, portões P1–P5, falhas típicas de modelos |
| **Sempre, antes de escrever código** | `examples/exemplar-dns/` e `examples/mecanismo.html` | O exemplar mostra o processo completo (brief, roteiro, fontes, aula); o mecanismo mostra a API mínima. Estude a forma, não copie o tema |
| Depois da entrada | [Didática](references/01-didatica.md) | Objetivos, pré-requisitos, progressão |
| Ao pesquisar | [Fontes e interfaces](references/02-fontes-e-interfaces.md) | Evidências, versões, mocks honestos |
| Ao roteirizar | [Roteiro de telas](references/03-roteiro-de-cenas.md) | Tabela fala · imagem · tipo; passos |
| Ao desenhar | [Direção visual](references/04-direcao-visual.md) | Tokens, blocos do kit, geometria |
| Ao animar | [Motion](references/05-motion.md) e [Receitas](references/06-receitas-motion.md) | Tempo, easing, câmera, mocks animados |
| Ao implementar | [Runtime e HTML](references/07-runtime-html.md) | Player, kit, API de captura |
| Antes de entregar | [Captura e revisão](references/08-captura-e-revisao.md) | Storyboard, frames, testes, reparos |
| Para julgar | [Falhas e critérios](references/09-criterios-e-falhas.md) | Critérios de aceitação |

## Pipeline de produção

1. **Preparar.** `node scripts/check_env.mjs --channel chrome`. Reutilize um `node_modules` existente com Playwright e Sharp (`find ~ -maxdepth 4 -type d -path '*node_modules/playwright'`) via `LESSON_NODE_MODULES`; instale em `$WORK/tooling` só se não houver.
2. **Pesquisar e decidir (portão P1).** Preencha `$WORK/brief.md` a partir de `templates/brief.md`: as 7 decisões do [arco](references/10-arco-da-aula.md), com caso único e resultados calculados. Objetivo observável, mapa de pré-requisitos, fontes primárias. Para software, verifique comandos, nomes e formatos de saída que vão aparecer nos mocks (execute-os se puder). Guarde `brief.md` e `sources.json` no diretório de trabalho `$WORK`: uma pasta própria da aula, **fora da pasta da skill**.
3. **Roteirizar (portão P2).** Escreva `$WORK/roteiro.md` a partir de `templates/roteiro.md`: uma linha por passo com movimento do arco, tipo, frase e imagem; preencha as conferências; faça o teste de leitura em voz alta de [escrita](references/11-escrita.md#10-teste-de-leitura-em-voz-alta). Antes de desenhar, confira: cada termo é definido antes de ser usado; cada conceito tem um mock ou desenho; o aprofundamento, quando houver, cabe num bloco só; afirmações sobre o caso não viram regra geral; os tipos alternam. É aqui que a aula fica boa ou ruim.
4. **Montar.** Copie a pasta `templates/` para `$WORK/source/templates/` e a aula para `$WORK/source/lesson.html`, com `<script src="templates/…">` e `<link href="templates/player.css">` (o exemplo usa `../templates/` só porque mora dentro da skill). Parta de `examples/mecanismo.html`. Monte cada tela com o kit (`LessonKit.diagram`, `split`, `hero`, `terminal`, `app`, `quiz`, `cards`) e o modelo calculado no `render`. Escolha a paleta do assunto nos tokens do `:root`; não reescreva o player.
5. **Primeira impressão (portão P3).** Com 2–3 telas prontas, capture e veja o storyboard; acerte tipografia, paleta e desenho antes de fazer o resto.
6. **Animar.** Use `templates/motion.js` (`enter`, `stagger`, `spring`, `pulse`, `camera`, `typed`). O movimento mostra o mecanismo; entradas são calmas; o passo termina parado.
7. **Revisar em ciclos (portão P4).** Capture keyframes em `1440x900,390x844` e motion a 30 fps; gere o **storyboard** (desktop, celular e os cenários de erro) e leia tela por tela com o checklist de [experiência](references/00-experiencia-do-aluno.md#9-checklist-da-experiência-rode-no-storyboard); abra em tamanho real os passos com cara de problema; revise o motion pelas folhas de contato com a amostragem de [captura e revisão](references/08-captura-e-revisao.md#8-inspeção-visual-efetiva); escreva testes da própria aula (cálculos, feedback de cada alternativa, navegação) em `$WORK/test_aula.mjs`; rode `audit.mjs`. Faça a autocrítica em três papéis e dê as notas da rubrica em `$WORK/qualidade.md` ([qualidade](references/12-qualidade-e-portoes.md)). Corrija, recapture, repita até toda dimensão ter nota ≥ 4, o storyboard passar no checklist e a captura não ter problemas.
8. **Empacotar e entregar (portão P5).** `pack.mjs` gera um HTML único; abra-o no navegador do usuário, salvo pedido em contrário. Entregue só o HTML. Roteiro, capturas e relatórios ficam em `$WORK`, nunca na pasta da skill nem junto da entrega; ao fim, avise que as capturas podem ser apagadas.

Não peça aprovação de roteiro ou keyframe. Decisões estéticas comuns são suas. Áudio, vídeo e 3D só entram se ajudarem o objetivo. A aula funciona sem som.

## Invariantes

**Experiência**
- Arco completo com caso único: gancho, revelação, vocabulário, modelo, mecanismo, prova real, prática e fechamento.
- Uma ação principal (Continuar), sempre no mesmo lugar; o aluno nunca precisa de pausar, reproduzir ou reiniciar.
- Uma ideia por tela e uma frase-guia por passo. Texto longo é permitido num bloco de aprofundamento; poluição visual não: uma família, no máximo 4 tamanhos de texto por tela, poucas cores com papel, uma região de texto. Nenhuma fonte, citação ou nota de versão na tela: fontes vão em `sources` e aparecem no painel Fontes.
- Todo termo técnico é definido (com desenho) antes de ser usado.
- O desenho ocupa a cena; no desktop a tela cabe em 1440×900 sem rolar; texto ≥ 11 px renderizado em todo viewport revisado.
- Mocks usam formatos verificados e trazem o selo “simulação”.

**Execução**
- O mesmo slide, passo, tempo e entradas produzem o mesmo frame, inclusive buscando fora de ordem. Nada de relógio, rede, aleatoriedade sem seed ou transição CSS na cena.
- Fonte, imagens e recursos carregam antes de `lesson.ready`; falha de recurso é informada.
- O modelo determina texto, cores, estados e feedback; a frase do passo deriva do mesmo estado do desenho.
- Interações têm consequência e feedback causal; uma resposta errada recebe a explicação do porquê.
- Dados reais, mocks, reconstruções e valores ilustrativos recebem rótulos corretos.

## Comandos

`$SKILL` é a pasta desta skill; `$WORK` é a pasta da aula, fora dela. Use caminhos absolutos.

```bash
node $SKILL/scripts/check_env.mjs --channel chrome
node $SKILL/scripts/pack.mjs $WORK/source/lesson.html --out $WORK/out/lesson.html
node $SKILL/scripts/capture.mjs $WORK/out/lesson.html --out $WORK/qa/kf --mode keyframes --viewports 1440x900,390x844 --channel chrome
node $SKILL/scripts/storyboard.mjs $WORK/qa/kf/manifest.json                      # desktop
node $SKILL/scripts/storyboard.mjs $WORK/qa/kf/manifest.json --viewport 390x844   # celular
node $SKILL/scripts/storyboard.mjs $WORK/qa/kf/manifest.json --scenario errada    # feedback de erro
node $SKILL/scripts/capture.mjs $WORK/out/lesson.html --out $WORK/qa/motion --mode motion --fps 30 --channel chrome
node $SKILL/scripts/contact_sheet.mjs $WORK/qa/motion/manifest.json --stride 3
node $SKILL/scripts/audit.mjs $WORK/out/lesson.html --capture $WORK/qa/motion/manifest.json --out $WORK/qa/audit.json --channel chrome
```

**Apostila em PDF (quando o usuário pedir ou quando a aula for distribuída para impressão ou leitura offline):** `node $SKILL/scripts/pdf.mjs $WORK/out/lesson.html --out $WORK/out/lesson.pdf --channel chrome` gera A4 paisagem: capa, uma página por tela (estado final da cena + as frases de todos os passos, em ordem), práticas sem resposta, gabarito com o feedback no fim e fontes com links. Abra algumas páginas do PDF antes de entregar.

**Vídeo da aula (só se o usuário pedir):** `node $SKILL/scripts/video.mjs $WORK/out/lesson.html --out $WORK/video --channel chrome` grava a aula sendo usada (cada passo anima, um cursor clica em Continuar, as práticas recebem a resposta certa) em 1920×1080, 1080×1080, 1080×1350 e 1080×1920, nativos. `--formats` escolhe formatos; `--hold` e `--read` ajustam as pausas. Assista a um quadro de cada formato antes de entregar.

`test_player.mjs` e `test_tools.mjs` testam o player e as ferramentas com o exemplo incluído; rode-os ao editar a skill, não para validar uma aula.

Sem `--channel`, usa o Chromium do Playwright. Não troque falha por silêncio nem marque inspeção visual como feita sem ter olhado.

## Conclusão

Conclua quando: os portões P1–P5 passaram; toda dimensão da rubrica tem nota ≥ 4; o storyboard passa no checklist de experiência em desktop e celular; a captura não tem problemas; as animações foram inspecionadas; a prática tem feedback; o HTML final foi aberto e testado. Se uma verificação não puder ser feita, diga qual.

Na resposta final: onde está a aula (e abra-a), como navegar em uma linha (“Continuar ou →”), o PDF ou vídeo se foram pedidos, e limitações materiais. Ao editar esta skill: valide os scripts e o exemplo, rode `test_player.mjs` e `test_tools.mjs`, e não deixe artefatos de `work/` no repositório.
