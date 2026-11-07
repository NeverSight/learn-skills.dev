---
name: wayfinder
disable-model-invocation: true
description: >-
  Lập bản đồ cho một chunk việc QUÁ LỚN với một phiên agent và còn MÙ MỜ — dựng một bản đồ
  các ticket QUYẾT ĐỊNH trên ledger issue, rồi giải từng ticket một cho tới khi đường tới đích
  hiện rõ. Gọi bằng tay khi có một ý tưởng lớn chưa rõ hình dạng, TRƯỚC cả /propose. Chỉ-gọi-tay.
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: orchestrate
---



# Wayfinder — tìm đường, không lao vào đích

Một ý tưởng lớn vừa tới — quá lớn cho một phiên agent, và bọc trong sương: **đường** từ đây tới **đích** chưa hiện. Wayfinding là tìm cái đường đó, không phải lao thẳng vào đích. Skill này vẽ đường thành một **bản đồ** trên ledger issue, rồi làm các **ticket quyết định** của nó — mỗi ticket là *một câu hỏi mà lời giải là một quyết định*, không phải một lát cắt build — từng cái một, cho tới khi đường tới đích rõ và không còn gì để quyết.

Đây là bậc **trước** `/propose`: propose giả định đã biết hình dạng công việc; wayfinder dành cho lúc **chưa biết**.

## WHAT

### Purpose và context
- **Purpose:** tìm ĐƯỜNG tới đích cho một chunk việc quá lớn và còn mù mờ — dựng bản đồ các ticket quyết định trên ledger issue rồi giải từng ticket tới khi đường rõ và không còn gì để quyết.
- **Trigger (when to use):** gọi bằng tay khi có một ý tưởng lớn chưa rõ hình dạng, TRƯỚC cả `/propose`. Chỉ-gọi-tay (`disable-model-invocation: true`).
- **Non-goals:** không sinh deliverable/build (đó là sau `/propose`); không giải hộ phía người trong ticket HITL; không cắt sẵn sương thành ticket; không giải việc nằm sau đích (out of scope).

### Mental model
`ý tưởng loose → Destination → bản đồ (issue wayfinder:map, chỉ mục) → ticket quyết định (issue con, cạnh chặn) → frontier → giải một ticket → Decisions-so-far + dọn sương → … → đường rõ → bàn giao /propose`.

#### Plan, don't do
Wayfinder mặc định là **lập kế hoạch**: mỗi ticket giải một quyết định, và bản đồ xong khi đường đã rõ — không còn gì phải quyết trước khi ai đó đi làm. Cái kéo bạn *nhảy vào làm* thường là tín hiệu đã tới **mép bản đồ** và tới lúc bàn giao sang `/propose`. Sinh **quyết định**, không sinh **deliverable**.

#### Gọi tên bằng TÊN, không bằng id
Mỗi bản đồ và ticket là một issue, nên có một **tên** — tiêu đề của nó. Trong mọi thứ người đọc (tường thuật, Decisions-so-far), gọi bằng tên đó, không bao giờ bằng id trần. Một bức tường `#42, #43, #44` không đọc nổi; tên đọc được ngay. Id và link không biến mất — tên bọc lấy link — nhưng chúng đi *bên trong* tên, không thay tên.

#### Bốn kiểu ticket
Mỗi ticket là **HITL** (có người sống trả lời) hoặc **AFK** (agent chạy một mình). Một ticket HITL chỉ giải qua trao đổi sống; **agent không bao giờ đứng thay phía người** — một agent grilling mà tự trả lời câu hỏi của chính mình là đã phá vỡ điều này.

