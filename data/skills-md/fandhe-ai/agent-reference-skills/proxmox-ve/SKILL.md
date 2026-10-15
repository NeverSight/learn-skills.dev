---
name: proxmox-ve
description: >
  Proxmox VE (PVE) ハイパーバイザーリファレンス。KVM/QEMU 仮想マシン、LXC コンテナ、
  クラスター構築・HA・SDN・Ceph・ZFS・ストレージ管理。
  qm, pct, pvecm, pvesm, pveceph, pvesh, pveum, vzdump, pveam, pvesr, ha-manager CLI。
  REST API、設定ファイル (qm.conf, pct.conf, datacenter.cfg)、バックグラウンドサービス一覧。
user-invocable: false
---

## ディレクトリ構成

```text
skills/proxmox-ve/
  SKILL.md
  references/
    core/
      README.md
      installation.md
      cluster.md
      storage.md
      vm-qemu.md
      container-lxc.md
      networking-sdn.md
      ceph.md
      ha.md
      backup-restore.md
      firewall.md
      user-access.md
      notifications.md
    cli/
      README.md
      qm.md
      pct.md
      pvesm.md
      pvecm.md
      pveceph.md
      pvenode.md
      pveum.md
      pvesh.md
      vzdump.md
      pveam.md
      pvesr.md
      ha-manager.md
      misc-cli.md
    config/
      README.md
      qm-conf.md
      pct-conf.md
      datacenter-cfg.md
      cpu-models-conf.md
    api/
      README.md
      rest-overview.md
      endpoints-qemu.md
      endpoints-lxc.md
      endpoints-cluster.md
      endpoints-access-storage.md
    services/
      README.md
      daemons.md
  samples/
    README.md
    vm-lifecycle.md
    container-lifecycle.md
    cluster-setup.md
    backup-restore.md
    api-automation.md
  scripts/
    README.md
    install.md
    vm-commands.md
    container-commands.md
    cluster-commands.md
    storage-commands.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの README.md を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| インストール・初期設定・ZFS/LVM ルート構成を知りたい | core | [references/core/README.md](references/core/README.md) |
| クラスター作成・ノード参加・Corosync 設定を知りたい | core | [references/core/README.md](references/core/README.md) |
| ストレージバックエンド (NFS/ZFS/RBD/iSCSI) を設定したい | core | [references/core/README.md](references/core/README.md) |
| KVM/QEMU 仮想マシンの作成・管理・マイグレーションを知りたい | core | [references/core/README.md](references/core/README.md) |
| LXC コンテナの作成・設定・スナップショットを知りたい | core | [references/core/README.md](references/core/README.md) |
| ネットワーク構成・SDN ゾーン・VNet を設定したい | core | [references/core/README.md](references/core/README.md) |
| Ceph クラスター (OSD/MON/MGR/プール) を構築したい | core | [references/core/README.md](references/core/README.md) |
| HA リソース・フェンシング・ウォッチドッグを設定したい | core | [references/core/README.md](references/core/README.md) |
| バックアップ・リストア・PBS 連携・保持設定を知りたい | core | [references/core/README.md](references/core/README.md) |
| ファイアウォールルール・セキュリティグループを設定したい | core | [references/core/README.md](references/core/README.md) |
| ユーザー・グループ・ロール・API トークン・2FA を管理したい | core | [references/core/README.md](references/core/README.md) |
| 通知ターゲット (SMTP/Gotify/webhook) を設定したい | core | [references/core/README.md](references/core/README.md) |
| qm コマンドのオプション・サブコマンドを調べたい | cli | [references/cli/README.md](references/cli/README.md) |
| pct コマンドの使い方を知りたい | cli | [references/cli/README.md](references/cli/README.md) |
| pvesm / pvecm / pveceph / pveum コマンドを調べたい | cli | [references/cli/README.md](references/cli/README.md) |
| pvesh で REST API を直接呼び出したい | cli | [references/cli/README.md](references/cli/README.md) |
| vzdump でバックアップ・スケジュールを組みたい | cli | [references/cli/README.md](references/cli/README.md) |
| pveam でテンプレートをダウンロード・管理したい | cli | [references/cli/README.md](references/cli/README.md) |
| pvesr でストレージレプリケーションを設定したい | cli | [references/cli/README.md](references/cli/README.md) |
| ha-manager のリソース監視・フェイルオーバーを知りたい | cli | [references/cli/README.md](references/cli/README.md) |
| VM 設定ファイル (qm.conf) の書式を知りたい | config | [references/config/README.md](references/config/README.md) |
| コンテナ設定ファイル (pct.conf) の書式を知りたい | config | [references/config/README.md](references/config/README.md) |
| データセンター設定 (datacenter.cfg) のパラメーターを知りたい | config | [references/config/README.md](references/config/README.md) |
| カスタム CPU モデル定義 (cpu-models.conf) を知りたい | config | [references/config/README.md](references/config/README.md) |
| REST API の認証・エンドポイント体系・pvesh の使い方を知りたい | api | [references/api/README.md](references/api/README.md) |
| QEMU/LXC の REST API エンドポイントを調べたい | api | [references/api/README.md](references/api/README.md) |
| クラスター・アクセス・ストレージ系 API を呼び出したい | api | [references/api/README.md](references/api/README.md) |
| バックグラウンドデーモン (pvedaemon/pveproxy/pvestatd/pmxcfs 等) の役割・ポートを調べたい | services | [references/services/README.md](references/services/README.md) |
| pveproxy → pvedaemon の通信フロー・内部ポートを知りたい | services | [references/services/README.md](references/services/README.md) |
| 使用ポート一覧・systemctl 操作を知りたい | services | [references/services/README.md](references/services/README.md) |
| 典型的な使い方・ワークフロー例を見たい | samples | [samples/README.md](samples/README.md) |
| インストール・VM・コンテナ・クラスター・ストレージの実行コマンドを知りたい | scripts | [scripts/README.md](scripts/README.md) |
