---
name: massgen-develops-massgen
description: Guide for using MassGen to develop and improve itself. This skill should be used when agents need to run MassGen experiments programmatically (using automation mode) OR analyze terminal UI/UX quality (using visual evaluation tools). These are mutually exclusive workflows for different improvement goals.
---

# MassGen Develops MassGen

This skill provides guidance for using MassGen to develop and improve itself. Choose the appropriate workflow based on what you're testing.

## Two Workflows

1. **Automation Mode** - Test backend functionality, coordination logic, agent responses
2. **Visual Evaluation** - Test terminal display, colors, layout, UX

---

## Workflow 1: Automation Mode

Use this to test functionality without visual inspection. Ideal for programmatic testing.

### Running MassGen with Automation

Run MassGen in the background (exact mechanism depends on your tooling):

```bash
uv run massgen --automation --config massgen/configs/basic/multi/two_agents_gemini.yaml "What is 2+2?"
```

**For MassGen agents**: Use `custom_tool__start_background_tool` targeting `mcp__command_line__execute_command`, then poll with `custom_tool__get_background_tool_status` / `custom_tool__get_background_tool_result`.
**For Claude Code**: Use Bash tool's `run_in_background` parameter.

### Why Automation Mode

| Feature | Benefit |
|---------|---------|
| Clean output | ~10 parseable lines vs 3,000+ ANSI codes |
| LOG_DIR printed | First line shows log directory path |
| status.json | Real-time monitoring file |
| Exit codes | 0=success, 1=config, 2=execution, 3=timeout, 4=interrupted |
| Workspace isolation | Safe parallel execution |

### Expected Output

```
LOG_DIR: .massgen/massgen_logs/log_20251120_143022_123456
STATUS: .massgen/massgen_logs/log_20251120_143022_123456/status.json

🤖 Multi-Agent Mode
Agents: gemini-2.5-pro1, gemini-2.5-pro2
Question: What is 2+2?

============================================================
QUESTION: What is 2+2?
[Coordination in progress - monitor status.json for real-time updates]

WINNER: gemini-2.5-pro1
DURATION: 33.4s
ANSWER_PREVIEW: The answer is 4.

COMPLETED: 2 agents, 35.2s total
```

Parse `LOG_DIR` from the first line to find the log directory.

### Monitoring Progress

Read the status.json file (updated every 2 seconds):

```bash
cat .massgen/massgen_logs/log_20251120_143022_123456/status.json
```

**Key fields:**

```json
{
  "coordination": {
    "completion_percentage": 65,
    "phase": "enforcement"
  },
  "results": {
    "winner": null  // null = running, "agent_id" = done
  },
  "agents": {
    "agent_a": {
      "status": "streaming",
      "error": null
    }
  }
}
```

**Agent status values:** `waiting`, `streaming`, `answered`, `voted`, `completed`, `error`

### Reading Results

After completion (exit code 0):

```bash
# Read final answer
cat [log_dir]/final/[winner]/answer.txt
```

### Timing Expectations

- **Standard tasks**: 2-10 minutes
- **Complex/meta tasks**: 10-30 minutes
- **Check if stuck**: Read status.json - if `completion_percentage` increases, it's working

### Advanced: Multiple Background Monitors

You can create multiple background monitoring tasks that run independently alongside the main MassGen process. Each monitor can track different aspects and write to separate log files for later inspection.

#### Approach

Create small Python scripts that run in background shells. Each script:
- Monitors a specific aspect (tokens, errors, progress, coordination, etc.)
- Writes timestamped data to its own log file
- Runs in a loop with `sleep()` intervals
- Can be checked anytime without blocking the main task

#### Example Monitor Scripts

**Token Usage Monitor** (`token_monitor.py`):
```python
import json, time, sys
from pathlib import Path

log_dir = Path(sys.argv[1])  # Pass LOG_DIR as argument
while True:
    if (log_dir / "status.json").exists():
        with open(log_dir / "status.json") as f:
            data = json.load(f)
        with open("token_monitor.log", "a") as log:
            log.write(f"=== {time.strftime('%H:%M:%S')} ===\n")
            log.write(f"Tokens: {data.get('total_tokens_used', 0)}\n")
            log.write(f"Cost: ${data.get('total_cost', 0):.4f}\n\n")
    time.sleep(5)
```

