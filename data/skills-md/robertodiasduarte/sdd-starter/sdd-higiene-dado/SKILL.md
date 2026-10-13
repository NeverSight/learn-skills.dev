---
name: sdd-higiene-dado
license: MIT
description: "Instala, com o OK explícito de quem usa o computador, um alarme de commit (pre-commit do git) que recusa o commit quando encontra CPF ou CNPJ com dígito verificador válido, arquivo de senhas (.env), certificado com chave privada (.pfx, .p12, .pem) ou planilha nova, explica por que e como corrigir, cita git commit --no-verify e diz como desinstalar. Use quando o usuário quiser proteger o repositório contra dado de cliente ou certificado A1 indo para o git, ao preparar a máquina do escritório para trabalhar com SDD, ou quando um commit for recusado por este alarme. Não se aplica a períodos (não consulta norma nem calcula). Não conserta histórico do git, não revoga certificado, não lê planilha .xlsx por dentro, não dá parecer sobre LGPD ou sigilo profissional; para diagnosticar o ambiente sem instalar nada, use sdd-checar-ambiente."
metadata:
  author: Roberto Dias Duarte
  methodology: Metodologia de Roberto Dias Duarte
  version: "1.0.0"
  updated: "2026-10"
---

# Higiene de dado

Na primeira resposta desta skill, comece com esta linha, uma vez só:
`sdd-higiene-dado v1.0.0 · out/2026 · versão atual: https://github.com/robertodiasduarte/sdd-starter/releases/latest`

Um alarme que roda a cada `git commit` no computador de quem trabalha com dado de cliente. Ele
não impede o trabalho: recusa o commit suspeito, explica, e deixa a pessoa decidir.

## Quick start

`SKILL_ROOT` é a pasta que contém este `SKILL.md` (`.claude/skills/sdd-higiene-dado/` ou
`.agents/skills/sdd-higiene-dado/`, no projeto ou na pasta global do agente). De dentro da pasta
do projeto:

```bash
bash "$SKILL_ROOT/scripts/alarme.sh" verificar     # só lê
bash "$SKILL_ROOT/scripts/alarme.sh" instalar      # só depois do OK explícito
bash "$SKILL_ROOT/scripts/alarme.sh" desinstalar
```

## Quando usar / Quando não usar

Usar para:
- instalar o alarme num projeto, com o OK da pessoa;
- explicar um commit recusado pelo alarme e como corrigir;
- desinstalar o alarme;
- dizer se o alarme já está instalado e em qual versão.

Não usar para (e dizer isso ao usuário):
- apagar arquivo, tirar do histórico ou reescrever commits — entregue o comando, quem roda é a pessoa;
- revogar certificado, trocar senha ou mexer em conta externa;
- ler CPF dentro de `.xlsx`, `.xls` ou `.ods`, ou varrer commits antigos — o alarme olha só o que está
  indo no commit atual;
- parecer sobre LGPD, sigilo profissional ou responsabilidade do contador;
- diagnóstico geral do ambiente — isso é a `sdd-checar-ambiente`, que só lê.

## Dados necessários

- Um terminal com bash e git, aberto na pasta do projeto (Claude Code, Codex, ou o terminal da
  pessoa). No macOS e no Linux já existe; no Windows, o Git Bash que vem com o Git for Windows.
- Que a pasta seja um repositório git (`alarme.sh` diz se não for).
- O OK explícito da pessoa antes de `instalar`. Silêncio, "ok" a outra pergunta ou um pedido antigo
  não são OK.

Sem terminal (claude.ai ou ChatGPT na web), esta skill não consegue instalar nem verificar nada: diga
isso em uma frase e indique rodar a skill no Claude Code ou no Codex, de dentro da pasta do projeto.
Não entregue o conteúdo do alarme para a pessoa colar à mão.

## Procedimento passo a passo

1. **Verificar.** Rode `bash "$SKILL_ROOT/scripts/alarme.sh" verificar` e leia o estado:
   - *nenhum alarme instalado* — siga para o passo 2;
   - *o alarme desta skill já está instalado* — diga a versão instalada; instalar de novo atualiza;
   - *outro alarme* (husky, lefthook, `core.hooksPath`, pre-commit escrito à mão) — **não instale**.
     Mostre o que o script disse, inclusive a linha para acrescentar à mão no alarme existente, e pare.
2. **Explicar e pedir o OK.** Em poucas linhas, sem jargão:
   - o que o alarme recusa: CPF ou CNPJ válidos nas linhas novas; `.env` (exceto `.env.example` e
     `.env.sample`); `.pfx`, `.p12` e `.pem` com chave privada; planilha nova (`.xlsx`, `.xls`, `.ods`,
     `.csv`) de qualquer tamanho;
   - que ele grava um único arquivo, `.git/hooks/pre-commit`, que vale para todas as frentes do projeto
     e não vai para o GitHub;
   - que, depois de conferir, dá para gravar mesmo assim com `git commit --no-verify`;
   - como desinstalar.

   Termine com a pergunta: **"Posso instalar o alarme neste projeto?"** e aguarde a resposta.
3. **Instalar** só com um sim a essa pergunta: `bash "$SKILL_ROOT/scripts/alarme.sh" instalar`.
   Repasse a saída: onde ficou, a versão, `--no-verify` e o comando de desinstalar.
