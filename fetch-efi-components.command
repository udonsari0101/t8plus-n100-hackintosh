#!/bin/bash
# Fetch the OpenCore + kext components listed in components.lock.json into EFI/OC/...
# Third-party binaries are NOT redistributed in this repo; this downloads them from their
# official releases. Needs: curl, unzip, (python3 or python), shasum.
set -euo pipefail
here=$(cd -- "$(dirname -- "$0")" && pwd -P)
cd "$here"
command -v curl  >/dev/null || { echo "ERROR: curl required";  exit 1; }
command -v unzip >/dev/null || { echo "ERROR: unzip required"; exit 1; }
py=python3; command -v "$py" >/dev/null 2>&1 || py=python
command -v "$py" >/dev/null 2>&1 || { echo "ERROR: python3 required"; exit 1; }
[ -f components.lock.json ] || { echo "ERROR: run from the repo root (components.lock.json not found)"; exit 1; }

tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
"$py" - components.lock.json > "$tmp/plan.tsv" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
for c in d["components"]:
    f = c.get("fetch", {})
    print("\t".join([c["name"], c.get("version",""), f.get("type","manual"),
                     f.get("url",""), f.get("extract",""), c["dest"], c.get("note","")]))
PY

manual=0
while IFS=$'\t' read -r name version ftype url extract dest note; do
  case "$ftype" in
    github-release-zip|url-zip)
      echo ">> $name $version  ->  $dest"
      curl -fL --retry 3 "$url" -o "$tmp/pkg.zip" || { echo "   !! download failed: $url (fetch manually)"; manual=$((manual+1)); continue; }
      rm -rf "$tmp/x"; mkdir -p "$tmp/x"; unzip -qo "$tmp/pkg.zip" -d "$tmp/x"
      src=$(find "$tmp/x" -maxdepth 6 -path "*$extract" -print -quit || true)
      [ -n "$src" ] || { echo "   !! '$extract' not found in zip; fetch manually from $url"; manual=$((manual+1)); continue; }
      mkdir -p "$(dirname "$dest")"; rm -rf "$dest"; cp -R "$src" "$dest"
      ;;
    raw)
      echo ">> $name  ->  $dest"
      mkdir -p "$(dirname "$dest")"
      curl -fL --retry 3 "$url" -o "$dest" || { echo "   !! download failed: $url"; manual=$((manual+1)); }
      ;;
    *)
      echo ">> MANUAL  $name $version  ->  $dest"
      echo "     $note"
      manual=$((manual+1))
      ;;
  esac
done < "$tmp/plan.tsv"

echo "----"
echo "Automated components fetched. Manual components remaining: $manual (see notes above)."
echo "Next: cp EFI/OC/config.template.plist EFI/OC/config.plist ; fill in YOUR SMBIOS + USB map ; ocvalidate EFI/OC/config.plist"
