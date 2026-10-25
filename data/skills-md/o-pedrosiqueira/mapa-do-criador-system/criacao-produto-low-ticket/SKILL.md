---
name: criacao-produto-low-ticket
description: >
  Base de conhecimento para criação do conteúdo real de produtos digitais de entrada (low ticket).
  Cobre 6 formatos: e-book, checklist, mini-curso, desafio, agente GPT e planilha.
  Acionada automaticamente pelo agente estrategista-low-ticket na Etapa 2.
---

# Criação de Produto Low Ticket. Base de Conhecimento

## Regras Gerais (válidas para todos os formatos)

1. **Propor estrutura antes de gerar conteúdo.** Sempre apresente o esqueleto do produto (sumário, abas, dias, módulos) e peça aprovação antes de escrever qualquer conteúdo.
2. **Gerar em blocos, confirmar entre eles.** Para produtos extensos (e-book, mini-curso, desafio), gere e mostre um bloco de cada vez (capítulo, aula, dia) e pergunte antes de continuar.
3. **Nunca mostrar código HTML ao aluno.** Salve silenciosamente e informe apenas o caminho do arquivo.
4. **Só salvar após aprovação final.** Sempre mostrar o conteúdo e perguntar:
   ```
   1. Aprovar e salvar
   2. Quero ajustar algo
   ```
5. **Usar dados do perfil.** Quadro, Furadeira e Urgências Ocultas do `perfil.md` devem guiar o conteúdo gerado. não inventar do zero.
6. **Tom de escrita:** claro, direto, acessível. Mesmo padrão Light Copy do restante do sistema.

---

## Formato 1. E-book / Guia (PDF passo a passo)

**Objetivo:** documento completo que o aluno lê e aplica imediatamente.

### Fluxo

**Passo 1. Sumário**

Com base no Quadro e na Furadeira, proponha:
- Título principal e subtítulo do e-book
- Lista de capítulos (4 a 8), cada um com 1 frase descrevendo o que o leitor aprende/faz nele
- Estimativa de páginas

Mostre e pergunte:
```
1. Aprovar sumário e gerar o conteúdo
2. Quero ajustar o sumário
```

**Passo 2. Conteúdo por capítulo**

Para cada capítulo, gere:
- Título do capítulo
- Introdução (2-3 parágrafos contextualizando o problema que o capítulo resolve)
- Corpo (passo a passo, conceito explicado ou exercício prático)
- Recapitulação em bullets (3-5 pontos)
- Micro CTA de transição para o próximo capítulo

Mostre cada capítulo individualmente e pergunte:
```
1. Aprovar e continuar para o próximo capítulo
2. Quero ajustar algo neste capítulo
```

**Passo 3. Geração do arquivo**

Após todos os capítulos aprovados, gere um HTML com:
- Capa com título, subtítulo e campo "[Seu nome/logo aqui]"
- Sumário com âncoras clicáveis para cada capítulo
- Tipografia otimizada para leitura (fonte sans-serif 16-18px, linha 1.7, margens generosas)
- Rodapé com instruções: "Para salvar como PDF: Ctrl+P → Salvar como PDF → Layout: Retrato"
- Design limpo e profissional (sem excesso de cor, foco em legibilidade)

**Onde salvar:** `entregas/{ativo}/produto/ebook-[slug-produto].html`

---

## Formato 2. Checklist / Roteiro de autoaplicação

**Objetivo:** ferramenta que o aluno usa enquanto executa. não lê depois, usa agora.

### Fluxo

**Passo 1. Estrutura**

Proponha:
- Título do checklist e objetivo em 1 frase
- Número de seções (2 a 5) com nome e quantidade de itens por seção
- Tipo de uso: linear (sequência obrigatória) ou modular (pode usar qualquer seção)

Mostre e pergunte:
```
1. Aprovar estrutura e gerar o checklist
2. Quero ajustar a estrutura
```

**Passo 2. Conteúdo completo**

