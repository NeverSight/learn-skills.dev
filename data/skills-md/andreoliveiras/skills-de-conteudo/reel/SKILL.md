---
name: reel
description: Cria um reel vertical 1080x1920 pronto para postar, do gancho ao MP4 renderizado no computador da pessoa. Use quando a pessoa pedir "faz um reel sobre X", vídeo curto, reels para Instagram ou TikTok, roteiro com vídeo pronto, ou quiser transformar uma ideia, dica, lista ou conteúdo em vídeo animado com legenda. Faz uma entrevista curta, escreve gancho e roteiro cena a cena, gera a narração com a chave do ElevenLabs da própria pessoa (opcional), mixa a trilha que ela fornecer e renderiza com Remotion.
license: MIT
---

# Reel pronto, renderizado na sua máquina

Com um pedido como "faz um reel sobre 3 erros de quem começa a correr, para o meu perfil de
corrida", você entrega o reel **pronto**: gancho, roteiro cena a cena, narração, trilha e o MP4
vertical 1080x1920, renderizado localmente com Remotion. Nada é enviado para app de edição.

O vídeo é tipográfico: fundo escuro com um brilho suave, cenas com título grande, lista
numerada, número animado, cartão de antes/depois e um bloco final "Comenta PALAVRA", com a
legenda aparecendo palavra por palavra no centro, alternando peso forte e itálico.

`<skill>` abaixo é a pasta desta skill (onde está este SKILL.md).

## Pré-requisitos

- **Node 18 ou mais novo** (`node -v`). Obrigatório.
- **ffmpeg** (opcional). Só para nivelar o volume da trilha. Sem ele, a música entra como está.
  Mac: `brew install ffmpeg`. Windows: `winget install ffmpeg`. Linux: `sudo apt install ffmpeg`.
- **Chave do ElevenLabs** (opcional). Sem ela o reel sai sem voz, só com legenda animada e trilha.
- Uns **600 MB livres** para o Remotion (instalado uma vez) e o navegador que ele baixa no
  primeiro render. Internet no primeiro render, para baixar as fontes do Google Fonts.

## O fluxo, em 7 passos

### 1. Entrevista rápida (uma mensagem só)

Pergunte tudo de uma vez, com sugestão padrão entre parênteses, para a pessoa responder em uma
linha. Se ela já disse alguma coisa no pedido, não pergunte de novo.

1. **Nicho e perfil**: sobre o que é o perfil?
2. **Público**: quem assiste? (iniciante no assunto)
3. **Objetivo do reel**: alcance, salvar, ou gerar comentário para mandar um material? (comentário)
4. **CTA**: qual palavra a pessoa comenta e o que recebe? (ex.: "Comenta GUIA e eu te mando o guia")
5. **Tom**: direto, didático, provocativo, leve? (direto)
6. **Voz e música**: tem chave do ElevenLabs? Tem uma música (MP3 seu ou de biblioteca livre)?
   Quer cores específicas? (sem voz, sem música, tema escuro com destaque amarelo)

Nunca peça para a pessoa colar a chave no chat. Ela vai no arquivo `.env` (passo 4).

### 2. Gancho e roteiro

Escreva antes de qualquer código e mostre em bloco: gancho, cenas numeradas (tipo + o que
aparece na tela + a fala) e a duração estimada. **Peça ok antes de gerar narração**, porque a
narração gasta crédito do ElevenLabs. Sem narração, pode seguir direto se a pessoa pediu "só faz".

