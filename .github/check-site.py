"""Pre-merge checks for the site: renders the ConfigMap like Flux does and
checks size, completeness and the syntax of the inline scripts."""
import os
import re
import subprocess
import sys
import tempfile

LIMIT = 900 * 1024  # ConfigMaps are capped at 1 MiB; keep some headroom

errors = []

rendered = subprocess.run(
    ["kubectl", "kustomize", "."], capture_output=True, text=True, check=True
).stdout
# Keys of the generated ConfigMap: two-space indented entries under data/binaryData.
keys = set()
section = None
for line in rendered.splitlines():
    if not line.strip():
        continue
    if not line.startswith(" "):
        section = line.rstrip(":")
    elif section in ("data", "binaryData") and re.match(r"^  \S", line):
        keys.add(line.strip().split(":", 1)[0])
size = len(rendered.encode())
print(f"ConfigMap: {len(keys)} files, {size // 1024} KiB")
if size > LIMIT:
    errors.append(f"ConfigMap is {size // 1024} KiB, limit is {LIMIT // 1024} KiB")

# Every file under site/ must end up in the ConfigMap.
for root, _, files in os.walk("site"):
    for name in files:
        if name not in keys:
            errors.append(f"{os.path.join(root, name)} is not listed in kustomization.yaml")

for page in ("index.html", "404.html"):
    if page not in keys:
        errors.append(f"{page} missing from the ConfigMap")

# Inline scripts must parse.
for path in ("site/index.html", "site/404.html"):
    html = open(path, encoding="utf-8").read()
    scripts = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.S)
    for i, js in enumerate(scripts):
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
            f.write(js)
        result = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
        status = "ok" if result.returncode == 0 else "FAILED"
        print(f"{path} script {i}: {status}")
        if result.returncode != 0:
            errors.append(f"{path} script {i}: {result.stderr.strip()}")

for e in errors:
    print(f"ERROR: {e}")
sys.exit(1 if errors else 0)
