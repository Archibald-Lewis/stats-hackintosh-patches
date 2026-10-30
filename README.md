# Stats 黑苹果适配补丁

[GitHub](https://github.com/Archibald-Lewis/stats-hackintosh-patches) · [Gitee](https://gitee.com/archibald-lewis/stats-hackintosh-patches) · [Companion project](https://github.com/Archibald-Lewis/vk03-panel-macos)

让 Stats 在 AMD 黑苹果和社区 NVIDIA 驱动上显示更多可用读数，并把数据导出给 VK03 副屏。

[English](README.en.md) · [实现与限制](docs/TECHNICAL_NOTES.md) · [上游 Stats](https://github.com/exelban/stats)

这是针对 **Stats 3.0.23** 的补丁集。原项目是 [exelban/Stats](https://github.com/exelban/stats)，本仓库保留原作者署名和 MIT 许可证。

## 预编译安装

[下载 DMG 安装包](https://github.com/Archibald-Lewis/stats-hackintosh-patches/releases/latest) · [安装、签名与兼容性说明](docs/INSTALL.md)

提供 AMD64 / x86_64 版，实测 AMD Ryzen 7 9700X + RTX 5070 黑苹果，ad-hoc 签名、未经 Apple 公证。


## 补了什么

| 项目 | 修改 |
|---|---|
| AMD CPU 频率 | 通过 SMCProcessorAMD 读取驱动缓存的每核心频率寄存器；包含 Zen 5 解码路径，显示 GHz |
| NVIDIA 识别 | 识别社区驱动的 `NVAccel` 服务，处理 PCI 匹配掩码和 NVIDIA 厂商信息 |
| GPU 指标 | 将驱动实际提供的核心、显存带宽、视频引擎等读数对应到界面；缺失项标为“驱动未提供” |
| VK03 数据导出 | 从 Stats 的 CPU、GPU、内存回调写入本地 JSON，供副屏读取 |

不包含 CPU 或显卡驱动，也不安装内核扩展。CPU 温度仍由 Stats 的现有传感器读取路径提供；没有传感器来源时，这个补丁不会生成温度。

## 使用

准备一个干净的上游源码副本：

```bash
git clone https://github.com/exelban/stats.git stats-source
git -C stats-source checkout --detach 5cf09a8cb0561ff24c28be4e5374d579d0601818
python3 scripts/apply.py stats-source --check
python3 scripts/apply.py stats-source
```

随后在 Xcode 中打开 `stats-source/Stats.xcodeproj`，按上游方式构建。补丁工具只修改该源码副本，不安装应用、不操作 EFI，也不改动当前运行的 Stats。需要编译环境及相关驱动的读数来源。

工具固定校验上游提交；目标不匹配、已有本地改动或补丁冲突时会停止。请在独立源码副本中使用。补丁文件位于 [`patches/`](patches/stats-3.0.23-hackintosh.patch)。

## 副屏数据

CPU、GPU、RAM 模块运行时，把对应读数写入：

```text
~/Library/Application Support/Stats/VK03Panel/
```

数值读数包含时间戳，副屏会忽略超过 30 秒的样本。CPU 频率、负载、温度和 GPU 负载来自相应的 Stats 回调；内存值以字节表示。普通版 Stats 不提供这一导出接口。

## 验证与限制

修改此前已在一台 AMD Ryzen 7 9700X（Zen 5，8 核 16 线程）+ RTX 5070、macOS 26 的黑苹果上编译运行，并用于 VK03 副屏。公开补丁的应用流程另以干净的上游源码检查。没有跨机型、跨 macOS 版本的覆盖验证。

- AMD 实时频率依赖兼容的 SMCProcessorAMD 用户客户端。实时读数不可用时，当前实现会尝试读取 `hw.cpufrequency`，它可能是标称频率，不能当作实时频率。
- 其他 AMD 系列的解码路径、不同 NVIDIA 型号及 Apple Silicon 尚未在本项目中实机验证。
- NVIDIA 数据取决于已安装驱动暴露的属性。显存带宽利用率不等于显存容量使用率。
- RTX 5070 的 6144 CUDA 核心是界面规格信息，不是运行时检测到的活跃核心数量。
- 系统或 Stats 更新后可能需要调整补丁；更新回上游构建会覆盖这些修改。

## 贡献

欢迎提供清理过的硬件测试结果、完善指标映射和拆分可提交上游的改动。反馈时请注明 Stats 提交、macOS 版本、CPU/GPU 型号和读数来源，不要附带完整 EFI、序列号或账户数据。

如果补丁帮到了你，欢迎 Star，也请支持上游 [Stats](https://github.com/exelban/stats)。

## 许可与来源

Stats 采用 MIT 许可，版权归原作者及相应贡献者所有；许可证全文保留在 [LICENSE](LICENSE)。本补丁的新增改动同样采用 MIT 许可。[SMCProcessorAMD](https://github.com/aluveitie/SMCProcessorAMD) 是外部运行依赖，不在本仓库中分发。社区 NVIDIA 驱动也不随补丁分发。
