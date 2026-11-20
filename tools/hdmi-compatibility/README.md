# Assistente compatibilità HDMI per macOS

Quando macOS rileva uno schermo esterno con EDID HDMI e senza override già installato, l’assistente propone una modalità di compatibilità **1080p a 60 Hz, RGB a 8 bit, senza HDR**. Serve per schermi che vengono rilevati ma mostrano colori alterati o nessuna immagine. macOS deve riuscire a leggere l’EDID. Il risultato dipende da schermo e driver.

## Installazione

Con Python 3.9 o successivo disponibile in Terminale, scarica o clona il repository, entra nella sua cartella ed esegui:

```bash
bash tools/hdmi-compatibility/install.sh
```

Esegui il comando dalla tua sessione macOS, senza `sudo`. L’assistente parte subito e ai login successivi. La finestra offre **Lascia com’è** e **Prova 1080p**. Solo la seconda scelta richiede l’autenticazione di amministratore e salva un override per il modello di schermo. Dopo l’installazione, scollega e ricollega il cavo. Se macOS mantiene la modalità precedente, riavvia con lo schermo collegato.

## Rimozione

```bash
bash tools/hdmi-compatibility/uninstall.sh
```

Il comando disattiva l’assistente. Per annullare una prova su uno schermo, rimuovi il relativo file `DisplayProductID-…` dalla sottocartella `DisplayVendorID-…` in `/Library/Displays/Contents/Resources/Overrides/` e ricollegalo. Gli identificativi esadecimali si ricavano dai valori `DisplayVendorID` e `DisplayProductID` di `ioreg -r -c AppleDisplay -l -w0`.

Provato sul Dynabook con Tahoe. Sulla TV Hisense l’override manuale equivalente ha ripristinato l’immagine a 1080p/60 Hz.
