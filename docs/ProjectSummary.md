# Project Summary

## Project

Firebat T8 Plus N100 Hackintosh experiment using OpenCore 1.0.7 RELEASE.

This public repository is a sanitized project record. It tracks shareable EFI
components, the public config template, and high-level findings. Private
per-machine identity values and local working configs stay out of this repo.

## Hardware

| Component | Detail |
| --- | --- |
| Mini PC | Firebat T8 Plus |
| CPU | Intel N100, Alder Lake-N |
| Memory | 16GB LPDDR5 |
| Storage | 512GB SATA SSD |
| Wi-Fi/Bluetooth | Intel AX210NGW |
| Ethernet | Realtek RTL8111/8168 family |

## Goal

- Experimental macOS Sonoma boot and install path.
- Preserve the existing Windows installation for later Windows/macOS dual boot.
- Use the machine for light macOS testing, Python build/test work, and possible
  Command Line Tools or Xcode experiments if the install proves usable.

## Public/Private Split

- Public repo: sanitized templates, shareable EFI components, and public notes.
- Private working copy: local config, generated identity values, detailed test
  profiles, and machine-specific debug material.
- Public docs may describe what worked, but must not include real OpenCore
  identity values or private profile contents.
