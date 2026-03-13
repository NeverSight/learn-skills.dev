---
name: vibe-deploy
description: Автоматический деплой любых проектов (frontend, backend, fullstack) на Timeweb Cloud. Поддерживает два пути — App Platform (PaaS) и облачный сервер (VPS). Включает настройку доменов, DNS, SSL, баз данных, Docker, CI/CD (GitHub Actions). Используй этот скилл, когда пользователь хочет задеплоить, развернуть, опубликовать проект, сайт или приложение на Timeweb Cloud, или когда упоминается timeweb, twc, деплой.
---

# Timeweb Deploy — Скилл для деплоя проектов на Timeweb Cloud

## Обзор

Этот скилл позволяет ИИ-агенту самостоятельно задеплоить любой проект пользователя на Timeweb Cloud — от простого статического сайта до fullstack-монорепозитория с базой данных.

**Язык общения с пользователем**: русский.

**Структура скилла:**
- `scripts/` — Python-скрипты для API, анализа проекта, управления state-файлом
- `templates/` — Dockerfile, GitHub Actions workflows, Nginx, systemd
- `reference/` — справочники по API, ошибкам, пресетам

---

## Быстрый режим: возобновление и обновление

### Возобновление прерванного деплоя

Перед началом работы проверь, существует ли `deploy-state.md` в корне проекта. Если существует:

1. Прочитай `deploy-state.md`
2. Выполни `python3 scripts/deploy_state.py verify` — узнай незавершённые шаги
3. Предложи пользователю:

> Нашёл незавершённый деплой. Вот что осталось:
> {список незавершённых шагов}
>
> Продолжить с того места, где остановились, или начать заново?

Если пользователь хочет продолжить — перейди к первому незавершённому шагу, не повторяя уже выполненные.

### Быстрое обновление (передеплой)

Если пользователь говорит "обнови проект", "передеплой", "обнови код на сервере" — и `deploy-state.md` существует с заполненным IP сервера:

1. Прочитай state-файл: IP, стратегию, Docker/PM2/systemd
2. **Не проходи все 10 шагов.** Выполни только обновление:

**VPS + Docker:**
```bash
ssh -i ~/.ssh/timeweb_deploy root@<IP> "cd /opt/app && git pull origin main && docker compose down && docker compose up -d --build"
```

**VPS + PM2:**
```bash
ssh -i ~/.ssh/timeweb_deploy root@<IP> "cd /opt/app && git pull origin main && npm ci --omit=dev && npm run build && pm2 restart app"
```

**VPS + systemd:**
```bash
ssh -i ~/.ssh/timeweb_deploy root@<IP> "cd /opt/app && git pull origin main && source venv/bin/activate && pip install -r requirements.txt && systemctl restart app"
```

**App Platform:**
```bash
python3 scripts/timeweb_api.py app-status --id <app_id>
# Если auto-deploy включён — push в main уже обновил. Просто сообщи.
# Если нет — python3 scripts/timeweb_api.py <trigger deploy через API>
```

### Просмотр существующих ресурсов

Если пользователь спрашивает "какие серверы/приложения у меня есть":
```bash
python3 scripts/timeweb_api.py list-servers
python3 scripts/timeweb_api.py list-apps
python3 scripts/timeweb_api.py list-dbs
```

---

## Проверка Python перед началом работы

Скрипты скилла требуют Python 3. **Перед первым вызовом любого скрипта** проверь наличие:

```bash
python3 --version 2>/dev/null || python --version 2>/dev/null
```

**Если Python не найден** — спроси пользователя:

> Для работы скилла деплоя нужен Python 3, но он не установлен. Установить?
>
> **macOS:** `brew install python3` (нужен Homebrew) или скачать с https://www.python.org/downloads/
> **Windows:** `winget install Python.Python.3.12` или скачать с https://www.python.org/downloads/
> **Linux:** `sudo apt-get install -y python3` (Ubuntu/Debian) или `sudo dnf install -y python3` (Fedora)

**Не устанавливай без разрешения.** Дождись подтверждения пользователя.

После установки проверь ещё раз: `python3 --version`

**Примечание:** На Windows Python может быть доступен как `python` вместо `python3`. Если `python3` не найден, но `python --version` показывает 3.x — используй `python` во всех командах вместо `python3`.

Также для `scripts/github_api.py set-secret` / `set-all-secrets` нужна библиотека PyNaCl:
```bash
pip install pynacl
```
Установи её только если пользователь выбрал автоматическую настройку GitHub Secrets. Не ставь заранее.

---

## ⚠️ Критические правила поведения

Эти правила имеют наивысший приоритет и должны соблюдаться на всех этапах:

1. **Не обещай того, что не сделаешь.** Если сказал пользователю "настрою Docker" — ОБЯЗАН настроить Docker. Если сказал "настрою CI/CD" — ОБЯЗАН настроить CI/CD. Нельзя пообещать в плане и молча пропустить.

2. **Не принимай решения за пользователя молча.** Всегда спрашивай: Docker или без Docker? Git или SCP? App Platform или VPS? Домен или без? CI/CD или без? Не выбирай за него.

3. **Сначала читай данные проекта, потом спрашивай.** Если .env файл существует — прочитай его. Не спрашивай значения переменных, которые уже есть. Спрашивай только отсутствующие.

