# Beginner-Friendly Install Guide

A step-by-step walkthrough for reproducing the verified **macOS Sonoma 14.8.7 (23J520)**
GOP baseline on a **Firebat T8 Plus (Intel N100)**. This is the detailed companion to the
condensed [`Setup.md`](Setup.md); read both. For *what works and what doesn't*, see
[`Limitations.md`](Limitations.md).

> **Honest expectations — read first**
> - This is a **stable fallback baseline**: macOS boots and networks, but the display runs on the
>   firmware **GOP framebuffer** with **no GPU acceleration, no Metal, no hardware video decode**.
>   That is by design and will not change by following this guide.
> - The process is **not one-click.** Of 16 pinned components, **7 are fetched/generated manually**,
>   and your **SMBIOS and USB map are machine-specific** (you create them yourself).
> - Component downloads are **not checksum-verified** by the fetch script: `components.lock.json`
>   records a SHA-256 (`local_sha256`) for the kexts (not the OpenCore `.efi` binaries or your
>   generated UTBMap), but the script does not check
>   downloads against them. Verify artifacts yourself — against those hashes, or each project's
>   official release.
> - **Reproduction status:** the WORKING rows in the compatibility table are confirmed on the
>   author's own machine. A **complete fresh install has not been independently reproduced** by a
>   third party and signed off here. Treat this as a well-documented baseline to adapt, not a
>   guaranteed turnkey result. Expect to debug.

---

## 1. Prerequisites

**Hardware**
- A Firebat T8 Plus (or equivalent **Intel N100 / Alder Lake-N**, iGPU `8086:46D1`). Other N100
  boxes are *similar* but differ in USB layout and firmware — the USB map especially will differ.
