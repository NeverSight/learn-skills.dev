---
name: ship
description: "Workflow chốt PUSH/RELEASE/PR/MR — gọi khi user nhắc 'release'/'push'/'ship'/'lên release'/'mở PR'/'tạo MR'. Chạy CHECKLIST điều kiện TRƯỚC khi đẩy: (1) medic --ci (cổng sức khoẻ: luật cắn/drift/docs/code/eval), (2) UAT /fdk-uat qua remote thật nếu diff có năng lực mới (chỉ release/pr/mr, medic --ci không chứng minh được đường curl), (3) git sạch (scratchpad/ephemeral không track), (4) selftest, (5) version x.x.x+1 từ tag gần nhất (chỉ mức release), (6) patch note/PR-body trung thực (Added/Fixed/Removed/Known-limitations, KHÔNG phóng đại). Hỗ trợ 5 mức: 'ship push' = chỉ push không tag; 'ship release' = push + tag vX.Y.Z + release notes; 'ship pr' = push nhánh + gh pr create (GitHub); 'ship mr' = push nhánh + glab mr create (GitLab); 'ship merge' = liệt kê PR/MR ĐẾN của repo theo remote, kéo nhánh về, chạy gate+test, chỉ merge nếu XANH. STOP chờ duyệt trước bước side-effect. Trigger: /ship, 'release', 'push', 'ship', 'mở PR', 'tạo MR', 'ship pr', 'ship mr', 'ship merge', 'gom PR về merge', 'merge PR nếu test xanh', 'chuẩn bị push', 'lên release', 'checklist trước push', 'đủ điều kiện push chưa'."
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.1.0"
  loop: dev-loop
  requires:
    harness: ">=1.3.127"
    bin: [python3]
    scripts: [fdk/tools/ci-local.py, fdk/tools/medic.py, harness/scripts/repo_role.py]
    framework_scripts: [harness/scripts/fresh-install-smoke.sh]
---

# Skill: ship

> Workflow chốt quanh remote. Chạy checklist điều kiện, DỪNG chờ duyệt trước mọi bước side-effect (push/tag/PR/MR/merge). Năm mức — 4 mức ĐẨY ĐI (outbound) + 1 mức GOM VỀ (inbound): **push** (đủ mọi bước, không tag) · **release** (push + tag `vX.Y.Z` + release notes) · **pr** (push nhánh + mở Pull Request GitHub qua `gh`) · **mr** (push nhánh + mở Merge Request GitLab qua `glab`) · **merge** (liệt kê PR/MR *đến* → kéo nhánh về → gate+test → merge nếu xanh).

## WHAT

### Purpose và context
- **Purpose:** đưa thay đổi ra remote (push/release/PR/MR) hoặc gom PR/MR đến về (merge) CHỈ sau khi checklist điều kiện xanh, và dừng chờ duyệt trước mọi side-effect.
- **Trigger (when to use):**
- User nhắc "release" / "push" / "ship" / "lên release" / "chuẩn bị push" / "đủ điều kiện push chưa" / "mở PR" / "tạo MR".
- Trước khi đẩy code lên remote, cắt một release, hoặc mở PR/MR để review-then-merge.
- Muốn duyệt-rồi-merge các PR/MR đang mở của repo: "gom PR về merge" / "merge PR nếu test xanh" / "ship merge".
- **Non-goals:** không tự sửa lỗi gate (việc của `/medic` + skill sửa), không tự đóng issue, không tự cài/auth `gh`/`glab`.

