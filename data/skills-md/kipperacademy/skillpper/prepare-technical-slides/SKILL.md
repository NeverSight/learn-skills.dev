---
name: prepare-technical-slides
description: Pesquisar e preparar slides de aulas e palestras técnicas em PT-BR, com fontes verificáveis, sequência didática, contexto e um conceito por slide. Preserva o catálogo aprovado e a rastreabilidade de afirmações; usa concept-to-excalidraw para produzir diagramas, imagens e a apresentação nativa editável no Excalidraw.
---

# Preparar slides técnicos

Mantém pesquisa e bibliografia rastreáveis e incorpora as orientações de Fernanda sobre preparação didática dos slides. Trabalhe em PT-BR, a menos que seja solicitado outro idioma.

## Divisão de responsabilidades

- **Esta skill:** pesquisa, tese, duração, contexto, ordem dos conceitos, texto de cada slide, notas da professora, fontes e revisão didática.
- **`concept-to-excalidraw`:** transformar o plano em diagramas e imagens, aplicar o estilo visual e montar/conferir a apresentação com slides nativos do Excalidraw.
- Antes da produção visual, ler a [skill de execução](../concept-to-excalidraw/SKILL.md). Se estiver instalada em outro local, localizar pelo nome exato. Se não estiver disponível, concluir o blueprint e informar que falta essa dependência; não declarar slides gerados.
- Pedido de pesquisa pontual não exige apresentação. Preparar slides não implica gerar código, áudio ou configurar integrações novas.

## Regras inegociáveis

- Pesquise na web antes de afirmar que uma informação é nova, atual, quantitativa ou resultado de pesquisa. Registre a data de acesso.
- Use exclusivamente as fontes do [catálogo aprovado](references/source-catalog.md) como referências da palestra. Não use resultados de busca, resumos de IA ou conhecimento prévio como evidência.
- Em uma palestra, percorra todo o catálogo: busque cada fonte cuja categoria seja pertinente ao tema; quando não houver resultado útil, registre `sem resultado relevante`. Para pedidos rápidos, consulte as fontes mais adequadas, mas nunca fora do catálogo.
- Trate Hacker News, TechCrunch e X como sinais, descoberta de contexto ou opinião. Corrobore afirmações técnicas, de produto ou de mercado com uma fonte primária ou de pesquisa do catálogo sempre que ela existir.
- Não transforme hipótese, opinião ou correlação em fato. Marque como `opinião`, `hipótese`, `evidência preliminar` ou `sem consenso` quando aplicável.
- Não invente autores, datas, resultados, URLs, estatísticas ou citações. Se uma fonte estiver inacessível, anote a limitação e siga com fontes acessíveis.
- Produza a apresentação no Excalidraw por meio de `concept-to-excalidraw`, com slides nativos, diagramas editáveis e revisão em modo de apresentação. A escolha explícita posterior da usuária prevalece sobre este fluxo padrão.

## Escolher o modo de trabalho

### Pesquisa sob demanda

Use quando receber perguntas como “quais referências explicam RAG?”, “há novidades sobre agentes?” ou “me ajude a comprovar esta afirmação”.

1. Identifique a pergunta, o público e o nível técnico a partir do pedido; só peça contexto quando ele mudar materialmente a resposta.
2. Formule consultas curtas em português e inglês, combinando o tema com cada domínio pertinente do catálogo.
3. Priorize: artigos acadêmicos e repositórios de papers; depois laboratórios e documentação técnica; depois análises de especialistas; por último notícias e sinais sociais.
4. Para cada resultado útil, extraia: `S-id`, título, autor ou organização, data de publicação, URL canônica, data de acesso, tipo de evidência, afirmação que ele sustenta e ressalvas.
5. Entregue uma síntese com links, separando fatos sustentados, opiniões e lacunas. Inclua uma seção `Fontes` com a bibliografia completa dos itens usados.

