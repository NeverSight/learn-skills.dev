---
name: tailslayer-dram-hedged-reads
description: C++ library for reducing tail latency in RAM reads by hedging across multiple DRAM channels with uncorrelated refresh schedules
triggers:
  - reduce tail latency in RAM reads
  - DRAM refresh stalls hedging
  - hedged memory reads C++
  - tailslayer library
  - replicate data across DRAM channels
  - low latency memory access C++
  - hedged reads multiple channels
  - DRAM refresh cycle latency
---

# Tailslayer — DRAM Hedged Read Library

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Tailslayer is a C++ library that reduces tail latency in RAM reads caused by DRAM refresh stalls. It replicates data across multiple independent DRAM channels with uncorrelated refresh schedules, issues hedged reads across all replicas simultaneously, and returns whichever result responds first — eliminating worst-case stall spikes from DRAM refresh cycles.

Works on AMD, Intel, and AWS Graviton using undocumented channel scrambling offsets.

---

## How It Works

- Data is replicated N times, each copy placed on a different DRAM channel
- Each replica is monitored by a worker pinned to a separate CPU core
- When a read is triggered (via your signal function), all replicas are read simultaneously
- Whichever channel responds first wins; the result is passed to your work function
- DRAM refresh on one channel cannot stall all channels simultaneously → tail latency is eliminated

---

## Installation

### Copy the header into your project

```bash
git clone https://github.com/LaurieWired/tailslayer.git
cp -r tailslayer/include/tailslayer /your/project/include/
```

### Include in your code

```cpp
#include <tailslayer/hedged_reader.hpp>
```

### Build the provided example

```bash
git clone https://github.com/LaurieWired/tailslayer.git
cd tailslayer
make
./tailslayer_example
```

---

## Key API

### `tailslayer::HedgedReader<T, SignalFn, WorkFn, SignalArgs, WorkArgs>`

Template parameters:
| Parameter | Description |
|---|---|
| `T` | Value type stored and read |
| `SignalFn` | Function that waits for a trigger and returns the index to read |
| `WorkFn` | Function called with the value immediately after read |
| `SignalArgs` | (optional) `tailslayer::ArgList<...>` of compile-time args to signal function |
| `WorkArgs` | (optional) `tailslayer::ArgList<...>` of compile-time args to work function |

### Constructor optional parameters

```cpp
HedgedReader(
    uint64_t channel_offset = DEFAULT_OFFSET,  // undocumented channel scrambling offset
    uint64_t channel_bit    = DEFAULT_BIT,     // bit used for channel selection
    std::size_t n_replicas  = 2                // number of DRAM channel replicas
)
```

### Methods

```cpp
reader.insert(T value);       // Insert value, replicated across all channels
reader.start_workers();       // Launch per-channel worker threads (blocking)
```

### Utilities

```cpp
tailslayer::pin_to_core(core_id);        // Pin calling thread to a specific core
tailslayer::CORE_MAIN                    // Constant: recommended core for main thread
```

---

## Minimal Usage Pattern

```cpp
#include <tailslayer/hedged_reader.hpp>
#include <cstdint>
#include <cstdio>

// 1. Define your signal function — waits for your event, returns index to read
[[gnu::always_inline]] inline std::size_t my_signal() {
    // Example: busy-wait for an external flag, then return the index
    extern volatile std::size_t g_index;
    extern volatile bool g_trigger;
    while (!g_trigger) {}
    g_trigger = false;
    return g_index;
}

// 2. Define your work function — receives the read value immediately
template <typename T>
[[gnu::always_inline]] inline void my_work(T val) {
    // Process val as fast as possible
    printf("Read value: %u\n", (unsigned)val);
}

int main() {
    using T = uint8_t;

    // Pin main thread to recommended core
    tailslayer::pin_to_core(tailslayer::CORE_MAIN);

    // Construct reader with 2 replicas (default)
    tailslayer::HedgedReader<T, my_signal, my_work<T>> reader{};

    // Insert data — replicated across both DRAM channels automatically
    reader.insert(0x43);
    reader.insert(0x44);

    // Launch workers — blocks; workers spin until signal fires
    reader.start_workers();

    return 0;
}
```

---

## Passing Arguments to Signal and Work Functions

Use `tailslayer::ArgList<...>` to pass compile-time integer arguments:

```cpp
#include <tailslayer/hedged_reader.hpp>

// Signal function with args
[[gnu::always_inline]] inline std::size_t my_signal(int threshold, int channel) {
    // use threshold and channel...
    return 0;
}

// Work function with args
template <typename T>
[[gnu::always_inline]] inline void my_work(T val, int multiplier) {
    volatile int result = (int)val * multiplier;
    (void)result;
}

int main() {
    using T = uint8_t;
    tailslayer::pin_to_core(tailslayer::CORE_MAIN);

    tailslayer::HedgedReader<
        T,
        my_signal,
        my_work<T>,
        tailslayer::ArgList<10, 1>,   // args forwarded to my_signal: threshold=10, channel=1
        tailslayer::ArgList<2>        // args forwarded to my_work:   multiplier=2
    > reader{};

    reader.insert(0xAB);
    reader.start_workers();
}
```