4. **Не делай бесконечных циклов ожидания.** Максимум 5 попыток после начального ожидания. Если ресурс не готов за ~3-4 минуты — сообщи пользователю. (Лимит зашит в `scripts/timeweb_api.py`)

5. **Всегда проверяй IPv4 явно.** Timeweb Cloud может создать сервер только с IPv6. (Автоматическая проверка зашита в `scripts/timeweb_api.py wait-server`)

6. **Предпочитай Git над SCP.** Если в проекте настроен Git — используй `git clone` для загрузки на сервер, а не `scp`.

7. **НЕ ПРОПУСКАЙ ШАГИ.** Каждый шаг из обязательного чеклиста ниже должен быть выполнен или осознанно пропущен по решению пользователя.

8. **Различай ЛОКАЛЬНЫЕ и СЕРВЕРНЫЕ операции.** Всё, что связано с Git (commit, push, создание файлов проекта) — делай ЛОКАЛЬНО. На удалённый сервер по SSH заходи только для: установки ПО, запуска приложения, настройки systemd/nginx/docker, генерации deploy key. НИКОГДА не создавай файлы проекта на удалённом сервере и не пытайся пушить оттуда.

9. **Проверяй Git в начале.** Перед деплоем определи: инициализирован ли Git? Есть ли remote? Какой хостинг? Есть ли незакоммиченные изменения? (Автоматически через `scripts/analyze_project.py`)

10. **Если есть токен — используй его по максимуму.** Если пользователь дал GitHub PAT — используй его для ВСЕХ операций с GitHub API: добавление секретов, создание deploy key, push. Не проси пользователя делать вручную то, что можешь автоматизировать. (Используй `scripts/github_api.py`)

11. **Безопасность прежде всего.** НИКОГДА не создавай публичные репозитории — только приватные. Перед пушем в существующий публичный репозиторий — ОБЯЗАТЕЛЬНО предупреди пользователя.

---

## Система отслеживания состояния (State-файл)

**В начале деплоя** создай `deploy-state.md` через скрипт. Обновляй после КАЖДОГО значимого шага. Перечитывай перед каждым следующим шагом.

```bash
# Создать state-файл из результатов анализа проекта
python3 scripts/deploy_state.py init --project-json '<JSON из analyze_project.py>'

# Обновить поле
python3 scripts/deploy_state.py update --key "Стратегия" --value "VPS"

# Отметить шаг выполненным
python3 scripts/deploy_state.py check --step "API-токен"

# Отметить шаг пропущенным
python3 scripts/deploy_state.py check --step "Домен" --skip

# Проверить незавершённые шаги перед финальной проверкой
python3 scripts/deploy_state.py verify
```

### Правила работы со state-файлом

1. **Создай в начале деплоя** — сразу после анализа проекта
2. **Обновляй после каждого шага** — записывай результаты (ID серверов, IP, решения)
3. **Перечитывай перед новым шагом** — особенно если контекст уже длинный
4. **Проверяй перед завершением** — `python3 scripts/deploy_state.py verify`
5. **Добавь в .gitignore** — скрипт делает это автоматически
6. **Пункты "Домен" и "CI/CD" начинаются как "НЕ СПРОШЕН"** — ты не можешь поставить им `[x]`, пока не спросишь пользователя

---

## Общий алгоритм работы

```
0. Создать deploy-state.md, проверить Git
1. Анализ проекта пользователя
2. Получение/проверка API-токена Timeweb Cloud
3. Проверка баланса аккаунта
4. Выбор стратегии деплоя (App Platform vs VPS)
5. Подготовка проекта (Docker, env, конфиги)
6. Создание инфраструктуры (сервер/приложение, БД, S3)
7. Деплой проекта
8. Настройка домена, DNS, SSL ← ОБЯЗАТЕЛЬНО СПРОСИТЬ
9. Настройка CI/CD ← ОБЯЗАТЕЛЬНО СПРОСИТЬ
10. Финальная проверка и выдача результатов пользователю
```

### ОБЯЗАТЕЛЬНЫЙ ЧЕКЛИСТ — пройди ВСЕ пункты

**После завершения деплоя (шаг 7), но ДО финальной проверки (шаг 10), ты ОБЯЗАН пройти этот чеклист. Каждый пункт требует либо действия, либо явного ответа пользователя "не нужно". Сверяйся с deploy-state.md.**

```
ЧЕКЛИСТ ПОСЛЕ ДЕПЛОЯ:
□ Docker — Спросил пользователя? Если выбрал Docker — настроил?
□ Домен — Спросил: "Есть ли домен? Нужен ли домен?"
  □ Если есть домен → настроил DNS-записи
  □ Если нужно купить → дал инструкцию/ссылку
  □ Если не нужен → зафиксировал, что работаем по IP
□ SSL — Если есть домен → настроил Let's Encrypt (certbot)
□ CI/CD — Спросил: "Настроить автодеплой?"
  □ Если App Platform + автодеплой уже включён → сообщил "CI/CD уже работает", Actions НЕ НУЖНЫ
  □ Если App Platform + автодеплой выключен → предложил варианты (провайдер / Actions / вручную)
  □ Если VPS + да → создал .github/workflows/deploy.yml ЛОКАЛЬНО
  □ Если VPS + да → настроил GitHub Secrets через API (если есть PAT)
  □ Если нет → зафиксировал
□ deploy-state.md обновлён, все пункты закрыты
□ Все пункты пройдены → можно переходить к финальной проверке
```

