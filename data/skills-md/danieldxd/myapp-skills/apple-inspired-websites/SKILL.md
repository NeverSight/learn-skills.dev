---
name: apple-inspired-websites
description: Cria sites e landing pages de produto fortemente inspirados no apple.com, com hero centrado, vídeos com scrub no scroll, carrosséis de highlights, seções pin, tabs de features, comparativos e local nav pegajosa. Use quando o usuário pedir site estilo Apple, página de produto premium, landing "like apple.com" ou seções inspiradas em páginas como macbook-pro.
---

# Apple-Inspired Websites

Reproduza a gramática visual e narrativa das páginas de produto da Apple: um produto por página, uma ideia por seção, tipografia gigante e mídia protagonista. O tom é confiante e minimalista; o scroll conta a história.

## Direção de arte

- Fundos alternando branco puro e preto quase puro por seção; sem gradientes decorativos.
- Tipografia sans neo-grotesca (SF Pro ou similar: Inter, Söhne): headlines enormes (clamp até ~96px), tracking levemente negativo, pesos 600–700; corpo cinza (`#86868b` sobre claro, `#a1a1a6` sobre escuro).
- Headlines curtas com "pun" ou afirmação ousada ("Fast runs in the family.", "Pick your quick."), seguidas de um parágrafo denso e específico. Nunca lorem ipsum.
- Cor de destaque única (azul de link/CTA); todo o resto neutro. Produto é a única fonte de cor rica.
- Muito espaço negativo: padding vertical generoso (120–200px desktop), conteúdo centrado com max-width de leitura (~700px para texto).
- Imagens de produto em fundo limpo, grandes, muitas vezes sangrando a viewport.
- Rodapé de footnotes com disclaimers numerados (¹ ² ³) referenciados nos claims.

## Estrutura da página

Ordem canônica, adaptável ao produto:

1. **Local nav** — barra fina pegajosa com nome do produto à esquerda, âncoras/tabs e CTA "Comprar" à direita; ganha fundo translúcido com blur ao scrollar.
2. **Hero** — nome do produto, tagline curta, sub-linha ("Now with…"), CTA, e imagem/vídeo gigante do produto logo abaixo.
3. **Highlights** — "Get the highlights.": carrossel horizontal de cards grandes com mídia + frase, controles de seta e paginação.
4. **Closer look** — galeria interativa (cores, tamanhos, ângulos) com thumbnails/chips que trocam a mídia principal.
5. **Seções de feature** — uma por tema (performance, bateria, display, câmera…), cada uma com eyebrow, headline grande, parágrafo e mídia dominante; alternar claro/escuro.
6. **Comparativos** — barras horizontais animadas ("Up to 8x faster…¹") com baseline nomeada; stats gigantes (número enorme + label pequena).
7. **Tabs/explorador** — categorias (apps, usos) trocando painel de mídia + texto.
8. **Seção de compra/upsell** — cards de vantagens (trade-in, financiamento, educação).
9. **Footnotes** — todos os claims numerados e detalhados.

## Sistema de movimento

Se o projeto pedir estética cinematográfica combinada, aplique também a skill `cinematographic-websites`; em conflito, o estilo Apple vence: movimento discreto, curto e físico.

- Reveals de entrada: fade + translateY pequeno (16–24px), 0.6–0.8s, ease-out; disparados por IntersectionObserver ou ScrollTrigger quando GSAP já existir.
- Números de stats animam contagem quando entram na viewport; barras de comparativo crescem da esquerda.
- Nenhum bounce/elastic; nada gira nem pisca. O movimento serve o produto, não se exibe.
- Respeite `prefers-reduced-motion`: conteúdo visível sem animação, vídeos substituídos por poster.

### Vídeo com scrub no scroll

Padrão assinatura das páginas Apple (produto girando/abrindo conforme o scroll):

- Seção pin (sticky ou ScrollTrigger pin) com o vídeo/canvas fullscreen; a distância de scroll define o progresso.
- Implementações aceitas: sequência de frames em `<canvas>` (mais confiável) ou `video.currentTime` mapeado ao progresso (exige vídeo com keyframes densos).
- Pré-carregue os frames antes de ativar; mostre o primeiro frame estático como fallback.
- Texto sobreposto entra e sai em janelas do progresso, sincronizado com o momento certo da mídia.
- Em mobile e reduced motion: troque por vídeo autoplay curto ou imagem estática.

### Vídeos ambientes

- `autoplay muted loop playsinline` + `poster`; pause fora da viewport (IntersectionObserver).
- Ofereça botão discreto de pausa (acessibilidade) no canto do vídeo, como a Apple faz.
- Nunca reproduza áudio automaticamente.

## Carrosséis

- Scroll horizontal nativo com `scroll-snap-type: x mandatory` e cards com `scroll-snap-align`; setas prev/next que fazem `scrollBy` suave.
- Cards grandes (~70–85vw mobile, 380–480px desktop), border-radius generoso (~28px), mídia cobrindo o card com texto sobreposto ou abaixo.
- Indicadores de paginação (dots) sincronizados com o item visível.
- Acessível: cards focáveis, setas com `aria-label`, navegação por teclado; anuncie posição ("2 de 6").
- Não use bibliotecas pesadas de carrossel se snap nativo resolver.

## Componentes recorrentes

- **Stat gigante**: número em 80–120px + label pequena embaixo ("Up to **24 hours** battery life⁵").
- **Barra comparativa**: label da variante, barra proporcional animada, multiplicador à direita ("6.4x"), baseline marcada.
- **Chips de seleção** (cores/tamanhos): botões redondos ou pills que trocam a mídia com crossfade.
- **Tabs de categoria**: lista horizontal de pills; painel troca com fade rápido (0.3s).
- **Card de highlight**: mídia + uma frase forte; sem excesso de texto.
- **Ribbon promocional**: faixa fina acima do hero para ofertas, dispensável.

## Performance e qualidade

- LCP é o hero: imagem/vídeo prioritário, sem lazy; todo o resto lazy.
- Sequências de frames: WebP/AVIF comprimidos, resolução adaptada ao device; nunca dezenas de MB em mobile.
- Fontes com subset e `font-display: swap`; evite layout shift em headlines.
- Semântica: uma `h1` (nome do produto), seções com headings hierárquicos, footnotes linkadas com `aria-describedby` ou links de âncora.
- Teste em mobile real: carrosséis por toque, pin desativado ou simplificado, textos legíveis sem zoom.

## Anti-padrões

- Poluir com gradientes, glassmorphism, glow e badges — Apple é contenção.
- Headlines longas ou genéricas ("Bem-vindo ao futuro da tecnologia").
- Carrossel automático que gira sozinho sem controle do usuário.
- Scrub de vídeo sem fallback (página quebrada com JS desativado ou em conexão lenta).
- Claims numéricos sem footnote correspondente.
- Misturar mais de uma cor de acento.

## Critérios de conclusão

- Hero com tipografia gigante, produto protagonista e CTA claro.
- Pelo menos um padrão assinatura implementado (scrub no scroll, carrossel de highlights ou comparativo animado) conforme o pedido.
- Seções alternando claro/escuro com uma ideia cada.
- Carrosséis navegáveis por toque, setas e teclado.
- Reduced motion e mobile verificados.
- Footnotes presentes para todo claim quantitativo.
- Resultado inspecionado visualmente em desktop e mobile.
