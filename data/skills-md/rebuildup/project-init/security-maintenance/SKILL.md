---
name: security-maintenance
description: framework/runtime/dependencyの脆弱性情報を収集し、projectへの実影響と優先度を判定してticket/releaseへ反映する時に使用する。
---

# Security Maintenance

security updateは単純なCVSS順ではなく、projectへの実到達可能性とrelease riskまで含めて優先順位を付ける。

未知のsource vulnerability探索は `security-audit` が所有する。そこで `confirmed` になったfindingは本Skillへhandoffし、advisoryと同じproject-aware priority / remediation / release workflowへ統合する。`needs_validation` をconfirmed vulnerabilityとしてpriority化しない。

## 1. Source priority

初期化時および継続maintenance時に、実際に使用しているversionを基準に次を確認する。

1. framework/runtime/SDK official security advisories
2. official release notes / security announcements
3. language/package ecosystem official advisory source
4. GitHub Security Advisories / dependency alerts
5. maintainer issue / patch release information
6. trusted secondary source

一般ニュースやSNSだけをsecurity SoTにしない。

## 2. Inventory

最低限把握する:

- direct dependencies
- security-sensitive transitive dependencies
- framework/runtime/SDK versions
- container/base image
- OS/runtime packages when relevant
- build/deploy toolchain
- externally exposed services/endpoints
- auth/session/crypto/storage/network boundaries

lockfileやgenerated SBOM等、再現可能なinventoryを優先する。

## 3. Prioritization

severityだけで決めない。最低限次を評価する。

- advisory severity / CVSS等
- exploitability / exploit maturity
- projectでvulnerable pathがreachableか
- internet/external exposure
- auth前に到達可能か
- confidentiality / integrity / availability impact
- privilege required
- affected data / tenant scope
- fix/patch availability
- workaround quality
- regression/migration risk
- current target releaseとの距離

project固有priorityへ変換する。

推奨概念:

- **P0 / Critical**: active exploitationまたは高確率で直接exposed、即時対応。必要なら現在sprintを中断しpatch release。
- **P1 / High**: reachableで重大impact、fix available。current releaseのblocking候補。
- **P2 / Medium**: 条件付きreachableまたはimpact限定。計画ticketとして近いreleaseへ。
- **P3 / Low**: non-reachable/defense-in-depth。dependency hygieneとして処理。

CVSSが高いだけでP0にしない。逆にCVSSが中程度でもproject exposureが高ければ優先度を上げる。

## 4. Response workflow

meaningful advisoryを検出したら:

1. affected versionを確認
2. project reachabilityを確認
3. exploit/fix情報を確認
4. priority決定
5. GitHub Issueを日本語で作成/更新
6. target releaseを決定
7. isolated ticket branchで修正
8. focused + integration security verification
9.必要ならrelease gateへ追加
10. advisory sourceと判断根拠をIssue/ADRへ残す

緊急patchでは `release-x-y-z` のpatch versionを切ることを許可する。

## 5. Automated security checks

projectに適切なら初期化時に導入・修復する。

候補:

- dependency vulnerability scan
- dependency review on PR
- code scanning / SAST
- secret scanning
- container/image scanning
- SBOM generation
- license/security policy checks

ただし大量のfalse positiveをblockingにしてsignalを破壊しない。blocking/non-blockingはproject riskに合わせて明示する。

## 6. Security gate

security-related ticketは通常quality gateに加えて:

- exploit/reproduction条件の確認
- vulnerable pathが修正後に閉じていること
- regression test
- dependency/version resolution確認
- production artifactにfixed versionが入ること
- workaroundを入れた場合の撤去条件

を検証する。

## 7. Re-evaluation

framework/runtime major/minor update、security policy変更、exposure変更、新しいexternal service追加時はsecurity profileを再評価する。