- A USB flash drive (8 GB+) for the macOS installer, and a separate small FAT32 volume (or the
  installer's ESP) for the EFI.
- A second working computer to prepare the installer and EFI.

**A machine to build the EFI on**
- **macOS** is easiest (you'll need `ocvalidate` from OpenCorePkg, and `GenSMBIOS`/USBToolBox run
  there). macOS or Linux can run the fetch script.
- Command-line tools: `curl`, `unzip`, and `python3` (or `python`). On a fresh Unix clone the fetch
  script may need `chmod +x fetch-efi-components.command` first.

**Knowledge**
- Basic comfort with the terminal, editing a `.plist` (ProperTree or Xcode), and your PC's firmware
  boot menu. If OpenCore is entirely new, skim the [Dortania OpenCore guide](https://dortania.github.io/OpenCore-Install-Guide/)
  first — this repo assumes that workflow and only adds the T8 Plus specifics.

**What this repo gives you**
- A sanitized OpenCore `config.template.plist`, the ACPI SSDTs, a pinned component list
  ([`components.lock.json`](../components.lock.json)), and a fetch helper. It ships **no** Apple
  software and **no** third-party binaries — you fetch those from their official releases.

## 2. Get a macOS Sonoma installer

Create a Sonoma **14.8.7 (23J520)** USB installer the normal way (e.g. `createinstallmedia` from a
real Mac, or a community method). That step is outside this repo's scope; this guide covers the
**OpenCore EFI** you boot the installer and the installed system with.

## 3. Fetch the components

From the repo root:

```bash
./fetch-efi-components.command
```

It reads [`components.lock.json`](../components.lock.json) and downloads the automatable pieces
(OpenCore 1.0.7, Lilu, VirtualSMC, WhateverGreen, AppleALC, RestrictEvents, OpenRuntime,
OpenHfsPlus) from their **official** releases into `EFI/OC/...`, then prints the **manual** ones.
Nothing is redistributed by this repo.

**Fetch these 7 manually** (pinned versions from the lockfile — match them):

| Component | Version | Source | Notes |
|---|---|---|---|
| AirportItlwm | 2.3.0 | [OpenIntelWireless/itlwm](https://github.com/OpenIntelWireless/itlwm) | Pick the **Sonoma 14** build |
| IntelBluetoothFirmware | 2.4.0 | [OpenIntelWireless/IntelBluetoothFirmware](https://github.com/OpenIntelWireless/IntelBluetoothFirmware) | Release bundle |
| IntelBTPatcher | 2.4.0 | same bundle | In the IntelBluetoothFirmware release |
| BlueToolFixup | 2.7.2 | same bundle | In the IntelBluetoothFirmware release |
| RealtekRTL8111 | 3.0.4 | [Mieze/RTL8111_driver_for_OS_X](https://github.com/Mieze/RTL8111_driver_for_OS_X) | Trusted release or build from source |
| USBToolBox (kext) | 1.2.0 | [USBToolBox/kext](https://github.com/USBToolBox/kext) | Official release |
| **UTBMap** | — | [USBToolBox/tool](https://github.com/USBToolBox/tool) | **Generate your own** (step 5) — machine-specific |

Place each at the `dest` path shown in `components.lock.json` (all under `EFI/OC/Kexts/…`).

## 4. Generate your SMBIOS *(machine-specific — never reuse anyone's)*

With [GenSMBIOS](https://github.com/corpnewt/GenSMBIOS), generate an **`iMacPro1,1`** set and keep
your `SystemSerialNumber`, `MLB`, `SystemUUID`, and `ROM`. You'll paste them into
`config.plist → PlatformInfo → Generic` in step 6. **Never commit real values** — the template
ships placeholders (`CHANGEME…`, zero UUID/ROM) on purpose.

## 5. Build your USB map *(machine-specific)*

Use [USBToolBox/tool](https://github.com/USBToolBox/tool) to map your ports and export
**`UTBMap.kext`** into `EFI/OC/Kexts/`. USB maps are unique per board/firmware — do **not** reuse
someone else's.

## 6. Create and edit `config.plist`

```bash
cp EFI/OC/config.template.plist EFI/OC/config.plist
```

Then edit `EFI/OC/config.plist`:
- `PlatformInfo → Generic`: paste **your** SMBIOS (step 4).
- Confirm your **USB-map kext** entry (`UTBMap.kext`) is present under `Kernel → Add`.
- Boot-args in the template are `-v keepsyms=1 debug=0x100 alcid=1 -igfxvesa -btlfxnvramcheck`.
  `-igfxvesa` forces the firmware framebuffer (there is no GPU driver) — keep it;
  `-btlfxnvramcheck` is a BlueToolFixup flag. You can drop `-v keepsyms=1 debug=0x100` for a quiet
  boot once stable.

ACPI SSDTs in `EFI/OC/ACPI/` are already referenced by the template's `ACPI → Add`
(`SSDT-AWAC`, `SSDT-EC-USBX-DESKTOP`, `SSDT-PLUG-ALT`).

## 7. Validate

```bash
ocvalidate EFI/OC/config.plist
```

Use the **`ocvalidate` from the same OpenCore 1.0.7 release** — it ships inside the OpenCore 1.0.7
download under `Utilities/ocvalidate/` (the fetch script extracts only the `.efi` files, not the
utilities). It must report **no errors** before you boot.

## 8. Install to USB/ESP and boot

1. Format the target EFI volume **FAT32**.
2. Copy the assembled `EFI/` folder to its root.
3. In your PC's firmware boot menu, select the OpenCore entry.
4. Boot the macOS installer, install, then boot the installed system with the same EFI.
5. Expect an **unaccelerated** desktop at the firmware's GOP resolution.

---

## Setup checklist

- [ ] Sonoma 14.8.7 (23J520) USB installer created
- [ ] `./fetch-efi-components.command` run; automated components in `EFI/OC/…`
- [ ] 7 manual components fetched at pinned versions (table above)
- [ ] `UTBMap.kext` generated for **this** machine
- [ ] SMBIOS (`iMacPro1,1`) generated; values ready (not committed)
- [ ] `config.plist` created from template; SMBIOS + USB map filled in
- [ ] `ocvalidate EFI/OC/config.plist` → no errors
- [ ] `EFI/` copied to a FAT32 USB/ESP
- [ ] Booted via firmware boot menu → OpenCore → macOS

## Which steps are universal vs machine-specific

| Universal (same for every T8 Plus) | Machine-specific (you must customize) |
|---|---|
| OpenCore 1.0.7 + the pinned kext set | **SMBIOS** identity (`iMacPro1,1`, your own) |
| The ACPI SSDTs in `EFI/OC/ACPI/` | **UTBMap.kext** USB port map |
| Boot-args (incl. `-igfxvesa`) | Firmware/BIOS settings & boot-menu entry |
| The `config.template.plist` structure | Installer creation; disk layout |

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| `ocvalidate` reports errors | Wrong `ocvalidate` version (must match OpenCore 1.0.7), a kext listed in `Kernel → Add` but missing from `EFI/OC/Kexts/`, or a malformed template edit. Fix the specific path/entry it names. |
| OpenCore shows no boot entries / won't start | EFI not on a **FAT32** volume, or not at `EFI/BOOT/BOOTx64.efi` + `EFI/OC/OpenCore.efi`; Secure Boot still on; wrong firmware boot entry. Re-check the copied tree. |
| Kernel panic naming a kext, or "kext not found" | A kext in `config.plist` isn't present/complete in `EFI/OC/Kexts/`, versions mismatched, or load order wrong (Lilu must load before Lilu-plugins). Re-fetch at the pinned versions. |
| No Wi-Fi | AirportItlwm not matched to **Sonoma 14**; confirm you fetched the Sonoma-14 AirportItlwm build. Note: no 6 GHz, no AirDrop/Handoff/Continuity (AWDL). See [Limitations](Limitations.md#networking). |
| No Bluetooth | IntelBluetoothFirmware + IntelBTPatcher + BlueToolFixup all present and loading; check load order. |
| No Ethernet | RealtekRTL8111 present at the pinned version. |
| Black screen / wrong resolution | Expected on the unaccelerated path — the display is whatever the firmware **GOP** provides and macOS cannot mode-set here. Keep `-igfxvesa`. This is a hardware-acceleration limitation, not a config bug. |
| Choppy video / sluggish compositing | Expected: WindowServer runs on the CPU (no Metal). Prefer modest-resolution H.264; heavy 4K/VP9/AV1 can overload the compositor. |
| Sleep/wake issues | **Unverified** on this baseline — not characterized. Test at your own risk. |

If a step fails, fix *that* step before moving on — don't stack changes. Capture the exact error
text; most OpenCore issues name the precise kext, path, or config key at fault.

## Validation honesty

This repository is validated **offline/host-side** (config template structure, `ocvalidate`,
component pinning, documentation). That is **not** the same as a real fresh install: a complete,
independent end-to-end reinstall on separate hardware has **not** been reproduced and certified
here. The WORKING features in the [compatibility table](../README.md#01--compatibility) are
from the author's own machine. Use this as a thoroughly documented starting point, and expect to
adapt details for your exact unit.
