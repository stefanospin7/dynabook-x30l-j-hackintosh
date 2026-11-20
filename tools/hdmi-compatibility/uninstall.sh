#!/bin/bash
set -euo pipefail

label=local.hdmi.compatibility
service="gui/$(id -u)/$label"
folder="$HOME/Library/Application Support/HDMI Compatibility"
if launchctl print "$service" >/dev/null 2>&1; then
    launchctl bootout "$service"
fi
rm -f "$HOME/Library/LaunchAgents/$label.plist" "$folder/watch.py" "$folder/error.log"
if [ -d "$folder" ]; then
    rmdir "$folder" 2>/dev/null || true
fi
