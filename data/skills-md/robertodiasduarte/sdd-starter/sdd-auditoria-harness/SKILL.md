---
name: sdd-auditoria-harness
license: MIT
description: "Audita read-only o harness SDD de um repositório para FAXINA E DERIVA: inventaria comandos, agentes, skills, hooks, settings e scripts de QUALQUER motor (Claude Code, Codex, Kimi CLI: le CLAUDE.md e AGENTS.md, .claude/, .agents/ e .codex/), mede referências, recência, duplicação e deriva entre docs e código, e gera um único relatório AUDITORIA_SDD_<data>.md sem alterar nada. Invocar quando alguém disser \"o harness cresceu demais\", \"o que aqui ninguém usa\", \"os docs ainda batem com o código?\", ou pedir uma faxina do harness (`.claude/`, `.agents/` ou `.codex/`). ⚠️ Fronteira: esta skill pergunta O QUE SOBRA E O QUE DERIVOU (higiene). Para SEGURANÇA — easter egg, código malicioso, backdoor, exfiltração, unicode invisível em material de terceiro que você vai instalar — use a skill rdd-audita-harness. Excesso não é ameaça; as duas são read-only e se complementam."
metadata:
  author: Roberto Dias Duarte
---

# Auditoria Read-Only do Harness SDD

## Quick start

1. Defina `REPO_ROOT` como a raiz do repositório auditado.
2. Execute primeiro o **Safety Gate** desta Skill.
3. Leia as fontes de verdade do SDD: os arquivos de instrução do projeto (`CLAUDE.md` **e/ou** `AGENTS.md`), índice/readme do SDD e as configurações do motor (`.claude/settings.json` / `.claude/settings.local.json`, `.codex/config.toml`).
4. Opcionalmente, gere evidência estruturada somente em stdout:
   `python scripts/collect_evidence.py "$REPO_ROOT"`.
5. Faça a análise seguindo [references/AUDIT_PROTOCOL.md](references/AUDIT_PROTOCOL.md).
6. Crie somente o novo relatório `AUDITORIA_SDD_<AAAA-MM-DD>.md`, usando [references/REPORT_TEMPLATE.md](references/REPORT_TEMPLATE.md).
7. Termine no chat com o sumário executivo, o caminho do relatório e a frase:
   `nenhuma alteração foi feita — a faxina em si é decisão humana.`

## Quando usar / Quando não usar

### Quando usar

Use esta Skill para auditar o harness SDD de um repositório, **seja qual for o motor**. As
superfícies mudam de caminho conforme a ferramenta; audite as que existirem:

| Peça | Claude Code | Codex / Kimi CLI |
|---|---|---|
| Instruções do projeto | `CLAUDE.md`, `.claude/CLAUDE.md`, `CLAUDE.local.md` | `AGENTS.md` (padrão aberto; o Claude Code também o lê por fallback desde a 2.1.277) |
| Skills | `.claude/skills/*/SKILL.md` | `.agents/skills/*/SKILL.md`, `.codex/skills/*/SKILL.md` |
| Comandos | `.claude/commands/**/*.md` | `.codex/prompts/**/*.md` |
| Agentes/subagentes | `.claude/agents/**/*.md` | `.agents/agents/**/*.md` |
| Configuração | `.claude/settings.json`, `.claude/settings.local.json` | `.codex/config.toml` |
| Scripts do harness | `.claude/scripts/**` | `.agents/scripts/**`, `.codex/scripts/**` |

Audite ainda:
- hooks, permissões e scripts referenciados pelo harness;
- docs de processo, playbooks, notas de memória e diretórios de specs;
- divergências entre o fluxo SDD oficial e itens legados, duplicados ou sem evidência de uso.

### Quando não usar

Não use esta Skill para:
- apagar, editar, renomear, mover, formatar ou reorganizar arquivos existentes;
- corrigir automaticamente achados;
- fazer `git add`, `commit`, `push`, `pull`, `fetch`, `checkout`, `restore`, `reset`, `clean`, `rm` ou `mv`;
- instalar dependências, executar deploys ou comandos com efeito colateral;
- auditar fora da raiz informada do repositório;
- concluir que algo é “NÃO UTILIZADO” apenas porque parece antigo ou raro.

## Dados necessários

### Obrigatórios
- `REPO_ROOT`: raiz do repositório que contém o harness a auditar.
- Acesso de leitura ao repositório e, quando disponível, ao histórico Git.

### Derivados automaticamente
- `REPORT_DATE`: data local da execução, no formato `AAAA-MM-DD`.
- `REPORT_DIR`: pasta de relatórios do SDD, se houver uma claramente estabelecida; caso contrário, a raiz do repo.
- `REPORT_PATH`: `REPORT_DIR/AUDITORIA_SDD_<REPORT_DATE>.md`.

