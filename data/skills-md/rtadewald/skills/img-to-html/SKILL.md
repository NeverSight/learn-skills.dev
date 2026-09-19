---
name: img-to-html
description: >-
  Recria um mock de UI (imagem) como HTML + CSS + JS estáticos (sem framework),
  em etapas com aprovação do usuário: wireframe ASCII tipado com plano → fundo
  completo → componentes com fontes → assets restantes → revisão final. Use when the user
  mentions img-to-html or asks to recreate a UI mock as HTML.
disable-model-invocation: true
---

# Img → HTML

## O que é

Skill para transformar um **mock de interface** (PNG/JPG/WebP) numa **recriação HTML** fiel, passo a passo.

**Entrada:** uma imagem de referência (anexada no chat, path, ou URL). Se faltar, peça.

**Saída:** pasta `design-systems/<slug>/` com a referência copiada, o wireframe, o **`index.html`** e uma pasta **`assets/`** com o CSS, o JS e as mídias geradas.

O entrypoint final deve se chamar exatamente **`index.html`**. Não use outro nome para o HTML principal.

`<slug>` = nome curto do mock em kebab-case (ex.: `chatgpt-glass-dash`). Se o usuário não indicar, derive do nome do arquivo ou pergunte.

## Por que em etapas

Recriar a tela inteira de uma vez falha (cores, glass, ícones e fontes misturam erros). O fluxo é **bottom-up**: cada camada só começa depois da anterior **aprovada** pelo usuário. O wireframe define *o que* existe e seu plano indica *quando* e *como* implementar cada região. Assets entram conforme sua função: imagens que compõem o fundo são feitas junto dele.

## Pipeline

```
1. reference → $to-wireframe format=ascii → wireframe.txt + plano → [usuário aprova ambos]
2. fundo completo (CSS e/ou imagens)       → [usuário aprova]
3. estrutura e componentes + fontes       → [usuário aprova]
4. assets restantes (ícones, imagens etc.) → [usuário aprova, se houver]
5. revisão final integrada                → [usuário aprova]
```

## Gate de aprovação (vale para todas as etapas)

Ao terminar uma etapa:

1. Mostre o resultado (path + `open` no macOS e/ou screenshot no browser).
2. Pergunte se está correto / se mudaria algo.
3. **Pare.** Não inicie a etapa seguinte.

Só avance com confirmação explícita ("aprovado", "pode seguir", "ok"). Se o usuário pedir correção: edite, mostre de novo, aguarde nova aprovação.

A aprovação do plano autoriza a sequência proposta, sem substituir os gates de implementação. Se não houver assets restantes, indique isso no plano e omita a etapa 4; depois da aprovação da etapa 3, siga para a revisão final.

## Layout da pasta

```
design-systems/<slug>/
  reference.[ext]      # cópia da imagem de entrada
  wireframe.txt        # planta tipada criada por $to-wireframe format=ascii; plano apresentado junto
  index.html           # markup — só estrutura, sem <style>/<script> inline
  assets/
    styles.css         # todo o CSS
    app.js             # todo o JS (só se o mock precisar de comportamento)
    crops/             # recortes da reference
    *.png / *.mp4 …    # imagens, ícones, vídeos gerados
```

### Stack: HTML + CSS + JS separados

**Sem build, sem bundler, sem framework, sem `node_modules`, sem dev server** — abre com `open index.html` e funciona.

