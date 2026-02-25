---
name: strapi-v5-expert
description: Главный индекс базы знаний Strapi v5. Используй этот файл для поиска точных URL-адресов документации перед написанием архитектуры, конфигураций или кода бэкенда.
---

# Указания для Агента

Когда пользователь ставит задачу, найди наиболее подходящую категорию в разделе "Quick Reference" ниже.
Скопируй нужный URL и **ИСПОЛЬЗУЙ ИНСТРУМЕНТ WEB BROWSING**, чтобы прочитать актуальную документацию Strapi v5 по этой ссылке. Только после прочтения приступай к генерации кода.

---

## Quick Reference (Индекс Документации)

### 1. Document Service API (Главный инструмент работы с БД)
Используй эти ссылки для любых задач, связанных с CRUD операциями бэкенда. Устаревший `entityService` заменен на `strapi.documents()`.
* **Core API & CRUD:** https://docs.strapi.io/dev-docs/api/document-service
  *Описание:* Базовые методы (`findOne`, `findMany`, `create`, `update`, `delete`, `count`). Работа с `documentId`.
* **Documents Concept:** https://docs.strapi.io/dev-docs/api/document-service#documents
  *Описание:* Что такое Document в Strapi 5 (объединение локалей и статусов публикации в один объект).
* **Populate (Связи и Медиа):** https://docs.strapi.io/dev-docs/api/document-service/populate
  *Описание:* Как запрашивать вложенные связи и медиафайлы.
* **Fields Selection:** https://docs.strapi.io/dev-docs/api/document-service/fields
  *Описание:* Выборка конкретных колонок из БД (параметр `fields`).
* **Filters (Фильтрация):** https://docs.strapi.io/dev-docs/api/document-service/filters
  *Описание:* Операторы фильтрации (`$eq`, `$in`, `$not`, `$and` и др.).
* **Sort & Pagination:** https://docs.strapi.io/dev-docs/api/document-service/sort-pagination
  *Описание:* Сортировка по полям и пагинация (limit, start).
* **Locale (i18n):** https://docs.strapi.io/dev-docs/api/document-service/locale
  *Описание:* Манипуляции с документами для конкретной локали (языка).
* **Draft & Publish:** https://docs.strapi.io/dev-docs/api/document-service/draft-and-publish
  *Описание:* Работа со статусами (published, draft), методы `publish()` и `unpublish()`.
* **Document Service Middlewares:** https://docs.strapi.io/dev-docs/api/document-service/middlewares
  *Описание:* Перехват и модификация запросов `strapi.documents.use()` до обращения к БД.

### 2. Архитектура и Кастомизация Бэкенда
* **Overview & Structure:** https://docs.strapi.io/dev-docs/backend-customization
  *Описание:* Интерактивная диаграмма запросов бэкенда.
* **Project Structure:** https://docs.strapi.io/dev-docs/project-structure
  *Описание:* Структура папок Strapi-проекта (src/api, config и т.д.).
* **Routes:** https://docs.strapi.io/dev-docs/backend-customization/routes
  *Описание:* Настройка кастомных HTTP-маршрутов и core-роутов.
* **Controllers:** https://docs.strapi.io/dev-docs/backend-customization/controllers
  *Описание:* Создание кастомных контроллеров и расширение (`createCoreController`).
* **Services:** https://docs.strapi.io/dev-docs/backend-customization/services
  *Описание:* Инкапсуляция бизнес-логики (`createCoreService`).
* **Middlewares (HTTP):** https://docs.strapi.io/dev-docs/backend-customization/middlewares
  *Описание:* Глобальные и route-мидлвары Koa (`ctx`, `next`).
* **Policies:** https://docs.strapi.io/dev-docs/backend-customization/policies
  *Описание:* Защита эндпоинтов и проверка прав доступа до контроллера.
* **Requests & Responses:** https://docs.strapi.io/dev-docs/backend-customization/requests-responses
  *Описание:* Структура объекта `ctx` (`ctx.request`, `ctx.state.user`, `ctx.response`).