**ВАЖНО:** Не выводи этот чеклист пользователю. Это твой внутренний контрольный список. Пользователю задавай вопросы по каждому пункту естественным языком.

**Порядок вопросов после деплоя:**

После того как приложение запущено и работает, задай пользователю 2 вопроса (можно в одном сообщении):

> Приложение запущено и работает ✅
>
> Осталось два вопроса:
>
> 1. **Домен:** У тебя есть свой домен для проекта? Если да — скинь его, я настрою DNS и SSL. Если нет — хочешь купить через Timeweb или пока работать по IP?
>
> 2. **CI/CD:** *(формулируй в зависимости от стратегии)*
>    - **Если App Platform** и автодеплой включён: «CI/CD уже работает — при push в main App Platform автоматически пересоберёт приложение.»
>    - **Если App Platform** и автодеплой выключен: «Автодеплой не работает, потому что репо подключён по URL. Могу настроить через GitHub Actions или помочь переподключить через провайдер. Что предпочитаешь?»
>    - **Если VPS**: «Настроить автоматический деплой при push в GitHub (GitHub Actions)? При каждом push в main проект будет обновляться на сервере автоматически.»

---

## Шаг 1. Анализ проекта

### 1.0. Анализ и создание state-файла

```bash
# Автоматический анализ проекта
python3 scripts/analyze_project.py /path/to/project

# Результат — JSON с полями: runtime, framework, app_type, port,
# databases, docker, env, git, commands, monorepo
```

Из результата создай state-файл:
```bash
python3 scripts/deploy_state.py init --project-json '<JSON>'
```

### 1.0.1. Если Git не инициализирован или нет remote

**Git обязателен только для App Platform.** Для VPS можно деплоить без Git — через SCP (копирование файлов напрямую).

Если Git отсутствует — сообщи:

> В проекте не настроен Git-репозиторий. Это не проблема — есть два варианта:
>
> **A)** Создать репозиторий на GitHub — нужно для App Platform и для CI/CD (автодеплой при push)
> **B)** Обойтись без Git — загружу файлы на сервер напрямую через SCP (только VPS, без CI/CD)

**Если пользователь выбрал A:**

```bash
# ВСЕГДА приватный — безопасность!
python3 scripts/github_api.py create-repo --name <repo-name>
```

**Перед пушем в СУЩЕСТВУЮЩИЙ репозиторий** — проверь видимость:
```bash
python3 scripts/github_api.py check-visibility --owner <owner> --repo <repo>
```

Если публичный — **ОБЯЗАТЕЛЬНО** предупреди:
> ⚠️ Внимание: репозиторий `<owner>/<repo>` — **публичный**. Весь код будет виден всем.
> Убедись, что в проекте нет секретов. Продолжить? (да/нет)

**Если пользователь выбрал B:** запомни в state-файле, что деплой через SCP. На шаге 9 (CI/CD) учти, что без Git автодеплой невозможен — предупреди пользователя.

### 1.1. Показать карточку проекта

После анализа покажи пользователю краткую сводку и попроси подтвердить:

```
📦 Анализ проекта:
• Тип: fullstack (React + Express)
• Рантайм: Node.js 20
• Менеджер пакетов: pnpm
• Фреймворк: React (фронт) + Express (бэк)
• БД: PostgreSQL (через Prisma)
• Docker: отсутствует (нет .dockerignore)
• Env-переменные: DATABASE_URL, JWT_SECRET, PORT
• Порт: 3000
• Директория сборки: dist
```

**Обязательно** после после подтверждения обнови `deploy-state.md` через скрипт.

---

## Шаг 2. API-токен Timeweb Cloud

Спроси пользователя и **сразу дай инструкцию по получению**:

> У тебя уже есть аккаунт и API-токен Timeweb Cloud? Если да — отправь мне токен, я сохраню его для работы.
>
> Если нет — получи его за 2 минуты:
> 1. Зарегистрируйся (если нет аккаунта): https://timeweb.cloud/my
> 2. Открой раздел **API и Terraform**: https://timeweb.cloud/my/api-keys
> 3. Нажми «Создать» → имя: `deploy-bot` → срок: «Без ограничений»
> 4. Скопируй токен и отправь мне

Сохрани и проверь:
```bash
mkdir -p ~/.config/timeweb
```
Затем используй инструмент Write, чтобы записать файл `~/.config/timeweb/.env` с содержимым:
```
TIMEWEB_CLOUD_TOKEN=<токен>
```
```bash
chmod 600 ~/.config/timeweb/.env
export TIMEWEB_CLOUD_TOKEN=$(grep TIMEWEB_CLOUD_TOKEN ~/.config/timeweb/.env | cut -d= -f2)
python3 scripts/timeweb_api.py check-token
```
**⚠️ НИКОГДА не передавай токен напрямую в команду `echo` или `export` — он попадёт в историю shell и будет виден через `ps`.**