---

## Custom Channel Configuration

Override channel offset, channel bit, and replica count in the constructor:

```cpp
// Example: 4 replicas, custom channel bit 8 (common for AMD/Intel)
tailslayer::HedgedReader<T, my_signal, my_work<T>> reader{
    /* channel_offset */ 0,
    /* channel_bit    */ 8,
    /* n_replicas     */ 4
};
```

> **Note:** N-way (more than 2 replicas) hedging requires using the benchmark code in `discovery/benchmark/`. The main library header currently exposes 2 channels by default.

---

## Running Benchmarks

### Channel-hedged read benchmark (N-way)

```bash
cd discovery/benchmark
make
sudo chrt -f 99 ./hedged_read_cpp --all --channel-bit 8
```

Flags:
| Flag | Description |
|---|---|
| `--all` | Run all channel configurations |
| `--channel-bit N` | Specify the DRAM channel selection bit (try 6, 7, or 8 for your platform) |

### DRAM refresh spike timing probe

```bash
cd discovery
gcc -O2 -o trefi_probe trefi_probe.c
sudo ./trefi_probe
```

This measures your DRAM's tREFI refresh interval and the worst-case stall duration — useful for calibrating expectations.

---

## Platform Notes

| Platform | Typical Channel Bit | Notes |
|---|---|---|
| AMD (Zen) | 6 or 7 | Verify with benchmark |
| Intel | 6, 7, or 8 | Run benchmark with `--all` |
| AWS Graviton | 8 | Confirmed working |

Use `--all` in the benchmark to auto-detect the best channel bit for your system.

---

## Common Patterns

### Low-latency trading / event-driven read

```cpp
// Pre-load order book prices into hedged reader
// Signal on market data arrival, process immediately

[[gnu::always_inline]] inline std::size_t await_market_signal() {
    extern volatile std::size_t g_book_idx;
    extern volatile bool g_tick;
    while (!g_tick) { __builtin_ia32_pause(); }
    g_tick = false;
    return g_book_idx;
}

template <typename T>
[[gnu::always_inline]] inline void process_price(T price) {
    // Submit order using price with minimal latency
    extern void submit_order(T);
    submit_order(price);
}

int main() {
    tailslayer::pin_to_core(tailslayer::CORE_MAIN);
    tailslayer::HedgedReader<uint64_t, await_market_signal, process_price<uint64_t>> reader{};
    for (uint64_t price : preloaded_prices) {
        reader.insert(price);
    }
    reader.start_workers();
}
```

### Preloading a lookup table across channels

```cpp
// Each insert automatically maps to correct DRAM channel via address calculation
// Access is via logical index — tailslayer manages physical placement

tailslayer::HedgedReader<uint32_t, my_signal, my_work<uint32_t>> reader{};

std::vector<uint32_t> lut = {100, 200, 300, 400};
for (auto v : lut) {
    reader.insert(v);
}
reader.start_workers();
```

---

## Troubleshooting

### High latency still observed
- Verify you are using the correct `--channel-bit` for your CPU. Run benchmark with `--all`.
- Ensure workers are pinned to isolated cores (use `isolcpus=` kernel boot parameter).
- Run with real-time scheduling: `sudo chrt -f 99 ./your_binary`

### Build errors — missing headers
- Confirm `include/tailslayer/hedged_reader.hpp` is on your include path.
- Requires C++17 or later: add `-std=c++17` to your compiler flags.

### Workers don't start / deadlock
- `start_workers()` is blocking. It launches threads and waits — your signal function must eventually return.
- Ensure the signal function does not block indefinitely during testing.

### Data corruption / wrong values
- Each `insert()` replicates the value N times (one per channel). Logical indexing is handled internally — do not attempt to address replicas directly.
- Do not modify inserted data after `insert()` is called.

### Platform not supported
- Tailslayer uses undocumented DRAM channel scrambling offsets. If your platform is not AMD, Intel, or Graviton, run the trefi_probe and benchmark tools to characterize refresh behavior before using the library in production.

---

## Project Structure

```
tailslayer/
├── include/tailslayer/
│   └── hedged_reader.hpp       # Main library header (copy this)
├── tailslayer_example.cpp      # Usage example
├── discovery/
│   ├── trefi_probe.c           # DRAM refresh spike timing tool
│   └── benchmark/              # N-way channel hedging benchmark
└── Makefile
```
