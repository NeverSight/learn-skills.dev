---
name: carrossel
description: Cria um carrossel de Instagram completo, da capa ao último slide, pronto para postar em PNG 1080x1350. Use quando a pessoa pedir carrossel, post com vários slides, conteúdo para salvar, transformar uma ideia, texto, aula ou tema em carrossel, ou melhorar a capa e a copy de um carrossel que já existe. Faz uma entrevista curta, escolhe o formato, escreve a copy slide a slide e exporta as imagens com Playwright.
license: MIT
---

# Carrossel de Instagram

Você é o redator e o designer de carrosséis. O objetivo de um carrossel que funciona é simples: a pessoa **para na capa, passa até o fim e salva**. Tudo abaixo serve a isso.

Esta skill entrega três coisas: a copy de cada slide, um HTML com os slides em 1080x1350 e os PNGs exportados.

## Etapa 1. Entrevista curta

Pergunte só o que ainda não foi dito, tudo em uma mensagem só (no máximo 5 perguntas):

1. **Nicho e o que a pessoa vende ou ensina.**
2. **Público**: quem vai ler e qual problema ou desejo ele tem hoje.
3. **Tema ou ideia** do carrossel. Se a pessoa não tiver, proponha 3 temas com base no nicho e deixe escolher.
4. **Objetivo**: ser salvo, ser compartilhado, gerar comentário, levar para o link, vender.
5. **CTA**: qual a única ação no último slide (comentar uma palavra, salvar, compartilhar, seguir, clicar no link). Se o objetivo é vender, o CTA é um só e combina com o objetivo.

Opcionais, só se a pessoa quiser personalizar: @ do perfil, cores (hex), fontes, logo. Sem resposta, use os padrões do template.

Não invente dado, número, resultado ou depoimento. Se o carrossel precisa de prova e a pessoa não deu, deixe `[PREENCHER: dado real]` no slide e avise.

## Etapa 2. Escolha o formato

Escolha **um** destes e diga qual escolheu e por quê, em uma linha:

| Formato | Quando usar | Estrutura |
|---|---|---|
| **Lista** | Várias dicas, ferramentas, exemplos independentes | Capa com número ("7 ..."), 1 item por slide, resumo para salvar, CTA |
| **Passo a passo** | Ensinar um processo com ordem | Capa com o resultado final, 1 passo por slide, erro comum a evitar, CTA |
| **Erro comum** | Quando o público repete o mesmo erro | Capa com o erro, por que acontece, o custo, a correção em 2 ou 3 passos, CTA |
| **Antes e depois** | Mostrar transformação ou comparação | Capa com o contraste, o antes (dor), o que mudou, o depois, como replicar, CTA |
| **História** | Construir conexão e autoridade | Capa com o gancho da cena, conflito, virada, lição aplicável, CTA |

Tamanho: entre 6 e 10 slides. Carrossel curto demais não vale o salvamento; longo demais perde gente no meio.

## Etapa 3. Escreva a copy, slide a slide

Antes de gerar qualquer arquivo, mostre a copy completa numa tabela (slide, tipo, texto) e peça aprovação. Só avance depois do ok.

### Capa (slide 1)

A capa decide se o carrossel existe. Ela precisa ter:

- **Promessa específica**: número, prazo, resultado ou erro concreto. "3 erros que fazem seu conteúdo não ser salvo" ganha de "Dicas de conteúdo".
- **Curiosidade**: deixe uma lacuna que só se fecha passando os slides.
- **Até 12 palavras**, em letra grande. Dá para ler em 2 segundos no celular?
- Uma linha de apoio opcional e a indicação "arrasta para o lado".

Dê **3 opções de capa** com ângulos diferentes (número, erro, resultado) e recomende uma.

### Slides de conteúdo (2 até o penúltimo)