**Обязательно** обнови `deploy-state.md` через скрипт.

---

## Шаг 3. Проверка баланса

```bash
python3 scripts/timeweb_api.py balance
```

Если баланс < 100 руб:
> ⚠️ На балансе {balance} руб. Рекомендуется минимум 100-200 руб. Пополни: https://timeweb.cloud/my/billing

**Обязательно** обнови `deploy-state.md` через скрипт.

---

## Шаг 4. Выбор стратегии деплоя

Предложи пользователю выбор с рекомендацией:

> Какой способ деплоя предпочитаешь?
>
> **A) App Platform** — автодеплой из Git, всё настроено автоматически
> **B) Облачный сервер (VPS)** — полный контроль, настройка вручную
>
> Для твоего проекта я рекомендую **{рекомендация на основе анализа}**, потому что {причина}.

**Путь A (App Platform)** подходит: проект в GitHub/GitLab, стандартный фреймворк (см. `reference/presets-guide.md`), не нужен root-доступ.

**⚠️ App Platform ТРЕБУЕТ Git-репозиторий.** Если пользователь выбрал App Platform, но проект не в Git — объясни и спроси разрешение:

> App Platform работает только с Git-репозиторием — он берёт код оттуда и автоматически собирает проект. Сейчас у тебя нет репозитория. Могу создать приватный репозиторий на GitHub и загрузить туда код. Создать?

Если пользователь согласился:
```bash
python3 scripts/github_api.py create-repo --name <repo-name>
git init && git remote add origin <url> && git add . && git commit -m "Initial commit" && git push -u origin main
```
Если отказался — предложи переключиться на VPS (путь B), где Git не обязателен.
Только после наличия репозитория переходи к шагу 6A.

**Путь B (VPS)** подходит: нужен root, нестандартная конфигурация, SQLite, нет Git, fullstack-монорепо на одном сервере. Git не обязателен — можно загрузить код через SCP.

**Обязательно** обнови `deploy-state.md` через скрипт.

---

## Шаг 5. Подготовка проекта

### 5.1. Docker (если нет Dockerfile)

**Спроси пользователя:**
> В проекте нет Dockerfile. Как хочешь деплоить?
>
> **A) С Docker** (рекомендую) — я создам Dockerfile, окружение будет воспроизводимым
> **B) Без Docker** — чистая установка: apt + venv/nvm + systemd/pm2 + nginx

**Если выбрал Docker** — используй шаблон из `templates/dockerfiles/`, подставив порт и команды проекта:
- Node.js backend → `templates/dockerfiles/node-backend.Dockerfile`
- Python → `templates/dockerfiles/python-fastapi.Dockerfile`
- React/Vue/Svelte/Angular (статика) → `templates/dockerfiles/react-nginx.Dockerfile`
- Go → `templates/dockerfiles/go.Dockerfile`
- PHP → `templates/dockerfiles/php-nginx.Dockerfile`
- Bun → `templates/dockerfiles/bun.Dockerfile`
- Deno → `templates/dockerfiles/deno.Dockerfile`
- Fullstack монорепо → `templates/dockerfiles/docker-compose.fullstack.yml`

**⚠️ КРИТИЧЕСКИ ВАЖНО: Подстановка переменных в шаблонах.**
Шаблоны содержат плейсхолдеры вида `${NODE_VERSION}`, `${PORT}` и т.д. Это **НЕ** Docker ARG/ENV — агент ОБЯЗАН заменить их на конкретные значения перед записью Dockerfile. **Не копируй шаблон напрямую — прочитай его, замени все `${...}` на значения из анализа проекта, и запиши результат в `Dockerfile` проекта.**

**Подстановка переменных в шаблоны:**
1. **Версия рантайма** (`${NODE_VERSION}`, `${GO_VERSION}`, `${PHP_VERSION}`): из `runtime_version` анализа, или дефолт (Node: 20, Go: 1.22, PHP: 8.3, Python: 3.12)
2. **Менеджер пакетов** (`${INSTALL_CMD}`): из `package_manager` анализа:
   - npm → `npm ci`
   - yarn → `yarn install --frozen-lockfile`
   - pnpm → `pnpm install --frozen-lockfile`
   - bun → `bun install --frozen-lockfile`
3. **Директория сборки** (`${BUILD_OUTPUT_DIR}`): из `build_output_dir` анализа (Vite→`dist`, CRA→`build`, Next.js→`.next`, Gatsby→`public`, и т.д.)
4. **Порт** (`${PORT}`): из `port` анализа

**Если в проекте нет `.dockerignore`** — создай из шаблона `templates/dockerfiles/.dockerignore`. Это КРИТИЧЕСКИ ВАЖНО: без `.dockerignore` в Docker-образ попадут `.env` (секреты!), `node_modules`, `.git`.

**Если пользователь выбрал Docker — весь дальнейший пайплайн ДОЛЖЕН использовать Docker.** Не переключайся молча на вариант без Docker.

**ВАЖНО для App Platform:** В Dockerfile обязательно `EXPOSE <порт>`.

**ВАЖНО для fullstack на App Platform:** App Platform не имеет типа `fullstack`. Fullstack-приложения (Next.js, Nuxt.js, SvelteKit, Remix) деплоятся как тип `backend`.