- **research** (AFK) — đọc tài liệu/API/kho tri thức để lôi ra một *fact* mà một quyết định đang chờ. Giải bằng một subagent `/research` (hoặc `/agent-reach`). Dùng khi cần tri thức ngoài thư mục hiện tại.
- **prototype** (HITL) — nâng độ phân giải cuộc bàn bằng một bản thô cụ thể để phản ứng: một outline, một bản nháp, một stub, hoặc UI/logic. Dùng khi "trông thế nào" / "hành xử ra sao" là câu hỏi chính.
- **grilling** (HITL) — hội thoại từng câu một. Trường hợp mặc định.
- **task** (HITL hoặc AFK) — việc TAY phải xong trước khi một *quyết định* làm được: đăng ký một dịch vụ để xét API, cấp quyền, dời dữ liệu để thấy hình dạng. Kiểu duy nhất *làm* thay vì *quyết* — và nó đáng chỗ vì mở khoá một quyết định, không phải vì giao deliverable.

#### Fog of war
Bản đồ *cố ý* chưa đầy đủ: đừng vẽ cái chưa thấy. Ngoài các ticket sống là **sương** — cái nhìn mờ về những quyết định biết là sẽ tới nhưng chưa ghim được, vì chúng treo trên các câu hỏi còn mở. Giải một ticket **dọn sương phía trước nó**, cho tốt nghiệp bất cứ gì giờ đã ghim được thành ticket mới — từng cái một, tới khi đường tới đích rõ.

**Sương hay ticket?** Test là **đặt được câu hỏi cho chính xác BÂY GIỜ chưa** — *không* phải trả lời được chưa.
- **Ticket** khi câu hỏi đã sắc — kể cả khi nó bị chặn và bạn chưa làm được.
- **Not yet specified** khi bạn chưa phát biểu sắc được. Đừng cắt sẵn sương thành các mảnh cỡ-ticket: nó thô hơn một ticket, một mảng có thể tốt nghiệp thành vài ticket, hoặc không cái nào, khi frontier chạm tới.

#### Out of scope
Sương chỉ gom *về phía* đích. Đích cố định phạm vi, nên việc vượt nó là **out of scope** — không phải sương, không thuộc Not-yet-specified. Nó có mục riêng: việc bạn ý thức loại khỏi nỗ lực *này*. Out-of-scope không bao giờ tốt nghiệp. Một ticket đã tồn tại mà hoá ra nằm sau đích → **đóng nó** và để lại một dòng ở Out-of-scope, không giải nó trên đường.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | ý tưởng loose | có (chế độ Chart) | thứ cần tìm đường |
| In | bản đồ (issue `wayfinder:map`) | có (chế độ Work) | map đã dựng |
| In | ticket cụ thể | không (chế độ Work) | không có → lấy ticket frontier đầu tiên |
| Out | issue bản đồ + issue con + cạnh chặn | Chart | Destination, Not-yet-specified phác sương, Decisions-so-far rỗng |
| Out | một ticket đã claim → giải → đóng + con trỏ trong Decisions-so-far | Work | kèm ticket mới lộ ra / sương tốt nghiệp / out-of-scope cập nhật |

### Rules và capabilities
- RULE-01 (MUST): **Chỉ-gọi-tay** (`disable-model-invocation: true`) — wayfinder là một hành động có chủ ý của user, không phải thứ model tự nhảy vào. Xem `[[skill-craft]]`.
- RULE-02 (MUST): **Plan, don't do** — sinh quyết định, không sinh deliverable. Muốn nhảy vào làm = tới mép bản đồ = bàn giao `/propose`.
- RULE-03 (MUST): **Một ticket một phiên** (trừ research), và **claim trước khi làm** (dùng `frontier.py` + ô `claim` của ledger).
- RULE-04 (MUST): Ledger là nguồn chân lý; tracker remote là mirror. Đọc `[[issue-tracker]]` cho cách diễn đạt ở repo này.
- Capabilities: đọc/ghi issue trên ledger (tạo, nối cạnh chặn, claim, đóng); truy vấn frontier; hội thoại sống với user cho ticket HITL; bắn subagent research song song.

