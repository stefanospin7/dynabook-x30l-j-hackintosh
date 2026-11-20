#!/bin/bash
set -euo pipefail

source_dir="$(cd "$(dirname "$0")" && pwd)"
label=local.hdmi.compatibility
domain="gui/$(id -u)"
folder="$HOME/Library/Application Support/HDMI Compatibility"
agent="$HOME/Library/LaunchAgents/$label.plist"

python="$(command -v python3)"
"$python" -c 'import sys; assert sys.version_info >= (3, 9), "Serve Python 3.9 o successivo"'
launchctl print "$domain" >/dev/null
mkdir -p "$folder" "$(dirname "$agent")"
if launchctl print "$domain/$label" >/dev/null 2>&1; then
    launchctl bootout "$domain/$label"
fi
install -m 644 "$source_dir/watch.py" "$folder/watch.py"
"$python" - "$agent" "$folder" "$python" "$label" <<'PY'
import plistlib
import sys
from pathlib import Path

agent, folder, python, label = sys.argv[1:]
Path(agent).write_bytes(plistlib.dumps({
    'Label': label,
    'ProgramArguments': [python, str(Path(folder) / 'watch.py')],
    'RunAtLoad': True,
    'KeepAlive': True,
    'LimitLoadToSessionType': 'Aqua',
    'StandardErrorPath': str(Path(folder) / 'error.log'),
}))
PY
plutil -lint "$agent"
launchctl bootstrap "$domain" "$agent"