**Error Monitor** (`error_monitor.py`):
```python
import time, sys
from pathlib import Path

log_dir = Path(sys.argv[1])
while True:
    if log_dir.exists():
        with open("error_monitor.log", "a") as log:
            log.write(f"=== {time.strftime('%H:%M:%S')} ===\n")
            errors = []
            for logfile in log_dir.glob("*.log"):
                with open(logfile) as f:
                    for line in f:
                        if any(x in line.lower() for x in ['error', 'warning', 'failed']):
                            errors.append(line.strip())
            log.write('\n'.join(errors[-5:]) if errors else "No errors\n")
            log.write("\n")
    time.sleep(5)
```

**Progress Monitor** (`progress_monitor.py`):
```python
import json, time, sys
from pathlib import Path

log_dir = Path(sys.argv[1])
while True:
    if (log_dir / "status.json").exists():
        with open(log_dir / "status.json") as f:
            data = json.load(f)
        with open("progress_monitor.log", "a") as log:
            log.write(f"=== {time.strftime('%H:%M:%S')} ===\n")
            progress = data.get('completion_percentage', 0)
            active = sum(1 for a in data.get('agents', {}).values()
                        if a.get('status') == 'active')
            log.write(f"Progress: {progress}% Active agents: {active}\n\n")
    time.sleep(5)
```

**Coordination Monitor** (`coordination_monitor.py`):
```python
import json, time, sys
from pathlib import Path

log_dir = Path(sys.argv[1])
while True:
    if (log_dir / "status.json").exists():
        with open(log_dir / "status.json") as f:
            data = json.load(f)
        coord = data.get('coordination', {})
        with open("coordination_monitor.log", "a") as log:
            log.write(f"=== {time.strftime('%H:%M:%S')} ===\n")
            log.write(f"Phase: {coord.get('phase', 'unknown')}\n")
            log.write(f"Round: {coord.get('round', 0)}\n")
            log.write(f"Total answers: {coord.get('total_answers', 0)}\n\n")
    time.sleep(5)
```

#### Workflow

1. **Launch main task**, parse the LOG_DIR from output
2. **Create monitor scripts** as needed (write Python files)
3. **Launch monitors in background shells**: `python3 token_monitor.py [LOG_DIR] &`
4. **Check monitor logs anytime** by reading the .log files
5. **When complete**, kill monitor processes and analyze logs

#### Custom Monitors

Create monitors for any metric you want to track:
- Model-specific performance metrics
- Memory/context usage patterns
- Real-time cost accumulation
- Answer quality trends
- Agent coordination patterns
- Specific error categories

**Benefits:**
- Non-blocking inspection of specific metrics on demand
- Historical data captured for post-run analysis
- Independent monitoring streams for different aspects
- Easy to add new monitors without modifying configs

---

## Workflow 2: Visual Evaluation

Use this to analyze and improve MassGen's terminal display quality. Requires tools from `custom_tools/_multimodal_tools/`.

**Important:** This workflow records the rich terminal display, so the actual recording does NOT use `--automation` mode. However, you should ALWAYS pre-test with `--automation` first.

### Prerequisites

You should have these tools available in your workspace:
- `run_massgen_with_recording` - Records terminal sessions as video
- `understand_video` - Analyzes video frames with GPT-4.1 vision

### Step 0: Pre-Test with Automation (REQUIRED)

**Before recording the video**, verify the config works and API keys are valid:

```bash
# Start with --automation to verify everything works
uv run massgen --automation --config [config_path] "[question]"
```

**Wait 30-60 seconds** (enough to verify API keys, config parsing, tool initialization), then kill the process.

**Why this is critical:**
- Detects config errors before wasting recording time
- Validates API keys are present and working
- Ensures tools initialize correctly
- Prevents recording a broken session

**If the automation test fails**, fix the issues before proceeding to recording.

### Step 1: Record a MassGen Session

