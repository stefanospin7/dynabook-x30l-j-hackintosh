# HDMI compatibility assistant for macOS

When macOS detects an external display with an HDMI EDID and no installed override, the assistant offers a compatibility mode of **1080p at 60 Hz, 8-bit RGB, without HDR**. This can help when a detected display shows distorted colors or no picture. macOS must be able to read the EDID. Results depend on the display and graphics driver.

## Install

With Python 3.9 or later available in Terminal, download or clone the repository, open its folder, and run:

```bash
bash tools/hdmi-compatibility/install.sh
```

Run it from your macOS user session without `sudo`. The assistant starts immediately and at subsequent logins. Its dialog is currently in Italian. **Lascia com’è** keeps the current settings and **Prova 1080p** tries the override. Only the second choice requests administrator authentication and writes an override for the display model. After installation, disconnect and reconnect HDMI. If macOS keeps the previous display mode, restart with the display connected.

## Uninstall

```bash
bash tools/hdmi-compatibility/uninstall.sh
```

This stops and removes the assistant. To undo an override for a particular display, remove its `DisplayProductID-…` file from the relevant `DisplayVendorID-…` directory under `/Library/Displays/Contents/Resources/Overrides/` and reconnect the display. The display identifiers are available from `ioreg -r -c AppleDisplay -l -w0` as `DisplayVendorID` and `DisplayProductID`. Convert those values to hexadecimal to identify the filenames.

The assistant was tested on the Dynabook with macOS Tahoe. The equivalent manually installed override restored 1080p/60 Hz output on a Hisense TV.