4. **Quando um commit for recusado**, leia a mensagem com a pessoa: qual arquivo, qual linha, o que foi
   achado (o número aparece mascarado). Proponha a correção da própria mensagem (`git restore --staged`,
   `.gitignore`, trocar por dado fictício). **Nunca rode `git commit --no-verify` por conta própria**:
   só quando a pessoa disser, para aquele commit, que conferiu e quer gravar.
5. **Desinstalar** quando a pessoa pedir: `bash "$SKILL_ROOT/scripts/alarme.sh" desinstalar`. O script
   remove só o alarme desta skill; se o arquivo for de outra origem, recusa e não mexe.

## Validações e checklist de qualidade

- [ ] Rodei `verificar` antes de qualquer `instalar`.
- [ ] Pedi o OK com a pergunta do passo 2 e recebi um sim a ela.
- [ ] Não instalei por cima de outro alarme nem mexi em `core.hooksPath`.
- [ ] Ao relatar um commit recusado, não escrevi o CPF/CNPJ inteiro na conversa.
- [ ] Não usei `--no-verify` sem o pedido da pessoa para aquele commit.
- [ ] Disse como desinstalar.

Testes automatizados (para quem mantém a skill, não para o aluno):
`python3 -B -m unittest discover -s "$SKILL_ROOT/tests" -p "test_*.py"`.

## Tratamento de exceções

- **Fora de um repositório git:** o script sai com código 1 e diz isso; oriente abrir o terminal na
  pasta do projeto (ou `git init`, se o projeto ainda não tem git).
- **Outro alarme existente:** código 2; não instalar; mostrar a linha para acrescentar à mão.
- **Alarme acusou um número que não é CPF/CNPJ** (ex.: um telefone de 11 dígitos cujo dígito verificador
  coincide, cerca de 1 em 100): explique que é coincidência possível; a pessoa confere e, se for o caso,
  usa `--no-verify` naquele commit.
- **Planilha de exemplo legítima** (fictícia, sem dado de cliente): mesmo caminho — conferir e
  `--no-verify`.
- **Arquivo em UTF-16** (alguns "Texto Unicode" do Excel): o git o trata como binário e o alarme não lê
  o conteúdo; ainda pega pelo nome se for planilha nova.
- **CNPJ alfanumérico:** não é reconhecido nesta versão.

## Examples

**Positivo (sintético).** Pessoa: "quero proteger este projeto contra dado de cliente no git".
Rodar `verificar` → "nenhum alarme instalado". Explicar em quatro itens, perguntar "Posso instalar o
alarme neste projeto?". Pessoa: "pode". Rodar `instalar` e repassar o caminho, a versão, `--no-verify`
e como desinstalar.

**Commit recusado (sintético).** O alarme mostra `clientes.csv: planilha nova` e
`notas.md:12: CPF 123.***.***-09`. Propor `git restore --staged "clientes.csv"`, acrescentar ao
`.gitignore` e trocar a linha 12 por um CPF fictício. Não rodar `--no-verify`.

**Contraexemplo.** O projeto usa husky (`core.hooksPath = .husky/_`). `verificar` sai com código 2.
Não instalar; mostrar a linha a acrescentar em `.husky/pre-commit` e parar.

**Fora do escopo.** "O certificado A1 já foi para o GitHub, apaga do histórico pra mim." Responder com o
texto de recusa abaixo e indicar que a medida que protege é revogar o certificado com a autoridade
certificadora e emitir outro — apagar o histórico não desfaz cópias já feitas.

## Texto canônico de recusa

- "Esta skill instala e explica o alarme de commit; não altera o histórico do git. O comando é este, e
  quem decide rodar é você: …"
- "Revogar certificado ou trocar senha é feito por você, no emissor ou no serviço; esta skill não faz."
- "Sem terminal nesta conversa não consigo instalar nem verificar o alarme. Rode esta skill no Claude
  Code ou no Codex, de dentro da pasta do projeto."
- "Não tenho seu OK para instalar. Posso instalar o alarme neste projeto?"

## Scripts determinísticos

- `scripts/alarme.sh` — `verificar` (só lê), `instalar`, `desinstalar`. Nunca sobrescreve alarme de
  outra origem. Códigos de saída: 0 feito/informação, 2 recusado por outro alarme, 1 fora de repositório.
- `scripts/pre-commit.sh` — o alarme em si; é a fonte copiada para `.git/hooks/pre-commit` com a
  marca e a versão. Usa só bash, git e awk.

## Inventário do bundle

- `SKILL.md` — este procedimento.
- `scripts/alarme.sh`, `scripts/pre-commit.sh` — ver acima.
- `tests/test_alarme.py` — testes de detecção e de instalação (CPF/CNPJ gerados em tempo de execução).
- `references/COMO_FUNCIONA.md` — explicação para quem decide usar.
- `references/RUNTIME_COMPATIBILITY.md` — onde funciona e onde não.
- `references/ESCOPO_CONFIRMADO.md` — o escopo aprovado desta versão.
- `evals/cases.json` — cenários de comportamento para rodar no agente.
- `manifest.json`, `CHANGELOG.md`, `agents/openai.yaml`.

## Metodologia e autoria

Esta skill foi construída com a metodologia de Roberto Dias Duarte.

---

Parte do SDD Starter by RDD — https://github.com/robertodiasduarte/sdd-starter
