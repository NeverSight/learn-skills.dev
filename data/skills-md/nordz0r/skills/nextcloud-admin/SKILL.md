---
name: nextcloud-admin
description: "Управление Nextcloud через OCS API и WebDAV: файлы, шаринг, пользователи, группы, приложения. Используй этот скилл при ЛЮБЫХ задачах, связанных с Nextcloud — загрузка/скачивание файлов, создание папок, управление доступом (шары, публичные ссылки), администрирование пользователей и групп, управление приложениями. Триггеры: nextcloud, шаринг файлов, облачное хранилище, WebDAV, OCS API, публичная ссылка на файл, управление пользователями nextcloud, загрузить файл в облако, скачать из облака, расшарить файл."
---

# Nextcloud Admin — Управление через API

Скилл для полноценного управления Nextcloud-инстансом через OCS REST API и WebDAV. Все операции выполняются через `curl` из терминала.

## Подключение

Конфигурация берётся из переменных окружения:

| Переменная | Назначение |
|---|---|
| `NEXTCLOUD_URL` | Базовый URL инстанса (например `https://cloud.example.com`) |
| `NEXTCLOUD_USER` | Имя пользователя для аутентификации |
| `NEXTCLOUD_TOKEN` | App-токен пользователя (используется вместо пароля) |
| `NEXTCLOUD_ADMIN_TOKEN` | App-токен администратора (для операций управления пользователями/группами/приложениями) |

Перед выполнением любых операций **всегда** проверяй наличие переменных:

```bash
# Проверка обязательных переменных
if [ -z "$NEXTCLOUD_URL" ] || [ -z "$NEXTCLOUD_USER" ] || [ -z "$NEXTCLOUD_TOKEN" ]; then
  echo "ERROR: Set NEXTCLOUD_URL, NEXTCLOUD_USER, NEXTCLOUD_TOKEN env vars"
  exit 1
fi
```

## Базовые принципы

### Аутентификация
Все запросы используют Basic Auth с логином и app-токеном:
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_TOKEN" ...
```

Для административных операций (пользователи, группы, приложения) используй admin-токен:
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" ...
```

### Обязательные заголовки
Все OCS-запросы требуют заголовка:
```
-H "OCS-APIRequest: true"
```

Для получения ответа в JSON (вместо XML по умолчанию) добавляй `format=json`:
```
?format=json
```

Все POST-запросы к OCS требуют:
```
-H "Content-Type: application/x-www-form-urlencoded"
```

### Формат ответов
OCS API возвращает XML по умолчанию. Для JSON добавляй `?format=json` или `&format=json`.

Успешный ответ (OCS v1): `statuscode: 100`
Успешный ответ (OCS v2): `statuscode: 200`

Рекомендуется использовать `format=json` и парсить через `jq`.

---

## Операции с файлами (WebDAV)

WebDAV — основной протокол для работы с файлами. Базовый URL:
```
$NEXTCLOUD_URL/remote.php/dav/files/$NEXTCLOUD_USER/
```

### Листинг файлов (PROPFIND)
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_TOKEN" \
  -X PROPFIND \
  "$NEXTCLOUD_URL/remote.php/dav/files/$NEXTCLOUD_USER/" \
  -H "Depth: 1"
```
- `Depth: 0` — только указанный ресурс
- `Depth: 1` — ресурс + непосредственные дочерние элементы
- `Depth: infinity` — вся иерархия (может быть отключено на сервере)

### Загрузка файла на сервер
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_TOKEN" \
  -T "/path/to/local/file.txt" \
  "$NEXTCLOUD_URL/remote.php/dav/files/$NEXTCLOUD_USER/remote/path/file.txt"
```

### Скачивание файла
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_TOKEN" \
  -o "/path/to/save/file.txt" \
  "$NEXTCLOUD_URL/remote.php/dav/files/$NEXTCLOUD_USER/remote/path/file.txt"
