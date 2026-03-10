---
name: zapret-openwrt-guide
description: "Полная русскоязычная справка по проекту zapret-openwrt: Anti-DPI утилита для OpenWrt роутеров. Используй этот скилл при любых вопросах о zapret-openwrt — архитектура проекта, конфигурация, стратегии обхода DPI, веб-интерфейс LuCI, скрипты, обновление, диагностика, custom.d хуки, списки хостов, nfqws параметры, сервис-менеджмент через procd. Также используй при разработке: добавлении новых стратегий, модификации UI, написании custom.d скриптов, отладке проблем. Триггерится на слова: zapret, nfqws, DPI desync, обход блокировок, антиблокировка, стратегии zapret, hostlist, autohostlist."
---

# Zapret-OpenWrt: Полная справка

## Что такое Zapret

Zapret — это Anti-DPI (Deep Packet Inspection) утилита для OpenWrt роутеров. Это **не VPN** — zapret не меняет IP-адрес и не скрывает трафик. Вместо этого он модифицирует сетевые пакеты, чтобы обойти системы глубокой инспекции пакетов (DPI).

**Репозиторий:** https://github.com/remittor/zapret-openwrt
**Upstream:** https://github.com/bol-van/zapret
**Текущая версия:** v72.20260226

## Архитектура проекта

Проект состоит из двух пакетов:

| Пакет | Назначение |
|-------|-----------|
| `zapret` | Основной пакет: демон nfqws, конфиги, скрипты, ipset-списки |
| `luci-app-zapret` | Веб-интерфейс для управления через LuCI |

### Структура на роутере

```
/opt/zapret/
├── nfq/nfqws              # Основной демон DPI desync
├── ip2net/ip2net           # Конвертер IP в подсети
├── mdig/mdig               # DNS-утилита
├── config                  # Рабочий конфиг (runtime)
├── config.default          # Шаблон по умолчанию
├── def-cfg.sh              # Стратегии и дефолты
├── sync_config.sh          # Синхронизация UCI -> config
├── restore-def-cfg.sh      # Сброс настроек
├── update-pkg.sh           # Обновление пакетов
├── dwc.sh                  # DPI-чекер
├── comfunc.sh              # Общие функции
├── init.d.sh               # Init-скрипт (procd)
├── ipset/                  # Списки хостов и IP
│   ├── zapret-hosts-google.txt
│   ├── zapret-hosts-user.txt
│   ├── zapret-hosts-user-exclude.txt
│   ├── zapret-hosts-auto.txt
│   ├── zapret-ip-exclude.txt
│   ├── zapret-ip-user.txt
│   ├── zapret-ip-user-exclude.txt
│   └── cust[1-4].txt
├── files/fake/             # Шаблоны поддельных пакетов (.bin)
└── init.d/openwrt/custom.d/  # Пользовательские скрипты хуки
    ├── 10-script.sh
    ├── 20-script.sh
    ├── 50-script.sh        # Пример: Discord/STUN
    ├── 60-script.sh
    └── 90-script.sh
```

### Конфигурационная система

Zapret использует **двойную систему конфигурации:**

1. **UCI конфиг** (`/etc/config/zapret`) — хранит настройки, редактируемые через LuCI
2. **Основной конфиг** (`/opt/zapret/config`) — используется демоном nfqws

При каждом старте/рестарте вызывается `sync_config.sh`, который синхронизирует значения из UCI в основной конфиг.

---

## Быстрый старт

1. Установить пакеты `zapret` и `luci-app-zapret`
2. Открыть LuCI: **Services -> Zapret -> Service**
3. Нажать **Reset settings** и выбрать стратегию (рекомендуется `v6_by_StressOzz` или `v7_by_StressOzz`)
4. Нажать **Enable** и **Start**
5. Проверить работу через **Diagnostics -> Sites check**

---

## Конфигурация

Подробная справка по всем параметрам конфигурации: прочитай файл `references/config.md` в директории этого скилла.

