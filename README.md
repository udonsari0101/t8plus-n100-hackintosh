<div align="center">

<img src="assets/readme/mark.svg" alt="Firebat T8 Plus N100 project mark" width="76" height="76">

<img src="assets/readme/hero.svg" alt="Firebat T8 Plus — macOS Sonoma on Intel N100. OpenCore 1.0.7 EFI baseline, Sonoma 14.8.7 build 23J520, firmware GOP display." width="100%">

<br><br>

**English** · [한국어](README.ko.md)

A sanitized, reproducible **OpenCore EFI** for running **macOS Sonoma 14.8.7 (23J520)** on the
**Firebat T8 Plus** mini PC — **Intel N100** / Alder Lake-N. A stable fallback baseline: it boots
and networks reliably on the firmware **GOP** framebuffer. The N100 iGPU is **not** hardware-accelerated.

<br>

![macOS](https://img.shields.io/badge/macOS-Sonoma_14.8.7_(23J520)-1f6feb?style=flat-square&labelColor=0b1220&logo=apple&logoColor=white)
![OpenCore](https://img.shields.io/badge/OpenCore-1.0.7-1f6feb?style=flat-square&labelColor=0b1220)
![Intel N100](https://img.shields.io/badge/Intel-N100_Alder_Lake--N-1f6feb?style=flat-square&labelColor=0b1220&logo=intel&logoColor=white)
![Display](https://img.shields.io/badge/display-GOP_only,_no_GPU_accel-8899a6?style=flat-square&labelColor=0b1220)

[**Quick Start**](#quick-start) · [Compatibility](#hardware-compatibility) · [Limitations](docs/Limitations.md) · [Setup](docs/Setup.md)

</div>

---

## Overview

This repository is the **sanitized configuration layer** for the build — OpenCore `config` template,
ACPI SSDTs, component lockfile, and setup tooling. It redistributes **no** Apple software and **no**
third-party binaries; OpenCore and every kext are fetched from their official open-source releases.

| | |
|---|---|
| **Machine** | Firebat T8 Plus mini PC |
| **SoC** | Intel **N100** (Alder Lake-N, Xe-LP iGPU `8086:46D1`), 16 GB LPDDR5 |
| **macOS** | Sonoma **14.8.7** · build **23J520** |
| **Bootloader** | OpenCore **1.0.7** |
| **Wireless** | Intel **AX210** (Wi-Fi + Bluetooth) |
| **Wired** | Realtek **RTL8111** Ethernet |
| **Display** | Firmware **GOP** framebuffer (unaccelerated) |

> **Baseline, not an accelerated Mac.** GPU acceleration, Metal, and hardware video decode are
> **not implemented** here — by design. Custom N100 GPU-driver research is a *separate, ongoing*
> effort and is **not** part of this baseline.

## Hardware compatibility

Only rows marked **Working** are runtime-confirmed on the real machine. Everything GPU-related is
deliberately **not implemented** in this baseline.

| Feature | Status |
|---|:--|
| macOS Sonoma 23J520 boot | ✅ **Working** |
| 3440×1440 firmware GOP display | ✅ **Working** — unaccelerated, no Metal |
| Intel AX210 Wi-Fi | ✅ **Working** — with [documented limits](docs/Limitations.md#networking) |
| Intel AX210 Bluetooth | ✅ **Working** — with [documented limits](docs/Limitations.md#networking) |
| Realtek Ethernet | ✅ **Working** |
| Audio (basic output) | ✅ **Working** |
| Intel N100 GPU acceleration | ⛔ **Not implemented** |
| Metal | ⛔ **Not implemented** |
| Hardware video decode | ⛔ **Not implemented** |
| Native Alder Lake-N display driver | ⛔ **Not implemented** |
| Sleep / wake | ⚪ **Unverified** |

## Quick Start

> Prerequisites: a working OpenCore workflow and basic Hackintosh familiarity. All component
> versions are pinned in [`components.lock.json`](components.lock.json).

**1 · Fetch pinned components** (OpenCore 1.0.7 + kexts, from their official releases — nothing is
redistributed in this repo):

```bash
./fetch-efi-components.command
```

**2 · Generate your own machine identity** (never reuse someone else's):

- **SMBIOS** — [GenSMBIOS](https://github.com/corpnewt/GenSMBIOS), model `iMacPro1,1`
  (`SystemSerialNumber`, `MLB`, `SystemUUID`, `ROM`).
- **USB map** — [USBToolBox](https://github.com/USBToolBox/tool) → your own `UTBMap.kext`.

**3 · Create your config from the template:**

```bash
cp EFI/OC/config.template.plist EFI/OC/config.plist
# edit PlatformInfo > Generic (your SMBIOS) and your USB-map kext entry
```

**4 · Validate** (must pass clean):

```bash
ocvalidate EFI/OC/config.plist
```

**5 · Install** — copy `EFI/` to your USB/ESP FAT32 partition and select OpenCore in the firmware
boot menu. Expect an **unaccelerated** desktop.

Full walkthrough: [`docs/Setup.md`](docs/Setup.md) · Known limits: [`docs/Limitations.md`](docs/Limitations.md).

## Repository layout

```
.
├─ EFI/                        OpenCore tree (config.template.plist + ACPI SSDTs; no binaries)
├─ docs/
│  ├─ Setup.md                 condensed install guide
│  └─ Limitations.md           what works, what does not, and why
├─ assets/readme/              original README artwork (static SVG)
├─ components.lock.json        pinned upstream projects + exact versions
├─ fetch-efi-components.command downloader that reads the lockfile
└─ .githooks/                  identity + template-placeholder guards
```

## Reproducibility

[`components.lock.json`](components.lock.json) pins every upstream project and exact version
(OpenCore 1.0.7 and the Acidanthera / OpenIntelWireless / Mieze kexts). `fetch-efi-components.command`
reads it and pulls each artifact from its **official** release, printing manual-fetch instructions
for anything it can't automate. Binaries are intentionally **not** committed — favoring
reproducibility over vendoring.

## Privacy & identity

The shipped `config.template.plist` contains **placeholders only** (`CHANGEME…`, zero UUID/ROM).

- Generate and keep your **own** SMBIOS (`SystemSerialNumber`, `MLB`, `SystemUUID`, `ROM`) and USB map.
- **Never commit** real identifiers. The repo's `.githooks` guard the template placeholders and the
  human Git identity.

## Credits

Built on the open-source Hackintosh ecosystem — all fetched from their official releases:

- [OpenCorePkg](https://github.com/acidanthera/OpenCorePkg) and the Acidanthera kexts
- [AirportItlwm / itlwm](https://github.com/OpenIntelWireless/itlwm) and
  [IntelBluetoothFirmware](https://github.com/OpenIntelWireless/IntelBluetoothFirmware) (OpenIntelWireless)
- [RealtekRTL8111](https://github.com/Mieze/RTL8111_driver_for_OS_X) (Mieze)
- [USBToolBox](https://github.com/USBToolBox/tool) (USB mapping) and [GenSMBIOS](https://github.com/corpnewt/GenSMBIOS) by CorpNewt
- [Dortania](https://dortania.github.io/) guides and prebuilt SSDTs

## Scope & disclaimer

This is a personal, sanitized configuration baseline provided **as-is**, for interoperability and
educational use. It ships only the config template, ACPI SSDTs, and tooling — no Apple software and
no third-party binaries. You are responsible for your own SMBIOS, licensing compliance, and any risk
of running macOS on non-Apple hardware. Not affiliated with or endorsed by Apple, Intel, Firebat,
or any listed upstream project.
