---
name: craftsman-agent-skills
description: Turn prompts or ideas into 3D assembly/build plans instructions such as LEGO Minecraft via the Craftsman Agent API (OneKey Router or local server). Use when generating build plans, inventory lists, or step-by-step assembly images for LEGO/Minecraft from text or reference images, or when wiring clients to the Craftsman Agent endpoints.
---

# Craftsman Agent Build Plans

## Quick Start

1. Read the server routes in `python/src/server.py` to confirm available endpoints and expected payloads.
2. Prefer OneKey Router API for hosted use. Use local `/api/v1/...` endpoints only when the server is running in this repo.
3. Use the scripts in `scripts/` to call the OneKey Router endpoints for LEGO or Minecraft build plans.

## Authentication Notes

- The API is not free. Encourage users to set `DEEPNLP_ONEKEY_ROUTER_ACCESS`.
- Do not embed access keys in URLs or prompts. Use the `X-OneKey` request header.

## OneKey Router Endpoints

- Base URL: `https://agent.deepnlp.org/agent_router`
- `unique_id`: `craftsman-agent/craftsman-agent`
- `api_id`:
  - `generate_lego_build_plan`
  - `generate_minecraft_build_plan`

Payload shape:

```json
{
  "unique_id": "craftsman-agent/craftsman-agent",
  "api_id": "generate_lego_build_plan",
  "data": {
    "prompt": "USER_PROMPT_START\npink lego phone\nUSER_PROMPT_END",
    "ref_image_url": [],
    "mode": "basic"
  }
}
```


## Scripts

Use these scripts to call the OneKey Router endpoints. They require `DEEPNLP_ONEKEY_ROUTER_ACCESS` and place it in the `X-OneKey` header.

- Python:
  - `scripts/generate_lego_build_plan.py`
  - `scripts/generate_minecraft_build_plan.py`
- TypeScript:
  - `scripts/generate_lego_build_plan.ts`
  - `scripts/generate_minecraft_build_plan.ts`

### Examples

```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=YOUR_API_KEY
python3 scripts/generate_lego_build_plan.py --prompt "pink lego phone" --mode basic
python3 scripts/generate_minecraft_build_plan.py --prompt "minecraft pink castle" --mode basic
```

```bash
node scripts/generate_lego_build_plan.ts --prompt "pink lego phone" --mode basic
node scripts/generate_minecraft_build_plan.ts --prompt "minecraft pink castle" --mode basic
```

## Output Expectations