### Mental model
`repo_role (framework · module · downstream · foreign) → bảng gate của ĐÚNG loại repo → ` rồi mới tới chuỗi chung:
`mức (push · release · pr · mr · merge) → gate sức khoẻ (medic --ci + ci-local) → UAT remote (chỉ release/pr/mr có năng lực mới) → git sạch → selftest → [version + patch note] → checklist → DỪNG duyệt → side-effect → [UAT pha 2]`. Các mức khác nhau ở **bước cuối**, không ở checklist.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | `repo_role` | tự đọc | `python3 harness/scripts/repo_role.py . --json` (máy khách: `~/.claude/harness/harness/scripts/repo_role.py`) — nhãn KHAI BÁO trong `.overstack.yaml`; thiếu thì suy kèm bằng chứng rồi HỎI user một lần và `--set`; ép tay lần này: `ship <mức> --as <role>` |
| In | mức | không (mặc định = push) | `push` · `release` · `pr` · `mr` · `merge` — user mô tả phạm vi, không cần nhớ cờ |
| In | duyệt của user | có, trước mọi side-effect | "yes" tường minh cho push/tag/release/PR/MR/merge/canary |
| Out | checklist + lệnh đề xuất | có | kết quả từng bước gate, UAT pha 1 hoặc lý do skip, commit msg, lệnh cuối |
| Out | văn bản | theo mức | `release` → `RELEASE-vX.Y.Z.md`; `pr`/`mr` → PR/MR body; `push` → chỉ commit msg; `merge` → báo cáo test + quyết định |
| Out | side-effect | chỉ sau duyệt | push / tag / release / PR / MR / merge đã thực thi |

### Rules và capabilities
- RULE-01 (MUST): **Không push khi `medic --ci` đỏ** — trừ khi user override tường minh; kể cả override phải ghi lý do vào patch note.
- RULE-02 (MUST): **Patch note không phóng đại** — Known-limitations là bắt buộc nếu có phần chưa xong.
- RULE-03 (MUST): **Mức khác nhau ở BƯỚC CUỐI, không ở checklist:** mọi mức đều qua gate sức khoẻ; chỉ khác sản phẩm cuối (tag / release / PR / MR / merge). Đừng tag khi user nói "pr"/"mr"; đừng mở PR khi user chỉ nói "push".
- RULE-04 (MUST): **`medic --ci` xanh KHÔNG chứng minh đường remote chạy được — đó là việc của `/fdk-uat`.** `release`/`pr`/`mr` có năng lực mới BẮT BUỘC qua UAT pha 1 (canary) trước khi đề xuất bước 7; bỏ qua chỉ khi diff xác nhận không thêm năng lực gì user thấy, và phải ghi lý do. Quyết định đã cháy thật 2026-09-17: mọi push trước đó (kể cả `6c839d8`) chỉ qua `medic --ci`/`ci-local`, chưa từng qua UAT remote thật.
- RULE-05 (MUST): **Mức `merge` — TEST là điều kiện merge, không phải hình thức:** phải kéo nhánh về + chạy `medic --ci` + test THẬT trước khi merge; đỏ thì tuyệt đối KHÔNG merge, để nguyên cho tác giả. Một-tại-một, không merge gộp mù nhiều PR cùng lúc.
- RULE-06 (MUST): **PR/MR body cùng luật patch note:** giọng người-dùng, Known-limitations bắt buộc nếu có phần nửa vời. Không SHA/tên hàm nội bộ. KHÔNG `Closes #N` tự động.
- RULE-07 (MUST): **Side-effect cần "yes":** push/tag/release/PR/MR là hành động khó lùi (outward-facing) → luôn STOP show lệnh, chờ duyệt; không commit/PR-body AI-attribution (theo fdk).
- RULE-08 (MUST): **Không tự cài/auth `gh`/`glab`:** thiếu công cụ → DỪNG, báo user; đừng đoán host.
- RULE-10 (MUST): **Biết mình đang ở LOẠI repo nào trước khi chạy bất cứ gate nào.** Dòng đầu tiên của checklist luôn là `🏷 repo_role=<role> (khai báo | sổ máy | suy luận | ép tay)`. Nguồn `suy luận` → hỏi user xác nhận rồi ghi nhãn (`repo_role.py . --set <role>`; riêng `foreign` ghi vào sổ MÁY, không đụng repo người khác). Gate của loại repo này KHÔNG áp cho loại khác: `ci-local`/`capability-stamp`/UAT chỉ có nghĩa ở `framework`; chạy chúng ở `module`/`downstream` là chấm nhầm, bỏ chúng ở `framework` là hở. Bài học 20/09/2026: `/ship` một-luồng khiến việc ship repo engine phải tự nhớ quy trình khác hẳn.
- RULE-11 (MUST): **ĐỌC rc của gate rồi mới đẩy.** Lệnh push/tag đứng ở một bước RIÊNG sau khi đã in và đọc `rc=`; cấm nối gate với push bằng `;` hay ống `| tail` (nuốt rc). Hai lần cháy cùng ngày 20/09/2026: push `c83b065` khi `medic` đang đỏ, và tag `v3.0.1` khi `install-test` báo FAIL — cả hai do nối lệnh. Ở `framework` khi working tree có file lạ chưa commit (vd bị tool khác ghi đè), chạy gate trên CHECKOUT SẠCH của commit (`git worktree add --detach <tmp> HEAD`) để không chấm nhầm workflow.
- RULE-12 (MUST): **`foreign` = khách trong nhà người khác.** Chỉ mức `pr`/`mr`, không `push` thẳng nhánh mặc định; theo luật commit/CI của HỌ (đọc CONTRIBUTING, không áp R15 hay luật overstack); KHÔNG cài, không ghi `.overstack.yaml`, không thêm file cấu hình nào của ta vào repo.
- RULE-09 (MUST): Compose, đừng đẻ lại: dùng `medic` cho sức khoẻ, `git tag` cho version, `gh`/`glab` cho PR/MR — skill này chỉ điều phối checklist.
- Capabilities: đọc repo + chạy gate cục bộ; ghi remote (push/tag/PR/MR/merge) CHỈ qua công cụ đã auth và sau duyệt.

