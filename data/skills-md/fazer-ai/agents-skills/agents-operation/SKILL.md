---
name: agents-operation
description: "Modo operação do fazer.ai agents: debugar conversas em produção e corrigir comportamentos inesperados do agente. Investiga (conversa no Chatwoot + ExecutionLog/flowlog + traces no Langfuse), reproduz no playground, ajusta o agente (prompt/ferramentas/behavior/KB) e re-valida, com toda mutação aprovada. Use quando uma instância JÁ em produção se comporta de forma inesperada e precisa de diagnóstico/ajuste, não é onboarding (subir do zero) nem desenvolvimento de código."
---

# Modo operação do fazer.ai agents

Pega uma instância **já em produção** que está se comportando de forma inesperada e leva de "a conversa do cliente deu errado" até "causa entendida, ajuste validado e aplicado com aprovação". Audiência: **operador de uma instância viva**. Para subir uma instância nova use `agents-onboarding`; para mexer no código-fonte use `agents-dev`.

## ⚠️ Segurança de produção (lê primeiro)

Este modo **inverte** o fence do onboarding: lá o alvo é uma VPS de teste e "nada de produção"; aqui o alvo **é** produção.

- **Investigação read-only é livre** (ler conversas, logs, traces, config do agente, queries de leitura). Mutação **não**.
- **Toda mudança precisa de OK explícito do usuário para aquela mudança específica.** Autorização a um objetivo (corrigir um comportamento) não é autorização para escolher o método nem para aplicar sozinho. Proponha o diff/ajuste e espere o aval.
- **Nunca editar o DB de produção direto** para mudar estado da aplicação: use a UI/API/console da própria app (editor de agente, write tools de MCP **dry-run por padrão**). Write direto no DB fura o passo de publish/validação da app.
- **Sem segredo em log, output ou commit;** mascarar ao exibir.

## O fluxo (references)

Siga em ordem; cada etapa é uma reference. Leia a da etapa antes de executá-la.

1. [`references/00-production-safety.md`](references/00-production-safety.md): a postura invertida: read-only livre, toda mutação aprovada item a item, nunca DB direto, dry-run por padrão. **Lê primeiro.**
2. [`references/01-diagnose.md`](references/01-diagnose.md): localizar a conversa (`display_id`), ler o `ExecutionLog` (`/logs`), traces no Langfuse, config do agente: isolar **qual estágio** (stt/embed/generate/tts/split/handoff) divergiu.
3. [`references/02-reproduce.md`](references/02-reproduce.md): reconstituir o turno no **playground** (modelo real, isolado da conversa real).
4. [`references/03-adjust.md`](references/03-adjust.md): corrigir na camada certa: prompt, grants (replace-the-set), behavior, grounding/KB. Console ou MCP (dry-run primeiro).
5. [`references/04-validate-and-apply.md`](references/04-validate-and-apply.md): re-validar no playground, conversa de teste controlada (Inbox API) quando fizer sentido, aplicar só com aprovação (audit cobre o write).
6. [`references/05-load-sim.md`](references/05-load-sim.md): **(opcional)** simular **N clientes concorrentes** (Inbox API, `scripts/simulate-load.py`) pra validar carga + que as **ferramentas disparam**; contorna o `/teste` ativando cada conversa. Use pra estresse ou pra reproduzir bug que só aparece com concorrência.

Fronteiras duras em [`guardrails.md`](guardrails.md); armadilhas de diagnóstico em [`gotchas.md`](gotchas.md).

## Guardrails

Resumo (detalhe em [`guardrails.md`](guardrails.md)):

- **Produção-first:** read-only livre; toda mutação aprovada item a item; nunca DB de produção direto.
- **Dry-run:** toda write tool de MCP previewa; aplica só com OK.
- **Estilo:** PT-BR com acentuação; sem em-dash; `fazer.ai` minúsculo.

## Skills irmãs

- `agents-onboarding`: subir uma instância nova num VPS (do zero ao agente).
- `agents-dev`: trabalhar no código-fonte (Free/Full, implementar, gerar imagem).