**After the automation pre-test succeeds**, record the visual session:

```python
from custom_tools._multimodal_tools.run_massgen_with_recording import run_massgen_with_recording

result = await run_massgen_with_recording(
    config_path="massgen/configs/basic/multi/two_agents_gemini.yaml",
    question="What is 2+2?",
    output_format="mp4",  # ALWAYS use mp4 for maximum compatibility
    timeout_seconds=120,
    width=1920,
    height=1080
)
```

**Format recommendation**: Always use `"mp4"` for maximum compatibility. GIF and WebM are supported but MP4 is preferred.

**The recording captures**: Rich terminal display with colors, status indicators, coordination visualization (WITHOUT --automation flag).

### Step 2: Analyze the Recording

**Use `understand_video` to analyze the MP4 recording.** Call it at least once, but as many as multiple times to analyze different aspects:

```python
from custom_tools._multimodal_tools.understand_video import understand_video

# Overall UX evaluation
ux_eval = await understand_video(
    video_path=result["video_path"],  # The MP4 file from Step 1
    prompt="Evaluate the overall terminal display quality, clarity, and usability",
    num_frames=12
)

# Focused on coordination
coordination_eval = await understand_video(
    video_path=result["video_path"],
    prompt="How clearly does the display show agent coordination phases and voting?",
    num_frames=8
)

# Status indicators
status_eval = await understand_video(
    video_path=result["video_path"],
    prompt="Are status indicators (streaming, answered, voted) clear and visually distinct?",
    num_frames=8
)
```

**Key points:**
- The recording tool saves the video to workspace - use that path for analysis
- You can call `understand_video` multiple times on the same video with different prompts
- Each call focuses on a specific aspect (UX, coordination, status, colors, etc.)

### Evaluation Criteria

When analyzing terminal displays, assess:

1. **Visual Clarity** - Contrast, colors, font rendering, ANSI handling, spacing
2. **Information Organization** - Layout, content density, streaming display, scroll handling
3. **Status Indicators** - Agent states, progress tracking, phase transitions, winner selection
4. **User Experience** - Real-time feedback, error visibility, cognitive load, information hierarchy

### Output Format Recommendations

**Default to MP4** - Maximum compatibility and quality.

| Format | Use Case | Notes |
|--------|----------|-------|
| **MP4** | **Default - use for everything** | Best quality, universally supported, ideal for detailed analysis |
| GIF | Smaller file size, easy embedding | Lower quality, larger files than expected, avoid unless size-constrained |
| WebM | Modern web publishing | Good quality, not universally supported |

**Rule of thumb**: Use MP4 unless you have a specific reason not to.

### Frame Count Guidelines

| Frames | Use Case |
|--------|----------|
| 4-8 | Quick evaluation |
| 8-12 | Standard evaluation |
| 12-16+ | Detailed analysis |

---

## Which Configs to Test

### Model Selection Guidelines

**Default to mid-tier models** when generating configs or running experiments. These provide the best balance of cost, speed, and capability for development and testing.

**CRITICAL: Always check model recency based on TODAY'S DATE.** Models older than 6-12 months should be considered outdated.

#### How to Select Models

**Step 1: Read backend files to check release dates**
```bash
# Check Gemini models and their release dates
grep -A 5 "model.*2\." massgen/backend/gemini.py

# Check OpenAI models and their release dates
grep -A 5 "model.*gpt" massgen/backend/openai.py

# Check Claude models and their release dates
grep -A 5 "model.*claude" massgen/backend/claude.py
```

**Step 2: Check token costs**
```bash
cat docs/source/reference/token_budget.rst | grep -A 3 "gemini\|gpt\|claude"
```

