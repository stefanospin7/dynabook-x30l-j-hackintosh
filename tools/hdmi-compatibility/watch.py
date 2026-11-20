import plistlib
import re
import shlex
import subprocess
import tempfile
import time
from pathlib import Path

OVERRIDES = Path('/Library/Displays/Contents/Resources/Overrides')


def displays():
    registry = subprocess.check_output(
        ['/usr/sbin/ioreg', '-r', '-c', 'AppleDisplay', '-l', '-w0'], text=True
    )
    for match in re.finditer(r'"IODisplayEDID" = <([0-9a-f]+)>', registry):
        edid = bytes.fromhex(match[1])
        if len(edid) < 128 or edid[:8] != bytes.fromhex('00ffffffffffff00'):
            continue
        vendor = int.from_bytes(edid[8:10], 'big')
        product = int.from_bytes(edid[10:12], 'little')
        blocks = []
        for start in range(128, len(edid) - 127, 128):
            cta = edid[start:start + 128]
            if cta[0] != 2 or not 4 <= cta[2] <= 127 or sum(cta) % 256:
                continue
            index = 4
            while index < cta[2]:
                header = cta[index]
                end = index + 1 + (header & 31)
                if end > cta[2]:
                    break
                blocks.append((header >> 5, cta[index + 1:end]))
                index = end
        if sum(edid[:128]) % 256 == 0 and any(
            tag == 3 and block[:3] == b'\x03\x0c\x00' for tag, block in blocks
        ):
            yield vendor, product, edid, blocks


def make_override(vendor, product, edid, blocks):
    base = bytearray(edid[:128])
    base[20] = (base[20] & 0x8f) | 0x20
    base[24] = (base[24] & ~0x18) | 2
    base[35:38] = bytes(3)
    base[38:54] = bytes.fromhex('0101' * 8)
    base[54:72] = bytes.fromhex('023a801871382d40582c4500' + base[66:69].hex() + '00001e')
    for index in (72, 90, 108):
        item = base[index:index + 18]
        if item[:2] != bytes(2) or item[3] not in (0xfc, 0xff, 0xfe):
            base[index:index + 18] = bytes.fromhex('000000100000000000000000000000000000')
    vendor_block = next(block for tag, block in blocks if tag == 3 and block[:3] == b'\x03\x0c\x00')
    if len(vendor_block) < 5:
        raise ValueError('HDMI vendor block too short')
    video = bytes([0x41, 0x90, 0x67]) + vendor_block[:5] + bytes([0, 33])
    audio = b''.join(bytes([(tag << 5) | len(block)]) + block for tag, block in blocks if tag in (1, 4))
    payload = video + audio if len(video + audio) <= 123 else video
    cta = bytearray([2, 3, 4 + len(payload), 0x40 if audio and payload != video else 0]) + payload
    cta.extend(bytes(128 - len(cta)))
    for block in (base, cta):
        block[127] = -sum(block[:127]) & 255
    return plistlib.dumps(dict(DisplayVendorID=vendor, DisplayProductID=product, IODisplayEDID=bytes(base + cta)))


def ask_and_install(vendor, product, edid, blocks, target):
    name = next((edid[i + 5:i + 18].decode('ascii', 'replace').strip()
                 for i in (54, 72, 90, 108) if edid[i:i+5] == b'\0\0\0\xfc\0'),
                f'{vendor:04x}:{product:04x}')
    prompt = '''on run argv
display dialog ("Lo schermo " & item 1 of argv & " ha problemi di immagine? Puoi provare 1080p a 60 Hz senza HDR.") buttons {"Lascia com’è", "Prova 1080p"} default button 1 giving up after 30
return button returned of result
end run'''
    result = subprocess.run(['/usr/bin/osascript', '-e', prompt, name], capture_output=True, text=True)
    if result.stdout.strip() != 'Prova 1080p':
        return
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / 'override.plist'
        source.write_bytes(make_override(vendor, product, edid, blocks))
        quote = shlex.quote
        command = (
            f'test ! -e {quote(str(target))} && '
            f'/usr/bin/install -d -o root -g wheel -m 755 {quote(str(target.parent))} && '
            f'/usr/bin/install -o root -g wheel -m 644 {quote(str(source))} {quote(str(target))} && '
            f'/usr/bin/cmp {quote(str(source))} {quote(str(target))}'
        )
        subprocess.run(['/usr/bin/osascript', '-e', 'on run argv',
                        '-e', 'do shell script (item 1 of argv) with administrator privileges',
                        '-e', 'display notification "Scollega e ricollega il cavo HDMI." with title "Override HDMI installato"',
                        '-e', 'end run', command], check=True)


def watch():
    seen = set()
    while True:
        try:
            connected = {(v, p): (e, b) for v, p, e, b in displays()}
            for (v, p), (edid, blocks) in connected.items():
                target = OVERRIDES / f'DisplayVendorID-{v:x}' / f'DisplayProductID-{p:x}'
                if (v, p) not in seen and not target.exists():
                    seen.add((v, p))
                    try:
                        ask_and_install(v, p, edid, blocks, target)
                    except (ValueError, subprocess.SubprocessError) as error:
                        print(error, flush=True)
            seen.intersection_update(connected)
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            print(error, flush=True)
        time.sleep(4)


if __name__ == '__main__':
    watch()
