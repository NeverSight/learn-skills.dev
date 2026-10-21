---
name: ui-humanizer
description: |
  Remove a "cara de IA" de sites, landing pages, apps, dashboards, docs e slides
  (HTML/CSS, Tailwind, React, shadcn). Use ao criar ou revisar qualquer interface, ou
  quando pedirem design "menos IA", "mais humano", "menos template", "menos SaaS", ou
  pedirem referências visuais (Pinterest, Dribbble, Awwwards). Cobre o processo inteiro:
  brief, rascunho antes do código, busca de referências no navegador, design system,
  construção e auditoria com detector. Pega os tells que a galera reconhece em 2 segundos:
  eyebrow acima do título, palavra do título em gradiente ou em outra cor, card com borda
  lateral, chip com bolinha pulsando, emoji no lugar de ícone, roxo do Tailwind, pill em
  tudo, glassmorphism, "como funciona" em 3 passos, Playfair com itálico no fim, site sem
  imagem, cara de SaaS pra padaria. Baseado nas 51 respostas à thread de @greco_dev (out/2026).
metadata:
  version: "2.0.0"
  source: https://x.com/greco_dev/status/2112133909458960896
---

# UI Humanizer: tirar a cara de IA da interface

## Por que site de IA é reconhecível em 2 segundos

Um modelo escolhe o que é mais provável, então cada decisão visual vira a escolha média: a que serve pra qualquer produto, qualquer público, qualquer seção. Um designer escolhe pra um produto e um público, então as escolhas dele são desiguais e específicas. Todo tell desta skill é uma forma da escolha média, e o que denuncia é a **soma**: eyebrow + título em gradiente + chip pulsando + 3 cards com ícone = template.

Cinco coisas que a thread ensinou e que guiam tudo abaixo:

1. **O elemento não é o problema, o default é.** "Tudo que vão falar, em algum momento foi boa prática de UI" (@marp_sol). Eyebrow num site editorial com motivo tá ok. Eyebrow em toda seção, não.
2. **Trocar clichê por clichê piora.** "Lutar contra isso da IA e tentar tornar mais humano tem o efeito contrário, quase sempre sai um negócio mais óbvio" (@lamarcke_). Tirar o roxo e botar bege + serif é só o outro default (o do `/frontend-design`, citado por @Dan3pm). Toda troca precisa vir do conteúdo, não de "fazer o oposto".
3. **Skill sozinha não salva; processo salva.** "Não tem skill que salve, tu tem que definir primeiro o design system [...] depois dar referências" (@DavidMendonca01). "Pensar no design sem IA, desenhar, pensar de fato em como o site vai ser, fonte, layout, imagens" (@greco_dev). Por isso esta skill é um processo com fases, não só uma lista de proibições.
4. **Humano decide, IA executa.** Quem tem gosto usa a IA como "designer de chão de fábrica" e é a "supervisora" (@gr33d1sg00d_). Nas decisões de direção, mostre opções e deixe o usuário escolher.
5. **Função vem antes.** Pra muita gente "se for performático e servir pra ocasião" não importa (@h1ckzz, @geanjeorge). Nunca piore usabilidade, performance, acessibilidade ou clareza pra parecer menos IA.

## Regra principal

Toda escolha visual precisa de um motivo que venha **deste** produto: conteúdo, público, material real (fotos, dados, produto, pessoas), marca. Se a mesma escolha caberia igual num site de padaria, numa fintech e num SaaS de IA, é default. Troque ou justifique.

**Teste dos 3 segundos** (YC, via @junow0z): quem bate o olho no hero tem que saber o que a empresa faz. Headline abstrata ("Clareza para decidir melhor", "Transforme seu fluxo") falha nisso e ainda entrega a IA.

## Arquivos desta skill

Leia conforme a fase:

| Arquivo | Quando ler |
|---|---|
| `references/tells.md` | Sempre que for construir ou auditar. Catálogo completo: cada tell com como reconhecer, assinatura no código, por que a IA faz, quem citou, troca e quando pode ficar. |
| `references/referencias.md` | Fase 3. Como buscar referências no Pinterest, Dribbble, Awwwards etc. pelo Chrome, o que extrair de cada uma e como virar decisão. |
| `references/copy.md` | Sempre que houver texto na UI. Palavras e estruturas de copy que entregam IA (PT e EN). |
| `references/casos.md` | Pra calibrar o olho. Três sites reais citados na thread, dissecados tell por tell. |
| `references/outros-formatos.md` | Docs, slides, dashboards, apps, e-mails. A mesma assinatura fora da landing page. |
| `references/cobertura.md` | Mapa de cada um dos 51 comentários pra onde ele entrou nesta skill. |
| `references/comentarios.md` | Os comentários originais, verbatim. |
| `scripts/audit.py` | Detector por grep: `python3 -I ~/.claude/skills/ui-humanizer/scripts/audit.py <arquivo-ou-pasta>` |

