---
name: transcrever-groq
description: Transcreve vídeos e áudios com a API da Groq (Whisper) e gera texto, legendas SRT e JSON com tempo por palavra (inclusive no formato do Remotion). Na primeira vez o próprio agente instala o que falta, pede a chave da Groq no chat e a guarda no cofre do sistema (Windows Credential Manager ou macOS Keychain); depois nunca mais pede, em nenhum projeto, sem arquivo .env. Use sempre que o usuário pedir para transcrever, legendar, gerar SRT, extrair o texto ou os tempos das palavras de um vídeo/áudio (mp4, mov, mp3, wav...), achar o melhor trecho de um vídeo pela fala, ou falar em Groq, Whisper, chave/API key da Groq, GROQ_API_KEY, "configurar a transcrição" ou "trocar a chave". Funciona em qualquer pasta.
---

# Transcrever com Groq

Transforma um arquivo de vídeo ou áudio em transcrição com o tempo de cada palavra. Quem usa costuma ser leigo: **você, o agente, faz toda a configuração**; a pessoa só precisa enviar a chave da Groq no chat, uma vez.

`<skill>` abaixo é a pasta onde esta skill está instalada. Use `python` (Windows) ou `python3` (macOS); a skill cria sozinha um ambiente próprio para as bibliotecas, então não instale nada com `pip` por conta própria.

## Fluxo

### 1. Ver o que já está pronto

```
python <skill>/scripts/configurar.py status --json
```

Saída: `{"configurada": true|false, "origem": "cofre"|"variavel"|null, "ambiente_pronto": ...}`. Nunca mostra a chave. Se `configurada` for `true`, vá direto ao passo 4.

### 2. Preparar o computador (só se faltar algo)

Rode `python <skill>/scripts/configurar.py ambiente`. Ele confere Python (3.10 ou mais novo) e FFmpeg e cria o ambiente próprio. Se faltar alguma coisa, explique em uma frase o que é e peça permissão antes de instalar:
- Python: Windows `winget install Python.Python.3.13`; macOS `brew install python` (ou python.org).
- FFmpeg (extrai o áudio do vídeo): Windows `winget install Gyan.FFmpeg`; macOS `brew install ffmpeg`.
- Depois de instalar com `winget`, o PATH só atualiza em terminais novos: abra um novo shell ou peça para reabrir o app, e rode `ambiente` de novo para confirmar.

### 3. Pedir e guardar a chave da Groq

Se `configurada` for `false`, diga algo simples como:

> Para transcrever eu preciso da sua chave da Groq. Entre em console.groq.com/keys, clique em **Create API Key** e cole a chave aqui no chat. Eu guardo no cofre do seu computador, e você não precisa mandar de novo em nenhum projeto.

Quando a pessoa enviar, guarde pela **entrada padrão**, nunca como argumento do comando (argumentos aparecem na lista de processos):

- Bash / macOS / Git Bash: `printf '%s' 'CHAVE' | python <skill>/scripts/configurar.py setup --stdin`
- PowerShell: `'CHAVE' | python <skill>/scripts/configurar.py setup --stdin`

O comando valida a chave com a Groq antes de guardar. Resultado pelo código de saída:

| Código | Significado | O que fazer |
|---|---|---|
| 0 | Guardada | Confirme com `status` e siga. |
| 1 | A Groq recusou a chave (ou veio vazia) | Peça para conferir/copiar de novo ou gerar outra. |
| 3 | Não deu para validar (sem internet, limite, instabilidade) | Tente de novo em instantes; só use `--salvar-sem-validar` se a internet estiver ok e a Groq instável. |
| 2 | Problema com o cofre do sistema (bloqueado, indisponível) | Leia a mensagem impressa e `references/solucao-de-problemas.md`. Alternativa: variável de ambiente `GROQ_API_KEY`. |

Cuidados com a chave, por serem um segredo da conta da pessoa:
- só passe a chave pelo pipe acima; não escreva em arquivo, `.env`, código, commit, nem em outro lugar;
- não repita a chave nas suas respostas;
- avise uma vez, em uma frase, que a chave ficou na conversa e que dá para revogá-la quando quiser em console.groq.com/keys (e, se preferir, criar uma chave só para isso).

Se o comando disser "A chave ja esta configurada" e a pessoa quer trocar, use `update --stdin` (mesma forma). Trocar também é o caminho quando a transcrição falhar com HTTP 401.

### 4. Transcrever

```
python <skill>/scripts/transcrever.py "<arquivo>" --saida "<pasta>" [--nome NOME] [--contexto "termos"] [--inicio T] [--fim T]
```

- `--saida` é obrigatório: a ferramenta não escolhe onde gravar. Se a pessoa não disser, use uma pasta do projeto atual (ex.: `./transcricoes`) e informe qual usou.
- Cria `<saida>/<nome>/` com `transcricao.txt`, `legendas.srt`, `transcricao.json` (palavras com tempo) e `legendas.remotion.json`. Detalhes em `references/saidas.md`. Ao terminar, resuma o resultado e diga onde estão os arquivos.
- `--contexto` ajuda com grafia de nomes e termos técnicos ("Claude Code, VPS, Railway"). Não elimina erros: revise nomes próprios.
- `--inicio/--fim` aceitam segundos, `MM:SS` ou `HH:MM:SS`. Em arquivos longos os tempos das palavras podem escorregar alguns décimos de segundo; para sincronia precisa (cortes, legendas animadas), transcreva só o trecho com `--inicio/--fim`.
- Vídeos longos são divididos em blocos de até 10 minutos. Se a conexão cair, rode o mesmo comando de novo: o que já foi feito fica em cache e retoma. `--refazer` ignora o cache.
- O arquivo original nunca é alterado; só áudio mono 16 kHz é enviado à Groq.

### 5. Outros pedidos

| Pedido | Comando |
|---|---|
| Ver se está configurada | `configurar.py status` |
| Trocar a chave | `configurar.py update --stdin` (chave pelo pipe) |
| Apagar a chave do computador | `configurar.py remove --sim` |
| Consertar o ambiente | `configurar.py ambiente --forcar` |

A pessoa também pode rodar `configurar.py setup` sozinha num terminal; aí a chave é digitada de forma oculta.

## Erros comuns

- "Chave da Groq nao configurada": volte ao passo 3.
- "Groq retornou HTTP 401": chave inválida ou revogada, faça `update`.
- "Groq retornou HTTP 429": limite de uso; espere e repita (o progresso fica em cache).
- "ffmpeg nao encontrado": passo 2.
- Cofre bloqueado/indisponível, Python antigo: `references/solucao-de-problemas.md`.

A variável de ambiente `GROQ_API_KEY` também funciona (útil em servidores), mas o cofre tem prioridade quando as duas existem.