Ключевые группы параметров:
- **Firewall**: FWTYPE, POSTNAT, FLOWOFFLOAD, INIT_APPLY_FW
- **Сеть**: DISABLE_IPV4, DISABLE_IPV6, FILTER_TTL_EXPIRED_ICMP
- **NFQWS**: NFQWS_ENABLE, NFQWS_PORTS_TCP/UDP, NFQWS_OPT, connbytes (PKT_OUT/IN)
- **Фильтрация**: MODE_FILTER (hostlist/autohostlist), FILTER_MARK
- **AutoHostList**: RETRANS_THRESHOLD, FAIL_THRESHOLD, FAIL_TIME
- **Логирование**: DAEMON_LOG_ENABLE, DAEMON_LOG_SIZE_MAX, DAEMON_LOG_FILE
- **Прочее**: WS_USER, DISABLE_CUSTOM, DESYNC_MARK

## Стратегии DPI-обхода

Подробное описание всех стратегий: прочитай файл `references/strategies.md` в директории этого скилла.

Доступные стратегии (определены в `def-cfg.sh`):

| Стратегия | Порты TCP | Порты UDP | Особенности |
|-----------|-----------|-----------|-------------|
| empty | 80,443 | 443 | Пустая, без desync |
| v1_by_StressOzz | 80,443 | 443 | fake,multidisorder + QUIC fake |
| v2_by_StressOzz | 80,443 | 443 | fake,fakeddisorder + seqovl |
| v3_by_StressOzz | 80,443 | 443 | Как v2, другой TLS-шаблон (t2.bin) |
| v4_by_StressOzz | 80,443 | 443 | fake,multisplit + 3 секции --new |
| v5_by_StressOzz | 80,443 | 443 | ip-id=zero + multisplit |
| v6_by_StressOzz | 80,443,2053,2083,2087,2096,8443 | 443,19294-19344,50000-50100 | Discord + STUN поддержка |
| v7_by_StressOzz | 80,443,2053,2083,2087,2096,8443 | 443,19294-19344,50000-50100 | Улучшенная v6, больше repeats |
| v9_by_StressOzz | 80,443,2053,2083,2087,2096,8443 | 443,19294-19344,50000-50100 | hostfakesplit вариант |
| ALT7_by_Flowseal | 80,443 | 443 | ip-id=zero, multisplit + seqovl |
| TLS_AUTO_ALT3_by_Flowseal | 80,443 | 443 | fooling=ts, больше repeats |

**Стратегия по умолчанию:** `v6_by_StressOzz`

## Веб-интерфейс LuCI

Подробная справка по UI: прочитай файл `references/ui.md` в директории этого скилла.

LuCI-интерфейс доступен по пути **Services -> Zapret** и содержит 5 страниц:

1. **Service** (`service.js`) — управление сервисом, статус, кнопки enable/disable/start/stop/restart/reset, диагностика, обновление
2. **Settings** (`settings.js`) — настройки в 5 вкладках: Main settings, NFQWS options, AutoHostList, Host lists, custom.d
3. **Log** (`dmnlog.js`) — просмотр логов демонов в реальном времени (polling каждую секунду)
4. **Diagnostics** (`diagnost.js`) — DPI check и Sites check через `dwc.sh`
5. **Updater** (`updater.js`) — проверка и установка обновлений с GitHub

## Скрипты

Подробная справка по скриптам: прочитай файл `references/scripts.md` в директории этого скилла.

| Скрипт | Назначение |
|--------|-----------|
| `comfunc.sh` | Общие функции: пути, PID, валидация конфига, init_before_start |
| `init.d.sh` | Procd init-скрипт (START=21, USE_PROCD=1) |
| `sync_config.sh` | UCI -> config синхронизация при start/restart |
| `def-cfg.sh` | Определения стратегий и дефолтных значений |
| `restore-def-cfg.sh` | Сброс конфигурации к умолчаниям |
| `update-pkg.sh` | Обновление пакетов с GitHub (опции: -c, -p, -u, -f, -t) |
| `dwc.sh` | DPI-чекер (TCP 16-20 тест, проверка сайтов) |
| `script-exec.sh` | Запуск скриптов в фоне с логированием |
| `renew-cfg.sh` | Обновление конфига при загрузке |
| `uci-def-cfg.sh` | Создание UCI-конфига при установке |

## Списки хостов и IP