Se o projeto tem design system próprio (tokens, skill de marca como `rti-ui`, guia do cliente), ele **vence** esta skill. Aqui você só tira o default do que o design system não decidiu.

## O processo

Use todas as fases ao criar do zero. Ao revisar algo existente, vá direto pra fase 6 e volte às fases 1–4 se a auditoria mostrar que o problema é estrutural (cara de SaaS, layout padrão, sem imagem), porque isso não se corrige trocando CSS.

### Fase 0 · Triagem

- O que é: landing, site institucional, e-commerce, app logado, dashboard, doc, deck? Cada um tem convenções próprias que **não** são tells (um app logado pode ter sidebar e cards; um dashboard pode ter grid de KPIs).
- Quanto importa: um protótipo interno não precisa da fase 3 inteira. Um site público de marca precisa.
- O que já existe: design system, marca, fotos, conteúdo, site anterior. Leia antes de propor.

### Fase 1 · Brief (escreva antes de qualquer pixel)

Responda em poucas linhas e mostre ao usuário:

1. **O que é, pra quem, e o que a pessoa faz na página.** Uma padaria não é um SaaS (@eucaioba). Se a resposta não é "assinar software", a estrutura de SaaS está proibida.
2. **O que a pessoa tem que entender em 3 segundos.** Escreva a frase. Ela vira o headline ou a imagem principal.
3. **Material real disponível.** Fotos, prints do produto, dados, rostos, endereço, cardápio, preços, depoimentos verdadeiros. "Ausência de imagens" é dos tells mais citados (@joaquimcassano, @vborotoo). Se não há material, peça ao usuário. Se ainda assim não houver, use placeholders explícitos (`[foto da fachada]`, `[print do painel]`) e avise. Nunca preencha o vazio com cards de ícone, gradiente ou ilustração genérica.
4. **O que não pode faltar e o que é opcional.** Corta excesso de texto e seções de enchimento (@vborotoo).
5. **Restrições.** Marca, cores obrigatórias, acessibilidade, stack, prazo.

### Fase 2 · Rascunho antes do código (o "desenhar sem IA")

Antes de escrever componentes, faça o esqueleto em texto ou wireframe ASCII: quais seções, em que ordem, o que tem em cada uma, qual é **o elemento que só este site tem** (o mapa, a foto gigante do produto, a tabela de preços real, o gráfico dos dados, o cardápio). Construa o layout em volta dele.

Regras do rascunho:
- Ordem e tamanho das seções vêm da importância do conteúdo, não do template hero → logos → features → como funciona → depoimentos → pricing → FAQ → CTA.
- Seções podem ter tamanhos, larguras e alinhamentos diferentes. Nem tudo é centralizado.
- Não é obrigatório ter "como funciona", "por que escolher", grid de features, FAQ, CTA final. Cada seção precisa de um motivo.

Mostre o rascunho ao usuário e ajuste antes de seguir. É o ponto mais barato pra mudar.

### Fase 3 · Referências

Leia `references/referencias.md` e siga. Resumo:
- Peça referências ao usuário primeiro (sites que ele admira, prints, boards do Pinterest). É a melhor fonte.
- Se ele não tiver, busque no navegador: Pinterest (filtro "Menos IA"), Dribbble, Siteinspire, Awwwards, Godly, Land-book, Lapa Ninja, One Page Love, Fonts In Use, sites reais do mesmo setor.
- Junte 6–12, descarte as que têm os tells do catálogo (muita referência hoje já é gerada por IA), e preencha uma ficha por referência: layout, tipografia, cor, imagem, densidade, detalhe memorável.
- Apresente 2–3 direções ao usuário, cada uma com 2–3 referências e o porquê. Ele escolhe.
- Use a referência pela **lógica** (como organiza, como usa a imagem, que tipo de contraste), misturando 2–3. Não copie layout nem marca de ninguém.