Se `REPO_ROOT` não estiver claro, pergunte apenas:
`Qual é a raiz do repositório SDD que devo auditar?`

## Procedimento passo a passo

### 0. Safety Gate bloqueante

Antes de executar qualquer comando:

1. Confirme que a ação é somente leitura.
2. Recuse qualquer comando que possa escrever, apagar, mover, renomear, instalar, sincronizar ou alterar Git/estado do projeto.
3. Prefira comandos de inspeção como `git log`, `git status`, `git diff`, `git ls-files`, `git grep`, `rg`, `grep`, `find` sem ações destrutivas, `cat`, `sed` sem `-i`, `awk`, `head`, `tail`, `wc` e leitura via ferramentas nativas.
4. Não use `find -delete`, `find -exec` com comandos mutantes, `sed -i`, redirecionamentos `>`/`>>`, `tee`, `touch`, `mkdir`, `cp`, `rsync` ou scripts que escrevam durante a auditoria.
5. A única escrita permitida é a criação do relatório final novo, no caminho calculado.
6. Se `REPORT_PATH` já existir, **não sobrescreva**. Pare a escrita, entregue o sumário no chat e peça um novo nome explicitamente autorizado.

### 1. Estabelecer o SDD principal

Leia, nesta ordem:
1. o arquivo de instruções do projeto na raiz — `CLAUDE.md` **ou** `AGENTS.md`, o que existir (podem coexistir);
2. o mesmo, em subdiretórios relevantes ao harness;
3. índice/readme do diretório SDD, como `sdd/_index.md`, `.claude/sdd/_index.md` ou equivalente;
4. a configuração do motor: `.claude/settings.json` e `.claude/settings.local.json`, e/ou `.codex/config.toml`, incluindo hooks e permissões.

⚠️ **Se o repositório tem `AGENTS.md` e nenhum `CLAUDE.md`**, isso não é lacuna: desde o
Claude Code **2.1.277** o `AGENTS.md` é lido por fallback, e Codex/Cursor/Gemini CLI já o
liam nativamente. Não classifique a ausência de `CLAUDE.md` como achado.

⚠️ **Se os dois existem**, registre a precedência real: por padrão o Claude Code lê **só**
os arquivos `CLAUDE.md` e **ignora** o `AGENTS.md` — a menos que o `CLAUDE.md` o importe com
`@AGENTS.md` ou que **Project instructions** esteja em `claude-md-and-agents-md`. Instrução
que o aluno acha que vale e não é lida é **CONFLITANTE**, e é dos achados mais úteis desta
auditoria.

Produza um resumo de 5–10 linhas contendo:
- fases oficiais;
- comandos que invocam cada fase;
- caminho dos artefatos produzidos;
- regras de precedência/fonte de verdade, se declaradas.

Esse resumo é a régua para classificar **AMBÍGUO** e **CONFLITANTE**.

### 2. Inventário completo do harness

Inclua um item por linha para:
- comandos/slash commands;
- agentes;
- skills;
- hooks e permissões;
- scripts de apoio;
- docs de processo e diretórios de specs;
- scripts externos à pasta do motor (`.claude/`, `.agents/`, `.codex/`) que sejam referenciados pelo harness.

Para cada item registre:
`caminho | tipo | propósito declarado | idioma/origem aparente`.

Não marque “copiado de template” sem indício concreto. Se a origem não puder ser provada, use `indeterminada`.

### 3. Medir uso e vitalidade

Para cada item, colete:
1. **Referências cruzadas**: referências de entrada no restante do harness.
2. **Recência**: `git log -1 --format=%cs -- <arquivo>`.
3. **Sinal de execução**: menções em relatórios/logs do SDD, quando existirem.
4. **Duplicação**: sobreposição objetiva de propósito/saída com outro item.
5. **Deriva**: referências a arquivos, fases, modelos, comandos ou paths inexistentes.

O helper `scripts/collect_evidence.py` pode acelerar os itens 1–3 e apontar candidatos do item 5. Ele só lê arquivos e escreve JSON em stdout.

Zero referências de entrada **e** nenhum sinal de execução é apenas a condição mínima para considerar `NÃO UTILIZADO`. Se o item puder ser raro por design, classifique como dúvida e não como certeza.

### 4. Classificar achados

Use somente estes rótulos, exatamente:
- **EXCESSO**
- **OBSOLETO**
- **SUPÉRFLUO**
- **NÃO UTILIZADO**
- **AMBÍGUO**
- **CONFLITANTE**

Um item pode receber mais de um rótulo.

Todo achado precisa conter:
- arquivo;
- linha, quando a evidência estiver em conteúdo textual;
- evidência concreta;
- recomendação.

Achado sem evidência verificável não entra na tabela de achados; vai para “Dúvidas para o dono do repo”.