```

### Создание директории
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_TOKEN" \
  -X MKCOL \
  "$NEXTCLOUD_URL/remote.php/dav/files/$NEXTCLOUD_USER/new-folder/"
```

### Удаление файла/директории
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_TOKEN" \
  -X DELETE \
  "$NEXTCLOUD_URL/remote.php/dav/files/$NEXTCLOUD_USER/path/to/delete"
```

### Перемещение файла
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_TOKEN" \
  -X MOVE \
  -H "Destination: $NEXTCLOUD_URL/remote.php/dav/files/$NEXTCLOUD_USER/new/path/file.txt" \
  "$NEXTCLOUD_URL/remote.php/dav/files/$NEXTCLOUD_USER/old/path/file.txt"
```

### Копирование файла
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_TOKEN" \
  -X COPY \
  -H "Destination: $NEXTCLOUD_URL/remote.php/dav/files/$NEXTCLOUD_USER/copy/path/file.txt" \
  "$NEXTCLOUD_URL/remote.php/dav/files/$NEXTCLOUD_USER/original/path/file.txt"
```

---

## Шаринг (OCS Share API)

Базовый URL: `$NEXTCLOUD_URL/ocs/v2.php/apps/files_sharing/api/v1`

Подробный справочник всех эндпоинтов шаринга — см. `references/api-reference.md` (раздел «Share API»).

### Получить все шары
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_TOKEN" \
  -X GET \
  "$NEXTCLOUD_URL/ocs/v2.php/apps/files_sharing/api/v1/shares?format=json" \
  -H "OCS-APIRequest: true"
```

### Создать публичную ссылку
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_TOKEN" \
  -X POST \
  "$NEXTCLOUD_URL/ocs/v2.php/apps/files_sharing/api/v1/shares" \
  -H "OCS-APIRequest: true" \
  -d "path=/Documents/report.pdf" \
  -d "shareType=3" \
  -d "permissions=1"
```

**shareType**: 0=пользователь, 1=группа, 3=публичная ссылка, 4=email, 6=федеративный, 10=Talk

**permissions**: 1=чтение, 2=обновление, 4=создание, 8=удаление, 16=шаринг, 31=все

### Создать ссылку с паролем и сроком
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_TOKEN" \
  -X POST \
  "$NEXTCLOUD_URL/ocs/v2.php/apps/files_sharing/api/v1/shares" \
  -H "OCS-APIRequest: true" \
  -d "path=/Documents/secret.pdf" \
  -d "shareType=3" \
  -d "permissions=1" \
  -d "password=SuperSecret123" \
  -d "expireDate=2025-12-31"
```

### Расшарить файл конкретному пользователю
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_TOKEN" \
  -X POST \
  "$NEXTCLOUD_URL/ocs/v2.php/apps/files_sharing/api/v1/shares" \
  -H "OCS-APIRequest: true" \
  -d "path=/Documents/report.pdf" \
  -d "shareType=0" \
  -d "shareWith=otheruser" \
  -d "permissions=1"
```

### Удалить шару
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_TOKEN" \
  -X DELETE \
  "$NEXTCLOUD_URL/ocs/v2.php/apps/files_sharing/api/v1/shares/{shareId}" \
  -H "OCS-APIRequest: true"
```

---

## Управление пользователями (OCS Provisioning API)

Требует admin-токен. Базовый URL: `$NEXTCLOUD_URL/ocs/v1.php/cloud`

Подробный справочник — см. `references/api-reference.md` (раздел «User Provisioning API»).

### Список пользователей
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" \
  -X GET \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/users?format=json" \
  -H "OCS-APIRequest: true"
```

### Создать пользователя
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" \
  -X POST \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/users" \
  -H "OCS-APIRequest: true" \
  -d "userid=newuser" \
  -d "password=SecurePass123" \
  -d "displayName=New User" \
  -d "email=newuser@example.com" \
  -d "groups[]=team1"
```

### Информация о пользователе
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" \
  -X GET \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/users/{userid}?format=json" \
  -H "OCS-APIRequest: true"