### Failure boundaries
- Gate đỏ (`medic --ci` / `ci-local` / `freshinstall`) → **blocked**, in chỗ hở + lệnh sửa, không push.
- UAT FAIL ở pha nào → **failed**, dừng ship, xoá canary; pha 2 FAIL → gỡ commit khỏi remote theo `/fdk-uat` bước 5.
- Không chắc diff có "năng lực mới" hay bậc version → **clarify** (hỏi user), không tự quyết.
- Thiếu `gh`/`glab` hoặc chưa auth → **blocked**, báo user cài + login.
- Mức `merge`: PR đỏ → không merge PR đó (**partial** cho cả lô), báo lý do.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W00 | deterministic | repo | `repo_role.py . --json` → in `🏷 repo_role=…`; nguồn `inferred` thì hỏi user + `--set`; chọn cột gate ở bảng "Luồng theo repo_role" | role + bảng gate | role không hợp lệ → blocked |
| W01 | deterministic | repo | Cổng sức khoẻ `medic --ci` rồi `python3 fdk/tools/ci-local.py` (gồm probe `freshinstall`) | rc 0 | đỏ → blocked |
| W02 | effect | diff, mức | UAT `/fdk-uat` pha 1 — chỉ `release`/`pr`/`mr` có năng lực mới (B02) | PASS hoặc lý do skip | FAIL → failed |
| W03 | deterministic | worktree | Git sạch: `git status --short`, rác ephemeral không track | sạch | bẩn → dọn rồi lặp W03 |
| W04 | deterministic | diff | Selftest/kiểm nhanh engine đụng tới | rc 0 | đỏ → blocked |
| W05 | judgment | tag gần nhất | Version `vX.Y.(Z+1)` — chỉ `release` (B01) | tag đề xuất | không chắc bậc → clarify |
| W06 | judgment | `git log`, scratch-log | Patch note / PR-MR body trung thực, Known-limitations bắt buộc nếu có phần nửa vời | văn bản | — |
| W07 | deterministic | kết quả W01–W06 | Hiện checklist + đề xuất lệnh, **DỪNG chờ duyệt** | "yes" | không duyệt → cancelled |
| W08 | effect | duyệt | Thực thi theo mức; nếu W02 đã chạy thì UAT pha 2 ngay sau đó | side-effect + receipt | pha 2 FAIL → gỡ commit |

Chi tiết từng bước (nguồn chân lý cho W01–W08):

Mô tả phạm vi thay vì nhớ cờ: **"push"** (chỉ đẩy) · **"release"** (đẩy + tag + notes) · **"pr"** (đẩy nhánh + Pull Request GitHub) · **"mr"** (đẩy nhánh + Merge Request GitLab) · **"merge"** (gom PR/MR đến → test → merge). Mặc định = push.

Mức `push/release/pr/mr` (ĐẨY ĐI) chạy bước 1-8 dưới. Mức `merge` (GOM VỀ) chạy nhánh riêng ở step 8 (đọc mục "Mức merge").