Gere todos os itens do checklist. Cada item deve ser:
- Escrito como ação concreta no imperativo ("Confirme se...", "Anote o valor de...", "Verifique se...")
- Acompanhado de instrução curta quando o item for ambíguo
- Agrupado por seção com título destacado

**Passo 3. Geração do arquivo**

Gere HTML com:
- Caixas de checagem visíveis (estilo checkbox com CSS)
- Cabeçalho com título, nome do produto e campo "[Seu logo aqui]"
- Seções separadas visualmente
- Instruções de uso no topo ("Como usar este checklist...")
- Layout otimizado para impressão A4 e uso em tela

**Onde salvar:** `entregas/{ativo}/produto/checklist-[slug-produto].html`

---

## Formato 3. Mini-curso (roteiros de aulas)

**Objetivo:** sequência de 3 a 5 aulas curtas (5-15 min cada) que ensinam o método passo a passo.

### Fluxo

**Passo 1. Estrutura do mini-curso**

Proponha:
- Nome do mini-curso
- Número de módulos/aulas (3 a 5)
- Para cada aula: título, objetivo em 1 frase, duração estimada

Mostre e pergunte:
```
1. Aprovar estrutura e gerar os roteiros
2. Quero ajustar a estrutura
```

**Passo 2. Roteiro por aula**

Para cada aula, gere roteiro com:
- **Abertura (30 seg):** o que o aluno vai aprender nesta aula e por que importa
- **Conteúdo principal (blocos):** 2-4 blocos de ensino com explicação + exemplo prático
- **Exercício ou ação prática:** o que o aluno deve fazer após a aula
- **Encerramento (30 seg):** resumo da aula + gancho para a próxima

Mostre roteiro por roteiro. Pergunte entre cada um:
```
1. Aprovar e continuar para a próxima aula
2. Quero ajustar algo neste roteiro
```

**Passo 3. Material de apoio (opcional)**

Após todos os roteiros aprovados, pergunte:
```
Quer que eu gere um material de apoio para o aluno (slides ou apostila resumo)?

1. Sim, gerar material de apoio
2. Não, só os roteiros já bastam
```

Se sim: gere HTML com slides/apostila simples. tópicos de cada aula, espaço para anotações, design clean.

**Onde salvar:**
- Roteiros: `entregas/{ativo}/produto/roteiros-[slug-produto].md`
- Material de apoio (se gerado): `entregas/{ativo}/produto/material-apoio-[slug-produto].html`

---

## Formato 4. Desafio (5 a 7 dias)

**Objetivo:** experiência guiada dia a dia que leva o aluno a um resultado tangível ao final.

### Fluxo

**Passo 1. Estrutura do desafio**

Proponha:
- Nome do desafio
- Duração (5, 6 ou 7 dias)
- Para cada dia: título do dia, tarefa principal e resultado esperado ao final do dia
- Resultado final ao terminar o desafio completo (deve ser o Quadro ou um degrau claro para ele)

Mostre e pergunte:
```
1. Aprovar estrutura e gerar o conteúdo dos dias
2. Quero ajustar a estrutura
```

**Passo 2. Conteúdo por dia**

Para cada dia, gere:
- **Mensagem de boas-vindas do dia** (motivacional, contextualiza o que vem pela frente. 1 parágrafo)
- **Instrução da tarefa** (passo a passo detalhado do que fazer)
- **Dica do dia** (insight prático que facilita a execução)
- **Entregável esperado** (o que o aluno deve ter feito/produzido ao fim do dia)
- **Gancho para o próximo dia** (1 frase que gera antecipação)

Mostre dia a dia e pergunte:
```
1. Aprovar e continuar para o próximo dia
2. Quero ajustar algo neste dia
```

**Passo 3. Geração do arquivo**

Gere HTML como "caderno do desafio" com:
- Capa com nome do desafio e campo "[Seu nome/logo aqui]"
- 1 seção por dia com visual diferenciado (número do dia em destaque)
- Espaço para anotações em cada dia
- Design motivacional (cores energizantes, não sóbrias demais)
- Barra de progresso visual ao longo do desafio

**Onde salvar:** `entregas/{ativo}/produto/desafio-[slug-produto].html`