* **Error Handling:** https://docs.strapi.io/dev-docs/error-handling
  *Описание:* Выброс стандартизированных ошибок (`ApplicationError`, `ValidationError`).
* **Lifecycle Functions (Global):** https://docs.strapi.io/dev-docs/configurations/functions
  *Описание:* Использование `register`, `bootstrap` и `destroy` в файле `src/index.ts`.

### 3. Модели и База Данных
* **Models & Content-Types:** https://docs.strapi.io/dev-docs/backend-customization/models
  *Описание:* Создание схем данных (`schema.json`), типы атрибутов.
* **Lifecycle Hooks:** https://docs.strapi.io/dev-docs/backend-customization/models#lifecycle-hooks
  *Описание:* Триггеры БД (`beforeCreate`, `afterUpdate`).
* **Relations:** https://docs.strapi.io/dev-docs/api/rest/relations
  *Описание:* Управление связями (connect, disconnect, set) через API.
* **Database Transactions:** https://docs.strapi.io/dev-docs/database/transactions
  *Описание:* Использование `strapi.db.transaction()` для атомарных операций.
* **Database Migrations:** https://docs.strapi.io/dev-docs/database/migrations
  *Описание:* Скрипты миграции структуры или данных (папка `database/migrations`).
* **Database Configuration:** https://docs.strapi.io/dev-docs/configurations/database
  *Описание:* Настройка `config/database.ts` (SQLite, PostgreSQL, MySQL).

### 4. Внешние API (REST, GraphQL, Client)
* **Content API Overview:** https://docs.strapi.io/dev-docs/api/content-api
  *Описание:* Обзор внешних API Strapi.
* **REST API Reference:** https://docs.strapi.io/dev-docs/api/rest
  *Описание:* Основной справочник эндпоинтов. Плоский формат ответа v5.
* **REST API Parameters:** https://docs.strapi.io/dev-docs/api/rest/parameters
  *Описание:* Полный список параметров REST API.
* **REST API Guides:** https://docs.strapi.io/dev-docs/api/rest/guides
  *Описание:* Специфичные кейсы использования REST API.
* **REST API Populate & Select:** https://docs.strapi.io/dev-docs/api/rest/populate-select
  *Описание:* Параметры `populate` и `fields` в REST запросах.
* **REST API Sort & Pagination:** https://docs.strapi.io/dev-docs/api/rest/sort-pagination
  *Описание:* Сортировка и пагинация по offset и page.
* **REST API Status:** https://docs.strapi.io/dev-docs/api/rest/status
  *Описание:* Фильтрация REST ответов по статусу (published/draft).
* **REST API Locale:** https://docs.strapi.io/dev-docs/api/rest/locale
  *Описание:* Запросы REST API с параметром `locale`.
* **REST API Upload:** https://docs.strapi.io/dev-docs/api/rest/upload
  *Описание:* Загрузка файлов через POST `/api/upload`.
* **Interactive Query Builder:** https://docs.strapi.io/dev-docs/api/rest/interactive-query-builder
  *Описание:* Использование библиотеки `qs` для построения сложных URL.
* **GraphQL API:** https://docs.strapi.io/dev-docs/api/graphql
  *Описание:* Использование GraphQL мутаций и запросов, фильтрация.
* **GraphQL Plugin Config:** https://docs.strapi.io/dev-docs/plugins/graphql
  *Описание:* Настройка Apollo Server, Shadow CRUD и лимитов сложности в `config/plugins.ts`.
* **Strapi Client:** https://docs.strapi.io/dev-docs/strapi-client
  *Описание:* Официальная библиотека `@strapi/client` для фронтенда.
* **OpenAPI & Swagger:** https://docs.strapi.io/dev-docs/api/openapi
  *Описание:* Генерация OpenAPI спецификации, плагин Documentation.

### 5. TypeScript
* **TypeScript Setup & Overview:** https://docs.strapi.io/dev-docs/typescript
  *Описание:* Использование TypeScript в Strapi.