Bước 1, 3-4 áp dụng cho MỌI mức. Bước 2 (UAT) CHỈ `release`/`pr`/`mr`. Bước 5 (version tag) CHỈ mức `release`. Bước 6 đổi tên "sản phẩm viết": `release`→`RELEASE-vX.Y.Z.md`; `pr`/`mr`→ **PR/MR body** (cùng giọng người-dùng, cùng luật Known-limitations). `push` không cần văn bản, chỉ commit msg. Mức `merge` không viết note (chỉ báo cáo kết quả test + quyết định merge/không).

1. **CỔNG SỨC KHOẺ — `medic --ci`** (hoặc `python3 fdk/tools/medic.py --ci`). FAIL → **DỪNG**, in chỗ hở + lệnh sửa; không push khi đỏ. Warn (nợ đã biết) → cho qua nhưng LIỆT KÊ trong patch note.
   - **Rồi `python3 fdk/tools/ci-local.py`** (repo framework) — chạy TRỌN mọi step `run:` của mọi workflow GitHub tại local (L4). medic là L2; có gate CHỈ ở CI (search-index, skill-provenance, retrieval-eval…) — đã cháy 080926: medic xanh, push, CI đỏ 2 job. Đỏ → không push.
   - Gồm probe **`freshinstall`** (E2E): curl-cài overstack vào một dự án TRỐNG cô lập (mktemp ngoài repo) qua working-tree → assert 3 trụ + harness cắn + **orchestration-ready**. Đỏ = đường cài người-mới hỏng → KHÔNG push. Bản đầy đủ curl-github + acceptance live: `bash harness/scripts/fresh-install-smoke.sh --remote`.
