#!/usr/bin/env python3
"""Rebuilds the checker plugin: re-bundles the two documents from the tool directory,
lints the PHP, runs the plugin's own test suite, and zips it for upload.

The bundling is the point. The plugin ships its own copies of embed.html and
carry-on-size-checker.html, so without this the zip silently goes stale the moment
the tool is edited. test-consistency.py asserts the two copies match.
"""
import hashlib
import pathlib
import shutil
import subprocess
import sys
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
TOOL = HERE.parent / 'tool'
PLUG = HERE / 'lft-checker-embed'
ZIP = HERE / 'lft-checker-embed.zip'

# published name in the plugin  <-  source in the tool directory
BUNDLE = {
    'embed.html': 'embed.html',
    'checker.html': 'carry-on-size-checker.html',
}

# Never ships: it redefines add_action() and friends, which would be dangerous
# inside a live plugin directory.
EXCLUDE = {'test-plugin.php'}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    fail = False

    for dest, src in BUNDLE.items():
        s, d = TOOL / src, PLUG / dest
        if not s.exists():
            print(f"  MISSING  {s}")
            fail = True
            continue
        if d.exists() and sha(s) == sha(d):
            print(f"  same     {dest}")
        else:
            shutil.copy2(s, d)
            print(f"  bundled  {dest}  <- {src}")
    if fail:
        return 1

    php = PLUG / 'lft-checker-embed.php'
    r = subprocess.run(['php', '-l', str(php)], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout + r.stderr)
        return 1
    print("  lint     clean")

    r = subprocess.run(['php', str(PLUG / 'test-plugin.php')], capture_output=True, text=True)
    print('  tests    ' + (r.stdout.strip().splitlines() or ['no output'])[-1])
    if r.returncode != 0:
        print(r.stdout + r.stderr)
        return 1

    ZIP.unlink(missing_ok=True)
    with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(PLUG.rglob('*')):
            if p.is_dir() or p.name in EXCLUDE:
                continue
            z.write(p, p.relative_to(PLUG.parent).as_posix())
    names = zipfile.ZipFile(ZIP).namelist()
    assert not any(n.endswith(tuple(EXCLUDE)) for n in names), "test file leaked into the zip"
    print(f"  zipped   {ZIP.name}  {ZIP.stat().st_size // 1024} KB, {len(names)} files")
    for n in names:
        print(f"             {n}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
