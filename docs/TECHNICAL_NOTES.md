# Technical notes

## Pinned source

- Project: https://github.com/exelban/stats
- Version: 3.0.23
- Commit: `5cf09a8cb0561ff24c28be4e5374d579d0601818`
- Patch: `patches/stats-3.0.23-hackintosh.patch`

The patch is a combined diff of nine upstream files. Keeping it as a patch preserves the original project identity and makes the current local changes easy to review before splitting them for upstream submission.

## AMD frequency

On x86_64 the reader opens the `SMCProcessorAMD` user client and calls selector 2. It copies the driver's existing per-core `MSRC001_0293` cache; it does not send an MSR address or write request. The buffer and returned core count are checked before decoding.

The code contains family `0x17`, `0x19` and `0x1A` handling. Only the Zen 5 installation has been used in this project. A failure falls back to `hw.cpufrequency` when available; that fallback can be nominal and is not guaranteed to track live clocks.

The patch does not provide the SMCProcessorAMD kernel extension, add CPU family support to a driver, or change CPU power management.

## NVIDIA

The GPU reader recognizes the `NVAccel` IOClass and masked PCI matches. Available driver counters are copied with 0–100 validation. A counter's presence and meaning still depend on the installed driver.

The RTX 5070 desktop PCI match includes a static CUDA core specification. No driver is bundled and no GPU firmware is changed.

## JSON feed

| File | Payload fields besides `timestamp` |
|---|---|
| `cpu-temperature.json` | `celsius` |
| `cpu-frequency.json` | `ghz` |
| `cpu-load.json` | `usage` |
| `gpu.json` | `usage` |
| `memory.json` | `used`, `total` |

Usage is a fraction, memory values are bytes, timestamps are Unix seconds. `hardware.json` and `gpu-info.json` supply static descriptions. The current version exports through active module callbacks; disabled modules will not supply fresh readings. Output is local to the current user account.

## Undo

In a dedicated source checkout that contains only this patch's changes, inspect the diff before reversing it:

```bash
git -C stats-source diff
git -C stats-source apply --reverse --check /absolute/path/to/stats-3.0.23-hackintosh.patch
git -C stats-source apply --reverse /absolute/path/to/stats-3.0.23-hackintosh.patch
```

Reversing source changes does not replace an already installed binary. Keep normal upstream and patched builds separate during testing.
