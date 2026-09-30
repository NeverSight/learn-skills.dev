---
name: invoke-subagents
description: Khởi tạo và chạy một Subagent chuyên biệt trong một tiến trình/branch riêng biệt.
parameters:
  type: object
  properties:
    agent_name:
      type: string
      description: Tên của subagent cần gọi (vd ba, dev, tester)
    prompt:
      type: string
      description: Yêu cầu nhiệm vụ cụ thể gửi cho subagent đó
  required:
    - agent_name
    - prompt
---

# Lệnh khởi chạy Subagent
Khi skill này được gọi, hệ thống sẽ spawn một subagent tương ứng từ thư mục `.agents/agents/<agent_name>.md`.