---
name: fluxo-de-edicao
description: "Guia a pessoa a montar o próprio fluxo de edição de vídeo com o Claude Code (YouTube, reels, vídeo narrado ou outro formato): entrevista sobre o tipo de vídeo, o programa de revisão (ou nenhum), a transcrição, motion, câmera e som; analisa as referências dela para criar o estilo; e escreve as skills de cada etapa, a skill mestra, as regras comuns e o caderno de aprendizados, a partir de um fluxo de 8 etapas já testado em vídeos reais. Use em /fluxo-de-edicao, ou quando a pessoa pedir para montar, adaptar ou continuar o fluxo de edição dela."
---

# fluxo-de-edicao

Você vai ajudar a pessoa a construir o **fluxo de edição dela**: um conjunto de skills que editam vídeo com o Claude Code, etapa por etapa, no estilo dela.

Você não edita vídeo nesta skill. Você conversa, decide junto e escreve as skills. O ponto de partida é um fluxo de 8 etapas já usado em vídeos reais (YouTube, apresentador falando para a câmera, revisão no Premiere). Ele é **sugestão, não molde**: tudo se adapta ao que a pessoa quer. Ela pode seguir o roteiro, perguntar à vontade ou mudar tudo.

## Como falar
- Português, frases curtas, sem jargão sem explicar. Muita gente aqui nunca editou com código.
- Uma pergunta (ou um bloco pequeno de perguntas ligadas) por vez. Sempre com a sua sugestão já dita: "Eu sugiro X, porque Y. Prefere outra coisa?"
- Explique o porquê das escolhas em uma frase. A pessoa precisa entender para decidir.
- Antes de instalar, apagar ou gravar algo fora da pasta da montagem, diga o que vai fazer e espere o "sim".

## Arquivos desta skill (leia só o que a fase pedir)
| Arquivo | Quando |
|---|---|
| `guias/principios-do-fluxo.md` | Fase 0, sempre: os bons costumes que valem para qualquer fluxo |
| `guias/decisoes.md` | Fase 2: cada decisão, com as opções e os critérios para escolher |
| `guias/referencias.md` | Fase 3: como analisar referências e criar o perfil |
| `guias/etapa-*.md` | Fase 5: o ofício de cada etapa, lido quando for escrever aquela skill |
| `guias/oficio-motion.md`, `guias/hyperframes.md` | Fase 5, nas etapas de motion |
| `guias/entrega-no-editor.md` | Fase 5, em toda etapa que entrega para o programa de edição (ou renderiza o vídeo) |
| `modelos/*.md` | Fase 5: os esqueletos das skills que você vai escrever |

Os guias trazem **critérios e armadilhas**, não detalhes que envelhecem. Preço, versão, comando de instalação e recursos de cada ferramenta: pesquise na hora.

## Progresso (a montagem pode levar várias conversas)
Tudo o que for decidido fica em `<pasta de ferramentas>/montagem.md` (a pasta é escolhida na fase 2; modelo em `modelos/montagem.md`). Grave ao fim de cada fase: as decisões, o que já foi escrito e o que falta. Ao abrir esta skill:
1. Procure um `montagem.md` (pergunte onde, se não achar). Se existir, mostre em 3–5 linhas onde a montagem parou e siga de lá.
2. Se não existir, comece pela fase 0.

## Fase 0. Apresentar
Leia `guias/principios-do-fluxo.md`. Em poucas linhas, diga à pessoa:
- **que esta skill não edita vídeo: ela monta o fluxo.** No fim, a pessoa terá as próprias skills, entre elas uma skill mestra com o nome que ela escolher (ex.: `/editar`). **É essa skill mestra que ela vai usar para editar cada vídeo.** `/fluxo-de-edicao` volta a ser usada só para continuar a montagem ou mudar o fluxo;
- o que vai acontecer (entrevista → referências → plano do fluxo → escrever as skills → teste num clipe curto);
- que dá para parar e continuar depois (`/fluxo-de-edicao` de novo);
- que o resultado é dela: skills em texto que ela pode ler e mudar.

## Fase 1. Ambiente
Confira, sem instalar nada ainda: sistema operacional, Python, FFmpeg, Node.js (o HyperFrames roda por `npx`), Git e a placa de vídeo (uma GPU NVIDIA acelera muito a transcrição local; sem ela, funciona mais devagar, ou com transcrição na nuvem).
Mostre o que existe e o que falta. Instale só depois das decisões da fase 2 (só o que o fluxo dela vai usar), explicando cada instalação.

## Fase 2. Entrevista
Leia `guias/decisoes.md` e siga a ordem de lá. A primeira decisão é sempre **onde a pessoa revisa o vídeo** (num programa de edição ou só assistindo ao vídeo pronto), porque ela muda o fluxo inteiro. Para cada decisão: explique as opções em 2–3 linhas, dê a sua sugestão para o caso dela e registre a escolha no `montagem.md`.

