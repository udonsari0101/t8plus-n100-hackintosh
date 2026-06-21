# Boot Findings

## OpenCore Picker

OpenCore picker booted successfully from an EFI-only USB. The picker displayed
Windows and the external OpenCore boot volume, confirming the base OpenCore
files and USB boot path were viable.

## EXITBS:START

Early macOS Recovery attempts reached `EXITBS:START` and stopped. A later
attempt-3-style Booter quirk profile passed this point. The useful direction was
to use `SetupVirtualMap` with a conservative memory-map handoff combination.

This finding is public-safe as a high-level behavior note. The private working
copy keeps the exact local active config.

## CoreAnalyticsHub

After EXITBS was solved, several boots reached macOS kernel logs and stopped
around the CoreAnalyticsHub area. That log line appears to have been the last
visible symptom rather than the true root cause.

The major breakthrough was adding the official SSDT-PLUG-ALT sample, compiled
for use in the private EFI. With SSDT-PLUG-ALT enabled, the system reached the
macOS Sonoma Recovery GUI.

## USB Input In Recovery

The first Recovery GUI boot showed the macOS setup input prompt, but keyboard
and mouse were not usable. Retesting USBToolBox.kext with UTBDefault.kext after
the PLUG-ALT breakthrough fixed USB input in Recovery.

USBToolBox alone was not enough before the PLUG-ALT profile could reach the GUI.
The working interpretation is that CPU power-management initialization had to be
fixed first, then USB input troubleshooting became meaningful.

## Failed Or Neutral Attempts

| Attempt | Result |
| --- | --- |
| Safe mode | Did not materially change the hang. |
| `npci=0x3000` | Did not materially change the hang. |
| `cpus=1` | Did not materially change the hang. |
| Graphics-safe boot args | Did not materially change the hang. |
| USBToolBox before PLUG-ALT | Did not fix the CoreAnalyticsHub-stage stop. |
| Minimal kext set | Did not materially improve the stop. |
| RHUB/TXHC experiments | Did not solve the hang. |
| XHCI-to-TXHC rename | Did not solve the hang. |

## USB Controller Path Finding

Private ACPI investigation found that the native USB controller path is in the
XHCI family, not a native TXHC device. The raw dump is not published here because
it is machine-specific, but the public-safe conclusion is that RHUB/TXHC guesses
were not the winning path for this machine.