### Failure boundaries
- Vẽ frontier không lôi ra sương nào → đường đã rõ, không cần bản đồ: **dừng**, hỏi user muốn đi tiếp thế nào.
- Ticket HITL không có người trả lời → **blocked**; agent không tự trả lời thay.
- Ticket đã claim bởi phiên khác → không giải; chọn ticket frontier khác.
- Lời giải lộ ra việc nằm sau đích → đóng ticket, ghi Out-of-scope (**cancelled** cho ticket đó).
- Cái kéo muốn nhảy vào làm → tới mép bản đồ → bàn giao `/propose`.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | judgment | ý tưởng | (Chart) Đặt tên đích qua `/grilling` + `/domain-modeling` | một câu Destination | — |
| W02 | judgment | Destination | (Chart) Vẽ frontier theo bề rộng | quyết định mở + bước đầu | không có sương → dừng, hỏi user |
| W03 | effect | W01–W02 | (Chart) Tạo bản đồ + ticket ghim được, nối cạnh chặn lượt hai | issue map + issue con | — |
| W04 | effect | ticket research | (Chart) Bắn subagent research song song, rồi dừng | phát hiện gắn con trỏ | — |
| W05 | deterministic | bản đồ | (Work) Nạp bản đồ, chọn ticket (user nêu hoặc `frontier.py --map <id>`), **claim trước** | ticket đã claim | đã bị claim → chọn cái khác |
| W06 | judgment | ticket | (Work) Giải — zoom khi cần; HITL thì hỏi người sống | lời giải | bí → `/grilling` + `/domain-modeling` |
| W07 | effect | lời giải | (Work) Ghi resolution, đóng issue (`status: done`), append Decisions-so-far; tạo ticket mới / tốt nghiệp sương / loại out-of-scope | bản đồ cập nhật | — |

Chi tiết từng bước (nguồn chân lý cho W01–W07):

Hai chế độ. Cả hai: **không bao giờ giải quá một ticket mỗi phiên** — trừ research.

#### Chart the map (dựng bản đồ)
User gọi với một ý tưởng loose.
1. **Đặt tên đích.** Chạy `/grilling` + `/domain-modeling` (nếu có) ghim đích này tìm đường tới cái gì. Đích cố định phạm vi nên chốt trước. → **Xong khi:** một câu Destination mà mọi phiên sau định hướng được vào.
2. **Vẽ frontier.** Grill lại, **theo bề rộng**: fan ra khắp không gian thay vì sâu một luồng, lôi ra các quyết định mở và bước đầu làm được ngay. Không lôi ra sương nào → đường đã rõ, không cần bản đồ; dừng, hỏi user muốn đi tiếp thế nào.
3. **Tạo bản đồ** (nhãn `wayfinder:map`): Destination + Notes điền, Decisions-so-far rỗng, sương phác vào Not-yet-specified.
4. **Tạo các ticket ghim được** thành issue con — rồi nối cạnh chặn ở **lượt hai** (issue cần id trước khi trỏ nhau). → **Xong khi:** mọi ticket ghim-được đã có, phần chưa ghim ở lại sương.
5. **Bắn subagent research.** Mỗi ticket `research` → một subagent giải song song, ghi phát hiện, gắn con trỏ ngữ cảnh từ ticket.
6. Dừng — dựng bản đồ là việc của một phiên; nó không tự-giải ticket nào.