* **TypeScript Development:** https://docs.strapi.io/dev-docs/typescript/development
  *Описание:* Автокомплит, типизация `strapi` instance.
* **Manipulating Documents:** https://docs.strapi.io/dev-docs/typescript/manipulating-documents
  *Описание:* Использование `UID.ContentType` и `Data.Document` для строгой типизации.
* **TypeScript Configuration:** https://docs.strapi.io/dev-docs/typescript/configuration
  *Описание:* Настройки `config/typescript.ts` и автогенерация типов.
* **Adding TypeScript:** https://docs.strapi.io/dev-docs/typescript/migration
  *Описание:* Как добавить TS в существующий JS проект.

### 6. Конфигурации и Автоматизация (Settings)
* **Configurations Overview:** https://docs.strapi.io/dev-docs/configurations
  *Описание:* Обзор папки `/config`.
* **Server Config:** https://docs.strapi.io/dev-docs/configurations/server
  *Описание:* `config/server.ts` (host, port, url, proxy).
* **API Config:** https://docs.strapi.io/dev-docs/configurations/api
  *Описание:* `config/api.ts` (префиксы, лимиты пагинации).
* **Middlewares Config:** https://docs.strapi.io/dev-docs/configurations/middlewares
  *Описание:* Настройка встроенных мидлваров (CORS, security, body) в `config/middlewares.ts`.
* **Plugins Config:** https://docs.strapi.io/dev-docs/configurations/plugins
  *Описание:* Подключение и настройка плагинов локально (`config/plugins.ts`).
* **Environment Variables:** https://docs.strapi.io/dev-docs/configurations/environment
  *Описание:* Работа с `.env` и хелпером `env()`.
* **CRON Jobs:** https://docs.strapi.io/dev-docs/configurations/cron
  *Описание:* Выполнение фоновых задач по расписанию (node-schedule).
* **Webhooks:** https://docs.strapi.io/dev-docs/configurations/webhooks
  *Описание:* Настройка триггеров HTTP-запросов во внешние системы.
* **Features (Feature Flags):** https://docs.strapi.io/dev-docs/configurations/features
  *Описание:* Включение экспериментальных функций.

### 7. Плагины и Расширения
* **Installing Plugins:** https://docs.strapi.io/user-docs/plugins
  *Описание:* Использование Marketplace и CLI для установки плагинов.
* **Users & Permissions:** https://docs.strapi.io/dev-docs/plugins/users-permissions
  *Описание:* Управление пользователями, JWT, ACL, регистрация и роли.
* **Upload files / Media Library:** https://docs.strapi.io/dev-docs/plugins/upload
  *Описание:* Настройка провайдеров загрузки файлов (AWS S3, Local).
* **Email Plugin:** https://docs.strapi.io/dev-docs/plugins/email
  *Описание:* Отправка транзакционных писем, настройка провайдеров SMTP.
* **Custom Fields:** https://docs.strapi.io/dev-docs/custom-fields
  *Описание:* Создание и регистрация кастомных типов полей.
* **Sentry Plugin:** https://docs.strapi.io/dev-docs/plugins/sentry
  *Описание:* Интеграция с Sentry для отслеживания ошибок.

### 8. Миграция v4 -> v5
* **Upgrading Introduction:** https://docs.strapi.io/dev-docs/migration/v4-to-v5
  *Описание:* Обзор процесса обновления на Strapi 5.
* **Step-by-step Guide:** https://docs.strapi.io/dev-docs/migration/v4-to-v5/step-by-step
  *Описание:* Пошаговая инструкция по апгрейду.
* **Upgrade Tool:** https://docs.strapi.io/dev-docs/migration/v4-to-v5/upgrade-tool
  *Описание:* Использование CLI-утилиты (codemods) для автоматической миграции.
* **Breaking Changes:** https://docs.strapi.io/dev-docs/migration/v4-to-v5/breaking-changes
  *Описание:* Полный список ломающих изменений.
