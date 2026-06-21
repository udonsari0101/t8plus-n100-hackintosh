# Limitations

## Graphics

Intel N100 uses Alder Lake-N graphics, which is not a normal supported macOS
iGPU target. This project currently treats display output as a basic VESA-style
boot/install path rather than a fully accelerated graphics setup.

Expected limitations:

- No normal macOS graphics acceleration target is established.
- Installer and recovery testing prioritize visibility and stability over GPU
  features.
- This machine should not be presented as a polished daily-driver Mac.

## USB

USBToolBox.kext plus UTBDefault.kext is a temporary installer diagnostic. If the
macOS install succeeds, the project should generate a proper USB map and remove
UTBDefault.kext.

## Wi-Fi And Bluetooth

Intel AX210 Wi-Fi and Bluetooth support are not finalized in the public EFI.
Those kexts should be added only after the base install and boot path are stable.

## Audio And Ethernet

AppleALC and RealtekRTL8111 are present in the public EFI, but post-install
behavior still needs to be tested and documented.

## Dual Boot

The plan is to preserve Windows. OpenCore should stay USB-based until both
Windows and macOS boot paths are proven and recoverable.