#### Work through the map (làm qua bản đồ)
User gọi với một bản đồ. Ticket là **tuỳ chọn** — không có thì bạn chọn quyết định kế, không phải user.
1. Nạp **bản đồ** (view thấp-phân-giải, không phải mọi thân ticket).
2. Chọn ticket. User nêu thì dùng. Không thì lấy ticket **frontier** đầu tiên (`frontier.py --map <id>`). **Claim nó** — ghi ô `claim`, **trước** mọi việc.
3. Giải — **zoom khi cần**: lấy thân đầy đủ của ticket liên quan trên yêu cầu; gọi các skill Notes chỉ tên. Bí thì `/grilling` + `/domain-modeling`.
4. Ghi lời giải: post lời giải làm resolution, **đóng** issue (`status: done`), **append** một con trỏ vào Decisions-so-far của bản đồ.
5. Thêm ticket mới lộ ra (tạo-rồi-nối); cho tốt nghiệp sương mà lời giải vừa ghim được, dọn khỏi Not-yet-specified. Lời giải lộ ra một ticket nằm sau đích → **loại out of scope**. Lời giải phủ định phần khác của bản đồ → cập nhật/xoá ticket đó.

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | user_optional | user gọi với bản đồ có sẵn | chế độ Work through the map (W05–W07) thay cho Chart (W01–W04) | — | kết thúc phiên sau một ticket |
| B02 | conditional_required | ticket kiểu research | giải bằng subagent `/research` (hoặc `/agent-reach`), được phép song song quá một ticket | — | W07 |
| B03 | conditional_required | ticket HITL (prototype/grilling/task-HITL) | chỉ giải qua trao đổi sống với người | không có người → blocked | W07 |
| B04 | recovery | lời giải phủ định phần khác của bản đồ | cập nhật/xoá ticket đó | — | W07 |

### Validation và stopping
Chart dừng sau W04 (không tự giải ticket nào). Work dừng sau đúng một ticket (trừ research). Bản đồ xong khi đường tới đích rõ và không còn gì để quyết → bàn giao `/propose`. Ticket tiếp theo do `frontier.py` + ô `claim` quyết, không đoán.

### Examples
- **Positive:** "/wayfinder chuyển overstack sang multi-model dispatch" → grill ra Destination một dòng, frontier lộ 3 ticket (1 research về API provider, 2 grilling) → tạo map `wayfinder:map` + 3 issue con, nối cạnh chặn lượt hai, bắn 1 subagent research → dừng.
- **Boundary/failure:** "/wayfinder <map>" nhưng ticket frontier là grilling (HITL) và user vắng → blocked, agent không tự trả lời câu hỏi của mình; không giải ticket thứ hai trong phiên.

### Reference — Bản đồ
Bản đồ là **một issue** trên ledger (nhãn `wayfinder:map`). Ticket của nó là issue con. Bản đồ là một **chỉ mục**, không phải một kho: nó liệt kê các quyết định đã làm và trỏ tới ticket giữ chi tiết — một quyết định sống ở đúng một chỗ (ticket của nó), bản đồ không kể lại, chỉ gist và link. Cách bản đồ, ticket con, cạnh chặn, và frontier query sống ở đâu là **tuỳ tracker** — đọc `[[issue-tracker]]` § "Wayfinding operations".

Thân bản đồ (nạp một lần mỗi phiên):

```markdown
## Destination
<đi tới cuối bản đồ này trông như thế nào — spec, quyết định, hay thay đổi mà nỗ lực này tìm đường tới. Một hai dòng; mỗi phiên định hướng vào nó trước khi chọn ticket.>

## Decisions so far
<!-- chỉ mục — một dòng mỗi ticket đã đóng: đủ để phán đoán liên quan, rồi zoom link lấy chi tiết -->
- [<tên ticket đã đóng>](link) — <gist một dòng của lời giải>

## Not yet specified
<!-- fog of war: sương trong-phạm-vi chưa ticket được; tốt nghiệp khi frontier tiến tới -->

## Out of scope
<!-- việc bị loại khỏi ĐÍCH này; đóng, không bao giờ tốt nghiệp -->
```

Ticket là issue con, thân là câu hỏi, cỡ vừa một phiên:

```markdown
## Question
<quyết định hay điều tra mà ticket này giải>
```

## Origin
- Chưng cất từ `mattpocock/skills` — `skills/engineering/wayfinder/SKILL.md` (clone `scratchpad/mattpocock-skills/`, 2026-07-15).
- Absorb qua `/propose` → `150726-mattpocock-absorb` (T8), task `T-260715-01`. Đứng trên hạ tầng ledger T6/T7.
- **Commit:** _(verify-before-commit điền)_
