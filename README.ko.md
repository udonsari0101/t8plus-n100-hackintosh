```text
+------------------------------------------+
| FIREBAT T8 PLUS                     N100 |
+------------------------------------------+
| os       macOS Sonoma 14.8.7 (23J520)    |
| boot     OpenCore 1.0.7                  |
| gpu      8086:46D1  not accelerated      |
| display  firmware GOP framebuffer        |
| net      AX210 Wi-Fi/BT, RTL8111 ether   |
+------------------------------------------+
```

`Firebat T8 Plus` — **Intel N100에서 구동하는 macOS Sonoma.** 검증된 **비가속** Sonoma
베이스라인을 위한, 정제되고 재현 가능한 OpenCore EFI입니다. 펌웨어 GOP 프레임버퍼 위에서 부팅과
네트워크가 안정적으로 동작하지만, N100 내장 GPU에는 macOS 드라이버가 **없어** Metal과 하드웨어
비디오 디코딩이 동작하지 않습니다. 위 패널은 프로젝트 요약이며, 실제 런타임 출력이 아닙니다.

![OpenCore](https://img.shields.io/badge/OpenCore-1.0.7-5c5c5c?style=flat&labelColor=2b2b2b)
![macOS](https://img.shields.io/badge/macOS-Sonoma_23J520-5c5c5c?style=flat&labelColor=2b2b2b)
![GPU](https://img.shields.io/badge/GPU_accel-not_implemented-5c5c5c?style=flat&labelColor=2b2b2b)

[English](README.md) · `한국어`   —   [00 개요](#00--개요) · [01 호환성](#01--호환성) · [02 빠른 시작](#02--빠른-시작) · [03 하드웨어](#03--하드웨어) · [04 제약](#04--제약) · [05 크레딧](#05--크레딧)

---

## 00 / 개요

이 저장소는 **설정 계층** 만 담습니다: OpenCore `config` 템플릿, ACPI SSDT, 고정된 구성요소
잠금 파일, 설치 도구. Apple 소프트웨어나 서드파티 바이너리는 **일절 재배포하지 않으며**, OpenCore와
모든 kext는 각 공식 릴리스에서 내려받습니다.

의도적으로 GPU가 없는 **안정적인 폴백 베이스라인** 입니다. 커스텀 N100 GPU 드라이버 연구는 별도로
진행 중인 작업이며 이 저장소에 **포함되지 않습니다**.

## 01 / 호환성

**동작** 으로 표시된 항목만 실제 기기에서 확인되었습니다. GPU 관련 항목은 이 베이스라인에서
의도적으로 **미구현** 입니다.

| 기능 | 상태 |
|---|:--|
| macOS Sonoma 23J520 부팅 | 동작 |
| 3440×1440 펌웨어 GOP 디스플레이 | 동작 — 비가속, Metal 없음 |
| Intel AX210 Wi-Fi | 동작 — [문서화된 제약](docs/Limitations.md#networking) |
| Intel AX210 Bluetooth | 동작 — [문서화된 제약](docs/Limitations.md#networking) |
| Realtek 이더넷 | 동작 |
| 오디오 (기본 출력) | 동작 |
| Intel N100 GPU 가속 | 미구현 |
| Metal | 미구현 |
| 하드웨어 비디오 디코딩 | 미구현 |
| 네이티브 Alder Lake-N 디스플레이 드라이버 | 미구현 |
| 절전 / 복귀 | 미검증 |

## 02 / 빠른 시작

처음이라면 단계별 [**Install Guide**](docs/Install-Guide.md)(영문: 체크리스트 + 수동 구성요소 +
문제 해결)를 따르세요. 요약:

```sh
# 1  고정된 구성요소(OpenCore 1.0.7 + kext)를 공식 릴리스에서 받기
./fetch-efi-components.command

# 2  본인만의 머신 식별자 생성 (타인의 값 재사용 금지)
#    - SMBIOS  : GenSMBIOS, 모델 iMacPro1,1  (SystemSerialNumber, MLB, SystemUUID, ROM)
#    - USB 맵  : USBToolBox -> 본인의 UTBMap.kext

# 3  템플릿에서 config 생성 후 SMBIOS + USB 맵 입력
cp EFI/OC/config.template.plist EFI/OC/config.plist

# 4  검증 (오류 없이 통과; ocvalidate는 OpenCore 1.0.7 zip에 포함)
ocvalidate EFI/OC/config.plist

# 5  EFI/ 를 FAT32 USB/ESP에 복사하고 펌웨어 부트 메뉴에서 OpenCore 선택
```

7개 구성요소는 수동으로 받거나 생성해야 하고, SMBIOS와 USB 맵은 기기별이라 **원클릭이 아닙니다**.
자세한 내용은 [Install Guide](docs/Install-Guide.md) 와 [`docs/Setup.md`](docs/Setup.md) 참고.

## 03 / 하드웨어

| | |
|---|---|
| 기기 | Firebat T8 Plus 미니 PC |
| SoC | Intel N100 (Alder Lake-N, Xe-LP iGPU `8086:46D1`), 16 GB LPDDR5 |
| 무선 | Intel AX210 — Wi-Fi + Bluetooth |
| 유선 | Realtek RTL8111 이더넷 |
| 디스플레이 | 펌웨어 GOP 프레임버퍼 (비가속) |

```
.
├─ EFI/                         OpenCore 트리 (config.template.plist + ACPI SSDT; 바이너리 없음)
├─ docs/
│  ├─ Install-Guide.md          초보자용 단계별 안내 (영문)
│  ├─ Setup.md                  간결한 참고
│  └─ Limitations.md            동작/미동작 항목과 그 이유
├─ components.lock.json         고정된 업스트림 + 정확한 버전 (+ 기록된 SHA-256)
└─ fetch-efi-components.command 잠금 파일을 읽는 다운로더
```

**재현성.** `components.lock.json` 은 프로젝트/버전을 고정하고 kext에 대해 `local_sha256` 을
기록합니다(OpenCore `.efi` 바이너리와 직접 생성하는 UTBMap은 제외). `fetch-efi-components.command`
는 각 아티팩트를 공식 릴리스에서 받습니다(아직 그 해시로 다운로드를 검증하지는 않으니 직접
확인하세요).

## 04 / 제약

- **GPU 가속 없음.** Alder Lake-N(Gen12)에는 macOS 드라이버가 없습니다(Apple 최신 Intel 그래픽은
  Ice Lake/Gen11). 데스크톱은 펌웨어 GOP 프레임버퍼에서 동작 — Metal/IOAccelerator 없음, CPU
  컴포지팅, 하드웨어 비디오 디코딩 없음.
- **Wi-Fi/Bluetooth** 는 OpenIntelWireless 스택으로 동작하나 6 GHz 와 AWDL 기능
  (AirDrop/Handoff/Continuity)은 제외.
- **절전/복귀, USB-C/TB, 전원 관리** 는 특성화되지 않음 — 미검증으로 간주.

자세히: [`docs/Limitations.md`](docs/Limitations.md).

> **개인정보.** 템플릿에는 플레이스홀더 SMBIOS만 들어 있습니다. 본인의 `SystemSerialNumber`,
> `MLB`, `SystemUUID`, `ROM`, USB 맵을 생성하고 실제 값을 **절대 커밋하지 마세요**. `.githooks` 가
> 플레이스홀더와 사람 Git 식별자를 보호합니다.

## 05 / 크레딧

오픈소스 Hackintosh 생태계 위에서, 모두 공식 릴리스에서 받습니다:
[OpenCorePkg](https://github.com/acidanthera/OpenCorePkg) + Acidanthera kext ·
[itlwm / AirportItlwm](https://github.com/OpenIntelWireless/itlwm) +
[IntelBluetoothFirmware](https://github.com/OpenIntelWireless/IntelBluetoothFirmware) (OpenIntelWireless) ·
[RealtekRTL8111](https://github.com/Mieze/RTL8111_driver_for_OS_X) (Mieze) ·
[USBToolBox](https://github.com/USBToolBox/tool) · [GenSMBIOS](https://github.com/corpnewt/GenSMBIOS) (CorpNewt) ·
[Dortania](https://dortania.github.io/).

---

개인적으로 정제한 베이스라인이며 상호운용성과 교육 목적을 위해 **있는 그대로(as-is)** 제공됩니다.
Apple 소프트웨어나 서드파티 바이너리는 재배포하지 않습니다. 본인의 SMBIOS, 라이선스 준수, 비(非)Apple
하드웨어에서 macOS를 구동하는 위험은 사용자 책임입니다. Apple·Intel·Firebat 및 언급된 프로젝트와
제휴/보증 관계가 없습니다.