### 5.2. Переменные окружения

Данные уже есть в результате `analyze_project.py` (поле `env`). Алгоритм:
1. Если все переменные заполнены — «Все env-переменные из .env подхвачены ✅»
2. Если чего-то не хватает — спроси только недостающие:

> В .env найдены: ✅ DATABASE_URL, ✅ JWT_SECRET
> Не хватает: ❌ SMTP_HOST, ❌ SMTP_PASSWORD — отправь значения или скажи, что email не используется.

Для секретов (JWT_SECRET и т.п.) — предложи сгенерировать: `openssl rand -hex 32`

**Обязательно** обнови `deploy-state.md` через скрипт.

---

## Шаг 6. Создание инфраструктуры

### ПУТЬ A: App Platform

```bash
# Получить доступные фреймворки и пресеты
python3 scripts/timeweb_api.py app-frameworks
python3 scripts/timeweb_api.py app-presets

# Создать приложение
python3 scripts/timeweb_api.py create-app \
  --name <имя> --type <backend|frontend> \
  --preset <preset_id> --framework <framework_id> \
  --repo-url <git-url> --branch main \
  --env KEY1=val1 KEY2=val2 \
  --build-cmd "npm run build" --run-cmd "npm start"

# Проверить статус / логи
python3 scripts/timeweb_api.py app-status --id <app_id>
python3 scripts/timeweb_api.py app-logs --id <app_id>
```

### Оценка стоимости (перед созданием ресурсов)

**Перед созданием любого ресурса** сообщи пользователю примерную стоимость:

> Создаю ресурсы:
> - Сервер (пресет X): ~Y руб/мес
> - БД (пресет X): ~Y руб/мес (если нужна)
> - **Итого: ~Z руб/мес**
>
> Продолжить?

Стоимость пресетов можно получить из `server-presets` / `app-presets` / `db-presets` (поля `price` или `price_monthly`). Не создавай ресурсы без подтверждения пользователя.

### ПУТЬ B: Облачный сервер (VPS)

```bash
# Выбрать пресет и ОС (рекомендации — см. reference/presets-guide.md)
python3 scripts/timeweb_api.py server-presets
python3 scripts/timeweb_api.py os-images

# Создать SSH-ключ
ssh-keygen -t ed25519 -f ~/.ssh/timeweb_deploy -N "" -q
python3 scripts/timeweb_api.py upload-ssh-key --name deploy-agent-key --pub-key-path ~/.ssh/timeweb_deploy.pub

# Создать сервер
python3 scripts/timeweb_api.py create-server --name <project>-server --preset <id> --os <id> --ssh-keys <key_id>

# Дождаться готовности + автоматическое получение IPv4
python3 scripts/timeweb_api.py wait-server --id <server_id>
```

#### Безопасность VPS (обязательно)

**Сразу после готовности сервера**, перед установкой ПО, выполни базовую защиту:

```bash
ssh -o StrictHostKeyChecking=accept-new -i ~/.ssh/timeweb_deploy root@<IP> << 'SECURITY'
# Создать пользователя app (приложение не должно работать от root)
useradd -r -m -d /opt/app -s /bin/bash app

# Firewall — открыть только нужные порты
apt-get install -y ufw
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw --force enable

# Защита от брутфорса SSH
apt-get install -y fail2ban
systemctl enable fail2ban
systemctl start fail2ban
SECURITY
```

**Что делает эта настройка (объясни пользователю точно):**
- Создаётся пользователь `app` — **процессы приложения** (через systemd `User=app`, PM2, Docker) запускаются от него, а не от root
- Настраивается firewall (ufw) и защита от брутфорса (fail2ban)
- **SSH-подключения для управления сервером остаются от `root`** — это необходимо для установки ПО, управления сервисами, nginx и т.д. Это стандартная практика для VPS-администрирования.

**⚠️ Не говори пользователю фразы вроде "деплою без root" или "убрал root".** Правильная формулировка: «Приложение будет работать от непривилегированного пользователя `app`, а не от root — это защищает систему в случае уязвимости.»

**ВАЖНО:** Все systemd-сервисы из `templates/systemd/` используют `User=app`. Файлы в `/opt/app` должны принадлежать `app:app`.

#### Подготовка сервера через SSH

**С Docker:**
```bash
ssh -o StrictHostKeyChecking=accept-new -i ~/.ssh/timeweb_deploy root@<IP> << 'SETUP'
apt-get update && apt-get upgrade -y
curl -fsSL https://get.docker.com | sh
apt-get install -y docker-compose-plugin nginx certbot python3-certbot-nginx
mkdir -p /opt/app && chown app:app /opt/app
SETUP
```

**Без Docker (Node.js):**
```bash
ssh root@<IP> << 'SETUP'
apt-get update && apt-get upgrade -y
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
nvm install ${NODE_VERSION:-20} && npm install -g pm2
apt-get install -y nginx certbot python3-certbot-nginx
mkdir -p /opt/app && chown app:app /opt/app
SETUP
```

**Без Docker (Python):**
```bash
ssh root@<IP> << 'SETUP'
apt-get update && apt-get upgrade -y
apt-get install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx
mkdir -p /opt/app && chown app:app /opt/app
SETUP
```

