# Dynabook Portégé X30L-J con macOS Tahoe

Configurazione OpenCore per il Portégé X30L‑J **PCR10E‑208**, con **Core i5‑1135G7**, **Intel Iris Xe 8086:9a49** e **BIOS 8.60**. Provata con **macOS Tahoe 26.7.2 (25G332)** e **OpenCore 1.0.8**.

## Cosa funziona sul portatile provato

| Funzione | Esito e soluzione |
| --- | --- |
| Avvio via USB | Verificato con Crucial P3 CT500P3SSD8 da 500 GB in box USB. OpenCore risiede nella partizione EFI del Crucial. |
| Avvio NVMe interno | Verificato spostando lo stesso Crucial nello slot M.2 e rimuovendo l’esclusione NVMe. L’installazione APFS è stata riutilizzata. |
| Grafica e luminosità | Iris Xe con Metal 2 mediante WhateverXe 0.8.3 e WhateverXe Graphics 0.4.4. SSDT-PNLF con _UID 19 abilita il profilo di luminosità. SSDT-BRKD e BrightnessKeys 1.0.3 abilitano Fn+F6 e Fn+F7. |
| Tastiera e retroilluminazione | VoodooPS2 2.3.7 per la tastiera. SSDT-KBLD ripristina Fn+Z tramite il metodo Dynabook SKBL. |
| Trackpad | Movimento e tocco funzionano con VoodooI2C e VoodooI2CHID. SSDT-TPOS e SSDT-TPST espongono le risorse e il dispositivo I²C del firmware. |
| Wi‑Fi | AX201 con itlwm 2.3.0 e HeliPort 1.5.0. |
| Bluetooth | AX201 USB 8087:0026 con IntelBluetoothFirmware e IntelBTPatcher 2.5.3 più BlueToolFixup 2.7.2. Riconnessione a volte intermittente. |
| Audio | Realtek ALC257 con VoodooHDA_BL 3.7.1. macOS espone gli altoparlanti e il jack cuffie. |
| Batteria | Percentuale e ricarica rilevate con SMCBatteryManager 1.3.8. |
| MicroSD | Realtek RTS522A con RealtekCardReader 0.9.8. |
| USB e webcam | Due porte verificate a 10 Gbit/s con lo stesso box USB. Webcam provata nell’uso normale. |

**Limiti osservati.** AccuPoint e pulsanti fisici sopra il trackpad restano inattivi. La prova con VoodooRMI 1.4.3 ha interrotto anche il movimento, poi ripristinato con VoodooI2CHID. Dopo una sospensione prolungata, a volte macOS risponde con lo schermo interno ed HDMI neri. L’HDMI può richiedere una modalità compatibile a seconda del display.

## Quale profilo usare

- **[NVMe interno](profiles/nvme-interno.plist)** per macOS sul Crucial nello slot M.2. È adatto anche come punto di partenza per USB se il disco interno non causa problemi.
- **[USB con esclusione NVMe](profiles/usb-con-esclusione-nvme.plist)** per macOS sul Crucial esterno quando l’NVMe interno provoca errori AppleNVMe all’avvio. Sul modello provato il Samsung interno con Ubuntu era sul percorso PCIe PciRoot(0x0)/Pci(0x1D,0x0)/Pci(0x0,0x0). Il profilo imposta su quel percorso class-code con dati esadecimali FF080100. L’esclusione segue lo slot. Verifica il percorso sul tuo esemplare e usa il profilo interno prima di spostarvi il disco macOS.

I due profili derivano dalla stessa configurazione aggiornata. L’avvio interno è stato verificato con questa configurazione. Il profilo USB è stato ricostruito riapplicando alla configurazione aggiornata l’esclusione già usata durante le prove USB.

## Montare la propria EFI

