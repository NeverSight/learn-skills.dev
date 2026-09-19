---
name: to-wireframe
description: >-
  Cria um wireframe tipado e aninhado de uma imagem ou brief de tela, em ASCII
  ou SVG conforme format=ascii|svg informado pelo usuário. Use when the user
  mentions to-wireframe or asks for a typed UI wireframe.
disable-model-invocation: true
---

# To Wireframe

Crie um wireframe tipado que descreve estrutura, componentes e conteúdo visível de uma tela. Use como referência canônica de densidade e marcação [`references/wireframe.example.svg`](references/wireframe.example.svg).

## Chamada obrigatória

O usuário deve informar o formato em toda chamada: `format=svg` ou `format=ascii`. Se faltar, pergunte qual formato quer; não escolha um padrão.

Também aceite uma única fonte:

- `image=<path>` ou imagem anexada: extraia a estrutura da tela existente;
- `brief=<descrição da tela>`: construa a planta a partir do briefing, proposta ou especificação recebida.

`output=<path>` é opcional para imagem e obrigatório para brief. Quando a entrada for uma imagem e não houver `output`, salve ao lado dela:

```text
image=mocks/dashboard.png format=svg    → mocks/dashboard.wireframe.svg
image=mocks/dashboard.png format=ascii  → mocks/dashboard.wireframe.txt
```

Exemplos de chamada:

```text
Use $to-wireframe: format=svg image=mocks/dashboard.png
Use $to-wireframe: format=ascii image=mocks/dashboard.png
Use $to-wireframe: format=svg brief="Dashboard de projetos com sidebar, KPIs e atividade" output=mocks/12-wire-a.svg
```

Mostre o path resultante. Abra SVG quando fizer sentido. A skill termina ao entregar o wireframe: não implemente HTML/CSS, assets, imagem final, plano de etapas ou gates de aprovação.

## O que o wireframe representa

O wireframe é uma planta estrutural, não uma recriação visual pixel-perfect. Cada superfície ou componente com estilo próprio recebe uma região com label: `nav`, `hero`, `media`, `card`, `card2`, `card3`, `form`, `rail`, `quote` ou `section`.

- Mesmo visual usa o mesmo id; uma variação visual recebe o próximo id (`card`, `card2`, `card3`).
- Regiões aninham quando a tela mostra uma superfície própria dentro de outra, como cards de lista, tooltip flutuante, dock de controles ou painel de gráfico.
- Toda caixa desenhada precisa de label. Não achate um componente em texto solto no pai.

## Tags tipadas

Todo texto e controle visível entra em uma tag; não deixe conteúdo solto. Use este vocabulário fechado:

| Tag | Uso |
|---|---|
| `[h1:]`, `[h2:]`, `[h3:]` | Títulos |
| `[t1:]`, `[t2:]`, `[t3:]` | Corpo, meta e microtexto |
| `[btn:]`, `[btn2:]`, `[btn3:]` | Botões com estilos distintos |
| `[lnk:]` | Link de navegação inativo |
| `[in:]` | Placeholder ou texto de input |
| `[ico:]` | Ícone |
| `[img:]` | Imagem, raster ou 3D |
| `[av:]` | Avatar |
| `[chart:]` | Gráfico |

Um mesmo id de tag representa o mesmo estilo. Botões visualmente diferentes usam ids diferentes. Nav ativo é `[btn:]`; nav inativo é `[lnk:]`. Um botão com ícone pode ser `[btn: [ico:plus] Add project]`. Escreva uma tag por linha visual: uma headline em três linhas vira três tags `[h1:]`.

Na entrada por imagem, use o texto essencial que estiver legível. Quando não der para ler com segurança, escreva a tag apropriada com `...`; não invente texto. Na entrada por brief, use somente conteúdo que o briefing fornece ou que seja necessário para explicar a função declarada da tela.

## Processo

1. Leia a imagem ou o brief e defina as regiões, seus estados e o conteúdo tipado.
2. Em uma passada, desenhe a planta no formato pedido.
3. Faça uma única revisão: toda superfície está rotulada; todo texto está em tag; componentes internos estão aninhados; e nav ativo/inativo está tipado corretamente.
4. Grave no `output` definido ou no caminho padrão da imagem.

Não meça pixels, faça OCR, crop, eyedropper ou simule a aparência final. Estime posições e tamanhos quando vier de imagem; quando vier de brief, priorize a hierarquia descrita.

## Renderização SVG

Para `format=svg`:

- Comece com `<?xml version="1.0" encoding="UTF-8"?>`.
- Use `viewBox` proporcional ao canvas da imagem; para brief sem proporção definida, use `0 0 1440 810`.
- Desenhe somente `rect` e `text`, em cinza, com strokes e labels simples.
- Não use cores de produto, tipografia premium, sombras, gradientes, curvas, ícones ou gráficos simulados.
- Use labels com letras e números básicos para evitar XML inválido.

## Renderização ASCII

Para `format=ascii`:

- Use somente `+`, `-` e `|` como bordas, para funcionar em qualquer terminal.
- Coloque o label de cada região na primeira linha de sua caixa e mantenha as tags tipadas dentro dela.
- Represente regiões aninhadas com caixas aninhadas e reserve espaço visual entre colunas e seções.
- Não use cores, sombras, gradientes, ícones desenhados, gráficos simulados ou medidas pixel-perfect.

```text
+------------------------------------------------------------------------+
| nav                                                                    |
| [ico:logo] [t1: Orbit]          [lnk: Explore] [btn: [av:] Profile]  |
+------------------------------------------------------------------------+
| hero                                                                   |
| [h1: Build your next project]                                          |
| [t2: Keep the team aligned from one place]          [btn2: Create]    |
+-----------------------------------+  +---------------------------------+
| card                              |  | card2                           |
| [h2: 24] [t2: Open projects]      |  | [h3: Activity]                  |
| [chart: sparkline]                |  | +-----------------------------+ |
|                                   |  | | card3                       | |
|                                   |  | | [av:] [t1: New comment]    | |
+-----------------------------------+  | +-----------------------------+ |
                                       +---------------------------------+
```