**Без Docker (Go):**
```bash
ssh root@<IP> << 'SETUP'
apt-get update && apt-get upgrade -y
# Установить Go
wget -q https://go.dev/dl/go${GO_VERSION:-1.23}.0.linux-amd64.tar.gz
tar -C /usr/local -xzf go*.tar.gz && rm go*.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> /etc/profile
export PATH=$PATH:/usr/local/go/bin
apt-get install -y nginx certbot python3-certbot-nginx
mkdir -p /opt/app && chown app:app /opt/app
SETUP
```

**Без Docker (PHP):**
```bash
ssh root@<IP> << 'SETUP'
apt-get update && apt-get upgrade -y
apt-get install -y php${PHP_VERSION:-8.3}-fpm php${PHP_VERSION:-8.3}-cli php${PHP_VERSION:-8.3}-mbstring \
  php${PHP_VERSION:-8.3}-xml php${PHP_VERSION:-8.3}-curl php${PHP_VERSION:-8.3}-mysql \
  nginx certbot python3-certbot-nginx unzip
# Composer
curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
mkdir -p /opt/app && chown app:app /opt/app
SETUP
```

#### Загрузить проект на сервер

Проверь state-файл — есть ли у проекта Git remote.

**Если Git remote есть:**
> Как загрузить проект на сервер?
> **A) Через Git** (рекомендую) — клонирую репозиторий. Удобнее для обновлений и CI/CD.
> **B) Через SCP** — загружу файлы напрямую.

**Если Git remote нет:**
> Проект не привязан к Git-репозиторию. Есть два варианта:
> **A) Создать репозиторий на GitHub** (рекомендую) — код будет в Git, удобнее обновлять, можно настроить CI/CD.
> **B) Загрузить файлы через SCP** — быстрее, но без Git не будет автодеплоя.

Если пользователь выбрал создать репо:
```bash
python3 scripts/github_api.py create-repo --name <repo-name>
# Затем локально:
git init && git remote add origin <url> && git add . && git commit -m "Initial commit" && git push -u origin main
```

**Git**: `ssh root@<IP> "cd /opt/app && git clone <repo-url> ."`
**SCP**: `scp -r -i ~/.ssh/timeweb_deploy /path/to/project/* root@<IP>:/opt/app/`

#### Запустить проект

**С Docker:** `ssh root@<IP> "cd /opt/app && docker compose up -d --build"`

**Node.js + PM2:** `ssh root@<IP> "cd /opt/app && npm ci --omit=dev && npm run build && pm2 start dist/index.js --name app && pm2 save && pm2 startup"`

**Python + systemd:** Скопируй шаблон `templates/systemd/python-gunicorn.service` в `/etc/systemd/system/app.service`, подставив порт. Затем:
```bash
ssh root@<IP> "cd /opt/app && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && pip install gunicorn && chown -R app:app /opt/app && systemctl daemon-reload && systemctl enable app && systemctl start app"
```

**Go + systemd:** Скомпилируй, скопируй шаблон `templates/systemd/go-app.service` в `/etc/systemd/system/app.service`. Затем:
```bash
ssh root@<IP> "cd /opt/app && go build -o server . && chown -R app:app /opt/app && systemctl daemon-reload && systemctl enable app && systemctl start app"
```

**PHP + nginx:** Для Laravel/Symfony используй PHP-FPM + nginx. Скопируй код, настрой nginx:
```bash
ssh root@<IP> "cd /opt/app && composer install --no-dev --optimize-autoloader && chown -R www-data:www-data /opt/app/storage /opt/app/bootstrap/cache 2>/dev/null || true && systemctl restart php8.3-fpm && systemctl reload nginx"
```

#### Настроить Nginx

Используй шаблон из `templates/nginx/reverse-proxy.conf`, подставив домен/IP и порт. Скопируй на сервер:
```bash
ssh root@<IP> << 'NGINX'
cat > /etc/nginx/sites-available/app << 'CONF'
<содержимое шаблона с подставленными значениями>
CONF
ln -sf /etc/nginx/sites-available/app /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
NGINX
```

**Обязательно** обнови `deploy-state.md` через скрипт.

---

## Шаг 7. Создание базы данных (если требуется)

- **SQLite** — не требует отдельной БД, работает на диске (только VPS)
- **PostgreSQL, MySQL, MongoDB, Redis** — управляемая БД через API (рекомендуется) или на VPS

```bash
# Пресеты и создание управляемой БД
python3 scripts/timeweb_api.py db-presets
python3 scripts/timeweb_api.py create-db --name <project>-db --type <postgres|mysql|mongodb|redis> --preset <id>
```

Формат DATABASE_URL — см. `reference/presets-guide.md`.

После создания БД — запусти миграции, если есть (Prisma: `npx prisma migrate deploy`, Django: `python manage.py migrate`, Alembic: `alembic upgrade head`).

**Обязательно** обнови `deploy-state.md` через скрипт.

---

## Шаг 8. Домен, DNS, SSL

**⚠️ ОБЯЗАТЕЛЬНЫЙ ШАГ — НЕ ПРОПУСКАЙ.**