### Fase 4 · Design system mínimo

Derivado da direção escolhida, não de defaults:
- **Tipografia:** 1–2 famílias com motivo (da marca, do setor, da referência). Escala com contraste de tamanho de verdade. Nada de "fonte padrão + título minimalista" (@Lukekw_) nem 10 fontes (@El_Sinisttro).
- **Cor:** de onde ela vem (fachada, embalagem, produto, setor, foto principal). Uma cor de acento usada pouco. Sem roxo do Tailwind por default (@Cirilorde), sem gradiente por default, sem cada coisa de uma cor.
- **Forma:** escala de raio pequena e consistente. Pill só onde tem motivo. Uma regra de borda e sombra, não cinco.
- **Ícones:** um set só, ou nenhum. Nunca emoji como ícone.
- **Motion:** liste as poucas animações que existem e o que cada uma explica. O resto é estático.

Escreva como tokens (CSS variables ou config do Tailwind) e aplique nos componentes, inclusive nos de biblioteca (shadcn com tema de fábrica é tell, @metalheadlost).

### Fase 5 · Construção

Construa seguindo o rascunho e o design system, consultando `references/tells.md` e `references/copy.md`. Regras rápidas:

- Nenhum tell da classe A sem justificativa escrita.
- Imagem real no primeiro viewport sempre que existir.
- Hover só em elemento que faz algo (@Fagner_Souza).
- Animação só se explica uma mudança de estado.
- Copy com fato concreto: o que é, pra quem, quanto, onde, com número e nome reais vindos do usuário. Nunca invente cliente, número, depoimento, logo ou prêmio.

### Fase 6 · Auditoria

1. **Detector:** rode `scripts/audit.py` no arquivo ou pasta. Ele acha a assinatura de código dos tells (eyebrow, gradiente em texto, borda lateral, pulse, emoji, roxo, glass, hover, pill, gradiente de fundo, fontes da moda, copy de template). É ponto de partida: confira cada hit, alguns são legítimos.
2. **Visual:** se der, abra a página no Chrome e tire screenshot do topo, do meio e do fim, em desktop e mobile. Vários tells só aparecem renderizados: layout padrão, cards todos iguais, falta de imagem, cara de SaaS, seções com o mesmo ritmo, mockup flutuante.
3. **Catálogo:** passe pelo `references/tells.md` marcando cada tell encontrado, fortes primeiro. A justifica mudança com uma ocorrência; B pesa quando aparece com outros; C só se já houver A ou B.
4. **Copy:** passe pelo `references/copy.md`. Pra parágrafos longos, combine com a skill `humanizer`.
5. **Checklist final** (abaixo).

### Fase 7 · Iteração

- Corrija os tells mudando a decisão por trás, não só a classe CSS. Se a seção inteira é template, refaça a seção.
- Rode o detector de novo e confira se não trocou um clichê por outro (roxo → bege, Inter → Playfair itálico, gradiente → glass, emoji → ícone em quadradinho colorido).
- Em dúvidas de gosto, mostre 2 versões lado a lado e pergunte.

## Checklist final

1. Dá pra saber o que é o negócio em 3 segundos olhando o hero?
2. Tem material real (foto, print, dado, produto) na página, especialmente no topo?
3. A estrutura é do tipo de site certo, ou é SaaS por default?
4. Sobrou algum tell A? Todos os B que ficaram têm motivo?
5. Troquei um clichê por outro?
6. Algum hover, cursor pointer ou animação em elemento que não faz nada?
7. A copy tem algum termo da lista de `copy.md`?
8. Inventei número, cliente, depoimento, logo ou prêmio? Se sim, remova ou marque como placeholder.
9. Piorei usabilidade, contraste, performance ou mobile pra parecer menos IA? Se sim, volte.
10. O usuário viu e aprovou as decisões de direção (rascunho, referências, design system)?

## O que devolver

- **Construindo:** o brief, o rascunho, as direções com referências, o design system, e depois o código. Pare pra aprovação do usuário depois do rascunho e depois das referências, a não ser que ele tenha pedido pra seguir direto.
- **Auditando:** lista dos tells encontrados, fortes primeiro, com `arquivo:linha` ou screenshot, a troca proposta pra cada um e o que fica de propósito com o motivo. Se o usuário pediu só auditoria, não edite.
- **Corrigindo:** as mudanças feitas, o detector antes e depois, e screenshots se possível.
