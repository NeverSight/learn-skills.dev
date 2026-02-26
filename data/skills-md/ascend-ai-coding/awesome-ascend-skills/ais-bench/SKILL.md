---
name: ais-bench
description: AISBench Benchmark - AI model evaluation tool for Ascend NPU. Supports accuracy evaluation (service/local models on text, multimodal datasets), performance evaluation (latency, throughput, stress testing, steady-state, real traffic simulation), vLLM/Triton inference services, 15+ benchmarks (MMLU, GSM8K, MMMU, docvqa, ocrbench_v2, etc.), multi-turn dialogue, Function Call (BFCL), and custom datasets.
keywords:
    - ais-bench
    - aisbench
    - model evaluation
    - benchmark
    - accuracy evaluation
    - performance evaluation
    - vllm
    - multimodal
    - llm evaluation
github_url: https://github.com/AISBench/benchmark
github_hash: 03f0f43383c3efdb6ecdcc845eb24bc7a1537575
version: 1.0.0
created_at: 2026-02-25
entry_point: ais_bench
---

# AISBench Benchmark Tool

AISBench Benchmark is a model evaluation tool built based on OpenCompass. It supports evaluation scenarios for both accuracy and performance testing of AI models on Ascend NPU.

## Overview

- **Accuracy Evaluation**: Accuracy verification of service-deployed models and local models on various QA and reasoning benchmark datasets, covering text, multimodal, and other scenarios.
- **Performance Evaluation**: Latency and throughput evaluation of service-deployed models, extreme performance testing under stress test scenarios, steady-state performance evaluation, and real business traffic simulation.

### Supported Scenarios

| Scenario | Description |
|----------|-------------|
| **Accuracy Evaluation** | Model accuracy on text/multimodal datasets |
| **Performance Evaluation** | Latency, throughput, stress testing |
| **Steady-State Performance** | Obtain true optimal system performance |
| **Real Traffic Simulation** | Simulate real business traffic patterns |
| **Multi-turn Dialogue** | Evaluate multi-turn conversation models |
| **Function Call (BFCL)** | Function calling capability evaluation |

### Supported Benchmarks

- **Text**: GSM8K, MMLU, Ceval, FewCLUE series, dapo_math, leval
- **Multimodal**: docvqa, infovqa, ocrbench_v2, omnidocbench, mmmu, mmmu_pro, mmstar, videomme, textvqa, videobench, vocalsound
- **Multi-turn Dialogue**: sharegpt, mtbench
- **Function Call**: BFCL (Berkeley Function Calling Leaderboard)

---

## Installation

### Environment Requirements

**Python Version**: Only Python **3.10**, **3.11**, or **3.12** is supported.

```bash
# Create conda environment
conda create --name ais_bench python=3.10 -y
conda activate ais_bench
```

### Install from Source

```bash
git clone https://github.com/AISBench/benchmark.git
cd benchmark/
pip3 install -e ./ --use-pep517
```

Verify installation:
```bash
ais_bench -h
```

### Optional Dependencies

```bash
# For service-deployed model evaluation (vLLM, Triton, etc.)
pip3 install -r requirements/api.txt
pip3 install -r requirements/extra.txt

# For Huggingface multimodal / vLLM offline inference
pip3 install -r requirements/hf_vl_dependency.txt

# For BFCL Function Calling evaluation
pip3 install -r requirements/datasets/bfcl_dependencies.txt --no-deps
```

---

## Quick Start

### Basic Command Structure

```bash
ais_bench --models <model_task> --datasets <dataset_task> [--summarizer example]
```

- `--models`: Specifies the model task configuration
- `--datasets`: Specifies the dataset task configuration
- `--summarizer`: Result presentation task (default: `example`)

### Find Configuration Files

```bash
# List all available task configurations
ais_bench --models vllm_api_general_chat --datasets demo_gsm8k_gen_4_shot_cot_chat_prompt --search
```

### Example: Service Model Accuracy Evaluation

1. **Start vLLM inference service** (follow vLLM documentation)