| Файл | Назначение | Формат |
|------|-----------|--------|
| `zapret-hosts-google.txt` | YouTube/Google домены (дефолт) | По одному домену на строку |
| `zapret-hosts-user.txt` | Пользовательские домены `<HOSTLIST>` | По одному домену на строку |
| `zapret-hosts-user-exclude.txt` | Исключения из обработки | По одному домену на строку |
| `zapret-hosts-auto.txt` | Автоматически обнаруженные хосты | Заполняется при autohostlist |
| `zapret-ip-exclude.txt` | Исключаемые IP-адреса/подсети | IP или CIDR (128.199.0.0/16) |
| `zapret-ip-user.txt` | Пользовательские IP | IP или CIDR |
| `zapret-ip-user-exclude.txt` | Исключаемые пользовательские IP | IP или CIDR |
| `cust[1-4].txt` | Кастомные файлы (до 4 штук) | Произвольный |

### Плейсхолдеры в NFQWS_OPT

- `<HOSTLIST>` — подставляет `--hostlist` и `--hostlist-exclude` из стандартных списков, работает в режимах hostlist и autohostlist
- `<HOSTLIST_NOAUTO>` — то же, но `zapret-hosts-auto.txt` добавляется как обычный (не авто) список

## Custom.d скрипты

Хуки выполняются при старте/стопе сервиса в порядке номера:
- `10-script.sh` — ранний init
- `20-script.sh` — ранняя основная фаза
- `50-script.sh` — основная фаза (пример: Discord/STUN4ALL)
- `60-script.sh` — поздняя основная фаза
- `90-script.sh` — финальная фаза

Включаются через параметр `DISABLE_CUSTOM=0` (в UI: вкладка custom.d -> "Use custom.d scripts").

## Сборка и CI/CD

Сборка выполняется через GitHub Actions (`.github/workflows/build.yml`):
- Триггер: push тега `v[0-9]+*` или ручной запуск
- Матрица: 30+ архитектур (ARM, MIPS, x86_64, RISC-V)
- Две ветки OpenWrt: IPK (v24.10.x) и APK (v25.12.x)
- Релизы публикуются на gh-pages как JSON для автообновления

## Решение проблем

Подробный troubleshooting: прочитай файл `references/troubleshooting.md` в директории этого скилла.

**Быстрые проверки:**
1. Статус сервиса: LuCI -> Services -> Zapret -> Service (или `service zapret status`)
2. DPI-проверка: Diagnostics -> DPI check
3. Логи: включить DAEMON_LOG_ENABLE=1, смотреть на вкладке Log
4. Проверка сайтов: Diagnostics -> Sites check с выбором DNS

## Для разработчиков

### Структура исходников

```
zapret-openwrt/
├── zapret/                     # Основной пакет
│   ├── Makefile                # OpenWrt SDK build
│   ├── config.default          # Шаблон конфига
│   ├── *.sh                    # Shell-скрипты
│   ├── custom.d/               # Хуки custom.d
│   ├── files/fake/             # .bin шаблоны пакетов
│   ├── ipset/                  # Списки хостов/IP
│   └── patches/                # Патчи для upstream
└── luci-app-zapret/            # LuCI пакет
    ├── Makefile
    ├── htdocs/luci-static/resources/view/zapret/
    │   ├── env.js              # Пути и константы
    │   ├── tools.js            # Утилиты, RPC, диалоги
    │   ├── service.js          # Страница управления сервисом
    │   ├── settings.js         # Страница настроек
    │   ├── diagnost.js         # Диагностика
    │   ├── updater.js          # Обновление
    │   ├── dmnlog.js           # Просмотр логов
    │   └── styles.css          # Стили
    └── root/usr/share/
        ├── luci/menu.d/        # Определение меню
        └── rpcd/acl.d/         # ACL-правила
```

### Добавление новой стратегии

1. Добавить блок `if [ "$strat" = "имя_стратегии" ]` в `def-cfg.sh`
2. Определить порты TCP/UDP и NFQWS_OPT с параметрами desync
3. Стратегия автоматически появится в UI на странице Service -> Reset settings

### Ключевые файлы для UI-разработки

- `env.js` — все пути, имена файлов, URL-ы (загружается первым)
- `tools.js` — RPC-вызовы, POLLER, fileEditDialog, longstrEditDialog, decode_svc_info
- Каждая страница — отдельный view, наследующий `view.extend()` или `baseclass.extend()`
