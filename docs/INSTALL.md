# 预编译安装包 / Prebuilt installation

本版本为 AMD64 / x86_64 社区构建，实机验证设备为 AMD Ryzen 7 9700X（8 核 16 线程）+ GeForce RTX 5070 + 32 GB 内存的 macOS 26 黑苹果。不是 Apple Silicon 通用包；Intel CPU 设备尚未实测。安装前退出正在使用的同名应用，保留旧版本；打开 DMG，将应用拖入 Applications，然后退出磁盘映像并从应用程序目录打开。安装不会修改 EFI 或安装内核驱动。

The disk image contains a signed app and an Applications shortcut. Quit the existing app, keep a backup, drag the new app to Applications, eject the disk image, then open the installed app. No EFI changes or kernel extensions are installed. AMD64 / x86_64 binary. Tested hardware: AMD Ryzen 7 9700X (8 cores / 16 threads), GeForce RTX 5070 and 32 GB RAM, running macOS 26. Intel CPU machines and Apple Silicon are unverified.

## 签名 / Signing

代码签名为 ad-hoc，未使用 Developer ID，也未通过 Apple 公证。因此浏览器下载后可能被 Gatekeeper 拦截；构建和本地签名检查通过不代表 Apple 已批准运行。请阅读 Apple 的说明，自行决定是否允许该应用运行：
https://support.apple.com/en-us/102445

This build is ad-hoc signed, not Developer ID signed or notarized. A downloaded copy may be blocked by Gatekeeper. Review Apple's guidance and decide whether to approve this app yourself. No security settings are changed by the package.

## 校验 / Integrity

下载同一 Release 的 SHA256SUMS.txt，将文件放在同一目录后运行：

```bash
shasum -a 256 -c SHA256SUMS.txt
```

只下载部分文件时，可先从清单中选择对应行再校验。校验用于检查下载完整性，不替代开发者身份验证。

## Stats 社区版

基于上游 Stats 3.0.23，应用仍名为 Stats.app，会与原版共享偏好设置，不能和原版同时运行。安装前请自行保存原版。硬件补丁版本记录在 Info.plist 的 StatsCommunityPatchVersion 中。

编译版关闭上游自动更新和内置更新检查，避免被无适配补丁的原版覆盖。更新请从本项目 Release 手动下载。系统负载、内存和可用的驱动数据无需自行编译即可读取；AMD 实时频率与温度仍需要对应驱动。本安装包不会安装这些驱动。

风扇控制、SMC 特权助手的安装、桌面小组件和传感器跨机型兼容性尚未验证，不作为本预编译版的已验证功能。程序的权限提示由用户自行决定是否接受。

Based on upstream Stats 3.0.23. The app remains Stats.app and shares preferences with stock Stats; keep a backup and run one version at a time. Built-in upstream updating is disabled in this community binary. Drivers are not included. Fan control, privileged-helper installation, desktop widgets and cross-machine sensor compatibility are unverified. The package does not install or register the helper.

源码构建：先应用主补丁，再应用 patches/community-binary-updater.patch；使用 xcodebuild 的 Stats / Release 方案、ARCHS=x86_64、ONLY_ACTIVE_ARCH=YES 和 CODE_SIGNING_ALLOWED=NO。打包前设置 StatsCommunityBuild=true，StatsCommunityPatchVersion=0.1.1，附带原始 MIT 许可证，并进行 ad-hoc 签名。完整对应源码压缩包与安装包一起发布。