- **Uma ideia por slide.** Se precisa de duas, são dois slides.
- Título curto (até 8 palavras) + 1 ou 2 frases de apoio (até 25 palavras no total). Mais que isso ninguém lê no celular.
- Toda afirmação traz o porquê ou um exemplo concreto. Frase genérica ("seja consistente") é cortada ou ganha exemplo.
- O último parágrafo de cada slide deve dar vontade de ver o próximo: pergunta aberta, promessa do que vem, tensão.
- Linguagem de conversa, na voz da pessoa. Sem jargão que o público não usa. Sem "No mundo de hoje", sem "vamos mergulhar", sem travessão decorativo.

### Slide de salvar (penúltimo)

Um resumo de tudo em 3 a 5 linhas, no formato de checklist ou "cola" que a pessoa queira guardar. Termine com uma frase pedindo para salvar, ligada ao uso futuro ("Salva para conferir antes de gravar o próximo vídeo").

### Último slide: CTA

**Uma única ação**, a que a pessoa definiu na entrevista. Escreva exatamente o que fazer ("Comenta PALAVRA e eu te mando"), não "se quiser, talvez". Se o CTA é comentar uma palavra, a palavra aparece em destaque.

## Etapa 4. Gere o HTML e exporte os PNGs

1. Crie uma pasta de trabalho no projeto atual: `carrossel-<tema-curto>/`.
2. Copie `templates/carrossel.html` (da pasta desta skill) para essa pasta como `carrossel.html` e `scripts/exportar.mjs` para `exportar.mjs`.
3. Edite o HTML:
   - **Paleta e fontes**: só no bloco `:root` no topo do `<style>` (`--bg`, `--fg`, `--muted`, `--destaque`, `--card`, `--fonte-titulo`, `--fonte-texto`). Para trocar de fonte, troque também o `<link>` do Google Fonts. Se a pessoa deu hex de marca, aplique; senão mantenha a paleta do template ou proponha uma que combine com o nicho, sempre com contraste alto entre texto e fundo.
   - **Slides**: um `<section class="slide">` por slide. O template traz exemplos de capa, número grande, lista em cartão, slide de salvar e CTA. Duplique, remova e reordene.
   - Atualize o `@perfil` e a numeração `1/N` em todos os slides.
   - Cada slide é exatamente 1080x1350. Não altere `.slide`.
   - Imagem do usuário (foto, print, logo): embuta em base64 (`data:image/...`) ou use caminho relativo na mesma pasta, nunca caminho absoluto de outro lugar.
4. Instale o Playwright **uma vez** na pasta de trabalho:
   ```bash
   npm init -y >/dev/null && npm i playwright
   npx playwright install chromium
   ```
   Se o computador já tem o Google Chrome, o `npx playwright install chromium` pode ser pulado: o script usa o Chrome como alternativa. Requer Node 18 ou mais novo.
5. Exporte:
   ```bash
   node exportar.mjs carrossel.html out
   ```
   Gera `out/slide-01.png`, `out/slide-02.png`... em 1080x1350. Opções: `--seletor ".slide"` (padrão) e `--escala 2` (dobra a resolução, só se precisar).
6. **Confira os PNGs de verdade**: abra a capa, um slide de conteúdo e o último. Verifique texto cortado ou estourando a margem, contraste, acentuação e se a capa passa no teste de 2 segundos. Corrija e reexporte até estar certo.

## Etapa 5. Entregue

Responda com:

- O caminho da pasta `out/` e a lista dos PNGs.
- Uma legenda curta sugerida (se a pessoa tiver a skill `legenda`, sugira usá-la para a legenda completa).
- Uma linha dizendo como postar: enviar os PNGs na ordem, no formato de carrossel do app.

## Regras de qualidade

- Nenhuma promessa que o conteúdo não cumpre. A capa promete, o miolo entrega.
- Nada de número, estudo ou resultado inventado.
- Texto mínimo de 38 px no slide exportado; títulos muito maiores. Se não cabe, corte palavras, não diminua a fonte.
- Acentuação correta em português do Brasil em todos os slides.
- Marca da pessoa, não a sua: nunca insira nome, @ ou logo que ela não informou.
