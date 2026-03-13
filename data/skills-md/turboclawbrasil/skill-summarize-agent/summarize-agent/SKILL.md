---
name: summarize-agent
description: Sumarização universal via sub-agents (web, YouTube, podcasts, X, Instagram, PDFs).
metadata:
  emoji: 📝
  requires:
    python: ">=3.8"
  install:
    - id: yt-dlp
      kind: pip
      package: yt-dlp
      optional: true
      label: Para suporte a YouTube
    - id: poppler
      kind: apt
      package: poppler-utils
      optional: true
      label: Para suporte a PDFs
    - id: html2text
      kind: apt
      package: html2text
      optional: true
      label: Para extração HTML
---

# summarize-agent

Sumarização multi-formato usando sub-agents OpenClaw. Funciona com qualquer conteúdo: URLs, YouTube, podcasts, redes sociais, PDFs.

## Uso

```bash
# Via CLI OpenClaw
openclaw skill summarize-agent --url "https://exemplo.com"

# Ou diretamente
python3 ~/.openclaw/workspace/skills/summarize-agent/summarize-agent.py "URL"
```

## Exemplos

```bash
# Artigo web
summarize-agent "https://techcrunch.com/..."

# Vídeo YouTube
summarize-agent "https://youtube.com/watch?v=..."

# Podcast
summarize-agent "/path/para/podcast.mp3"

# Post do X
summarize-agent "https://x.com/usuario/status/..."

# Com tamanho específico
summarize-agent "URL" --length short
summarize-agent "URL" --length long
```

## Como funciona

1. **Detecção automática**: Identifica tipo pela URL/extensão
2. **Extração**: Obtém texto/transcrição do conteúdo
3. **Sumarização**: Sub-agent your-llm-model processa e resume

## Tipos suportados

| Tipo | Método de extração | Status |
|------|-------------------|--------|
| Web | `web_fetch` nativo | ✅ Pronto |
| YouTube | `yt-dlp` legendas | ✅ Pronto |
| Áudio/Podcast | Whisper API | ✅ Pronto |
| X/Twitter | Nitter/scraping | ⚠️ Instável |
| Instagram | API necessária | ⚠️ Requer serviço |
| PDF | `pdftotext` | ✅ Pronto |
| Vídeo | Whisper API | ✅ Pronto |

## Arquitetura

```
Input → Detecta Tipo → Extrai Conteúdo → Sub-agent (your-llm-model) → Resumo
```

O sub-agent recebe o conteúdo bruto e gera o resumo estruturado, permitindo:
- Processamento paralelo
- Fallback automático
- Isolamento de erros
