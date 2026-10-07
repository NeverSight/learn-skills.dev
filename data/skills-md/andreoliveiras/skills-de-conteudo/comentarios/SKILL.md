---
name: comentarios
description: Classifica comentários de Instagram e escreve a resposta pública e a DM de cada um. Use quando a pessoa colar ou exportar comentários de um post ou reel, pedir "responde esses comentários", "quem pediu o material", "monta as DMs", ou usar uma palavra-chave de isca (como "comenta GUIA"). Identifica a intenção (pediu o material, dúvida, elogio, objeção, hater, spam) e entrega tudo em tabela e CSV prontos para copiar. A skill escreve as respostas; ela não envia nada sozinha.
license: MIT
---

# Respostas para comentários do Instagram

Você transforma uma pilha de comentários em respostas prontas: uma **resposta pública curta** e, quando faz sentido, uma **DM** com o que a pessoa pediu.

## O que esta skill faz e o que não faz

**Faz:** lê os comentários, classifica a intenção de cada um e **escreve** as respostas (pública e DM), em tabela e CSV para copiar.

**Não faz:** enviar. Quem posta as respostas e manda as DMs é a pessoa, no aplicativo. Disparar de forma automática, sem ninguém clicando, exige uma **automação de DM conectada à API oficial do Instagram**, que é outra ferramenta e que esta skill não cria nem opera. Se a pessoa perguntar, diga isso com clareza e use o CSV como a base de texto que a automação (ou a própria pessoa) vai usar.

Nunca diga que "enviou", "respondeu" ou "disparou" algo.

## Entrada

1. **Os comentários**: colados, em lista (um por linha, de preferência `@usuario: texto`) ou exportados em CSV. Se vierem muitos (acima de 100), processe em lotes e avise.
2. **Contexto do post**: do que ele trata e qual era o CTA (por exemplo "comenta GUIA para receber o guia").
3. **O que entregar na DM** para quem pediu o material: o texto do material, o link, o arquivo. Se a pessoa ainda não deu, use `[LINK]` ou `[MATERIAL]` como marcador e avise no fim. **Nunca invente link, preço, prazo ou condição.**
4. **Tom** da pessoa (formal, descontraído, com ou sem emoji). Se ela colar respostas antigas, imite.
5. Palavra-chave do CTA, se houver (a que conta como "pediu o material").

Pergunte só o que faltar, em uma mensagem.

## Passo 1. Classifique a intenção

Uma intenção por comentário (a principal):

| Intenção | Sinal | Ação |
|---|---|---|
| **Pediu o material** | Escreveu a palavra-chave ou algo como "quero", "me manda", "eu quero o guia" | Resposta pública curta + DM com o material |
| **Dúvida** | Pergunta sobre o conteúdo, preço, como funciona, para quem é | Responder a dúvida de verdade. Pública se for curta e útil a outros; se for pessoal ou longa, resposta pública curta convidando e resposta completa na DM |
| **Elogio** | Agradece, concorda, marca amigo | Resposta pública curta e humana; se a pessoa marcou um amigo, agradeça por compartilhar |
| **Objeção** | "Isso não funciona", "é caro", "já tentei", "não tenho tempo" | Responder com respeito e com um fato ou exemplo concreto, sem discutir. Reconhecer o que for verdade na objeção |
| **Hater** | Ofensa, deboche, provocação sem argumento | Não alimentar. Se houver uma crítica legítima escondida, responda a crítica em uma linha neutra. Se for só ataque: **sem resposta**, e sugira ocultar ou restringir |
| **Spam** | Propaganda, golpe, link suspeito, "ganhe seguidores", emojis soltos de bot | **Sem resposta.** Sugira excluir ou ocultar. Nunca clique ou repasse links |

Na dúvida entre duas intenções, escolha a que gera a ação mais útil e anote a outra em "obs".

## Passo 2. Escreva a resposta pública

- **Curta**: até 1 ou 2 frases, até 120 caracteres quando possível.
- **Sem link no comentário público.** O Instagram derruba o alcance de comentários com link e a pessoa perde a distribuição do post. Para entregar algo, diga "te mandei no direct" ou "olha seu direct".
- Cite o primeiro nome ou o @ da pessoa quando soar natural. Varie o texto: 50 respostas idênticas parecem robô e podem ser tratadas como spam. Crie pelo menos 5 formulações diferentes para "pediu o material" e alterne.
- Para pedido de material, avise que, se a mensagem não aparecer, vale olhar a caixa de "solicitações" do direct.
- Termine perguntas abertas só quando fizerem a conversa render ("qual parte te pegou mais?"). Não force.
- Emoji: no máximo 1 por resposta, e só se combinar com o tom da pessoa.
- Nunca prometa o que o material não entrega, nem pressione ("corre", "últimas vagas") sem dado real.

## Passo 3. Escreva a DM

Só para **pediu o material** e para **dúvida** que precise de resposta longa.

Estrutura da DM de material:

1. Cumprimento com o primeiro nome, uma linha.
2. Entrega direta: o material ou o link, logo na segunda linha (quem pediu quer o material, não conversa).
3. Uma frase dizendo como usar ou por onde começar.
4. Uma pergunta curta que abre conversa ("me conta o que você vai fazer primeiro?") ou um próximo passo opcional. Um só.

Regras:

- Máximo de 600 caracteres. Frases curtas.
- Não peça dado pessoal sensível. Não peça pagamento nem senha.
- Não faça venda agressiva na primeira mensagem. Se houver oferta, apresente depois da entrega e com clareza do que é.
- Respeite quem pedir para parar: se algum comentário diz que não quer mensagens, não escreva DM para ele.
- Use `[LINK]` ou `[MATERIAL]` quando faltar o conteúdo real.

Observação para a pessoa: o Instagram limita o envio de mensagem para quem comentou. O jeito oficial de uma automação fazer isso é a resposta privada via API, que costuma ter prazo curto depois do comentário. Mandando à mão, o ideal é responder no mesmo dia.

## Passo 4. Entregue em tabela e em CSV

Primeiro, o resumo: quantos comentários, quantos por intenção, quantos precisam de DM, quantos sem resposta.

Depois a tabela em markdown:

| # | Usuário | Comentário | Intenção | Resposta pública | DM |
|---|---|---|---|---|---|

Depois o CSV em um bloco de código, com cabeçalho e **todos os campos entre aspas**, para colar numa planilha:

```csv
"numero","usuario","comentario","intencao","resposta_publica","dm","obs"
"1","@exemplo","quero o guia","pediu_material","Te mandei no direct, @exemplo!","Oi! Aqui está o guia: [LINK]. Começa pela página 2. Me conta o que você vai aplicar primeiro?",""
```

Regras do CSV: aspas duplas dentro de um campo viram duas aspas (`""`); sem quebra de linha dentro de campo (use espaço); intenções em minúsculas e sem acento: `pediu_material`, `duvida`, `elogio`, `objecao`, `hater`, `spam`; resposta pública e DM vazias quando a ação é não responder (e a coluna `obs` diz "ocultar" ou "ignorar").

Se a pessoa estiver trabalhando em uma pasta de projeto, ofereça salvar o CSV em um arquivo (por exemplo `respostas-<post>.csv`).

## Fechamento

Termine avisando: (1) o que ficou com marcador `[LINK]`/`[MATERIAL]` a preencher, (2) quais comentários merecem atenção humana (crítica legítima, cliente insatisfeito, algo que pareça risco jurídico ou de saúde) e (3) lembrando que **as respostas precisam ser postadas e as DMs enviadas pela pessoa ou por uma automação própria**.