- `index.html` carrega os outros dois: `<link rel="stylesheet" href="assets/styles.css">` no `<head>` e `<script src="assets/app.js" defer></script>`.
- **Nada de `<style>` ou `<script>` inline** no HTML, e nada de `style="…"` nos elementos. Todo CSS vive em `assets/styles.css`.
- Um `styles.css` só. Se ele passar de ~1500 linhas, aí sim quebre por região (`assets/nav.css`, `assets/cards.css`) e adicione os `<link>` correspondentes — mas o default é um arquivo.
- `assets/` é a única pasta auxiliar: CSS, JS, imagens, ícones, vídeos e os crops moram todos lá.
- Sem Tailwind, sem CDN de framework. CSS puro, com **custom properties** no `:root` para o design system (cores, radius, sombras, tipografia).
- Cada região do wireframe vira uma **classe CSS** (`.nav`, `.hero`, `.card`, `.card2`, …) e cada tag tipada vira uma classe utilitária (`.h1`, `.t2`, `.btn`, `.lnk`, …). Mesmo id no wireframe = mesma classe.
- Conteúdo repetido (lista de cards, itens de nav) é escrito direto no HTML. Só crie `app.js` se o mock exigir comportamento real; não gere markup por loop de JS.
- Paths sempre relativos: `assets/{id}.png`.

Se o usuário pedir React/Vite explicitamente, aí sim mude a stack.

---

## Etapa 1 — Wireframe ASCII tipado + plano

Objetivo: a **planta estrutural** da tela — quais regiões existem e que texto tem dentro delas — acompanhada de um plano curto de implementação por região.

O wireframe é o **contrato** com o HTML: cada região e cada tag tipada vira depois uma **classe CSS** (mesmo id = mesmo visual). A criação, o vocabulário tipado, o aninhamento e a revisão estrutural pertencem exclusivamente a [`$to-wireframe`](../to-wireframe/SKILL.md). Não replique essas regras nesta skill.

### Criar o wireframe

1. Criar `design-systems/<slug>/` e copiar a imagem para `reference.[ext]`.
2. Invocar a skill **`$to-wireframe`** com `format=ascii`, `image=design-systems/<slug>/reference.[ext]` e `output=design-systems/<slug>/wireframe.txt`.
3. Manter `wireframe.txt` como o contrato canônico desta execução. Não gerar SVG nesta etapa.
4. Não alterar o wireframe depois da entrega do `$to-wireframe`; qualquer correção estrutural volta para `$to-wireframe` com a mesma imagem e `format=ascii`.

### Plano de implementação (na mesma aprovação)

Depois de receber o ASCII do `$to-wireframe`, indique para cada região **a etapa de implementação e a técnica prevista**. Agrupe regiões iguais. Apresente o plano na mensagem, em uma tabela curta. Ele não é adicionado ao ASCII: etapas e técnicas não fazem parte dos ids/classes nem do texto da interface.

Exemplo de plano (adaptar à referência):

| Região / elemento | Etapa | Técnica prevista |
|-------------------|-------|------------------|
| Fundo da tela + arte decorativa | 2 | Gradiente CSS + ilustração transparente |
| Nav, hero e cards | 3 | HTML/CSS; família e peso definidos antes do ajuste fino |
| Fundo ilustrado de um card | 3 | Imagem + CSS, junto da superfície do card |
| Área de mídia | 3 / 4 | Estrutura na 3; imagem de conteúdo na 4 |
| Ícones e avatares | 4 | Assets gerados a partir dos recortes |
| Tela completa | 5 | Comparação integrada e correções finais |

Escolha visualmente entre **CSS, imagem ou composição dos dois**, considerando fidelidade, esforço e facilidade de ajustar posição/escala. Cores, gradientes e formas simples favorecem CSS; arte e texturas complexas favorecem imagem; camadas separadas ajudam quando precisam de ajustes independentes. Uma imagem de fundo única também é válida quando reproduz melhor a composição. Preserve textos e controles como HTML.

Classifique imagens pela **função**, não pelo formato: fundo da tela → etapa 2; fundo de componente → etapa 3; imagem de conteúdo, ícone ou avatar → etapa 4. Nenhuma superfície deve ser aprovada com parte essencial do seu fundo ainda pendente. Planejar esses assets na etapa 1 não significa recortá-los ou gerá-los ali.

Faça somente a revisão do plano: ele cobre todas as regiões do wireframe e distingue assets de fundo dos assets restantes? Depois mostre `wireframe.txt` junto do plano e aplique o **gate único para estrutura + sequência/técnicas propostas**.