---

## Formato 5. Agente GPT (assistente de IA personalizado)

**Objetivo:** assistente de IA configurado para ajudar o comprador com o tema do produto, disponível 24h.

### Antes de começar — Leitura obrigatória

Leia **obrigatoriamente** os dois arquivos abaixo antes de gerar qualquer coisa:
- `produtos/{ativo}/perfil.md` — para extrair: Quadro, Furadeira (cada etapa do método), Tom de voz, Vocabulário do comunicador
- `produtos/{ativo}/idconsumidor.md` — para extrair: frases que o público diria, palavras que conectam, palavras que afastam, objeções de compra

Esses dados são insumos diretos do prompt. Sem eles, o agente ficará genérico.

### Fluxo

**Passo 1. Escopo do agente**

Com base no que leu dos dois arquivos, proponha:
- Nome do agente (deve soar como um assistente pessoal, não uma ferramenta genérica)
- Função principal em 1 frase (o que ele faz de melhor, baseada no Quadro do produto)
- Tom de voz (extraído do perfil.md e do idconsumidor.md — nunca genérico)
- Lista do que o agente FAZ (5 a 8 capacidades, derivadas da Furadeira/método)
- Lista do que o agente NÃO FAZ (3 a 5 limitações claras, incluindo não diagnosticar, não substituir profissional)
- 3 exemplos de como o comprador usaria o agente no dia a dia (use frases reais do idconsumidor.md)

Mostre e pergunte:
```
1. Aprovar escopo e gerar o prompt
2. Quero ajustar o escopo
```

**Passo 2. Prompt completo**

Gere o prompt de configuração. O prompt DEVE conter obrigatoriamente todas as seções abaixo:

**2.1 Identidade**
- Nome do agente sem placeholder — nunca deixar `[nome]` ou `[produto]` no texto final
- Nome real da criadora (extraído do perfil.md — campo Identidade do Comunicador)
- Credencial real (anos de experiência, formação)
- Propósito em 1 frase clara

**2.2 O que FAZ e o que NÃO FAZ**
- Lista numerada do que faz (ações concretas baseadas no método)
- Lista numerada do que não faz (limitações, incluindo não diagnosticar e não substituir profissional de saúde se for nicho de saúde)
- Para temas fora do escopo: incluir frase de redirecionamento gentil pronta para o agente usar

**2.3 Tom de voz**
- Adjetivos do tom (extraídos do perfil.md)
- Proibições absolutas de estilo: nunca usar ponto de exclamação, nunca usar travessão, nunca usar perguntas retóricas como gancho, nunca usar "Não é X. É Y."
- **Vocabulário que conecta:** extrair do idconsumidor.md (campo "Palavras que conectam")
- **Vocabulário proibido:** extrair do idconsumidor.md (campo "Palavras que afastam")

**2.4 Reconhecer o vocabulário do público**
- Lista de frases que o público usa (extraídas do idconsumidor.md, campo "Frases que essa pessoa diria")
- Para cada frase: instrução de como o agente deve reagir (validar, acolher, perguntar, etc.)
- Esta seção torna o agente capaz de identificar o estado emocional da usuária pelo vocabulário, não só pelo conteúdo

**2.5 Conhecimento base**
- Principais conceitos do nicho (extraídos do perfil.md)
- Para produtos com método em etapas (desafio, mini-curso): detalhar CADA etapa com:
  - Quando usar após o produto (situação que indica essa prática)
  - Duração e o que a usuária precisa (posição, material, ambiente)
  - Adaptações para uso no dia a dia (versão reduzida, variação discreta)
  - Regras de sequência (ex: respiração sempre antes da liberação)

**2.6 Mapeamento situação → prática (obrigatório para produtos com método em etapas)**
Formato de tabela ou lista:
- O que a usuária relata → prática indicada → razão clínica ou lógica em 1 frase
- Cobrir pelo menos 6 a 8 situações distintas, incluindo casos de urgência aguda