### 8.1. Спросить про домен

**Не каждому проекту нужен домен.** Если это бэкенд-сервис, бот, демон, внутренний API — домен может быть не нужен. Учитывай тип проекта при формулировке вопроса.

**Если App Platform:** у проекта уже есть бесплатный технический домен (вида `app-name.timeweb.cloud`) с SSL. Сообщи об этом:

> Твой проект уже доступен по адресу `<технический_домен>` с SSL — это бесплатный домен от App Platform.
> Хочешь привязать свой домен? Если нет — можно оставить как есть.

**Если VPS:**

> У тебя есть свой домен для этого проекта?
> **A)** Да → скинь его, я настрою DNS и SSL
> **B)** Нет, хочу купить → помогу через Timeweb (от ~200 руб/год в зоне .ru)
> **C)** Нет, обойдусь без домена → ок, проект доступен по IP

### 8.2. Привязка домена

```bash
# Добавить домен в Timeweb
python3 scripts/timeweb_api.py add-domain --fqdn <domain.com>

# DNS-записи (VPS)
python3 scripts/timeweb_api.py add-dns --fqdn <domain.com> --subdomain @ --type A --value <IP>
python3 scripts/timeweb_api.py add-dns --fqdn <domain.com> --subdomain www --type A --value <IP>
```

Если домен не в Timeweb — скажи сменить NS-серверы:
> Измени NS у регистратора на: `ns1.timeweb.ru`, `ns2.timeweb.ru`, `ns3.timeweb.cloud`, `ns4.timeweb.cloud`

**Альтернатива:** пользователь может вручную создать A-запись у текущего регистратора.

### 8.3. Покупка домена

```bash
python3 scripts/timeweb_api.py check-domain --fqdn <domain.com>
```

Если API не поддерживает покупку — дай ссылку: https://timeweb.cloud/my/domains/order

### 8.4. SSL (VPS)

```bash
ssh root@<IP> "certbot --nginx -d <domain> -d www.<domain> --non-interactive --agree-tos -m <email>"
ssh root@<IP> '(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -'
```

App Platform выпускает SSL автоматически.

**Обязательно** обнови `deploy-state.md` через скрипт.

---

## Шаг 9. CI/CD

**⚠️ ОБЯЗАТЕЛЬНЫЙ ШАГ — НЕ ПРОПУСКАЙ.**

### 9.1. App Platform

Проверь автодеплой: `python3 scripts/timeweb_api.py app-status --id <app_id>` → поле `is_auto_deploy`.

- **Если `true`** → «CI/CD уже работает нативно. GitHub Actions не нужны.»
- **Если `false`** → предложи: A) переподключить через провайдер, B) GitHub Actions, C) оставить как есть.
- Для варианта B — используй шаблон `templates/workflows/app-platform.yml`.

### 9.2. VPS

> Настроить автоматический деплой при push в GitHub (GitHub Actions)?

**⚠️ ВАЖНО: Перед добавлением workflow-файла сначала настрой deploy key на сервере (шаг 9.3) и GitHub Secrets (шаг 9.4). Иначе первый push с workflow вызовет ошибку — `git pull` на сервере не сможет авторизоваться.**

Если да — скопируй подходящий шаблон из `templates/workflows/`:
- Docker → `vps-docker.yml`
- Node.js + PM2 → `vps-node-pm2.yml`
- Python + systemd → `vps-python-systemd.yml`
- Go + systemd → `vps-go.yml`
- PHP + nginx → `vps-php.yml`

**Создай файл ЛОКАЛЬНО:**
```bash
mkdir -p .github/workflows
cp <шаблон> .github/workflows/deploy.yml
git add .github/workflows/deploy.yml
git commit -m "Add CI/CD: auto-deploy to Timeweb VPS on push"
git push origin main
```

### 9.3. Deploy key на сервере (для git pull)

```bash
# Сгенерировать ключ НА СЕРВЕРЕ
ssh root@<IP> "ssh-keygen -t ed25519 -f /root/.ssh/github_deploy -N '' -q"
DEPLOY_PUB_KEY=$(ssh root@<IP> "cat /root/.ssh/github_deploy.pub")

# Настроить SSH-конфиг
ssh root@<IP> << 'SSHCONF'
cat >> /root/.ssh/config << 'EOF'
Host github.com
  IdentityFile /root/.ssh/github_deploy
  StrictHostKeyChecking no
EOF
chmod 600 /root/.ssh/config
SSHCONF

# Переключить remote на SSH
ssh root@<IP> "cd /opt/app && git remote set-url origin git@github.com:<user>/<repo>.git"
```

**Если есть GitHub PAT** — добавь deploy key автоматически:
```bash
python3 scripts/github_api.py add-deploy-key --owner <owner> --repo <repo> --pub-key-path /tmp/deploy_pub_key
```

**Если нет PAT** — дай инструкцию:
> Добавь deploy key: `https://github.com/<user>/<repo>/settings/keys/new`
> Title: `timeweb-server`, Key: `<ключ>`, Allow write access: НЕ нужно

### 9.4. GitHub Secrets

