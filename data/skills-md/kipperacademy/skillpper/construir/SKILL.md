---
name: construir
description: Construir um projeto para aprender programação. Use quando o aluno pede um projeto ou quando aprender entrega uma atividade que precisa de arquivos, execução e etapas persistentes.
argument-hint: "O que você quer construir e aprender?"
---

Conduza um projeto mínimo que roda e torna um conceito observável. Alterne decisões, previsões,
implementação e depuração com participação do aluno. A construção serve à missão de aprendizagem.

## 1. Receber ou retomar

Leia [WORKSPACE-FORMAT.md](./shared/WORKSPACE-FORMAT.md) e
[PROFILE.md](./shared/PROFILE.md). Se veio de aprender, leia
[HANDOFF.md](./shared/HANDOFF.md) e o contexto salvo; use a missão, o catálogo e as evidências
existentes. Consulta nova ao perfil só é necessária numa sessão nova ou quando os dados faltam.

Um projeto existente retoma seu checkpoint e ajuda pendente. Na entrada direta, crie uma missão
com [MISSION-FORMAT.md](./shared/MISSION-FORMAT.md); objetivo vago admite um resultado provisório.
Leia [EVENTS-FORMAT.md](./shared/EVENTS-FORMAT.md) antes de registrar eventos. Registre pedido
apenas se estiver abrindo um tópico novo. Preserve o plano de estudo quando ele já existe.

**Pronto quando:** missão, evidências disponíveis e próximo checkpoint estão identificados.

## 2. Propor o projeto

Confirme a linguagem apenas se faltam preferência e contexto suficientes. Escolha o menor
projeto que expõe o mecanismo: defaults simples para o que fica fora do assunto, um comando
para rodar e simplificações explicadas no README. Se a tecnologia é o próprio assunto, explicite
o preparo mínimo necessário e ajude a fazê-lo, em vez de prometer ausência de dependências.

Proponha em poucas linhas o resultado e três a seis checkpoints, com o comportamento que cada
um torna observável. Ordene por dependências do mecanismo, dificuldade relevante e avanço para
a missão; uma lacuna não deve vir antes do fundamento necessário para experimentá-la.

Leia [PLAN-FORMAT.md](./PLAN-FORMAT.md). Após a aceitação do aluno, crie o projeto em pasta nova
ou use o repositório atual se ele pediu. Em repositório existente, leia as instruções aplicáveis
e preserve o trabalho presente. Salve project_path na missão e o plano em BUILD.md.

**Pronto quando:** escopo aceito, caminho salvo e primeiro checkpoint com comportamento esperado.

## 3. Trabalhar um checkpoint

Leia [CHECKPOINTS.md](./CHECKPOINTS.md) para preparar cada checkpoint e
[EVIDENCE.md](./shared/EVIDENCE.md) para interpretar respostas e assistência.
Prepare a infraestrutura fora do assunto. Escolha uma participação central: decidir com
justificativa, prever, implementar a parte do conceito ou depurar uma falha.

Quando o checkpoint pedir implementação numa função ou classe, leia
[GUIDED-CODE.md](./shared/GUIDED-CODE.md): dê contexto e use comentários estruturados
no ponto de edição para guiar o trabalho do aluno.

Deixe o aluno tentar antes de revelar a solução. Apoie a tentativa com scaffolding e pistas;
para quem já mostrou o mecanismo, avance até a decisão nova. Quando o aluno preferir que a IA
escreva, peça uma previsão ou decisão relevante e execute o resultado para confrontá-la.

Se outra representação ajudar, leia [DRAWING-FORMAT.md](./shared/DRAWING-FORMAT.md).
Após cada participação, dê feedback, registre a evidência e atualize BUILD.md. Mudança de
representação e auxílio explícito são saídas para quem trava, não penalidades.

**Pronto quando:** o comportamento foi executado e comparado ao esperado; a contribuição e a
ajuda do aluno estão registradas. Um checkpoint assistido pode avançar com a lacuna preservada;
o código escrito pela IA, sozinho, não demonstra aprendizagem.

## 4. Fechar e devolver

Execute o projeto de ponta a ponta. Atualize o README com comando, mecanismo e simplificações.
Peça uma aplicação em condição nova: alterar o comportamento, diagnosticar uma falha ou prever
uma mudança que não foi mostrada. Registre o que foi demonstrado e o que ainda depende de ajuda.

Salve referências do conceito. Leia
[LEARNING-RECORD-FORMAT.md](./shared/LEARNING-RECORD-FORMAT.md) para registros locais.
Quando veio de aprender, use HANDOFF.md para devolver evidência e próximo passo; continue o fluxo
de aprender já ativo, ou ofereça /aprender com o pedido de continuação em outro chat. A preferência por ficar no
projeto mantém construir ativo. Entrada direta pode fechar sem passar por aprender.

**Pronto quando:** projeto executável, resultado ou falha explicitados, evidências e retomada
salvas. A conclusão do projeto não concede conquista; avaliação oficial depende da Kipper.

## Conversa

Uma participação central por turno, com feedback concreto e saída visível quando relevante.
Explique escolhas fora do assunto no README; mantenha o diálogo no mecanismo estudado. Ao pausar,
salve checkpoint, arquivos tocados, comando, tarefa pendente e ajuda já dada.