2. **Prepare dataset**:
   - Download GSM8K from [opencompass](http://opencompass.oss-cn-shanghai.aliyuncs.com/datasets/data/gsm8k.zip)
   - Extract to `ais_bench/datasets/gsm8k/`

3. **Modify model configuration** (`vllm_api_general_chat.py`):
   ```python
   from ais_bench.benchmark.models import VLLMCustomAPIChat

   models = [
       dict(
           attr="service",
           type=VLLMCustomAPIChat,
           abbr='vllm-api-general-chat',
           path="",
           model="",
           stream=False,
           request_rate=0,
           retry=2,
           api_key="",
           host_ip="localhost",
           host_port=8080,
           url="",
           max_out_len=512,
           batch_size=1,
           trust_remote_code=False,
           generation_kwargs=dict(
               temperature=0.01,
               ignore_eos=False,
           )
       )
   ]
   ```

4. **Run evaluation**:
   ```bash
   ais_bench --models vllm_api_general_chat --datasets demo_gsm8k_gen_4_shot_cot_chat_prompt
   ```

### Output Results

```
dataset                 version  metric   mode  vllm_api_general_chat
----------------------- -------- -------- ----- ----------------------
demo_gsm8k              401e4c   accuracy gen                   62.50
```

---

## Model Task Types

### Service-Deployed Models

| Model Type | Description |
|------------|-------------|
| `vllm_api_general_chat` | General vLLM API chat model |
| `vllm_api_function_call_chat` | Function calling model (BFCL) |
| `triton_api_*` | Triton inference service |

### Local Models

| Model Type | Description |
|------------|-------------|
| `hf_*` | HuggingFace models |
| `vllm_offline_*` | vLLM offline inference |

---

## Performance Evaluation

### Key Metrics

| Metric | Description |
|--------|-------------|
| **TTFT** | Time to First Token |
| **TPOT** | Time Per Output Token |
| **Throughput** | Tokens per second |
| **Latency** | Request latency (P50, P90, P99) |

### Performance Test Example

```bash
ais_bench --models vllm_api_general_chat --datasets custom_performance \
    --mode performance --concurrency 100
```

### Steady-State Performance

For obtaining true optimal system performance:
```bash
ais_bench --models vllm_api_general_chat --datasets sharegpt \
    --stable-stage --duration 300
```

### Real Traffic Simulation

```bash
ais_bench --models vllm_api_general_chat --datasets custom \
    --rps-distribution rps_config.json
```

---

## Multi-task Evaluation

### Multiple Models

```bash
ais_bench --models model1 model2 model3 --datasets dataset1
```

### Multiple Datasets

```bash
ais_bench --models model1 --datasets dataset1 dataset2 dataset3
```

### Parallel Execution

```bash
ais_bench --models model1 model2 --datasets dataset1 dataset2 --parallel 4
```

---

## Custom Datasets

### Performance Custom Dataset

Create a JSONL file with custom requests:
```json
{"input": "Your prompt here", "max_output_length": 512}
```

### Accuracy Custom Dataset

Refer to [Custom Dataset Guide](https://ais-bench-benchmark-rf.readthedocs.io/en/latest/advanced_tutorials/custom_dataset.html)

---

## Output Structure

```
outputs/default/20250628_151326/
├── configs/           # Combined configuration
├── logs/              # Execution logs
│   ├── eval/          # Evaluation logs
│   └── infer/         # Inference logs
├── predictions/       # Raw inference results
├── results/           # Calculated scores
└── summary/           # Final summaries
    ├── summary_*.csv
    ├── summary_*.md
    └── summary_*.txt
```

---

## Task Management Interface

During execution, a real-time task management interface displays:
- Task name and progress
- Time cost and status
- Log path
- Extended parameters

Controls:
- `P` key: Pause/Resume screen refresh
- `Ctrl+C`: Exit

---

## Common CLI Options

| Option | Description |
|--------|-------------|
| `--models` | Model task name(s) |
| `--datasets` | Dataset task name(s) |
| `--summarizer` | Result summarizer |
| `--search` | List config file paths |
| `--debug` | Print detailed logs |
| `--mode` | Evaluation mode (accuracy/performance) |
| `--parallel` | Number of parallel tasks |
| `--resume` | Resume from breakpoint |
| `--failed-only` | Re-run failed cases only |

---

## Advanced Features

### Breakpoint Resume

```bash
ais_bench --models model1 --datasets dataset1 --resume outputs/default/20250628_151326
```

### Failed Case Re-run

```bash
ais_bench --models model1 --datasets dataset1 --failed-only --resume outputs/default/20250628_151326
```

### Multi-file Dataset Merge

For datasets like MMLU with multiple files:
```bash
ais_bench --models model1 --datasets mmlu_merged
```

### Repeated Inference for pass@k

```bash
ais_bench --models model1 --datasets dataset1 --repeat-n 5
```

---

## Troubleshooting

### Installation Issues

1. **Python version mismatch**: Use Python 3.10/3.11/3.12
2. **Dependency conflicts**: Use conda environment
3. **bfcl_eval pathlib issue**: Use `--no-deps` flag

### Runtime Issues

1. **Model connection failed**: Check `host_ip`, `host_port`, and service status
2. **Dataset not found**: Download dataset to `ais_bench/datasets/`
3. **Memory issues**: Reduce `batch_size` or use smaller dataset
---

## Helper Scripts

Quick utility scripts for common operations:

| Script | Description |
|--------|-------------|
| [scripts/check_env.sh](scripts/check_env.sh) | Verify environment setup |
| [scripts/run_accuracy_test.sh](scripts/run_accuracy_test.sh) | Quick accuracy test runner |
| [scripts/run_performance_test.sh](scripts/run_performance_test.sh) | Quick performance test runner |
| [scripts/parse_results.py](scripts/parse_results.py) | Parse and summarize results |

```bash
# Check environment
bash scripts/check_env.sh

# Quick accuracy test
bash scripts/run_accuracy_test.sh vllm_api_general_chat demo_gsm8k --host-port 8080

# Quick performance test
bash scripts/run_performance_test.sh vllm_api_general_chat sharegpt --concurrency 100

# Parse results
python scripts/parse_results.py outputs/default/20250628_151326
```

---

## References

Detailed documentation for specific use cases:

- **[Model Configuration Reference](references/model-configs.md)**: All model types (vLLM, MindIE, Triton, TGI, offline) with parameter explanations
- **[CLI Reference](references/cli-reference.md)**: Complete CLI options for accuracy and performance evaluation

---

## Templates

Ready-to-use templates for custom evaluation:

| Template | Description |
|----------|-------------|
| [assets/model_config_template.py](assets/model_config_template.py) | Model configuration template |
| [assets/custom_qa_template.jsonl](assets/custom_qa_template.jsonl) | QA dataset template |
| [assets/custom_mcq_template.csv](assets/custom_mcq_template.csv) | Multiple choice dataset template |
| [assets/custom_meta_template.json](assets/custom_meta_template.json) | Dataset metadata template |

---
