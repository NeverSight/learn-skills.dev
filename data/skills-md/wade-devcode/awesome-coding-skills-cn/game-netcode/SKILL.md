---
name: game-netcode
description: 写多人/联网游戏时使用。同步模型、延迟、断线、防作弊。
category: gamedev
tags: [网络, 同步, 多人]
---

# 游戏联网同步

## 何时用

- 新增或修改任何多人联机逻辑（房间匹配、战斗同步、聊天广播）之前。
- 发现帧同步与状态同步混用、或不清楚权威端在哪里时。
- 遇到"客户端打了但服务端没算到"、"回放对不上"等同步类 bug 时。
- 准备接入帧同步 SDK 或自研 Relay 服务前做方案评审时。

## 核心规则

### 1. 选对同步模型

**规则：** 按游戏类型明确选择状态同步或帧同步，并在立项初期确定好权威端，后期切换代价极高。

**为什么：** 常见错误是用帧同步做 MMORPG——每帧广播全量输入，稍有延迟就全员卡顿；或者在格斗/RTS 里用状态同步，服务端每帧推送全局状态，带宽爆炸且客户端表现割裂。更隐蔽的错误是"临时先客户端权威，后面再改"，结果权威端逻辑散落到客户端每个角落，迁移时要全局重写。

**怎么做：**
- 格斗/RTS/竞技类：优先帧同步，输入上行、服务端转发、各端本地计算——前提是逻辑完全确定性（浮点要用定点或 libfixmath）。
- MMORPG/射击/休闲多人：优先状态同步，服务端跑权威逻辑，下发关键实体状态。
- 确定模型后立刻在设计文档写明「权威端：服务端」或「权威端：服务端转发，各客户端本地执行」，并在代码中用注释标注哪些函数只能在权威端调用。

---

### 2. 服务器权威：关键逻辑服务端校验

**规则：** 伤害计算、金币增减、技能命中判定等影响游戏公平性的逻辑必须在服务端执行并校验，客户端只负责表现与预测，不能只靠客户端上报结果。

**为什么：** 最常犯的错是"客户端算出伤害 150，发消息给服务端说'我打了 150 伤害'，服务端直接扣血"。这是最经典的游戏外挂入口——改一行本地代码就能无限秒杀。即使是"只是 Demo"也会留下习惯，真正上线时来不及改。

**怎么做：**
- 服务端持有所有玩家的 HP、金币、buff 列表等权威状态；客户端不能直接写这些值。
- 客户端发送的是**意图**（`MsgAttack{target_id, skill_id, client_tick}`），服务端收到后自己算伤害、自己扣血、再广播结果。
- 对高频操作做服务端速率限制（Rate Limit），防止通过高频请求刷出超额收益。
- 校验失败时服务端下发权威状态强制纠正客户端，而非静默忽略。

---

### 3. 延迟处理：预测 + 校正 + 插值三件套

**规则：** 客户端必须做本地预测（降低操作延迟感），服务端必须做状态校正（保证一致性），远端实体必须做插值（消除抖动），三者缺一不可。

**为什么：** 只做预测不做校正，高延迟玩家的角色会在服务端和客户端持续撕裂，最终位置对不上；只做插值不做预测，玩家按下跳跃键需要一个 RTT 才能看到角色起跳，手感极差；什么都不做，100ms 延迟就已经让动作游戏完全不可玩。

**怎么做：**
```
// 客户端预测：立刻在本地执行输入
void OnPlayerInput(InputCmd cmd) {
    ApplyInputLocally(cmd);          // 立刻移动本地角色
    pendingInputs.push_back(cmd);    // 暂存等服务端确认
    SendToServer(cmd);
}

// 服务端 ACK 后做 Reconciliation
void OnServerState(ServerSnapshot snap) {
    // 回滚到 snap.tick 时刻，重放 snap.tick 之后的本地输入
    RollbackTo(snap);
    for (auto& cmd : pendingInputs) {
        if (cmd.tick > snap.tick) ApplyInputLocally(cmd);
    }
}

// 远端实体插值（不是本地玩家）
void UpdateRemoteEntity(float deltaTime) {
    renderPos = Vector3.Lerp(renderPos, authorativePos, deltaTime * lerpSpeed);
}
```
- 插值缓冲区保持 2-3 帧的历史快照，避免网络抖动直接暴露到画面上。

---

### 4. 断线重连：状态可恢复、消息幂等、重连补帧

**规则：** 网络游戏必须将断线重连作为一等功能设计，而不是事后补丁。服务端状态快照可随时还原，消息处理天然幂等，重连后能补全缺失的帧/事件。

