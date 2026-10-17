# Setup

A condensed guide. Assumes familiarity with OpenCore. All component versions are pinned in
[`../components.lock.json`](../components.lock.json).

## 1. Fetch components

Run `./fetch-efi-components.command` (macOS/Linux, needs `curl` + `unzip` + `shasum`). It reads
`components.lock.json` and downloads OpenCore 1.0.7 and the Acidanthera kexts from their official
GitHub releases into `EFI/OC/...`. For components it cannot fully automate, it prints the exact
upstream project + version to fetch manually:

- **AirportItlwm** (Wi-Fi) — OpenIntelWireless/itlwm: download the **AirportItlwm** build that
  matches **Sonoma 14**.
- **IntelBluetoothFirmware + IntelBTPatcher + BlueToolFixup** — OpenIntelWireless/IntelBluetoothFirmware
  release bundle.
- **RealtekRTL8111** — Mieze/RTL8111_driver_for_OS_X.
- **USBToolBox.kext** — USBToolBox/kext (and generate your own **UTBMap.kext** with USBToolBox/tool).

## 2. SMBIOS (generate your own — never use someone else's)

With [GenSMBIOS](https://github.com/corpnewt/GenSMBIOS), generate an `iMacPro1,1` set and put your
`SystemSerialNumber`, `MLB`, `SystemUUID`, and `ROM` into `EFI/OC/config.plist` →
`PlatformInfo > Generic`. The template ships placeholders (`CHANGEME...`, zero UUID/ROM) on purpose.

## 3. Config

```
cp EFI/OC/config.template.plist EFI/OC/config.plist
# edit PlatformInfo>Generic (your SMBIOS), and your USB map kext entry
ocvalidate EFI/OC/config.plist        # must pass with no errors
```

Boot-args in the template: `-v keepsyms=1 debug=0x100 alcid=1 -igfxvesa` (`-igfxvesa` forces the
firmware framebuffer since there is no GPU driver). You can drop `-v debug=0x100 keepsyms=1` for a
quiet boot once stable.

## 4. ACPI

The SSDTs in `EFI/OC/ACPI/` are listed in the config's `ACPI > Add`. `SSDT-AWAC` and
`SSDT-EC-USBX-DESKTOP` are from Dortania's prebuilt set; `SSDT-PLUG-ALT` tunes CPU power management.

## 5. Install

Copy the assembled `EFI/` to your USB/ESP FAT32 partition and select OpenCore in the firmware boot
menu. Expect an **unaccelerated** desktop (see `Limitations.md`).
