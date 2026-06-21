# Progress Report

## Current State

The project has moved from basic OpenCore picker validation to a working macOS
Sonoma Recovery GUI path. USB keyboard and mouse input work in Recovery with
the current private installer profile.

## Timeline

| Stage | Public-safe result |
| --- | --- |
| Project setup | OpenCore-style EFI structure created and committed. |
| OpenCore base | OpenCore 1.0.7 RELEASE base files added from Acidanthera. |
| Drivers | OpenRuntime.efi and OpenHfsPlus.efi added from OpenCorePkg. |
| Core kexts | Lilu, VirtualSMC, WhateverGreen, AppleALC, RestrictEvents, and RealtekRTL8111 added from official release sources. |
| Minimal ACPI | Dortania prebuilt SSDT-AWAC and SSDT-EC-USBX-DESKTOP added. |
| Public template | Public config template created; local config remains ignored. |
| Picker test | OpenCore picker appeared successfully from an EFI-only USB. |
| Recovery media | macOS Sonoma Recovery USB was prepared separately. |
| EXITBS issue | Recovery boot initially hung at EXITBS:START. |
| EXITBS fix | An attempt-3-style Booter quirk set passed EXITBS and reached macOS kernel logs. |
| CoreAnalyticsHub issue | Boot later stopped around the CoreAnalyticsHub log area. |
| PLUG-ALT breakthrough | SSDT-PLUG-ALT allowed the boot to pass that point and reach the Recovery GUI. |
| USB input fix | USBToolBox.kext plus UTBDefault.kext allowed keyboard and mouse input in Recovery. |
| Dual-boot preparation | Windows is preserved; space has been prepared for macOS without creating a new public EFI dependency. |

## Known Working Direction

The current practical installer direction is:

```text
attempt-3-style Booter quirks
SSDT-PLUG-ALT
USBToolBox.kext
UTBDefault.kext
```

This is not final polish. UTBDefault.kext is temporary and should be replaced by
a real machine-specific USB map after installation testing.