**Step 3: Compare release dates against today's date**
- Calculate months since release: (today's year-month) - (model release year-month)
- If > 12 months: Model is outdated
- If 6-12 months: Model is aging, prefer newer if available
- If < 6 months: Model is current

#### Model Selection Examples

**✅ GOOD (Recent, mid-tier patterns):**
- **Gemini**: `gemini-2.5-pro`, `gemini-2.5-flash` (2.x series, 2025)
- **OpenAI**: `gpt-5-mini`, `gpt-4o-mini` (GPT-5 generation)
- **Claude**: `claude-sonnet-4-*` (4.x series, 2025)

**⚠️ BAD (Outdated patterns - check dates!):**
- ❌ `gpt-4o` (2024 release - likely >12 months old)
- ❌ `gpt-4-turbo` (2023-2024 era)
- ❌ `gemini-1.5-pro` (1.x series deprecated by 2.x)
- ❌ `claude-3.5-sonnet` (3.x series when 4.x exists)

**Selection criteria:**
- **Recency**: Released within last 6-12 months (ALWAYS check backend files for dates)
- **Mid-range pricing**: Not top-tier (expensive) or bottom-tier (cheap)
- **General availability**: Stable release, not experimental/preview/alpha
- **Version numbers**: Higher major versions are newer (gemini-2.x > gemini-1.x, gpt-5 > gpt-4, claude-4 > claude-3)

**When to deviate:**
- **Premium models**: Testing model ceiling capabilities (e.g., `gpt-5`, `claude-opus-4`, `gemini-3-pro`)
- **Budget models**: Cost optimization experiments (e.g., `gpt-5-mini`, `gemini-2.5-flash`)
- **Legacy testing**: Validating backwards compatibility with older models

### Generating a Config (Agent-Friendly)

Use `--generate-config` for programmatic config generation:

```bash
# WORKFLOW:
# 1. Read backend file to find recent mid-tier models
# 2. Verify release date (< 12 months old)
# 3. Check pricing tier (mid-range)
# 4. Use model in --config-model flag

# Example: Generate 2-agent config
massgen --generate-config ./test_config.yaml \
  --config-backend gemini \
  --config-model gemini-2.5-pro \  # (example - always verify this is current!)
  --config-agents 2 \
  --config-docker

# With context path
massgen --generate-config ./test_config.yaml \
  --config-backend openai \
  --config-model gpt-5-mini \  # (example - always verify this is current!)
  --config-context-path /path/to/project
```

**IMPORTANT**: The model names shown above are EXAMPLES. Always check backend files for current models based on today's date.

This creates a full-featured config with code-based tools, skills, and task planning enabled.

### Testing Specific Features

Modify the generated config to enable/disable features:

**Code execution:**
```yaml
agents:
  - backend:
      enable_mcp_command_line: true
      command_line_execution_mode: "docker"
```

**Custom tools:**
```yaml
agents:
  - backend:
      enable_code_based_tools: true
      auto_discover_custom_tools: true
```

**Different models per agent:**
```yaml
agents:
  - backend: {type: "gemini", model: "gemini-2.5-pro"}
  - backend: {type: "openai", model: "gpt-5-mini"}
```

Common parameters: `enable_code_based_tools`, `enable_mcp_command_line`, `command_line_execution_mode`, `auto_discover_custom_tools`, `timeout_settings`

---

## Docker Considerations

### Automatic Docker Detection

MassGen automatically detects when running inside a Docker container. If a config has `command_line_execution_mode: "docker"`, MassGen will:

1. Detect the container environment (via `/.dockerenv`)
2. Automatically switch to `"local"` execution mode
3. Log: "Already running inside Docker container - switching to local execution mode"

**Why this works:** The outer container already provides isolation. Running "locally" within that container is safe and sandboxed.

**No manual configuration needed** - configs with Docker mode just work when run inside containers.

### Tradeoffs

When auto-switching to local execution:
- ✅ Still sandboxed from host
- ✅ All features work (VHS, MassGen, tools are in container)
- ⚠️ No per-execution isolation between tool calls
- ⚠️ State persists within container session

---

## Reference Files

- **Status file docs**: `docs/source/reference/status_file.rst`
- **Terminal evaluation docs**: `docs/source/user_guide/terminal_evaluation.rst`
- **Example configs**: `massgen/configs/basic/`, `massgen/configs/meta/`
- **Recording tool**: `massgen/tool/_multimodal_tools/run_massgen_with_recording.py`
- **Video analysis tool**: `massgen/tool/_multimodal_tools/understand_video.py`