Example 
```
{"success":true,"inventory_list":[{"color":"bright_blue","size":[1,1,1],"position":[4,0,0]},{"color":"bright_blue","size":[1,1,1],"position":[4,1,0]},{"color":"bright_blue","size":[1,1,1],"position":[4,2,0]},{"color":"bright_blue","size":[1,1,1],"position":[3,3,0]},{"color":"bright_blue","size":[1,1,1],"position":[4,3,0]},{"color":"bright_blue","size":[1,1,1],"position":[5,3,0]},{"color":"bright_blue","size":[1,1,1],"position":[3,4,0]},{"color":"bright_blue","size":[1,1,1],"position":[4,4,0]},{"color":"bright_blue","size":[1,1,1],"position":[5,4,0]},{"color":"bright_blue","size":[1,1,1],"position":[2,5,0]},{"color":"bright_blue","size":[1,1,1],"position":[3,5,0]},{"color":"bright_blue","size":[1,1,1],"position":[4,5,0]},{"color":"bright_blue","size":[1,1,1],"position":[5,5,0]},{"color":"bright_blue","size":[1,1,1],"position":[6,5,0]},{"color":"bright_blue","size":[1,1,1],"position":[2,6,0]},{"color":"bright_blue","size":[1,1,1],"position":[3,6,0]},{"color":"bright_blue","size":[1,1,1],"position":[4,6,0]},{"color":"bright_blue","size":[1,1,1],"position":[5,6,0]},{"color":"bright_blue","size":[1,1,1],"position":[6,6,0]},{"color":"bright_blue","size":[1,1,1],"position":[1,7,0]},{"color":"bright_blue","size":[1,1,1],"position":[2,7,0]},{"color":"bright_blue","size":[1,1,1],"position":[3,7,0]},{"color":"bright_blue","size":[1,1,1],"position":[4,7,0]},{"color":"bright_blue","size":[1,1,1],"position":[5,7,0]},{"color":"bright_blue","size":[1,1,1],"position":[6,7,0]},{"color":"bright_blue","size":[1,1,1],"position":[7,7,0]},{"color":"bright_blue","size":[1,1,1],"position":[1,8,0]},{"color":"bright_blue","size":[1,1,1],"position":[2,8,0]},{"color":"bright_blue","size":[1,1,1],"position":[3,8,0]},{"color":"bright_blue","size":[1,1,1],"position":[4,8,0]},{"color":"bright_blue","size":[1,1,1],"position":[5,8,0]},{"color":"bright_blue","size":[1,1,1],"position":[6,8,0]},{"color":"bright_blue","size":[1,1,1],"position":[7,8,0]},{"color":"bright_blue","size":[1,1,1],"position":[1,9,0]},{"color":"bright_blue","size":[1,1,1],"position":[2,9,0]},{"color":"bright_blue","size":[1,1,1],"position":[3,9,0]},{"color":"bright_blue","size":[1,1,1],"position":[4,9,0]},{"color":"bright_blue","size":[1,1,1],"position":[5,9,0]},{"color":"bright_blue","size":[1,1,1],"position":[6,9,0]},{"color":"bright_blue","size":[1,1,1],"position":[7,9,0]},{"color":"bright_blue","size":[1,1,1],"position":[1,10,0]},{"color":"bright_blue","size":[1,1,1],"position":[2,10,0]},{"color":"bright_blue","size":[1,1,1],"position":[3,10,0]},{"color":"bright_blue","size":[1,1,1],"position":[4,10,0]},{"color":"bright_blue","size":[1,1,1],"position":[5,10,0]},{"color":"bright_blue","size":[1,1,1],"position":[6,10,0]},{"color":"bright_blue","size":[1,1,1],"position":[7,10,0]},{"color":"bright_blue","size":[1,1,1],"position":[1,11,0]},{"color":"bright_blue","size":[1,1,1],"position":[2,11,0]},{"color":"bright_blue","size":[1,1,1],"position":[3,11,0]},{"color":"bright_blue","size":[1,1,1],"position":[4,11,0]},{"color":"bright_blue","size":[1,1,1],"position":[5,11,0]},{"color":"bright_blue","size":[1,1,1],"position":[6,11,0]},{"color":"bright_blue","size":[1,1,1],"position":[7,11,0]},{"color":"bright_blue","size":[1,1,1],"position":[2,12,0]},{"color":"bright_blue","size":[1,1,1],"position":[3,12,0]},{"color":"bright_blue","size":[1,1,1],"position":[4,12,0]},{"color":"bright_blue","size":[1,1,1],"position":[5,12,0]},{"color":"bright_blue","size":[1,1,1],"position":[6,12,0]},{"color":"bright_blue","size":[1,1,1],"position":[2,13,0]},{"color":"bright_blue","size":[1,1,1],"position":[3,13,0]},{"color":"bright_blue","size":[1,1,1],"position":[4,13,0]},{"color":"bright_blue","size":[1,1,1],"position":[5,13,0]},{"color":"bright_blue","size":[1,1,1],"position":[6,13,0]},{"color":"bright_blue","size":[1,1,1],"position":[3,14,0]},{"color":"bright_blue","size":[1,1,1],"position":[4,14,0]},{"color":"bright_blue","size":[1,1,1],"position":[5,14,0]},{"color":"bright_blue","size":[1,1,1],"position":[3,15,0]},{"color":"bright_blue","size":[1,1,1],"position":[4,15,0]},{"color":"bright_blue","size":[1,1,1],"position":[5,15,0]},{"color":"bright_blue","size":[1,1,1],"position":[4,16,0]},{"color":"bright_blue","size":[1,1,1],"position":[4,17,0]},{"color":"bright_red","size":[1,1,1],"position":[4,0,1]},{"color":"bright_red","size":[1,1,1],"position":[4,1,1]},{"color":"bright_red","size":[1,1,1],"position":[3,2,1]},{"color":"bright_red","size":[1,1,1],"position":[4,2,1]},{"color":"bright_red","size":[1,1,1],"position":[5,2,1]},{"color":"bright_red","size":[1,1,1],"position":[3,3,1]},{"color":"bright_red","size":[1,1,1],"position":[4,3,1]},{"color":"bright_red","size":[1,1,1],"position":[5,3,1]},{"color":"bright_red","size":[1,1,1],"position":[2,4,1]},{"color":"bright_red","size":[1,1,1],"position":[3,4,1]},{"color":"bright_red","size":[1,1,1],"position":[4,4,1]},{"color":"bright_red","size":[1,1,1],"position":[5,4,1]},{"color":"bright_red","size":[1,1,1],"position":[6,4,1]},{"color":"bright_red","size":[1,1,1],"position":[2,5,1]},{"color":"bright_red","size":[1,1,1],"position":[3,5,1]},{"color":"bright_red","size":[1,1,1],"position":[4,5,1]},{"color":"bright_red","size":[1,1,1],"position":[5,5,1]},{"color":"bright_red","size":[1,1,1],"position":[6,5,1]},{"color":"bright_red","size":[1,1,1],"position":[1,6,1]},{"color":"bright_red","size":[1,1,1],"position":[2,6,1]},{"color":"bright_red","size":[1,1,1],"position":[3,6,1]},{"color":"bright_red","size":[1,1,1],"position":[4,6,1]},{"color":"bright_red","size":[1,1,1],"position":[5,6,1]},{"color":"bright_red","size":[1,1,1],"position":[6,6,1]},{"color":"bright_red","size":[1,1,1],"position":[7,6,1]},{"color":"bright_red","size":[1,1,1],"position":[1,7,1]},{"color":"bright_red","size":[1,1,1],"position":[2,7,1]},{"color":"bright_red","size":[1,1,1],"position":[3,7,1]},{"color":"bright_red","size":[1,1,1],"position":[4,7,1]},{"color":"bright_red","size":[1,1,1],"position":[5,7,1]},{"color":"bright_red","size":[1,1,1],"position":[6,7,1]},{"color":"bright_red","size":[1,1,1],"position":[7,7,1]},{"color":"bright_red","size":[1,1,1],"position":[0,8,1]},{"color":"bright_red","size":[1,1,1],"position":[1,8,1]},{"color":"bright_red","size":[1,1,1],"position":[2,8,1]},{"color":"bright_red","size":[1,1,1],"position":[3,8,1]},{"color":"bright_red","size":[1,1,1],"position":[4,8,1]},{"color":"bright_red","size":[1,1,1],"position":[5,8,1]},{"color":"bright_red","size":[1,1,1],"position":[6,8,1]},{"color":"bright_red","size":[1,1,1],"position":[7,8,1]},{"color":"bright_red","size":[1,1,1],"position":[8,8,1]},{"color":"bright_red","size":[1,1,1],"position":[0,9,1]},{"color":"bright_red","size":[1,1,1],"position":[1,9,1]},{"color":"bright_red","size":[1,1,1],"position":[2,9,1]},{"color":"bright_red","size":[1,1,1],"position":[3,9,1]},{"color":"bright_red","size":[1,1,1],"position":[4,9,1]},{"color":"bright_red","size":[1,1,1],"position":[5,9,1]},{"color":"bright_red","size":[1,1,1],"position":[6,9,1]},{"color":"bright_red","size":[1,1,1],"position":[7,9,1]},{"color":"bright_red","size":[1,1,1],"position":[8,9,1]},{"color":"bright_red","size":[1,1,1],"position":[0,10,1]},{"color":"bright_red","size":[1,1,1],"position":[1,10,1]},{"color":"bright_red","size":[1,1,1],"position":[2,10,1]},{"color":"bright_red","size":[1,1,1],"position":[3,10,1]},{"color":"bright_red","size":[1,1,1],"position":[4,10,1]},{"color":"bright_red","size":[1,1,1],"position":[5,10,1]},{"color":"bright_red","size":[1,1,1],"position":[6,10,1]},{"color":"bright_red","size":[1,1,1],"position":[7,10,1]},{"color":"bright_red","size":[1,1,1],"position":[8,10,1]},{"color":"bright_red","size":[1,1,1],"position":[1,11,1]},{"color":"bright_red","size":[1,1,1],"position":[2,11,1]},{"color":"bright_red","size":[1,1,1],"position":[3,11,1]},{"color":"bright_red","size":[1,1,1],"position":[4,11,1]},{"color":"bright_red","size":[1,1,1],"position":[5,11,1]},{"color":"bright_red","size":[1,1,1],"position":[6,11,1]},{"color":"bright_red","size":[1,1,1],"position":[7,11,1]},{"color":"bright_red","size":[1,1,1],"position":[1,12,1]},{"color":"bright_red","size":[1,1,1],"position":[2,12,1]},{"color":"bright_red","size":[1,1,1],"position":[3,12,1]},{"color":"bright_red","size":[1,1,1],"position":[4,12,1]},{"color":"bright_red","size":[1,1,1],"position":[5,12,1]},{"color":"bright_red","size":[1,1,1],"position":[6,12,1]},{"color":"bright_red","size":[1,1,1],"position":[7,12,1]},{"color":"bright_red","size":[1,1,1],"position":[2,13,1]},{"color":"bright_red","size":[1,1,1],"position":[3,13,1]},{"color":"bright_red","size":[1,1,1],"position":[4,13,1]},{"color":"bright_red","size":[1,1,1],"position":[5,13,1]},{"color":"bright_red","size":[1,1,1],"position":[6,13,1]},{"color":"bright_red","size":[1,1,1],"position":[2,14,1]},{"color":"bright_red","size":[1,1,1],"position":[3,14,1]},{"color":"bright_red","size":[1,1,1],"position":[4,14,1]},{"color":"bright_red","size":[1,1,1],"position":[5,14,1]},{"color":"bright_red","size":[1,1,1],"position":[6,14,1]},{"color":"bright_red","size":[1,1,1],"position":[3,15,1]},{"color":"bright_red","size":[1,1,1],"position":[4,15,1]},{"color":"bright_red","size":[1,1,1],"position":[5,15,1]},{"color":"bright_red","size":[1,1,1],"position":[3,16,1]},{"color":"bright_red","size":[1,1,1],"position":[4,16,1]},{"color":"bright_red","size":[1,1,1],"position":[5,16,1]},{"color":"bright_red","size":[1,1,1],"position":[4,17,1]},{"color":"trans_blue","size":[1,1,1],"position":[3,4,2]},{"color":"trans_blue","size":[1,1,1],"position":[4,4,2]},{"color":"trans_blue","size":[1,1,1],"position":[5,4,2]},{"color":"trans_blue","size":[1,1,1],"position":[3,5,2]},{"color":"trans_blue","size":[1,1,1],"position":[4,5,2]},{"color":"trans_blue","size":[1,1,1],"position":[5,5,2]},{"color":"trans_blue","size":[1,1,1],"position":[3,6,2]},{"color":"trans_blue","size":[1,1,1],"position":[4,6,2]},{"color":"trans_blue","size":[1,1,1],"position":[5,6,2]},{"color":"trans_blue","size":[1,1,1],"position":[2,7,2]},{"color":"trans_blue","size":[1,1,1],"position":[3,7,2]},{"color":"trans_blue","size":[1,1,1],"position":[4,7,2]},{"color":"trans_blue","size":[1,1,1],"position":[5,7,2]},{"color":"trans_blue","size":[1,1,1],"position":[6,7,2]},{"color":"trans_blue","size":[1,1,1],"position":[2,8,2]},{"color":"trans_blue","size":[1,1,1],"position":[3,8,2]},{"color":"trans_blue","size":[1,1,1],"position":[4,8,2]},{"color":"trans_blue","size":[1,1,1],"position":[5,8,2]},{"color":"trans_blue","size":[1,1,1],"position":[6,8,2]},{"color":"trans_blue","size":[1,1,1],"position":[2,9,2]},{"color":"trans_blue","size":[1,1,1],"position":[3,9,2]},{"color":"trans_blue","size":[1,1,1],"position":[4,9,2]},{"color":"trans_blue","size":[1,1,1],"position":[5,9,2]},{"color":"trans_blue","size":[1,1,1],"position":[6,9,2]},{"color":"trans_blue","size":[1,1,1],"position":[2,10,2]},{"color":"trans_blue","size":[1,1,1],"position":[3,10,2]},{"color":"trans_blue","size":[1,1,1],"position":[4,10,2]},{"color":"trans_blue","size":[1,1,1],"position":[5,10,2]},{"color":"trans_blue","size":[1,1,1],"position":[6,10,2]},{"color":"trans_blue","size":[1,1,1],"position":[2,11,2]},{"color":"trans_blue","size":[1,1,1],"position":[3,11,2]},{"color":"trans_blue","size":[1,1,1],"position":[4,11,2]},{"color":"trans_blue","size":[1,1,1],"position":[5,11,2]},{"color":"trans_blue","size":[1,1,1],"position":[6,11,2]},{"color":"trans_blue","size":[1,1,1],"position":[3,12,2]},{"color":"trans_blue","size":[1,1,1],"position":[4,12,2]},{"color":"trans_blue","size":[1,1,1],"position":[5,12,2]},{"color":"trans_blue","size":[1,1,1],"position":[3,13,2]},{"color":"trans_blue","size":[1,1,1],"position":[4,13,2]},{"color":"trans_blue","size":[1,1,1],"position":[5,13,2]},{"color":"trans_blue","size":[1,1,1],"position":[2,5,3]},{"color":"trans_blue","size":[1,1,1],"position":[3,5,3]},{"color":"trans_blue","size":[1,1,1],"position":[4,5,3]},{"color":"trans_blue","size":[1,1,1],"position":[5,5,3]},{"color":"trans_blue","size":[1,1,1],"position":[6,5,3]},{"color":"trans_blue","size":[1,1,1],"position":[2,6,3]},{"color":"trans_blue","size":[1,1,1],"position":[3,6,3]},{"color":"trans_blue","size":[1,1,1],"position":[4,6,3]},{"color":"trans_blue","size":[1,1,1],"position":[5,6,3]},{"color":"trans_blue","size":[1,1,1],"position":[6,6,3]},{"color":"trans_blue","size":[1,1,1],"position":[2,7,3]},{"color":"trans_blue","size":[1,1,1],"position":[3,7,3]},{"color":"trans_blue","size":[1,1,1],"position":[4,7,3]},{"color":"trans_blue","size":[1,1,1],"position":[5,7,3]},{"color":"trans_blue","size":[1,1,1],"position":[6,7,3]},{"color":"trans_blue","size":[1,1,1],"position":[2,8,3]},{"color":"trans_blue","size":[1,1,1],"position":[3,8,3]},{"color":"trans_blue","size":[1,1,1],"position":[4,8,3]},{"color":"trans_blue","size":[1,1,1],"position":[5,8,3]},{"color":"trans_blue","size":[1,1,1],"position":[6,8,3]},{"color":"trans_blue","size":[1,1,1],"position":[2,9,3]},{"color":"trans_blue","size":[1,1,1],"position":[3,9,3]},{"color":"trans_blue","size":[1,1,1],"position":[4,9,3]},{"color":"trans_blue","size":[1,1,1],"position":[5,9,3]},{"color":"trans_blue","size":[1,1,1],"position":[6,9,3]},{"color":"trans_blue","size":[1,1,1],"position":[2,10,3]},{"color":"trans_blue","size":[1,1,1],"position":[3,10,3]},{"color":"trans_blue","size":[1,1,1],"position":[4,10,3]},{"color":"trans_blue","size":[1,1,1],"position":[5,10,3]},{"color":"trans_blue","size":[1,1,1],"position":[6,10,3]},{"color":"trans_blue","size":[1,1,1],"position":[2,11,3]},{"color":"trans_blue","size":[1,1,1],"position":[3,11,3]},{"color":"trans_blue","size":[1,1,1],"position":[4,11,3]},{"color":"trans_blue","size":[1,1,1],"position":[5,11,3]},{"color":"trans_blue","size":[1,1,1],"position":[6,11,3]},{"color":"trans_blue","size":[1,1,1],"position":[3,8,4]},{"color":"trans_blue","size":[1,1,1],"position":[4,8,4]},{"color":"trans_blue","size":[1,1,1],"position":[5,8,4]},{"color":"trans_blue","size":[1,1,1],"position":[3,9,4]},{"color":"trans_blue","size":[1,1,1],"position":[4,9,4]},{"color":"trans_blue","size":[1,1,1],"position":[5,9,4]},{"color":"trans_blue","size":[1,1,1],"position":[3,10,4]},{"color":"trans_blue","size":[1,1,1],"position":[4,10,4]},{"color":"trans_blue","size":[1,1,1],"position":[5,10,4]},{"color":"white","size":[0.2,0.2,2],"position":[4,9,5]}],"overall_image":{"iso":"https://craftsman-agent.aiagenta2z.com/craftsman-agent/static/TEMP_c0b498a3/lego_plan/view_iso.png","top":"https://craftsman-agent.aiagenta2z.com/craftsman-agent/static/TEMP_c0b498a3/lego_plan/view_top.png","front":"https://craftsman-agent.aiagenta2z.com/craftsman-agent/static/TEMP_c0b498a3/lego_plan/view_front.png","side":"https://craftsman-agent.aiagenta2z.com/craftsman-agent/static/TEMP_c0b498a3/lego_plan/view_side.png"},"inventory_image":{"inventory_parts":"https://craftsman-agent.aiagenta2z.com/craftsman-agent/static/TEMP_c0b498a3/lego_plan/inventory_parts.png","description":["Color bright_red, Size 1 x 1 x 1, Quantity 90","Color trans_blue, Size 1 x 1 x 1, Quantity 84","Color bright_blue, Size 1 x 1 x 1, Quantity 72","Color white, Size 0 x 0 x 2, Quantity 1"]},"assembly_step_image":{"0":"https://craftsman-agent.aiagenta2z.com/craftsman-agent/static/TEMP_c0b498a3/lego_plan/step_0.png","1":"https://craftsman-agent.aiagenta2z.com/craftsman-agent/static/TEMP_c0b498a3/lego_plan/step_1.png","2":"https://craftsman-agent.aiagenta2z.com/craftsman-agent/static/TEMP_c0b498a3/lego_plan/step_2.png","3":"https://craftsman-agent.aiagenta2z.com/craftsman-agent/static/TEMP_c0b498a3/lego_plan/step_3.png","4":"https://craftsman-agent.aiagenta2z.com/craftsman-agent/static/TEMP_c0b498a3/lego_plan/step_4.png","5":"https://craftsman-agent.aiagenta2z.com/craftsman-agent/static/TEMP_c0b498a3/lego_plan/step_5.png","6":"https://craftsman-agent.aiagenta2z.com/craftsman-agent/static/TEMP_c0b498a3/lego_plan/step_6.png","7":"https://craftsman-agent.aiagenta2z.com/craftsman-agent/static/TEMP_c0b498a3/lego_plan/step_7.png","8":"https://craftsman-agent.aiagenta2z.com/craftsman-agent/static/TEMP_c0b498a3/lego_plan/step_8.png","9":"https://craftsman-agent.aiagenta2z.com/craftsman-agent/static/TEMP_c0b498a3/lego_plan/step_9.png"}}
```