### Construir ou revisar uma palestra

Use quando o pedido incluir roteiro, estrutura, slides, palestra, keynote, apresentação ou revisão de referências.

1. Defina a tese, público, duração e resultado desejado. Se o usuário não fornecer, faça uma suposição explícita e siga.
2. Liste as afirmações técnicas antes de desenhar os slides. Pesquise cada uma e atribua IDs como `S01`, `S02`.
3. Crie o arco: problema → modelo mental → evidência/demonstração → limites e trade-offs → conclusão acionável.
4. Coloque os IDs das fontes que sustentam cada afirmação técnica no próprio slide ou em suas notas. Não deixe números, marcos históricos, comparações, resultados de estudos ou funcionamento de sistemas sem citação.
5. Reserve o último slide substantivo para `Referências bibliográficas`. Ele deve conter todas — e somente — as fontes citadas, em formato completo e legível. Não coloque conteúdo após esse slide, exceto créditos legais obrigatórios.
6. Materialize primeiro um blueprint Markdown seguindo [o modelo](references/blueprint-template.md). Rode o validador antes de gerar ou entregar a apresentação. O script `scripts/validate_references.py` fica no diretório desta skill: localize o caminho onde ela está instalada e execute-o.

```bash
python3 <diretório-desta-skill>/scripts/validate_references.py caminho/da/palestra.md
```

7. Entregue o blueprint à skill `concept-to-excalidraw`, incluindo contexto, conceito central, frase explicativa, mecanismo visual, valores/estados, fontes, notas e ordem de cada slide. Indique quando é preciso exportar imagens além do arquivo editável.
8. Use essa skill para criar a apresentação no Excalidraw. O handoff deve distinguir slides de board: para slides, conferir a lista, a ordem e a navegação nativa; para um pedido explícito de board para vídeo, organizar mecanismos navegáveis por zoom sem impor a grade de slides. Manter a bibliografia e a rastreabilidade em uma área final ou no guia associado nesse modo. Se o acesso ao produto estiver indisponível, preserve o blueprint e os arquivos locais possíveis e informe o estágio real; não afirme que os slides nativos foram conferidos online.
9. Revise cada slide em escala de apresentação: uma ideia central, contexto suficiente, mecanismo evidente, legibilidade e consistência com as fontes. Confira citações e o slide final de referências. Abra os links usados, confirme suporte, data/autor e remova duplicatas.

## Preparação didática dos slides

### Abertura e independência da aula

- Primeiro slide: **capa com tema e tópicos OU breve conceito introdutório**. Não abrir com um exemplo solto como “A regra de matrícula”.
- Não presumir que o aluno assistiu aulas anteriores. Mesmo ao reutilizar uma história, contextualizar sistema, atores, entrada, regra, saída e desafio antes de usar seus nomes de classes.
- Dar base conceitual antes da aplicação: o que o conceito organiza ou resolve, quais são suas partes e relações. A explicação de uma arquitetura não pode ficar inteiramente restrita ao exemplo de matrícula.
- Aproveitar os vídeos de referência quando forem parte do pedido: observar fala e imagens, construção dos diagramas e transições para código. Informar se a análise foi por amostragem.

### Divisão e progressão

- **Um conceito por slide de conteúdo.** Não juntar todas as aplicações de SOLID ou todos os padrões numa tela para substituir suas explicações individuais.
- Capa, contexto, comparação, colaboração e recapitulação podem conter várias peças desde que respondam a uma pergunta central. Reservar a síntese para depois das definições.
- Preferir uma história contínua, com casos concretos, ao longo da aula. Apresentar conceito → contexto → mecanismo → mudança → efeito → síntese, adaptando a ordem à compreensão.
- Usar título explícito e uma frase curta **acima do desenho**. A imagem deve explicar o mecanismo dessa frase. Guardar lembretes de fala nas notas/roteiro, sem lotar a tela.
- Alocar tempo para teoria, transições, previsão e demonstração conforme o pedido mais recente. Não fixar em toda aula a duração ou quantidade de slides de um exemplo anterior.

