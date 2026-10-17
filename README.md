# Firebat T8 Plus (Intel N100) — macOS Sonoma OpenCore baseline

A sanitized, reproducible OpenCore EFI for running **macOS Sonoma 14.8.7 (build 23J520)** on the
**Firebat T8 Plus** mini PC (**Intel N100** / Alder Lake-N). This is a **stable fallback baseline**:
the machine boots and networks reliably, but the N100 iGPU is **not hardware-accelerated** (it runs on
the firmware GOP framebuffer only). Custom GPU-driver work is a separate, ongoing effort and is **not**
part of this baseline.

## Hardware

- Firebat T8 Plus · Intel **N100** (Alder Lake-N, Xe-LP iGPU `8086:46D1`) · 16 GB LPDDR5
- Intel **AX210** Wi-Fi + Bluetooth · **Realtek RTL8111** Ethernet

## Status

| Feature | Status | Notes |
|---|---|---|
| macOS Sonoma 23J520 boot | WORKING | OpenCore 1.0.7 |
| 3440×1440 GOP display | WORKING | firmware framebuffer; **unaccelerated, no Metal** |
| Intel AX210 Wi-Fi | WORKING | AirportItlwm; 802.11ac (no 6 GHz / AWDL / AirDrop / Continuity) |
| Intel AX210 Bluetooth | WORKING | IntelBluetoothFirmware + BlueToolFixup + IntelBTPatcher |
| Realtek Ethernet | WORKING | RealtekRTL8111 |
| Audio | WORKING (basic output) | AppleALC |
| N100 GPU acceleration | NOT IMPLEMENTED | no Intel graphics kext, no IOAccelerator |
| Metal | NOT IMPLEMENTED | — |
| Hardware video decode / acceleration | NOT IMPLEMENTED | video decodes on CPU |
| Native Alder Lake-N display driver | NOT IMPLEMENTED | — |
| Sleep / wake | UNVERIFIED | not characterized |

Only features marked WORKING are runtime-confirmed on the real machine. Everything GPU-related is
deliberately **NOT IMPLEMENTED** in this baseline.

## You must generate these yourself

- **SMBIOS identity** (`SystemSerialNumber`, `MLB`, `SystemUUID`, `ROM`): the template ships with
  obvious placeholders. Generate your own with [GenSMBIOS](https://github.com/corpnewt/GenSMBIOS) for
  `iMacPro1,1` and never commit them.
- **USB mapping** (`UTBMap.kext` via [USBToolBox](https://github.com/USBToolBox/tool)): machine-specific.

## Use

1. **Fetch components:** run `./fetch-efi-components.command`, or assemble manually using
   [`components.lock.json`](components.lock.json) (exact upstream projects + versions). Third-party
   kexts/drivers/OpenCore are **not** redistributed here — they are fetched from their official releases.
2. Place the fetched kexts/drivers/OpenCore files into `EFI/OC/...` per `components.lock.json`.
3. Copy `EFI/OC/config.template.plist` → `EFI/OC/config.plist`; fill in **your own** SMBIOS + USB map.
4. Validate: `ocvalidate EFI/OC/config.plist` (must pass clean).
5. Copy `EFI/` to your USB/ESP and boot.

See [`docs/Setup.md`](docs/Setup.md) and [`docs/Limitations.md`](docs/Limitations.md).

## Scope / credits

This repository contains only the **sanitized configuration template, ACPI SSDTs, and setup tooling**.
It redistributes no Apple software and no third-party binaries; OpenCore and all kexts are obtained
from their official open-source releases (see `components.lock.json`).
