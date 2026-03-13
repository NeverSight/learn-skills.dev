---
name: ddev-magento
description: "Advanced management for Magento 2 on DDEV with MariaDB, Redis, OpenSearch/Elasticsearch 8, RabbitMQ, Varnish, PhpMyAdmin, and XHGui/XHProf."
---

# Workflow

This skill provides comprehensive management for high-performance Magento 2 environments on DDEV.

## 1. Environment & Services
*   **Start/Stop:** Use `ddev start` or `ddev stop`.
*   **Project Info:** Run `ddev describe` to see URLs for:
    *   **Web Server:** (Main store URL)
    *   **PhpMyAdmin:** Database management interface.
    *   **Mailpit:** Email testing interface.
    *   **XHGui:** Performance profiling UI.
    *   **RabbitMQ:** Management dashboard.
*   **Performance (Mutagen):** For macOS/Windows, ensure Mutagen is enabled for optimal speed: `ddev config --performance-mode=mutagen`.

## 2. Magento 2 Operations
*   **Upgrade:** `ddev magento setup:upgrade`.
*   **Reindexing:** `ddev magento indexer:reindex`.
*   **Compilation:** `ddev magento setup:di:compile`.
*   **Static Assets:** `ddev magento setup:static-content:deploy -f`.
*   **Cache:** `ddev magento cache:flush`.
*   **Mode Management:** `ddev magento deploy:mode:set developer`.

## 3. Search Services (OpenSearch / Elasticsearch)
*   **OpenSearch (Recommended for 2.4+):** Install via `ddev add-on get ddev/ddev-opensearch`.
    *   Access via `http://opensearch:9200`. 
    *   Check status: `ddev exec curl -s opensearch:9200`.
*   **Elasticsearch 8:** Access via `http://elasticsearch:9200`.
*   **Configuration:** During install, use `--search-engine=opensearch --opensearch-host=opensearch --opensearch-port=9200`.

## 4. Typical Installation Workflow
1.  **Init:** `ddev config --project-type=magento2 --docroot=pub --upload-dirs=media --disable-settings-management`.
2.  **Add-ons:** `ddev add-on get ddev/ddev-opensearch`.
3.  **Composer:** `ddev composer create-project --repository https://repo.magento.com/ magento/project-community-edition`.
4.  **Install:** `ddev magento setup:install` with appropriate DB and Search parameters.
5.  **Dev Setup:** `ddev magento module:disable Magento_TwoFactorAuth` (optional for local dev) and `ddev magento deploy:mode:set developer`.

## 5. Other Specialized Services
*   **Redis:** Direct CLI access via `ddev redis-cli`.
*   **Varnish:** Managed via the Varnish container. Purge cache using `ddev magento cache:flush`.
*   **RabbitMQ:** Configure in `env.php` using host `rabbitmq`.
*   **Profiling (XHGui/XHProf):**
    *   Enable profiling for web requests via config.
*   **Logs:** `ddev logs -f` or `ddev logs -f web`.
*   **SSH Access:** `ddev ssh`.
*   **Database:** `ddev mysql` or PhpMyAdmin.
*   **Snapshot:** `ddev snapshot` for backups.