### Clareza causal e ligação com a prática

- Evitar caixas e setas que apenas nomeiam classes. Planejar o que entra, o que cada parte faz, o que muda e qual efeito resulta.
- Para acoplamento, especificar no blueprint a dependência concreta, a alteração solicitada e o trecho que precisa mudar. O aluno deve enxergar onde existe o acoplamento e por que ele importa.
- Comparar cenários com entradas equivalentes, destacando a variável alterada. Não atribuir a uma interface um efeito causado pela ordem das operações, tratamento de exceção ou conversão de unidade.
- Se houver demo, preparar uma previsão e uma diferença real observável, o momento WOW solicitado por Fernanda. Distinguir resultados esperados de resultados executados.
- Para visuais de código, usar poucas linhas, nomes iguais aos arquivos atuais e montagem explícita: quem instancia/obtém as dependências e quem as recebe. Uma Factory pode ter sua criação detalhada em tela própria.
- Revisar com a pergunta de Fernanda: **o aluno bate o olho, lê a explicação acima e entende como funciona?** Se precisar de uma longa fala para atribuir sentido ao desenho, reformular o plano e pedir a revisão visual à skill de execução.

Consultar os [direcionamentos didáticos](references/direcionamentos-didaticos.md) para a origem dos pedidos e os critérios de revisão. A paleta e os recursos de desenho ficam em `concept-to-excalidraw`.

## Padrão de citações

- Cite no slide com `[S01]` imediatamente após a afirmação ou como rodapé. Para vários suportes, use `[S01, S04]`.
- No slide final, use uma entrada por ID: `- [S01] Autor/organização. “Título”. Publicado em AAAA-MM-DD. URL. Acesso em AAAA-MM-DD.`
- Para paper acadêmico, acrescente versão, venue quando houver, e DOI/arXiv ID se disponível.
- Para post social, preserve o autor, data, URL do post e rotule `opinião` quando não houver uma evidência técnica independente.
- Uma referência pode apoiar mais de um slide; não use uma única referência para justificar alegações que ela não faz.
- No blueprint, slides de título, agenda, transição ou exercício sem alegação técnica devem conter `[sem-afirmacao-tecnica]` para documentar a exceção. Essa marca é de revisão, não texto a exibir ao aluno.

## Critérios de qualidade da pesquisa

- Prefira a fonte original de um resultado: paper para experimento, laboratório para anúncio ou metodologia, documentação oficial para comportamento de produto.
- Dê contexto operacional: condições do experimento, versão do sistema, população/amostra, métricas e limitações relevantes.
- Compare fontes quando houver discordância e explique de onde ela vem; não escolha silenciosamente a que confirma a tese.
- Dê mais espaço às fontes que sustentam a tese central. Um painel de referências não compensa uma narrativa sem evidência.
- Se uma referência for antiga, mantenha-a apenas por valor histórico/fundacional e procure uma atualização no catálogo.

## Entrega esperada

Para pesquisa, entregue: resposta direta, evidências ligadas a cada ponto, limitações e bibliografia.

Para palestra, entregue: premissas, título e tese, sequência de slides com textos/citações, notas de limites e o slide final de referências. Use `concept-to-excalidraw` para criar os diagramas e os slides nativos finais. Entregue o `.excalidraw`, o link editável quando houver e imagens exportadas quando solicitadas. Inclua o resultado do validador e corrija qualquer erro antes da entrega.

## Recursos

- [Catálogo aprovado de fontes](references/source-catalog.md): domínios, perfis e função de cada fonte.
- [Modelo de blueprint](references/blueprint-template.md): formato que o validador lê.
- `scripts/validate_references.py`: verifica o contrato mínimo de citações e bibliografia do blueprint.