2. **UAT gate — `/fdk-uat` (CHỈ mức `release`/`pr`/`mr`, KHÔNG `push` thường):** `medic --ci`/`ci-local` ở bước 1 chỉ cài qua `file://` working-tree — chứng minh "code trong máy lành", KHÔNG chứng minh "người lạ `curl` remote về chạy được" (lớp lỗi GH#77: "doc hứa mà user không nhận được", đo thật 2026-09-17 khi push `6c839d8` không hề qua UAT).
   - **Diff có năng lực MỚI** (skill mới / rule mới cắn được / engine-tool mới) → **BẮT BUỘC** chạy tối thiểu PHA 1 (canary: push nhánh tạm, curl-cài từ raw của chính nhánh đó, kiểm năng lực mới reachable) trước khi sang bước 7. PHA 2 (main-URL smoke, chờ CDN) chạy NGAY sau khi user duyệt merge/tag thật ở bước 8 — không phải lúc đề xuất.
   - **Diff thuần bugfix/refactor nội bộ, không thêm năng lực gì user thấy** → bỏ qua bước này, ghi rõ lý do trong checklist bước 7 ("không có năng lực mới — skip UAT").
   - **Không chắc diff có tính là "năng lực mới" hay không** → hỏi user, đừng tự quyết bỏ qua.
   - Push canary là side-effect thật (đẩy nhánh tạm lên remote) → DỪNG hỏi user trước khi chạy, cùng luật side-effect của skill này. FAIL ở pha nào → dừng ship, báo lỗi cụ thể + xoá canary (không phải "để sau").
3. **Git sạch:** `git status --short`; đảm bảo rác ephemeral (`scratchpad/…`) đã `.gitignore` + `git rm -r --cached` nếu lỡ track. Rà không có file bí mật/tạm lọt vào.
4. **Selftest/kiểm nhanh** các engine đụng tới (vd `council.py selftest`, test liên quan diff).
5. **Version:** `git tag --sort=-v:refname | head -1` → tag gần nhất `vX.Y.Z` → đề xuất **`vX.Y.(Z+1)`** (patch) hoặc minor/major nếu diff xứng — hỏi user nếu không chắc bậc.
6. **Patch note TRUNG THỰC (giọng release-note NGƯỜI DÙNG — kiểu Claude Code):** viết `RELEASE-vX.Y.Z.md`.
   - **Format:** header `Version X.Y.Z:` rồi danh sách bullet PHẲNG, mỗi bullet một dòng một ý.
   - **Giọng:** verb-first mô tả *thay đổi NGƯỜI DÙNG THẤY*, không dump commit/nội-bộ. `Fixed <triệu chứng> — <giờ ra sao>` · `Added <khả năng> — <dùng để làm gì>` · `Removed/Changed …`. Viết từ góc người đọc ("bạn/của bạn"), không SHA, không tên hàm trừ khi user gõ trực tiếp.
   - **Nhóm ngầm theo động từ:** Added/Changed trước, Fixed sau (như release-note Claude). KHÔNG cần tiêu đề nhóm nếu danh sách ngắn.
   - **Nguồn:** đọc `git log <tag-cũ>..HEAD` + scratch-log phiên → DỊCH commit kỹ-thuật sang câu người-dùng-hiểu (1 commit có thể gộp/tách thành bullet theo giá trị cảm nhận, không 1-1).
   - **Known-limitations (BẮT BUỘC nếu có phần nửa vời — điểm HƠN Claude):** proposal draft chưa impl, coverage một phần, warn medic đã biết → khai rõ "đang làm/đã biết". Im lặng = phóng đại (bài học council 2026-07-03).
7. **Hiện checklist + đề xuất lệnh** cho user (commit msg, push, tag/PR/MR, kết quả UAT pha 1 hoặc lý do skip). **DỪNG chờ duyệt.**
8. Sau khi user duyệt: thực thi theo mức. Không tự chạy bước side-effect trước khi có "yes". Nếu bước 2 đã chạy UAT pha 1 (PASS) → merge/tag/push xong thì chạy NGAY UAT pha 2 (main-URL smoke, chờ sentinel CDN) trước khi báo user "xong"; FAIL → gỡ commit khỏi remote theo `/fdk-uat` bước 5.
   - **push:** commit + `git push`.
   - **release:** commit + push + `git tag vX.Y.Z` + tạo release (notes = patch note).
   - **pr (GitHub):** commit + `git push -u origin <nhánh>` + `gh pr create --base <base> --head <nhánh> --title "…" --body-file <PR-body>`. Base mặc định = nhánh chính repo (vd `orca`), hỏi nếu không chắc.
   - **mr (GitLab):** commit + `git push -u origin <nhánh>` + `glab mr create --source-branch <nhánh> --target-branch <base> --title "…" --description "…"` (hoặc `-F <file>`).
   - **Chọn công cụ theo remote:** `git remote get-url origin` chứa `github.com`→`gh`, `gitlab`→`glab`. `ship pr`/`ship mr` ép rõ công cụ; nếu công cụ chưa cài/chưa auth (`gh auth status` / `glab auth status`) thì DỪNG, báo user cài+login (không tự làm).
   - **KHÔNG tự chèn `Closes #N`/`Fixes #N`** vào PR/MR body trừ khi user yêu cầu tường minh — để user giữ quyền đóng issue tay.

### Luồng theo repo_role (W00 chọn MỘT cột; W01–W08 bên trên mô tả cột `framework`)
| Bước | `framework` (Rheinmir/setup) | `module` (orca-graph, uiux-asset…) | `downstream` (dự án có `.llmwiki/`) | `foreign` (repo người khác) |
|---|---|---|---|---|
| Gate | `medic --ci` → `ci-local` (trên checkout sạch nếu cây có file lạ) | **commit trước** → test + eval + install-test CỦA CHÍNH NÓ (đọc từng rc; install-test clone từ HEAD nên chưa commit là chưa test) | test của dự án + `llmwiki-validate` + `medic` (chế độ downstream) | git sạch + test/CI của họ |
| UAT remote | khi diff có năng lực mới (B02) | smoke cài từ remote sau khi push (`install.sh` của module vào HOME tạm) | không | không |
| Version | `capability-stamp.py --update` KHI thứ đi xuống máy khách đổi (hook, shim, installer, tool global) — sha bề mặt không đổi vẫn phải bump, nếu không máy đã ở bản hiện tại sẽ không refresh | bump `VERSION` + hằng trong code + `CHANGELOG` | theo dự án | theo họ |
| Bước cuối | push (· tag/PR theo mức) | push → CHỜ CI xanh → tag + release → **re-pin ở framework** (`upstream_pin` trong `.overstack.yaml`: copy SKILL nếu đổi → `sync-skills.py` → ghi `commit`/`version` vào `fdk/skills.provenance.json` → ship framework) | push / pr | CHỈ pr / mr |
| Cấm | installer ghi vào repo này (tự từ chối rc 3) | `ci-local`, `capability-stamp` | đẩy file của framework, UAT, stamp | cài đặt, ghi cấu hình overstack, AI-attribution trái luật của họ |

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | conditional_required | mức = `release` | W05 version + tag `vX.Y.Z` + release notes | mức khác → skip | W06 |
| B02 | conditional_required | mức ∈ {release, pr, mr} VÀ diff có năng lực mới | UAT pha 1 trước W07, pha 2 sau W08 | bugfix/refactor nội bộ → skip, ghi lý do vào checklist; không chắc → clarify | W03 |
| B03 | user_optional | mức = `merge` | Vòng GOM VỀ riêng (mục dưới), bỏ W02, W05–W06 | PR đỏ → không merge PR đó | báo cáo tổng |

### Mức `merge` (GOM VỀ — duyệt-rồi-merge PR/MR đến)
Không viết note/tag. Bỏ qua bước 2, 5-6; thay bằng vòng test-per-request:
1. **Chọn công cụ theo remote** (như trên): `github.com`→`gh`, `gitlab`→`glab`. Chưa auth → DỪNG báo user.
2. **Liệt kê PR/MR đang mở của repo:**
   - GitHub: `gh pr list --json number,title,headRefName,mergeable,isDraft`
   - GitLab: `glab mr list` (hoặc `--output json` nếu bản hỗ trợ).
   Hiện danh sách cho user; nếu user chỉ định số cụ thể thì lọc, không thì hỏi làm hết hay chọn.
3. **Với mỗi PR/MR (một-tại-một, không gộp mù):**
   a. Kéo nhánh về LOCAL sạch: GitHub `gh pr checkout <n>`; GitLab `git fetch origin merge-requests/<n>/head:mr-<n> && git checkout mr-<n>` (hoặc `glab mr checkout <n>`).
   b. **Chạy GATE + TEST** trên nhánh đó: `medic --ci` + selftest/test liên quan diff của PR. Đây là điều kiện merge — KHÔNG merge khi chưa chạy.
   c. **Xanh** → đề xuất lệnh merge, **DỪNG chờ duyệt**, rồi merge: GitHub `gh pr merge <n> --squash` (hoặc --merge/--rebase theo repo); GitLab `glab mr merge <n>`. **Đỏ** → KHÔNG merge; báo cáo chỗ đỏ + để PR nguyên cho tác giả sửa.
   d. Sau merge: quay lại nhánh gốc (`git checkout <nhánh-cũ>`), dọn nhánh tạm.
4. **Báo cáo tổng:** mỗi PR/MR → đã-merge / bỏ-qua-vì-đỏ (kèm lý do) / bỏ-qua-vì-user.

### Validation và stopping
Điều kiện đi tiếp là rc của công cụ (medic, ci-local, fdk-uat, test), không phải model tự đánh giá. Mọi side-effect dừng ở W07 chờ "yes"; mức `merge` dừng chờ duyệt từng PR. Không retry push/tag tự động khi lỗi mạng — báo user.

### Examples
- **Positive (module):** ở repo `orca-graph` gõ "ship release" → W00 in `🏷 repo_role=module (khai báo)` → commit → `pytest tests` rc 0 → `evals/run.py` rc 0 → `tests/install-test.sh` rc 0 → bump `VERSION` → DỪNG duyệt → push → CI xanh → tag + release → nhắc bước re-pin ở `Rheinmir/setup` theo `upstream_pin`.
- **Boundary (foreign):** ở một repo không có stamp, không nhãn → W00 in `🏷 repo_role=foreign (suy luận: không có fdk/wiki, không có .harness-stamp)` → hỏi user xác nhận → chỉ đề xuất `ship pr`, đọc CONTRIBUTING của họ, không ghi file nào của overstack.
- **Positive:** "ship push" sau khi sửa doc → W01 xanh, B02 skip (không năng lực mới, ghi lý do), W03–W04 xanh → checklist + `git push` → user "yes" → push.
- **Boundary/failure:** "ship pr" có skill mới nhưng `ci-local` đỏ 1 job → blocked ở W01, in job đỏ + lệnh sửa, không push nhánh, không mở PR.
- **Boundary:** "ship merge" có 2 PR, PR #2 test đỏ → merge #1 sau duyệt, bỏ #2 kèm lý do (partial).