**Gancho (cena 1, até 2 segundos)**
- No máximo 6 ou 7 palavras faladas. Se precisa de mais, não é gancho, é introdução.
- A tela já mostra o gancho inteiro no primeiro quadro (o tipo `gancho` faz isso).
- Formatos que seguram: pergunta com a dor ("Treina todo dia e nada muda?"), afirmação contra
  o senso comum ("Postar todo dia está te atrapalhando"), número concreto ("3 erros que travam
  seu primeiro 5 km"), consequência ("Isso aqui faz você perder cliente no direct").
- Nada de "Oi, gente", "Neste vídeo", "Você sabia" ou apresentação pessoal.

**Roteiro (20 a 45 segundos no total)**
- De 4 a 8 cenas. Cada cena entre 1,5 e 6 segundos: no ritmo de 2,9 palavras por segundo,
  são de 5 a 17 palavras de fala por cena.
- **Fala contínua, não picada.** O texto de todas as cenas, lido em sequência, precisa soar
  como uma pessoa falando sem parar: cada cena continua a frase ou a ideia da anterior. Nada de
  frases de uma palavra, reticências para "dar pausa" ou listas faladas sem verbo. Escreva
  primeiro o texto corrido inteiro e só depois corte nas cenas.
- Uma ideia por cena. A tela mostra a versão curta (título, itens, número); a fala explica.
- Números curtos em dígito na fala ("23 horas", "1,6 grama") para a legenda ficar limpa.
- Promessa só do que é verdade. Não invente estatística: se não tem fonte, use outro tipo de cena.
- **Última cena é sempre `cta`**, e a fala diz a palavra em voz alta ("Comenta GUIA que eu te
  mando o passo a passo").

### 3. Montar o estúdio (uma vez) e a pasta do reel

O estúdio é uma pasta com o Remotion instalado; cada reel novo é só uma subpasta com o seu
`cenas.json`, então o `npm install` acontece uma vez só.

```bash
# primeira vez
cp -R <skill>/template ~/reels-estudio
cd ~/reels-estudio && npm install

# a cada reel (troque <slug> por um nome curto, ex.: 3-erros-corrida)
mkdir -p ~/reels-estudio/reels/<slug>/public
```

Escreva `~/reels-estudio/reels/<slug>/cenas.json` (formato abaixo). O `cenas.json` da raiz do
estúdio é só o exemplo que abre no Studio; não precisa mexer nele.

### 4. Narração (só com chave do ElevenLabs)

A chave fica em `~/reels-estudio/.env` (copie de `<skill>/.env.exemplo`):

```
ELEVENLABS_API_KEY=sua_chave
ELEVENLABS_VOICE_ID=id_da_voz   # opcional
```

Os scripts leem do ambiente ou desse `.env` e **nunca imprimem a chave**. Não leia, não mostre
e não copie a chave para nenhum outro lugar.

```bash
cd ~/reels-estudio
node <skill>/scripts/narrar.mjs --projeto reels/<slug> --simular   # valida, mostra custo, não chama a API
node <skill>/scripts/narrar.mjs --vozes-pt                         # vozes pt-BR da biblioteca pública
node <skill>/scripts/narrar.mjs --projeto reels/<slug>             # gera de verdade
```

- Rode `--simular` antes, sempre. Ele valida o `cenas.json` e diz quantos caracteres (créditos)
  a narração vai consumir.
- **Voz**: deixe a pessoa escolher. `--vozes-pt` lista vozes em português do Brasil da
  biblioteca pública; para usar uma delas, a pessoa adiciona à conta dela na Voice Library do
  site ("Add to my voices") e você passa `--voz <id>` ou põe `ELEVENLABS_VOICE_ID` no `.env`.
  `--vozes` lista as que já estão na conta. Sem escolha, o script usa uma voz pré-pronta do
  ElevenLabs que fala português com sotaque não nativo: avise isso.
- O texto inteiro vai numa chamada só (`/v1/text-to-speech/{voice_id}/with-timestamps`), para
  a entonação sair contínua. Os tempos de cada caractere viram o tempo de cada palavra
  (legenda sincronizada) e o tempo de cada cena.
- Saída: `reels/<slug>/public/narracao.mp3` e `public/palavras.json`, e o `cenas.json` passa a
  apontar para eles. Rodar de novo com o mesmo texto e a mesma voz não gasta crédito; para outra
  tomada, `--refazer`. `--velocidade 1.08` acelera (0.7 a 1.2).
- **Mudou a fala depois de narrar? Rode `narrar.mjs` de novo.** A legenda vem do áudio.

Sem chave: pule este passo. O reel sai sem voz, com a legenda animada no tempo estimado pela
fala (2,9 palavras por segundo) e a trilha, se houver.

### 5. Trilha (só se a pessoa fornecer)

A música vem da pessoa: uma faixa dela ou de biblioteca livre (YouTube Audio Library, Pixabay
Music), respeitando a licença de cada faixa. **Nunca baixe música de site de "download de MP3",
de vídeo do YouTube ou de qualquer fonte de licença duvidosa**, nem sugira isso. Sem trilha,
o reel sai sem música.

```bash
node <skill>/scripts/mixar.mjs /caminho/da/musica.mp3 --projeto reels/<slug>
node <skill>/scripts/mixar.mjs /caminho/da/musica.mp3 --projeto reels/<slug> --inicio 12   # pula a introdução
```

Com ffmpeg, o script corta no tamanho do reel (repete a música se for curta), nivela o volume e
põe fade de entrada e saída. Sem ffmpeg, copia como está. No render, a trilha fica baixa e
**abaixa sozinha quando há voz** (ducking simples na composição). Volume: `volumeTrilha` no
`cenas.json`, de 0 a 1 (padrão 0,3 com narração, 0,8 sem).

Se a pessoa trouxer a música depois da narração, rode `mixar.mjs` depois de `narrar.mjs` para o
corte usar a duração real.

### 6. Conferir, olhar e renderizar

```bash
cd ~/reels-estudio
node <skill>/scripts/checar.mjs --projeto reels/<slug>
```

Corrija todo `✖` (erro) e leia os `!` (avisos). Depois, **olhe 3 quadros antes do render**
(gancho, meio, CTA). Pegue os tempos na saída do `narrar.mjs` ou multiplique os segundos por 30:

```bash
npx remotion still Reel out/<slug>-q1.png --props=reels/<slug>/cenas.json --public-dir=reels/<slug>/public --frame=30
npx remotion still Reel out/<slug>-q2.png --props=reels/<slug>/cenas.json --public-dir=reels/<slug>/public --frame=<meio>
npx remotion still Reel out/<slug>-q3.png --props=reels/<slug>/cenas.json --public-dir=reels/<slug>/public --frame=<fim-20>
```

Abra as imagens e confira texto cortado, linha órfã e sobreposição. Então renderize:

```bash
npx remotion render Reel out/<slug>.mp4 --props=reels/<slug>/cenas.json --public-dir=reels/<slug>/public
```

Um reel de 30 s leva de 1 a 4 minutos. Em máquina fraca, some `--concurrency=2`. Para um
rascunho rápido, `--scale=0.5` (sai em 540x960).

### 7. Entregar com o checklist

Entregue o **caminho do MP4** (`~/reels-estudio/out/<slug>.mp4`), o roteiro final e a sugestão
de legenda do post. Antes, confirme e diga que conferiu:

- [ ] **Contraste**: a legenda lê bem sobre o fundo (o `checar.mjs` mede; mínimo 4,5:1).
- [ ] **Nada parado mais de ~3 s**: nenhuma cena acima de 6 s e nenhuma pausa longa sem legenda.
- [ ] **Gancho em até 2 s**, já visível no primeiro quadro.
- [ ] **CTA no fim**, na tela e na fala, com a palavra certa.
- [ ] Duração entre 20 e 45 s.
- [ ] Com voz: a legenda bate com a fala (veja um trecho do meio no MP4).
- [ ] Os PNGs de prévia em `out/` podem ser apagados.

## O `cenas.json`

```json
{
  "cores": { "fundo": "#0E0F12", "texto": "#F4F4F2", "destaque": "#FFC94A", "suave": "#9A9CA3", "sobreDestaque": "#0E0F12" },
  "fonte": "Inter",
  "fonteItalica": "Instrument Serif",
  "legenda": true,
  "narracao": null,
  "palavras": null,
  "trilha": null,
  "cenas": [
    { "tipo": "gancho", "titulo": "Treina todo dia e nada muda?", "destaque": "nada muda",
      "fala": "Treina todo dia e nada muda?" },
    { "tipo": "titulo", "titulo": "O problema não é o treino.", "subtitulo": "É o que acontece nas outras 23 horas.",
      "fala": "O problema quase nunca é o treino, é o que você faz nas outras 23 horas." },
    { "tipo": "lista", "titulo": "Os 3 vilões",
      "itens": ["Dormir menos de 7 horas", "Comer pouca proteína", "Repetir a mesma carga"],
      "fala": "São três vilões: dormir menos de sete horas, comer pouca proteína e repetir a mesma carga por meses." },
    { "tipo": "numero", "de": 0, "ate": 1.6, "decimais": 1, "sufixo": " g", "rotulo": "de proteína por quilo de peso, por dia",
      "fala": "Uma referência comum para quem treina é 1,6 grama de proteína por quilo, todo dia." },
    { "tipo": "antes-depois", "antes": "Treino novo toda semana", "depois": "Mesmo treino, carga subindo",
      "fala": "Em vez de trocar o treino toda semana, mantenha o mesmo e suba a carga." },
    { "tipo": "cta", "chamada": "Comenta", "palavra": "PLANO", "promessa": "que eu te mando o checklist das 23 horas",
      "fala": "Comenta PLANO que eu te mando o checklist das 23 horas." }
  ]
}
```

O mesmo exemplo está em `<skill>/exemplos/cenas.exemplo.json`.

### Tipos de cena

Todas têm `fala` (obrigatória) e `duracao` em segundos (opcional; só vale sem narração).

| tipo | campos | uso |
|---|---|---|
| `gancho` | `titulo`, `destaque` | Primeira cena. Título enorme; `destaque` é o trecho em itálico na cor de destaque. Se o título é igual à fala, a legenda não repete. |
| `titulo` | `titulo`, `subtitulo`, `destaque` | Uma afirmação forte. Título até ~50 caracteres. |
| `lista` | `titulo`, `itens` (2 a 5) | Itens numerados entrando um a um. Cada item até ~30 caracteres. |
| `numero` | `ate`, `de`, `prefixo`, `sufixo`, `decimais`, `rotulo` | Número que conta até o valor. Ex.: `"prefixo": "R$ "`, `"sufixo": "%"`. |
| `antes-depois` | `antes`, `depois`, `rotuloAntes`, `rotuloDepois` | Dois cartões; o "depois" entra no meio da cena, em destaque. |
| `cta` | `palavra`, `chamada`, `promessa` | Última cena. "Comenta" + PALAVRA num bloco + o que a pessoa recebe. Palavra até 9 letras. |

### Cores e fontes

- `cores`: qualquer cor `#rrggbb`. O padrão é neutro escuro com destaque amarelo. Para tema
  claro, inverta `fundo` e `texto` e escolha um `destaque` escuro o bastante. O `checar.mjs`
  reprova contraste baixo.
- `fonte` e `fonteItalica`: nomes de famílias do Google Fonts (ex.: `"Montserrat"`,
  `"Playfair Display"`). A `fonte` precisa ter peso 900. Use `"sistema"` para não baixar nada.
  Se a família não existir ou faltar internet, o render segue com a fonte do sistema.
- `legenda: false` desliga a legenda palavra por palavra.

## Problemas comuns

- **"palavras.json é de outra versão do cenas.json"**: a fala mudou depois da narração. Rode
  `narrar.mjs` de novo.
- **ElevenLabs 401**: chave errada ou sem permissão de text-to-speech. **404**: a voz não está
  na conta; adicione pela Voice Library.
- **Texto saindo da tela**: encurte o título ou os itens; o `checar.mjs` avisa os longos.
- **Render lento ou travando**: `--concurrency=2`, feche o navegador, e confira o espaço em disco.
- **Primeiro render demora mais**: o Remotion baixa um navegador headless (uma vez só).

## O que esta skill não faz

- Não filma nem usa vídeo gravado, imagem ou avatar: o reel é tipográfico (texto, número,
  cartões). Para editar filmagem, use outra ferramenta.
- Não clona voz nem gera voz sem a chave do ElevenLabs da própria pessoa.
- Não escolhe nem baixa música: a trilha é sempre fornecida pela pessoa.
- Não publica no Instagram nem agenda post.
- O ducking é simples (a música baixa quando há fala); não substitui uma mixagem profissional.