---

## Etapa 2 — Fundo completo (CSS e/ou imagens)

Pré-requisito: wireframe e plano aprovados.

1. Criar `index.html` (esqueleto mínimo com o `<link>` para `assets/styles.css` e `<body>` vazio) e `assets/styles.css` (reset curto + `:root` com as custom properties que já der para definir).
2. Recriar o fundo completo com a técnica escolhida no plano: CSS, imagem única ou composição de camadas. Produzir agora as imagens necessárias, usando o procedimento de assets abaixo; não deixá-las para a etapa 4. Quando houver várias camadas independentes, gere-as no mesmo lote paralelo e só componha o fundo depois que todas terminarem.
3. Sem navbar, cards ou conteúdo. O `<body>` pode receber elementos decorativos quando necessários para compor o fundo; também podem ser usados backgrounds CSS e pseudo-elementos.
4. Ajustar posição, escala, recorte, transparência e mistura entre camadas. Abrir o arquivo no browser (`open index.html`) e comparar o fundo composto com a referência.
5. **Gate.**

---

## Etapa 3 — Estrutura e componentes + fontes

Aqui entram a estrutura e os textos do wireframe (markup no `index.html`, estilo no `assets/styles.css`): primeiro o chrome (`nav` — top bar e/ou sidebar), depois cada tipo de card (`card`, `card2`, …) e as demais regiões. Imagens que compõem o fundo de um componente entram junto dele; as independentes usam o mesmo lote paralelo do procedimento de assets. Um gate só, no fim.

### Fontes antes do ajuste fino

1. Para cada tipo de tag distinto (`h1`…`t3`, `btn`, `lnk`, …), identificar **família + peso**. Se a skill/API local `find-font` estiver disponível, usar crop de uma linha com `text=` case-sensitive; caso contrário, escolher por julgamento visual a Google Font mais próxima e informar a aproximação.
2. Aplicar o `<link>` do Google Fonts no `index.html` ou `@font-face` no `styles.css`, com `font-family` / `font-weight` nas classes correspondentes. Mesmo id de tag = mesma tipografia.
3. Confirmar o carregamento das fontes antes de ajustar quebras de linha, dimensões e espaçamentos. Não adiar a escolha da família/peso para a revisão final.

Meta: cada superfície **indistinguível** da referência. Iterar medindo, não chutando:

- cores (eyedropper / sample de pixels na `reference`)
- gradientes (ângulo + stops)
- transparência (glass vs opaco)
- bordas / rim light (direção, soft vs hairline)
- glow / sombra externa e inset
- radius, padding, espaçamento entre elementos
- tipografia já aplicada (família/peso, tamanho, altura de linha e espaçamento)

Fluxo por superfície (nav primeiro, depois card a card):

1. Crop da referência (ou lab side-by-side no browser).
2. Amostrar pixels (fill, rim TL/BR, texto, meta).
3. Escrever o markup no `index.html` e a classe em `assets/styles.css`; valores reutilizados viram custom property no `:root`.
4. Screenshot recreate vs crop; ajustar até bater.

Somente os assets atribuídos à etapa 4 continuam como placeholders, com dimensões reservadas. Fundos e fontes dos componentes já devem estar completos. Com as regiões implementadas e comparadas → **gate**.

---

## Etapa 4 — Assets restantes

Implementar os `[ico:]` / `[img:]` / `[av:]` e demais assets que o plano deixou para esta etapa. Reutilizar os assets de fundo já aprovados; não regenerá-los apenas para cumprir esta etapa. Preparar todos os recortes da etapa e gerar os assets independentes em paralelo pelo procedimento abaixo; depois comparar o conjunto e apresentar o **gate**. Se não houver pendências, omitir esta etapa conforme o plano.

### Procedimento de assets (usado nas etapas 2, 3 e 4)

