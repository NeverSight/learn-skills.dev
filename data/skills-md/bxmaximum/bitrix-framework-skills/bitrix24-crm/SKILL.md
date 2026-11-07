---
name: bitrix24-crm
description: 'CRM в PHP коробки Битрикс24: Service\Container, Factory, Item, операции, смарт-процессы, права и события. Для серверной работы со сделками, клиентами и воронками в /local.'
---

# CRM Битрикс24: серверный PHP

Scope: Bitrix24 on-premise · Verified: crm 26.1900.0, main 26.1000.0

Перед PHP-кодом один раз прочитай `bitrix-framework`. Здесь код внутри портала: модули `/local/`, обработчики, агенты. Вызовы CRM через REST: `bitrix24-rest-api`.

| Задача | Открыть |
| --- | --- |
| Container, Factory, чтение Item, поля, телефоны и почта | `rules/factory-items.md` |
| Добавление/изменение/удаление, Context, проверки, свои действия | `rules/operations.md` |
| Смарт-процессы, воронки, стадии и смарт-счета | `rules/smart-processes.md` |
| Права и списки с их учётом | `rules/permissions.md` |
| Реакция на изменения, подмена фабрики, роботы и триггеры | `rules/events-automation.md` |
| Комментарии таймлайна, запланированные и прочие дела | `rules/timeline-activities.md` |
| Коллекция полей и пользовательские поля | `rules/fields-uf.md` |
| Замены `CCrmDeal`/`CCrmLead`/…, соответствие D7 и REST | `rules/legacy-rest.md` |

## Общие правила

- Подключи `Loader::includeModule('crm')`; сервисы получай из `Container::getInstance()`.
- Записывай через операции Factory: `getAddOperation()`/`getUpdateOperation()`/`getDeleteOperation()` и `launch()`. Прямые `DealTable::add()`, `$factory->getDataClass()::update()`, `Item::save()`/`Item::delete()` обходят права, обязательные поля, события, таймлайн, индекс и роботов.
- Используй `Item::FIELD_NAME_*`: фабрика сопоставляет их столбцам сущности (у лида `STAGE_ID` соответствует `STATUS_ID`).
- `entityTypeId`, ID воронок и стадий различаются между порталами. Ищи по коду или семантике при выполнении.
- У агента, CLI и очереди нет пользователя. Передай `Context` с ID инициатора; системный обход прав должен быть явным решением.
- Проверяй `isSuccess()` каждого `launch()` и передавай ошибки вызывающему коду.
