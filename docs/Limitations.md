# Limitations

This baseline is a **stable fallback**, not a fully accelerated Mac. Known limitations:

## Graphics (the big one)

- **No GPU acceleration.** The Intel N100 (Alder Lake-N / Xe-LP, Gen12) has no macOS driver: Apple's
  newest Intel graphics driver is Ice Lake (Gen11), two IP generations older. The desktop runs on the
  firmware **GOP framebuffer** (~18 MB, no Metal, no IOAccelerator).
- Consequences: no Metal; no hardware video decode; WindowServer/compositing runs on the CPU, so
  heavy video (e.g. fullscreen/4K/high-bitrate VP9/AV1) can be choppy or can overload the compositor.
  Light use and modest-resolution H.264 video are usable.
- The display resolution is whatever the firmware GOP provides; macOS cannot mode-set on this
  unaccelerated path.

## Networking

- Wi-Fi is **AirportItlwm** (Intel AX210): 802.11ac works; **no** 6 GHz / Wi-Fi 6E, and **no**
  AWDL-based features (AirDrop, Handoff, Continuity, Sidecar).
- Bluetooth works (pairing confirmed), subject to the usual third-party Intel Bluetooth caveats.

## Not characterized

- Sleep/wake, USB-C/Thunderbolt behavior, and power management are not validated here — treat as
  UNVERIFIED and test on your own hardware.

## Identity / safety

- You must supply your own SMBIOS and USB map. The shipped template has placeholders only.