**为什么：** 最常见的事故：断线重连成功，但服务端已经销毁了该玩家的战斗实体，客户端收到空数据崩溃；或者消息重发时，金币被加了两次——因为消息处理没有去重逻辑。另一个坑：帧同步游戏断线后无法快速追帧，重连要从第 0 帧开始 replay，追帧期间玩家干等几分钟。

**怎么做：**
- 每条上行消息带唯一 `msg_id`，服务端去重表（TTL 5 分钟）防止重放。
- 服务端每隔 N 秒（或每个逻辑段结束时）持久化全量状态快照，断线玩家重连时从最近快照恢复，再补发快照之后的增量事件。
- 帧同步游戏提供「快进追帧」模式：跳过渲染，全速 replay 逻辑帧，追上当前帧后切回正常渲染。
- 重连握手协议中服务端明确告知客户端「你断线时在第 X 帧，当前第 Y 帧，以下是补帧数据」。

---

### 5. 带宽与频率：按需压缩，拒绝全量高频广播

**规则：** 同步数据必须做增量差分、字段量化、AOI（Area of Interest）裁剪；同步频率按实体重要性分级，不对所有实体以最高频率广播全量状态。

**为什么：** 最常见的性能炸弹：100 个玩家的游戏，每帧把 100 个玩家的全量状态（位置、HP、所有 buff）广播给所有人——带宽是 O(N²) 的。50 个玩家时服务器还扛得住，200 人时直接打满带宽。量化（Quantization）也经常被忽略：用 float32 传位置精度远超需求，用 int16 传量化坐标可以砍掉一半带宽。

**怎么做：**
- **增量同步**：只发上一帧到这一帧发生变化的字段，未变化字段不发送；用 dirty flag 标记哪些字段被修改。
- **量化**：位置坐标量化到厘米精度（int16，±327m 范围足够大多数地图）；旋转用 uint8/uint16 表示角度。
- **AOI**：玩家只接收周围一定半径内实体的同步数据，超出范围的实体直接不广播；AOI 半径按游戏类型调整（MOBA 全图可见 vs 射击游戏 100m）。
- **频率分级**：本地玩家 60Hz，周围可见玩家 20Hz，远处/静止实体 5Hz 甚至事件驱动。

## 正例 / 反例

### 反例：客户端上报伤害结果，服务端直接信任

```python
# 反例 — 客户端计算完伤害直接告诉服务端"扣多少血"
# client.py
damage = calc_damage_locally(my_atk, target_def)  # 本地算
send_to_server({"type": "deal_damage", "target": enemy_id, "amount": damage})  # ❌ 外挂改这一行

# server.py
def on_deal_damage(msg):
    target = get_entity(msg["target"])
    target.hp -= msg["amount"]   # ❌ 直接信任客户端上报的数值
    broadcast_hp_update(target)
```

```python
# 正例 — 客户端只发意图，服务端自己算伤害
# client.py
send_to_server({"type": "attack", "target": enemy_id, "skill": skill_id, "tick": local_tick})  # ✅ 只发意图

# server.py
def on_attack(msg, attacker):
    target = get_entity(msg["target"])
    skill = get_skill(msg["skill"])
    # 服务端用权威数据计算
    damage = calc_damage(attacker.atk, target.def_, skill.multiplier)  # ✅ 服务端自己算
    target.hp -= damage
    broadcast_hp_update(target)
```

---

### 反例：每帧广播所有实体全量状态

```python
# 反例 — 每个 Tick 给每个玩家发所有实体的全量数据
def game_tick():
    all_state = serialize_all_entities()   # ❌ 全量，可能是几十 KB
    for player in all_players:
        player.send(all_state)             # ❌ O(N²) 广播
```

```python
# 正例 — 增量 + AOI 裁剪
def game_tick():
    for player in all_players:
        nearby = get_entities_in_aoi(player.pos, radius=150)   # ✅ AOI 裁剪
        delta = serialize_dirty_fields(nearby, since=player.last_ack_tick)  # ✅ 只发变更字段
        if delta:
            player.send(delta)
        player.last_ack_tick = current_tick
```

## 自查清单

- [ ] 同步模型（帧同步/状态同步）已在设计文档中明确，权威端已确定并在代码中有注释标注。
- [ ] 伤害、金币、命中等影响公平性的逻辑，全部在服务端计算，客户端没有直接上报结果的接口。
- [ ] 客户端做了本地预测，并在收到服务端 ACK 后执行 Reconciliation 回滚重放。
- [ ] 每条上行消息有唯一 msg_id，服务端有去重逻辑防止消息重放。
- [ ] 断线重连有完整流程：服务端状态快照 → 恢复实体 → 补发增量事件/追帧。
- [ ] 同步数据做了增量差分，高频字段（位置、旋转）做了量化压缩。
- [ ] AOI 或等效机制已接入，玩家不会收到与自己完全无关的远端实体更新。