**Если есть PAT — добавь автоматически:**
Создай временный файл с секретами через инструмент Write (например `/tmp/gh_secrets.json`):
```json
{"SERVER_IP": "<IP>", "SSH_PRIVATE_KEY": "<содержимое ~/.ssh/timeweb_deploy>"}
```
```bash
python3 scripts/github_api.py set-all-secrets --owner <owner> --repo <repo> --secrets-file /tmp/gh_secrets.json
rm -f /tmp/gh_secrets.json
```
**⚠️ Не передавай секреты через `--secrets` в CLI — они будут видны через `ps aux`.**

**Если нет PAT** — дай инструкцию:
> Добавь секреты: Settings → Secrets → Actions → New:
> - `SERVER_IP` — `<IP>`
> - `SSH_PRIVATE_KEY` — содержимое `~/.ssh/timeweb_deploy`

### 9.5. Запрос GitHub PAT (если нужен)

> Для автоматической настройки CI/CD нужен GitHub PAT с правами `repo` и `admin:repo_hook`.
> Создай: https://github.com/settings/tokens/new — Scopes: `repo`, Expiration: 30 days
> Отправь токен, и я настрою всё автоматически. Или скажи "вручную".

Сохрани PAT: используй инструмент Write, чтобы записать токен в `~/.config/timeweb/.github_pat`, затем:
```bash
chmod 600 ~/.config/timeweb/.github_pat
```
**⚠️ Не передавай PAT через `echo` в командной строке — он попадёт в историю shell.**

**Обязательно** обнови `deploy-state.md` через скрипт.

---

## Шаг 10. Финальная проверка

**⚠️ ОБЯЗАТЕЛЬНЫЙ ШАГ — НЕ ПРОПУСКАЙ.**

### 10.0. Самопроверка

```bash
python3 scripts/deploy_state.py verify
```

Если есть незавершённые шаги — выполни их СЕЙЧАС.

### 10.1. Проверка доступности

```bash
curl -s -o /dev/null -w "%{http_code}" http://<домен_или_IP>
```

### 10.2. Итоговая информация пользователю

**Покажи ВСЮ информацию, которую пользователю стоит сохранить.** Включай только релевантные блоки (например, блок БД — только если создавалась БД, блок CI/CD — только если настраивался).

```
✅ Деплой успешно завершён!

📍 Доступ к проекту:
   URL: https://<домен> (или http://<IP>:<порт>)

🖥 Сервер:                              ← только для VPS
   IP: <IP>
   ID: <server_id>
   Панель: https://timeweb.cloud/my/servers/<server_id>
   SSH: ssh -i <путь_к_ключу> root@<IP>
   Проект на сервере: /opt/app

🗄 База данных:                          ← только если создавалась
   Тип: <PostgreSQL/MySQL/...>
   Хост: <host>:<port>
   Логин: <login>
   Пароль: <password>
   DATABASE_URL: <полный_connection_string>

🔄 CI/CD:                                ← только если настраивался
   Файл: .github/workflows/deploy.yml
   Триггер: автодеплой при push в main

🔑 Токены и ключи (сохрани!):
   Timeweb API: ~/.config/timeweb/.env
   SSH-ключ: <путь> (например ~/.ssh/timeweb_deploy)
   GitHub PAT: ~/.config/timeweb/.github_pat   ← только если использовался

📋 Полезные команды:
   Подключиться: ssh -i <путь_к_ключу> root@<IP>
   Логи: ssh root@<IP> "<docker compose logs -f | pm2 logs | journalctl -u app -f>"
   Перезапуск: ssh root@<IP> "<docker compose restart | pm2 restart app | systemctl restart app>"
   Обновить код: ssh root@<IP> "cd /opt/app && git pull"
```

После вывода сводки спроси:

> Сохранить эту информацию в файл? Пароль БД и SSH-ключ невозможно восстановить, только пересоздать.

Если пользователь согласился — сохрани сводку в `DEPLOY.md` в корне проекта, добавь в `.gitignore` (файл содержит секреты!) и сообщи путь:

> Сохранено в `DEPLOY.md`. Файл добавлен в `.gitignore`, чтобы секреты не попали в репозиторий.

---

## Обработка ошибок

См. `reference/errors.md` — таблицы ошибок API и деплоя, инструкции по откату.

## Ограничения

1. **Регистрация** — невозможна через API, только через сайт
2. **Оплата** — создание ресурсов списывает средства. Всегда показывай стоимость перед созданием (см. "Оценка стоимости")
3. **Rate limiting** — не более 20 запросов/сек. Добавляй `sleep 1` между массовыми операциями. При 429 — скрипт автоматически повторит через 5 сек (до 3 раз)
4. **API обновляется** — при ошибке проверь документацию (см. `reference/api-endpoints.md`)
5. **Без Kubernetes и балансировщиков** — скилл для простых проектов
6. **SSH** — только для VPS, не для App Platform
7. **Персистентность App Platform** — данные не сохраняются между деплоями, используй S3 или БД
8. **Монорепозитории** — для App Platform укажи путь к подпроекту; для VPS — Docker Compose
9. **Bun/Deno** — определяются анализатором, но App Platform не поддерживает их нативно. Деплой только через Dockerfile
10. **Fullstack на App Platform** — тип `fullstack` не существует в API. Используй `backend` (скрипт конвертирует автоматически)
