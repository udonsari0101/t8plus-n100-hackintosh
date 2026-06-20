# Firebat T8 Plus Hackintosh Project

## Hardware

- Mini PC: Firebat T8 Plus
- CPU: Intel N100 (Alder Lake-N)
- Memory: 16GB LPDDR5
- Wi-Fi: Intel AX210
- Ethernet: Realtek RTL8111/8168
- Storage: 512GB SATA SSD

## Current Project Status

- Project directory initialized.
- Clean OpenCore-style EFI folder structure created.
- OpenCore 1.0.7 RELEASE base files added.
- Core boot kexts added from official GitHub RELEASE archives.
- Minimal prebuilt ACPI SSDTs added from official Dortania resources.
- No config.plist, Wi-Fi kexts, Bluetooth kexts, USB maps, machine-specific DSDT patches, or generated SMBIOS values have been added.

## Added Drivers

| Driver | Source |
| --- | --- |
| OpenRuntime.efi | OpenCorePkg 1.0.7 RELEASE |
| OpenHfsPlus.efi | OpenCorePkg 1.0.7 RELEASE |

## Added ACPI

| File | Purpose | Source |
| --- | --- | --- |
| SSDT-EC-USBX-DESKTOP.aml | Adds desktop EC/USBX support for macOS USB power properties and EC compatibility. | https://raw.githubusercontent.com/dortania/Getting-Started-With-ACPI/master/extra-files/compiled/SSDT-EC-USBX-DESKTOP.aml |
| SSDT-AWAC.aml | Handles common AWAC/RTC system clock compatibility for macOS. | https://raw.githubusercontent.com/dortania/Getting-Started-With-ACPI/master/extra-files/compiled/SSDT-AWAC.aml |

## Config Strategy

- `EFI/OC/config.template.plist` is tracked as the public template.
- `EFI/OC/config.plist` is local-only, ignored by Git, and may be copied from the template for testing.
- Real SMBIOS identity values must never be committed. The template uses obvious placeholders only.
- OpenCore 1.0.7 `ocvalidate` does not support `Misc > Security > AllowNvramReset`, so that key is not present in this template.

## Added Kexts

| Kext | Version | Source |
| --- | --- | --- |
| Lilu.kext | 1.7.2 | https://github.com/acidanthera/Lilu/releases/download/1.7.2/Lilu-1.7.2-RELEASE.zip |
| VirtualSMC.kext | 1.3.7 | https://github.com/acidanthera/VirtualSMC/releases/download/1.3.7/VirtualSMC-1.3.7-RELEASE.zip |
| WhateverGreen.kext | 1.7.0 | https://github.com/acidanthera/WhateverGreen/releases/download/1.7.0/WhateverGreen-1.7.0-RELEASE.zip |
| AppleALC.kext | 1.9.7 | https://github.com/acidanthera/AppleALC/releases/download/1.9.7/AppleALC-1.9.7-RELEASE.zip |
| RestrictEvents.kext | 1.1.6 | https://github.com/acidanthera/RestrictEvents/releases/download/1.1.6/RestrictEvents-1.1.6-RELEASE.zip |
| RealtekRTL8111.kext | V3.0.0 release, bundle 3.0.4 | https://github.com/Mieze/RTL8111_driver_for_OS_X/releases/download/v3.0.0/RealtekRTL8111-V3.0.0.zip |

## Next Steps

- Confirm target macOS version.
- Gather verified hardware details before adding ACPI or config.plist settings.
- Add Wi-Fi and Bluetooth kexts only after approval.
