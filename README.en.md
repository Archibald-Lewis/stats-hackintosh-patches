# Stats Hackintosh Patches

[GitHub](https://github.com/Archibald-Lewis/stats-hackintosh-patches) · [Gitee](https://gitee.com/archibald-lewis/stats-hackintosh-patches) · [Companion project](https://github.com/Archibald-Lewis/vk03-panel-macos)

AMD frequency readings, community NVIDIA driver metrics, and a local JSON feed for the VK03 macOS panel.

[中文](README.md) · [Technical notes](docs/TECHNICAL_NOTES.md) · [Upstream Stats](https://github.com/exelban/stats)

This is a patch set for **Stats 3.0.23**, not a replacement for the upstream project. The original Stats MIT license and author attribution are preserved.

## Prebuilt app

[Download the DMG](https://github.com/Archibald-Lewis/stats-hackintosh-patches/releases/latest) · [Installation, signing and compatibility](docs/INSTALL.md)

AMD64 / x86_64 build, tested on an AMD Ryzen 7 9700X + RTX 5070 Hackintosh. Intel CPU machines are unverified. Ad-hoc signed and not notarized.


## Changes

- Read cached AMD per-core frequency registers through SMCProcessorAMD, including a Zen 5 decoding path, and display GHz.
- Recognize `NVAccel`, NVIDIA PCI vendor information and masked PCI match expressions.
- Map available NVIDIA driver counters to GPU fields; identify unavailable counters rather than inventing readings.
- Export CPU, GPU and memory samples from Stats reader callbacks to local JSON for VK03 Panel.

No CPU or GPU drivers are included. CPU temperature still depends on Stats' existing sensor readers and a working sensor source.

## Apply

Use a clean checkout of the exact supported revision:

```bash
git clone https://github.com/exelban/stats.git stats-source
git -C stats-source checkout --detach 5cf09a8cb0561ff24c28be4e5374d579d0601818
python3 scripts/apply.py stats-source --check
python3 scripts/apply.py stats-source
```

Open `stats-source/Stats.xcodeproj` in Xcode and build using the upstream instructions. The script only changes this source checkout. It does not install an app, touch EFI, or modify a running Stats instance. It rejects the wrong revision, a dirty checkout or a conflicting patch.

## Status and limits

The changes were previously built and used on one AMD Ryzen 7 9700X (Zen 5, 8 cores / 16 threads) / RTX 5070 Hackintosh running macOS 26, with a VK03 panel. The public patch is also checked against clean upstream source. Other hardware and OS combinations have not been validated by this project.

Live AMD frequency requires a compatible SMCProcessorAMD user client. If that fails, this implementation tries `hw.cpufrequency`, which may be a nominal value rather than a live clock. NVIDIA fields depend on driver-provided properties. Memory bandwidth utilization is not allocated VRAM usage. The RTX 5070 CUDA core count is a static specification field.

The JSON feed is written under `~/Library/Application Support/Stats/VK03Panel/` when the relevant modules and readers run. Samples carry timestamps; VK03 Panel ignores samples older than 30 seconds. See [technical notes](docs/TECHNICAL_NOTES.md).

## Contributions and license

Hardware reports, better metric mappings and focused upstream contributions are welcome. Please remove EFI identifiers, serial numbers, account data and unrelated logs from reports.

MIT licensed, with the original Stats license retained. SMCProcessorAMD and community NVIDIA drivers are external dependencies and are not distributed here. If this helps, a Star is welcome; please also support [Stats](https://github.com/exelban/stats).