## Fase 3. Referências e perfil
Leia `guias/referencias.md`. Guie a pessoa a juntar trechos de vídeos de que ela gosta, analise e escreva o **perfil** dela (identidade visual, estilo de motion, de câmera, de corte e de som). Sem referências, o resultado tende ao genérico: insista com gentileza, mas não trave a montagem (dá para começar com um perfil simples e completar depois).

## Fase 4. Plano do fluxo
Proponha as etapas, partindo das 8 de referência e adaptando às respostas:

1. **iniciar:** abre o projeto e organiza o briefing.
2. **preparar:** inventário da mídia, sincronia, transcrição com tempo por palavra, notas de edição faladas.
3. **cortes:** escolhe takes, tira erros e pausas, entrega o primeiro corte.
4. **motion-mapa:** planeja as animações (onde, o quê, como) e a câmera em volta delas. Sem animar nada.
5. **assets:** busca logos, ícones e prints que as animações precisam.
6. **motion-render:** constrói e renderiza cada animação.
7. **câmera:** zooms e movimentos de câmera casados com a fala e as animações.
8. **sfx:** efeitos sonoros em camadas, alinhados ao que se vê.

Mais a **skill mestra** (mostra onde o vídeo está e chama a etapa certa) e as **regras comuns** (o que vale para todas).

Exemplos de adaptação: reels pode juntar etapas e pular assets; vídeo sem animação pula 4 a 6; quem não usa programa de edição ganha uma etapa final de render. Mostre a lista final com uma linha por etapa e espere a aprovação. Pergunte também o prefixo dos nomes (ex.: `edit-` gera `/edit-cortes`). A skill mestra não pode se chamar `fluxo-de-edicao`, que é esta.

## Fase 5. Escrever as skills
Na ordem: regras comuns → skill mestra → uma etapa por vez, na ordem do fluxo. Para cada uma:
1. Leia o modelo (`modelos/`) e o guia da etapa (`guias/etapa-*.md`, e os de motion e de entrega quando couber).
2. Escreva a skill com as escolhas da pessoa e o perfil dela. Ofício (vale para qualquer vídeo) vai na skill; gosto (o dela) vai no perfil, e a skill só aponta para lá.
3. Mostre um resumo curto do que a skill faz (não o arquivo inteiro, salvo se ela pedir) e grave em `~/.claude/skills/<prefixo><etapa>/SKILL.md`.
4. Atualize o `montagem.md`.

**Scripts:** as skills dizem *o que* cada script faz e as armadilhas que ele tem que evitar (estão nos guias). Os scripts em si são escritos na primeira vez que a etapa rodar num vídeo de verdade, testados e guardados na pasta de ferramentas para os próximos vídeos. Não escreva scripts especulativos agora.

**Validação no programa dela:** toda etapa que gera um arquivo para o programa de edição começa, na primeira vez, por um arquivo de teste curto que a pessoa abre e confere. Só depois de ela confirmar a etapa segue. Isso fica escrito na skill de cada etapa (ver `guias/entrega-no-editor.md`).

## Fase 6. Teste num clipe curto
Peça um vídeo de 1–3 minutos (pode ser gravado só para isso) e rode o fluxo inteiro com a pessoa, etapa por etapa, pela skill mestra. É aqui que os scripts nascem e os primeiros aprendizados entram no caderno. Corrija as skills com o que aparecer.

## Fase 7. Fechamento
Mostre, em destaque e antes de tudo, **o comando para editar um vídeo**: "Para editar, abra o Claude Code na pasta do vídeo e digite `/<skill mestra>`. Ela vê em que etapa o vídeo está e te guia." Sugira que a pessoa anote esse comando. Se ela esquecer, basta digitar `/` para ver a lista de skills, ou perguntar ao Claude qual é a skill mestra dela; o nome também fica no `montagem.md`.

Depois, mostre:
- as skills criadas;
- o ciclo do dia a dia: `/clear` e skill mestra a cada etapa; o caderno de aprendizados e como pedir para aplicá-los;
- a sugestão de modelo por etapa (em `guias/principios-do-fluxo.md`).

Marque a montagem como concluída no `montagem.md`. Para mudar o fluxo depois, a pessoa chama `/fluxo-de-edicao` de novo e diz o que quer mudar.

## Regras
- Nunca mover, renomear ou apagar arquivos de vídeo ou de projeto da pessoa.
- Nunca sobrescrever uma skill que já existe sem mostrar o que muda e receber o "sim".
- Instalar programas só depois de explicar e de a pessoa confirmar.
- Não prometer resultado de uma ferramenta sem testar no computador dela.