Critérios detalhados e cautelas estão em [references/AUDIT_PROTOCOL.md](references/AUDIT_PROTOCOL.md).

### 5. Recomendar, sem executar

Para cada achado, escolha exatamente uma ação sugerida:
- `MANTER`
- `APOSENTAR` — com tombstone/ponteiro; nunca recomendar delete seco;
- `FUNDIR com <item>`
- `ESCLARECER`
- `ARQUIVAR`
- `REDUZIR`

A recomendação descreve o que o dono poderia fazer depois; não faça a alteração.

### 6. Criar o relatório final

Use [references/REPORT_TEMPLATE.md](references/REPORT_TEMPLATE.md).

Local:
1. pasta de relatórios do SDD, se existir e for claramente a casa de relatórios;
2. senão, raiz do repositório.

Nome:
`AUDITORIA_SDD_<AAAA-MM-DD>.md`

Crie esse arquivo somente depois de toda a análise estar pronta e somente se ele ainda não existir.

### 7. Verificação final

Antes de concluir:
1. confirme que nenhum arquivo existente foi alterado;
2. confirme que somente o relatório final novo foi criado;
3. confirme que cada achado contém evidência;
4. confirme que rótulos e ações usam apenas os valores permitidos;
5. confirme que dúvidas não comprovadas ficaram fora da tabela de achados;
6. mostre no chat o sumário executivo e o caminho do relatório;
7. repita: `nenhuma alteração foi feita — a faxina em si é decisão humana.`

## Validações e checklist de qualidade

- [ ] O SDD principal foi resumido antes dos achados.
- [ ] Todos os itens do harness entraram no inventário.
- [ ] Cada item tem caminho, tipo, propósito e idioma/origem aparente.
- [ ] Referências cruzadas foram medidas por evidência objetiva.
- [ ] A última mudança Git foi coletada quando o histórico está disponível.
- [ ] Paths citados foram verificados antes de acusar deriva.
- [ ] Itens raros por design foram tratados como dúvida quando necessário.
- [ ] Cada achado usa somente rótulos permitidos.
- [ ] Cada achado cita evidência concreta e, quando útil, linha.
- [ ] Cada recomendação usa somente ações permitidas.
- [ ] O relatório tem as seis seções obrigatórias.
- [ ] O sumário executivo tem no máximo 10 linhas.
- [ ] Nenhum arquivo existente foi alterado.
- [ ] O relatório final não sobrescreveu arquivo pré-existente.
- [ ] A mensagem final afirma explicitamente que a faxina depende de decisão humana.

## Tratamento de exceções

- **Sem Git disponível** → marque recência como `não verificável`; não invente data.
- **Sem diretório de relatórios/logs** → não trate ausência de sinal como prova isolada de desuso.
- **Item sem referências, mas aparentemente sazonal/release-only** → mover para “Dúvidas”.
- **Dois documentos parecem duplicados, mas não há evidência suficiente de precedência** → `AMBÍGUO` somente se disputarem objetivamente o mesmo papel; caso contrário, “Dúvidas”.
- **Path citado contém variável/glob** → resolva somente se houver contexto inequívoco; caso contrário, “Dúvidas”.
- **Arquivo muito grande/binário** → inventarie, mas registre limitação de leitura.
- **Repositório com milhares de artefatos de processo** → o cruzamento de referências do
  `collect_evidence.py` é quadrático: cada item é procurado no corpo de todos os outros.
  Medido: ~0,5 s para 27 itens; acima de ~5.000 arquivos em pastas como `sdd/` ou `reports/`
  ele deixa de terminar em tempo útil. Nesse caso **não espere o script**: rode-o apontando
  para um subdiretório por vez (por exemplo só `.claude/commands` e `.claude/agents`), ou
  faça o inventário com `git ls-files` e meça referências com `git grep -c`. O script é um
  acelerador opcional — a auditoria não depende dele.
- **`REPORT_PATH` já existe** → não sobrescreva e não escolha silenciosamente outro nome.
- **Comando necessário teria efeito colateral** → não execute; registre a limitação em “Dúvidas”.

## Examples

### Exemplo de achado válido

| Item | Rótulo(s) | Evidência | Recomendação |
|---|---|---|---|
| `.claude/commands/old-release.md` | OBSOLETO, CONFLITANTE | Linha 18 grava specs em `docs/specs/`, enquanto o SDD principal define `.claude/sdd/specs/`; o path antigo não existe; último commit: `2025-11-03`. | APOSENTAR |

### Exemplo que deve virar dúvida

Um agente tem zero referências de entrada e nenhuma menção recente em logs, mas sua descrição diz que só é usado no release anual. Não classifique como `NÃO UTILIZADO` com certeza; registre em “Dúvidas para o dono do repo”.

---

Parte do SDD Open by RDD — https://github.com/robertodiasduarte/sdd-open