1. Fazer todos os crops necessários na `reference` → `assets/crops/{id}.png` antes de iniciar qualquer geração.
2. Separar os requests em lotes: assets sem dependência entre si e com arquivos de destino distintos pertencem ao mesmo lote. Um asset que depende de uma imagem recém-gerada, ou de uma composição ainda não aprovada, fica no lote seguinte.
3. Regenerar cada lote com **GPT Image 2** via OpenRouter (`gpt2`) em paralelo. Para ícones ou camadas recortadas, pedir PNG com **fundo transparente**; para um fundo completo, preservar o fundo necessário. Adaptar o prompt à arte (foto, textura, 3D etc.); não impor estilo flat a todo asset. Inicie cada comando em segundo plano e execute `wait` antes de encaixar qualquer resultado. Exemplo para dois ícones independentes:

```bash
uv run ~/.agents/skills/openrouter-img/scripts/generate_image.py \
  --prompt "Recreate this UI icon/asset exactly. Flat, clean edges. Transparent background. No extra padding, no mockup frame." \
  --input-image design-systems/<slug>/assets/crops/{id}.png \
  --filename design-systems/<slug>/assets/{id}.png \
  --model gpt2 --resolution 1K --aspect-ratio 1:1 &

uv run ~/.agents/skills/openrouter-img/scripts/generate_image.py \
  --prompt "Recreate this UI icon/asset exactly. Flat, clean edges. Transparent background. No extra padding, no mockup frame." \
  --input-image design-systems/<slug>/assets/crops/{id-2}.png \
  --filename design-systems/<slug>/assets/{id-2}.png \
  --model gpt2 --resolution 1K --aspect-ratio 1:1 &

wait
```

Rodar a partir do cwd do repo de skills (ou paths absolutos). Para um único asset, rode o mesmo comando sem `&` e sem `wait`. Ajustar `--aspect-ratio` ao crop ou à camada de destino. Ao gerar um fundo a partir do mock, pedir apenas a arte de fundo, sem reproduzir textos, cards ou controles sobrepostos. Requer `OPENROUTER_API_KEY` (`.env` do projeto ou `~/.env`).

4. Depois do `wait`, encaixar cada resultado no HTML via `<img src="assets/{id}.png">` (ou `background-image`) e comparar com a ref.
5. Se algum falhou: preparar somente os assets afetados para um novo lote, com prompt ajustado; não regenerar os que já passaram.
6. Avaliar os assets na composição da etapa que os utiliza; o gate é o dessa etapa, sem uma aprovação extra por arquivo.

---

## Etapa 5 — Revisão final integrada

1. Comparar uma screenshot da tela completa com a referência, no mesmo viewport, com fontes e assets carregados.
2. Conferir a cobertura do wireframe/plano e corrigir diferenças de integração: sobreposição de camadas, recortes, alinhamentos, quebras de linha e espaçamentos após a entrada dos assets.
3. Verificar paths relativos e os comportamentos implementados, se houver. Informar aproximações ou pendências reais.
4. Mostrar a tela completa e os arquivos finais → **Gate.** Esta etapa consolida o resultado; fontes e fundos já foram implementados nas etapas anteriores.

---

## Não fazer

- Pular gates ou "adiantar" várias etapas num único turno.
- Na etapa 1: medir, croppar, fazer OCR, desenhar arte, ou refinar o wireframe além da revisão única.
- Adiar imagens essenciais de fundo para a etapa 4, ou deixar a escolha de fontes para a revisão final.
- Inventar textos ilegíveis no wireframe.
- Desenhar caixa de componente sem label de região, ou achatar cards-filho em texto solto dentro do pai.
- Marcar nav ativo como `[lnk:]` (use `[btn:]` / variante).
- Tratar ícones/imagens com Lucide/placeholder "parecido" quando o plano pede asset gerado da ref.
- Escrever CSS inline (`<style>` no HTML ou `style="…"` no elemento) — todo estilo vai para `assets/styles.css`.
- Criar `package.json`, bundler, framework ou espalhar arquivos fora de `assets/`.