1. Parti dall’archivio ufficiale OpenCore 1.0.8 e conserva la struttura EFI con BOOTx64.efi, OpenCore.efi e OpenRuntime.efi. Aggiungi HfsPlus.efi e le SSDT della cartella [ACPI](ACPI/).
2. Aggiungi i kext delle versioni elencate qui sotto. Il profilo contiene i percorsi esatti dei bundle e dei plugin. Copia il profilo scelto come EFI/OC/config.plist.
3. Compila PlatformInfo → Generic con identificativi propri per **MacBookPro16,2**. SystemSerialNumber, MLB, SystemUUID e ROM sono segnaposto senza identificativi macchina. [Guida a PlatformInfo](https://dortania.github.io/OpenCore-Install-Guide/config-laptop.plist/ice-lake.html#platforminfo)
4. Valida config.plist con ocvalidate 1.0.8. Prova prima l’EFI su una chiavetta con una copia di recupero disponibile. Dopo l’installazione, copia la cartella EFI funzionante sulla partizione EFI del disco macOS e selezionala dal menu F12 del Dynabook.
5. Installa WhateverXe Graphics da macOS dopo aver avviato con WhateverXe e AMFIAnchor attivi. HeliPort si installa separatamente per il Wi‑Fi.

Le patch EC e del trackpad usano firme AML del firmware provato. Su altre varianti o versioni BIOS verifica che le firme corrispondano al tuo DSDT. Il menu OpenCore attende una scelta e l’avvio è senza verbose.

## Componenti da scaricare

- [OpenCore 1.0.8](https://github.com/acidanthera/OpenCorePkg/releases/tag/1.0.8) e [HfsPlus.efi](https://github.com/acidanthera/OcBinaryData/tree/master/Drivers).
- [Lilu 1.7.2](https://github.com/acidanthera/Lilu/releases/tag/1.7.2), [VirtualSMC e SMCBatteryManager 1.3.8](https://github.com/acidanthera/VirtualSMC/releases/tag/1.3.8), [IntelMausi 1.0.8](https://github.com/acidanthera/IntelMausi/releases/tag/1.0.8), [VoodooPS2 2.3.7](https://github.com/acidanthera/VoodooPS2/releases/tag/2.3.7), [BrightnessKeys 1.0.3](https://github.com/acidanthera/BrightnessKeys/releases/tag/1.0.3).
- [WhateverXe 0.8.3](https://github.com/b00t0x/WhateverXe/releases/tag/0.8.3), [WhateverXe Graphics 0.4.4](https://github.com/b00t0x/WhateverXe-Graphics/releases/tag/v0.4.4), [AMFIAnchor 0.1.2 e istruzioni per AMFIAnchorInjector](https://github.com/b00t0x/AMFIAnchor).
- [VoodooI2C e VoodooI2CHID](https://github.com/VoodooI2C/VoodooI2C/actions/runs/44008802131), build 2.9.1 dal commit 927797d4 con supporto per il controller Tiger Lake 8086:a0e8. La release 2.9.1 con lo stesso numero di versione è priva di quel match PCI.
- [itlwm 2.3.0](https://github.com/OpenIntelWireless/itlwm/releases/tag/v2.3.0), [HeliPort 1.5.0](https://github.com/OpenIntelWireless/HeliPort/releases/tag/v1.5.0), [driver Bluetooth Intel 2.5.3](https://github.com/lshbluesky/IntelBluetoothFirmware/releases/tag/v2.5.3) e [BlueToolFixup 2.7.2](https://github.com/acidanthera/BrcmPatchRAM/releases/tag/2.7.2).
- [VoodooHDA_BL 3.7.1 alpha](https://github.com/CloverHackyColor/VoodooHDA/releases/tag/v3.7.1-alpha) e [RealtekCardReader 0.9.8](https://github.com/0xFireWolf/RealtekCardReader/releases/tag/v0.9.8).

## Assistente HDMI per macOS

L’[assistente compatibilità HDMI](tools/hdmi-compatibility/README.md) è opzionale e si installa separatamente dall’EFI. Al collegamento di uno schermo riconosciuto può proporre un override **1080p a 60 Hz, SDR**. Su una TV Hisense l’override ha ripristinato l’immagine a 1080p/60 Hz. Sul Samsung LU28R55 i colori sono tornati normali dopo aver ricollegato l’HDMI, con il segnale ancora a 4K/30 Hz. L’effetto specifico dell’override sul Samsung non è stato isolato.