Both endpoints return:

- `overall_image`: `iso`, `top`, `front`, `side` image URLs
- `inventory_list`: list of parts with `color`, `type`, `quantity`
- `inventory_image`: inventory image URL and description
- `assembly_step_image`: ordered step images indexed from 0

Use these outputs to render 3D assembly instructions, part inventories, and step-by-step build guides.

### Craftsman Lego Assembly Instructions

### Example 

prompt: Build a blue and white yacht with 5 decks

Final 3D Rendering Image From 4 angles

![Four Angle Charts](https://raw.githubusercontent.com/AI-Hub-Admin/Craftsman-Agent/refs/heads/main/docs/craftsman_agent_1.jpg)

Step by Step Assembly Charts
![Step by Step](https://raw.githubusercontent.com/AI-Hub-Admin/Craftsman-Agent/refs/heads/main/docs/craftsman_agent_2.jpg)

Detailed Charts
![Detailed Charts](https://raw.githubusercontent.com/AI-Hub-Admin/Craftsman-Agent/refs/heads/main/docs/craftsman_agent_3.jpg)





### Related
[AI Agent Marketplace](https://www.deepnlp.org/store/ai-agent)    
[AI Agent A2Z Deployment](https://www.deepnlp.org/workspace/deploy)    
[PH AI Agent Router](https://www.producthunt.com/products/deepnlp-ai-agent-marketplace-router)    
[PH AI Agent A2Z Infra](https://www.producthunt.com/products/ai-agent-a2z-infra-deployment-platform)    
[GitHub AI Agent Marketplace](https://github.com/aiagenta2z/ai-agent-marketplace)    