**2.7 Regras absolutas**
- Nunca inventar dados clínicos ou estatísticas
- Nunca minimizar sintomas físicos
- Nunca diagnosticar ("seu problema é X")
- Nunca prometer resultados específicos
- Protocolo para crises (CVV, encaminhar para profissional)
- Repetir as proibições de estilo (travessão, ponto de exclamação, etc.)

**2.8 Formato de resposta**
- Tamanho conforme tipo de pergunta (curta vs. passo a passo)
- Quando fazer pergunta de clarificação antes vs. agir direto (ex: urgência aguda = agir direto)
- O que incluir ao sugerir uma prática (nome, duração, o que precisa, o que vai sentir)
- Perguntas abertas para continuar a conversa

**2.9 Exemplos de resposta dentro do prompt (mínimo 3)**
- Incluir pares Usuária/Agente diretamente no prompt, não só no arquivo .md
- Os exemplos devem cobrir: pergunta sobre prática, crise leve, frase do idconsumidor.md

**Verificação obrigatória antes de salvar o prompt:**
Antes de mostrar para aprovação, passe por este checklist:
- [ ] Nenhum placeholder do tipo `[nome]`, `[produto]`, `[especialidade]` foi deixado no texto
- [ ] O nome real da criadora está no primeiro parágrafo
- [ ] O vocabulário proibido do idconsumidor.md não aparece no corpo do prompt
- [ ] O próprio texto do prompt não usa travessão, ponto de exclamação ou perguntas retóricas
- [ ] Há pelo menos 6 situações mapeadas na tabela situação → prática
- [ ] Há pelo menos 3 exemplos de resposta com pares Usuária/Agente

Mostre o prompt completo e pergunte:
```
1. Aprovar e salvar
2. Quero ajustar algo
```

**Passo 3. Instruções de configuração**

Inclua no arquivo salvo um bloco de instruções com:
- Como configurar no ChatGPT (GPTs customizados): passo a passo numerado
- Como configurar no Claude (Projects): passo a passo numerado
- Sugestão de ícone com prompt de geração pronto
- 4 iniciadores de conversa sugeridos (use frases do idconsumidor.md como base)

**Onde salvar:** `entregas/{ativo}/produto/agente-gpt-[slug-produto].md`

---

## Formato 6. Planilha (ferramenta de cálculo ou organização)

**Objetivo:** ferramenta prática que o comprador usa repetidamente para resolver um problema específico.

### Fluxo

**Passo 1. Objetivo da planilha**

Pergunte:
```
O que a planilha vai ajudar o usuário a fazer?
(ex: "calcular o lucro de cada receita", "organizar metas semanais", "controlar finanças pessoais")
```

**Passo 2. Estrutura**

Com base no objetivo e no Quadro do produto, proponha:
- Nome da planilha
- Número de abas e nome de cada uma
- Para cada aba: objetivo, colunas principais, quais são de entrada (o usuário preenche) e quais são de resultado (calculadas automaticamente)
- Fórmulas principais que serão usadas (em linguagem simples, não em código)

Mostre e pergunte:
```
1. Aprovar estrutura e gerar a planilha
2. Quero ajustar a estrutura
```

**Passo 3. Geração do arquivo**

Gere HTML com:
- Tabelas funcionais por aba (use `<section>` ou tabs CSS para simular abas)
- **Células de entrada:** fundo amarelo claro `#fffbe6`, label "← preencha aqui"
- **Células de resultado:** fundo verde claro `#f0fff4`, label "← calculado automaticamente"
- **Células de referência/constante:** fundo azul claro `#ebf8ff`
- Instruções de uso no topo de cada aba
- Legenda de cores no cabeçalho da planilha

**Passo 4. Guia para Google Sheets**

No final do arquivo HTML, inclua um bloco colapsável "Como recriar no Google Sheets" com:
- Passo a passo para criar as abas
- Nome exato de cada coluna
- Fórmulas do Google Sheets prontas para copiar e colar em cada célula de resultado
- Dica de formatação (cores, negrito, largura de coluna)

**Onde salvar:** `entregas/{ativo}/produto/planilha-[slug-produto].html`