* **Entity Service to Document Service:** https://docs.strapi.io/dev-docs/migration/v4-to-v5/entity-service
  *Описание:* Рефакторинг старых запросов на новый API и `documentId`.
* **Plugins Migration:** https://docs.strapi.io/dev-docs/migration/v4-to-v5/plugins
  *Описание:* Обновление плагинов и использование Plugin SDK.
* **Helper-plugin Migration:** https://docs.strapi.io/dev-docs/migration/v4-to-v5/helper-plugin
  *Описание:* Замена удаленного `@strapi/helper-plugin`.
* **Design System Updates:** https://docs.strapi.io/dev-docs/migration/v4-to-v5/design-system
  *Описание:* Изменения в UI компонентах (Design System v2).

### 9. Инфраструктура и CLI
* **Installation & Quick Start:** https://docs.strapi.io/dev-docs/installation
  *Описание:* Установка Strapi (CLI, Docker).
* **Command Line Interface (CLI):** https://docs.strapi.io/dev-docs/cli
  *Описание:* Команды `strapi generate`, `build`, `ts:generate-types`.
* **Templates:** https://docs.strapi.io/dev-docs/templates
  *Описание:* Создание проектов на основе готовых шаблонов GitHub.
* **Deployment:** https://docs.strapi.io/dev-docs/deployment
  *Описание:* Требования к серверу, переменные для продакшена.
* **Data Management:** https://docs.strapi.io/dev-docs/data-management
  *Описание:* Импорт/Экспорт/Трансфер данных между базами (CLI).
* **Testing:** https://docs.strapi.io/dev-docs/testing
  *Описание:* Настройка Jest и Supertest для unit и интеграционных тестов.

### 10. CMS Features и Админ-Панель
* **Admin Panel Settings:** https://docs.strapi.io/user-docs/intro
  *Описание:* Обзор графического интерфейса администратора.
* **Admin Panel Configuration:** https://docs.strapi.io/dev-docs/configurations/admin-panel
  *Описание:* Настройка `config/admin.ts` (секреты, переводы).
* **Homepage Customization:** https://docs.strapi.io/dev-docs/admin-panel-customization/homepage
  *Описание:* Добавление виджетов на главную страницу админки.
* **Content-Type Builder:** https://docs.strapi.io/user-docs/content-type-builder
  *Описание:* Использование GUI для создания моделей данных.
* **Content Manager:** https://docs.strapi.io/user-docs/content-manager
  *Описание:* Интерфейс редактирования записей.
* **Draft & Publish (CMS):** https://docs.strapi.io/user-docs/draft-and-publish
  *Описание:* Механика статусов контента.
* **Internationalization (CMS):** https://docs.strapi.io/dev-docs/plugins/i18n
  *Описание:* Перевод контента на разные языки в админке.
* **Preview:** https://docs.strapi.io/dev-docs/plugins/preview
  *Описание:* Настройка Live Preview (предпросмотр контента на фронтенде).
* **API Tokens:** https://docs.strapi.io/user-docs/api-tokens
  *Описание:* Токены для Server-to-Server интеграций.
* **Role-Based Access Control (RBAC):** https://docs.strapi.io/user-docs/users-roles-permissions
  *Описание:* Настройка прав администраторов панели.
* **Single Sign-On (SSO):** https://docs.strapi.io/dev-docs/configurations/sso
  *Описание:* Авторизация админов через Azure, Google (Enterprise).
* **Audit Logs:** https://docs.strapi.io/user-docs/audit-logs
  *Описание:* Журналирование действий администраторов (Enterprise).
* **Review Workflows:** https://docs.strapi.io/user-docs/review-workflows
  *Описание:* Настройка стадий ревью контента (Enterprise).
* **Content History:** https://docs.strapi.io/user-docs/content-history
  *Описание:* Версионирование и откат изменений контента (Enterprise).
* **Releases:** https://docs.strapi.io/user-docs/releases
  *Описание:* Пакетная публикация контента (Growth/Enterprise).