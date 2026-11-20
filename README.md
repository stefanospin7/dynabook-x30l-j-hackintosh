# Dynabook Portégé X30L-J Hackintosh on macOS Tahoe

OpenCore configuration for the Portégé X30L-J **PCR10E-208** with a **Core i5-1135G7**, **Intel Iris Xe 8086:9a49**, and **BIOS 8.60**. Tested with **macOS Tahoe 26.7.2 (25G332)** and **OpenCore 1.0.8**.

## Tested features and fixes

| Feature | Result and configuration |
| --- | --- |
| USB boot | Tested with a 500 GB Crucial P3 CT500P3SSD8 in a USB enclosure. OpenCore was installed on the Crucial’s EFI System Partition. |
| Internal NVMe boot | Tested by moving the same Crucial into the M.2 slot and removing the NVMe exclusion. The existing APFS installation booted from the internal slot. |
| Graphics and display brightness | Iris Xe with Metal 2 using WhateverXe 0.8.3 and WhateverXe Graphics 0.4.4. SSDT-PNLF uses `_UID=19` for the brightness profile. SSDT-BRKD and BrightnessKeys 1.0.3 enable Fn+F6 and Fn+F7. |
| Keyboard and keyboard backlight | VoodooPS2 2.3.7 drives the keyboard. SSDT-KBLD restores Fn+Z through Dynabook’s `SKBL` firmware method. |
| Trackpad | Pointer movement and tap-to-click work through VoodooI2C and VoodooI2CHID. SSDT-TPOS and SSDT-TPST expose the I²C resources and trackpad device. |
| Wi-Fi | Intel AX201 using itlwm 2.3.0 and HeliPort 1.5.0. |
| Bluetooth | Intel AX201 Bluetooth over USB (8087:0026) using IntelBluetoothFirmware and IntelBTPatcher 2.5.3 with BlueToolFixup 2.7.2. Reconnection is sometimes intermittent. |
| Audio | Realtek ALC257 with VoodooHDA_BL 3.7.1. macOS exposes both internal speakers and the headphone jack. |
| Battery | SMCBatteryManager 1.3.8 reports battery percentage and charging status. |
| MicroSD | Realtek RTS522A using RealtekCardReader 0.9.8. |
| USB and webcam | Two ports negotiated 10 Gbit/s with the same USB enclosure. The webcam worked in normal use. |

**Known issues.** The AccuPoint and the physical buttons above the trackpad remain inactive. Testing VoodooRMI 1.4.3 also broke pointer movement. Restoring VoodooI2CHID brought it back. After prolonged sleep, macOS sometimes responds while the internal panel and HDMI both stay black. Some HDMI displays need a compatibility mode.

## Choose a profile

- **[Internal NVMe](profiles/nvme-interno.plist)** for macOS on the Crucial in the M.2 slot. It can also be used as a starting point for USB boot if the internal drive causes no problems.
- **[USB boot with NVMe exclusion](profiles/usb-con-esclusione-nvme.plist)** for macOS on an external USB SSD when the internal NVMe causes AppleNVMe errors during boot. The tested Samsung drive with Ubuntu occupied `PciRoot(0x0)/Pci(0x1D,0x0)/Pci(0x0,0x0)`. This profile sets `class-code` to hex data `FF080100` at that path. The exclusion follows the slot. Check the PCI path on your machine and switch to the internal profile before moving macOS into that slot.

Both profiles use the same updated configuration. The internal configuration was tested on the laptop. The USB profile was rebuilt by applying the exclusion used in the original USB boot tests to the updated configuration.

## Build your EFI

1. Start with the official OpenCore 1.0.8 archive and retain the EFI layout for `BOOTx64.efi`, `OpenCore.efi`, and `OpenRuntime.efi`. Add `HfsPlus.efi` and the SSDTs in [ACPI](ACPI/).
2. Add the kext versions listed below. The profile lists the exact bundle and plug-in paths. Copy your chosen profile to `EFI/OC/config.plist`.
3. Generate your own identifiers for **MacBookPro16,2** and enter them under `PlatformInfo → Generic`. `SystemSerialNumber`, `MLB`, `SystemUUID`, and `ROM` are placeholders. [PlatformInfo guide](https://dortania.github.io/OpenCore-Install-Guide/config-laptop.plist/ice-lake.html#platforminfo)
4. Validate the configuration with `ocvalidate` 1.0.8. Test the EFI from a USB stick first and keep a recovery copy. After installation, copy the working EFI folder to the macOS drive’s EFI System Partition and select it from the Dynabook’s F12 boot menu.
5. Boot with WhateverXe and AMFIAnchor enabled, then install WhateverXe Graphics from macOS. Install HeliPort separately for Wi-Fi.

The embedded controller and trackpad patches use AML signatures from the tested firmware. On a different BIOS version or hardware variant, verify the signatures against your own DSDT. The OpenCore picker waits for a selection and verbose boot is disabled.

## Component downloads

- [OpenCore 1.0.8](https://github.com/acidanthera/OpenCorePkg/releases/tag/1.0.8) and [HfsPlus.efi](https://github.com/acidanthera/OcBinaryData/tree/master/Drivers).
- [Lilu 1.7.2](https://github.com/acidanthera/Lilu/releases/tag/1.7.2), [VirtualSMC and SMCBatteryManager 1.3.8](https://github.com/acidanthera/VirtualSMC/releases/tag/1.3.8), [IntelMausi 1.0.8](https://github.com/acidanthera/IntelMausi/releases/tag/1.0.8), [VoodooPS2 2.3.7](https://github.com/acidanthera/VoodooPS2/releases/tag/2.3.7), [BrightnessKeys 1.0.3](https://github.com/acidanthera/BrightnessKeys/releases/tag/1.0.3).
- [WhateverXe 0.8.3](https://github.com/b00t0x/WhateverXe/releases/tag/0.8.3), [WhateverXe Graphics 0.4.4](https://github.com/b00t0x/WhateverXe-Graphics/releases/tag/v0.4.4), [AMFIAnchor 0.1.2 and AMFIAnchorInjector instructions](https://github.com/b00t0x/AMFIAnchor).
- [VoodooI2C and VoodooI2CHID](https://github.com/VoodooI2C/VoodooI2C/actions/runs/44008802131), version 2.9.1 built from commit 927797d4, which supports the Tiger Lake 8086:a0e8 controller. The standard 2.9.1 release does not match that PCI ID.
- [itlwm 2.3.0](https://github.com/OpenIntelWireless/itlwm/releases/tag/v2.3.0), [HeliPort 1.5.0](https://github.com/OpenIntelWireless/HeliPort/releases/tag/v1.5.0), [Intel Bluetooth drivers 2.5.3](https://github.com/lshbluesky/IntelBluetoothFirmware/releases/tag/v2.5.3) and [BlueToolFixup 2.7.2](https://github.com/acidanthera/BrcmPatchRAM/releases/tag/2.7.2).
- [VoodooHDA_BL 3.7.1 alpha](https://github.com/CloverHackyColor/VoodooHDA/releases/tag/v3.7.1-alpha) and [RealtekCardReader 0.9.8](https://github.com/0xFireWolf/RealtekCardReader/releases/tag/v0.9.8).

## HDMI compatibility assistant

The optional [HDMI compatibility assistant](tools/hdmi-compatibility/README.md) installs separately from OpenCore. On connection of a recognized display it can offer a **1080p at 60 Hz SDR** override. An override restored output on a Hisense TV at 1080p/60 Hz. On a Samsung LU28R55, colors returned to normal after reconnecting HDMI and the signal stayed at 4K/30 Hz. The effect of the override on the Samsung was not isolated.
