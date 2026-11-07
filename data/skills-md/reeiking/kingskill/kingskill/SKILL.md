---
name: kingskill
description: Análise completa de um projeto — construção (build, dependências, configuração), segurança, desempenho, qualidade de código, testes, banco de dados, interface e deploy — com medições antes/depois, busca de skills especializadas no ecossistema skills.sh (via find-skills) e aplicação das melhorias seguras. Use SEMPRE que o usuário disser "analise projeto", "analisar projeto", "análise completa", "auditoria do projeto", "revisa o projeto inteiro", "o que dá para melhorar no projeto" ou pedir para verificar segurança/desempenho/qualidade de um projeto inteiro, mesmo sem citar esta skill.
---

# KingSkill: análise de projeto

Roteiro fixo para auditar um projeto inteiro, achar skills especializadas para os pontos fracos e aplicar melhorias com evidência. Responda no idioma do usuário.

## 0. Qual projeto

- Use o diretório atual se ele for um projeto (tem `package.json`, `Package.swift`, `pyproject.toml`, `supabase/`, `.git` etc.).
- Se não for, ou se o pedido citar um projeto pelo nome ("analise projeto Loja"), procure a pasta nas memórias e nas pastas de projetos do usuário (ex.: `~/Desktop`, `~/Projects`, `~/Developer`, `~/code`). Pergunte só se houver ambiguidade real.
- Leia `CLAUDE.md`, `README` e as memórias do projeto (se houver) antes de tudo. **As restrições das memórias valem mais que as sugestões desta skill** (ex.: projeto só local, não apagar dados de teste, recurso adiado de propósito). Não recomende o que já foi decidido contra.

## 1. Reconhecimento

Levante, sem alterar nada:
- Stack, linguagens, frameworks e versões; gerenciador de pacotes; estrutura de pastas; tamanho (arquivos e linhas por área).
- Como se compila, testa, roda e publica (scripts, CI, Vercel, Supabase local/cloud).
- Estado do git (branch, alterações pendentes). Se houver alterações do usuário não commitadas, não as misture com as suas.

## 2. Linha de base (medir antes de mexer)

Rode o que existir e anote os números: build, testes (quantos passam/falham), lint/typecheck, avisos do compilador, tamanho do bundle, tempo de build, benchmarks já existentes. Se não houver medição para um ponto suspeito, escreva um benchmark ou teste temporário. Sem número, é hipótese: diga isso.

## 3. Análise por área

Percorra todas as áreas de `references/checklist.md`, pulando só as que não se aplicam à stack (diga quais pulou e por quê). Para cada achado registre: área, gravidade (crítico / alto / médio / baixo), arquivo:linha, evidência e correção proposta.

Priorize leitura dos caminhos críticos (o que roda a cada requisição, quadro, evento ou login) em vez de varrer tudo superficialmente.

## 4. Buscar skills especializadas

Para cada área com achados relevantes:
1. Veja primeiro se já existe skill instalada que cubra (lista de skills disponíveis na sessão e `~/.claude/skills`). Skills embutidas úteis: `security-review`, `code-review`, `simplify`, `supabase`, `supabase-postgres-best-practices`, `browser-debug`.
2. Se não houver, siga a skill `find-skills`. Se ela não estiver instalada, instale primeiro (`npx -y skills add vercel-labs/skills --skill find-skills -g -y -a claude-code`) e leia o SKILL.md dela. Requer Node.js (`npx`); sem ele, avise e siga só com as skills já instaladas. Busque com `npx -y skills find "<stack> <área>"` com 2–4 buscas específicas no mesmo comando (filtre a saída com `sed 's/\x1b\[[0-9;]*m//g'`).
3. Verifique qualidade antes de usar: 1K+ instalações, repositório com 100+ estrelas (`gh api repos/<dono>/<repo> --jq .stargazers_count`, ou a página do GitHub se não houver `gh`), atualizado no último ano, autor conhecido.
4. Instale globalmente só para Claude Code: `npx -y skills add <dono/repo> --skill <nome> -g -y -a claude-code`.
5. **Leia o SKILL.md e liste os arquivos da skill antes de usar.** Se tiver scripts executáveis, leia-os; se algo for suspeito (rede, credenciais, apagar arquivos), não use e avise.
6. Aplique o roteiro da skill ao projeto. No máximo 3 skills novas por análise; prefira poucas e boas.

## 5. Aplicar melhorias

Aplique direto, sem perguntar, o que for **seguro e local**: mudanças pequenas, cobertas por teste ou build, reversíveis, dentro do código do projeto. Depois de cada uma, rode testes/build de novo e compare com a linha de base.

**Pergunte antes** de: migrations ou alterações em banco, qualquer coisa em produção (Supabase cloud, Vercel, deploys), apagar dados, trocar dependências grandes ou versão de linguagem/framework, refatorações amplas, mudanças de comportamento visível ao usuário final, commit e push.

Remova benchmarks temporários no final; transforme em teste permanente os que protegem contra regressão de uma melhoria feita.

## 6. Relatório

No terminal, curto e direto:
1. Uma frase com o estado geral do projeto.
2. Tabela de medições antes/depois (só o que foi medido).
3. O que foi corrigido (arquivo, efeito medido).
4. Achados pendentes por gravidade, cada um com a correção proposta e por que não foi aplicado (precisa de aprovação, risco, fora do escopo).
5. Skills instaladas/usadas nesta análise.
6. Próximo passo recomendado (um só), e pergunta se pode commitar/reinstalar/publicar quando fizer sentido.

Se o relatório ficar grande (muitos achados) ou o usuário for mostrar a alguém, ofereça publicar como página.