```

### Редактировать пользователя
```bash
# Изменить email
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" \
  -X PUT \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/users/{userid}" \
  -H "OCS-APIRequest: true" \
  -d "key=email" \
  -d "value=newemail@example.com"
```
Доступные ключи: `email`, `quota`, `displayname`, `phone`, `address`, `website`, `twitter`, `password`, `language`, `locale`

### Включить/выключить пользователя
```bash
# Выключить
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" \
  -X PUT \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/users/{userid}/disable" \
  -H "OCS-APIRequest: true"

# Включить
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" \
  -X PUT \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/users/{userid}/enable" \
  -H "OCS-APIRequest: true"
```

### Удалить пользователя
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" \
  -X DELETE \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/users/{userid}" \
  -H "OCS-APIRequest: true"
```

---

## Управление группами

Требует admin-токен.

### Список групп
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" \
  -X GET \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/groups?format=json" \
  -H "OCS-APIRequest: true"
```

### Создать группу
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" \
  -X POST \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/groups" \
  -H "OCS-APIRequest: true" \
  -d "groupid=newgroup"
```

### Участники группы
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" \
  -X GET \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/groups/{groupid}?format=json" \
  -H "OCS-APIRequest: true"
```

### Добавить пользователя в группу
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" \
  -X POST \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/users/{userid}/groups" \
  -H "OCS-APIRequest: true" \
  -d "groupid=targetgroup"
```

### Удалить пользователя из группы
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" \
  -X DELETE \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/users/{userid}/groups" \
  -H "OCS-APIRequest: true" \
  -d "groupid=targetgroup"
```

### Удалить группу
```bash
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" \
  -X DELETE \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/groups/{groupid}" \
  -H "OCS-APIRequest: true"
```

---

## Управление приложениями

Требует admin-токен.

### Список приложений
```bash
# Все
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" \
  -X GET \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/apps?format=json" \
  -H "OCS-APIRequest: true"

# Только включённые
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" \
  -X GET \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/apps?filter=enabled&format=json" \
  -H "OCS-APIRequest: true"
```

### Включить/выключить приложение
```bash
# Включить
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" \
  -X POST \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/apps/{appid}" \
  -H "OCS-APIRequest: true"

# Выключить
curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_ADMIN_TOKEN" \
  -X DELETE \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/apps/{appid}" \
  -H "OCS-APIRequest: true"
```

---

## Обработка ответов и ошибок

Всегда проверяй HTTP-код и OCS-статус:

```bash
response=$(curl -s -w "\n%{http_code}" -u "$NEXTCLOUD_USER:$NEXTCLOUD_TOKEN" \
  -X GET \
  "$NEXTCLOUD_URL/ocs/v1.php/cloud/users?format=json" \
  -H "OCS-APIRequest: true")

http_code=$(echo "$response" | tail -1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
  status=$(echo "$body" | jq -r '.ocs.meta.status')
  if [ "$status" = "ok" ]; then
    echo "Success"
    echo "$body" | jq '.ocs.data'
  else
    echo "OCS Error: $(echo "$body" | jq -r '.ocs.meta.message')"
  fi
else
  echo "HTTP Error: $http_code"
fi
```

### Частые проблемы

| Проблема | Причина | Решение |
|---|---|---|
| 401 Unauthorized | Неверный токен/пароль | Проверь `NEXTCLOUD_TOKEN`, используй app-токен вместо пароля |
| 997 Unauthorized | Пропущен заголовок OCS-APIRequest | Добавь `-H "OCS-APIRequest: true"` |
| 404 Not Found | Неверный путь или файл не существует | Проверь URL и наличие файла |
| CSRF Error | Пропущен заголовок | Добавь `-H "OCS-APIRequest: true"` |
| Ответ в XML вместо JSON | Не указан format | Добавь `?format=json` |

---

## Составные сценарии

Для детального справочника всех эндпоинтов, аргументов и кодов ошибок — читай `references/api-reference.md`.
