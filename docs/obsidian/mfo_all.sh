#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
PROJECT="${MFO_PROJECT:-$HOME/mfo/mfo-turbo-ai-center}"
ROOT="${MFO_VAULT_ROOT:-/mnt/e/MFO_TURBO_AI_CENTER_OBSIDIAN}"
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="$ROOT/$STAMP"
if ! mountpoint -q /mnt/e; then echo 'BLAD: dysk E: nie jest zamontowany'; exit 1; fi
if [[ ! -d "$PROJECT" ]]; then echo "BLAD: nie znaleziono projektu: $PROJECT"; exit 1; fi
mkdir -p "$ROOT"
mkdir "$OUT"
mkdir "$OUT/Moduly" "$OUT/Dowody"
LOG="$OUT/Dowody/audyt.txt"
exec > >(tee -a "$LOG") 2>&1
printf 'MFO VAULT BUILD %s\nPROJECT=%s\nVAULT=%s\n' "$STAMP" "$PROJECT" "$OUT"
probe_url() { curl --noproxy '*' -fsS --connect-timeout 2 --max-time 5 "$1" >/dev/null 2>&1; }
probe_pm2() {
  command -v pm2 >/dev/null || return 1
  [[ -S "$HOME/.pm2/rpc.sock" ]] || return 1
  pm2 jlist 2>/dev/null | python3 -c '
import json,sys
try:
 a=json.load(sys.stdin)
 sys.exit(0 if any(x.get("pm2_env",{}).get("status")=="online" and any(w in str(x.get("name","")).lower() for w in ("antigravity","whatsapp")) for x in a) else 1)
except Exception:
 sys.exit(1)
'
}
STATUS_PANEL=NIEZWERYFIKOWANY
STATUS_MODEL=NIEZWERYFIKOWANY
STATUS_BOT=NIEZWERYFIKOWANY
STATUS_RAG=NIEZWERYFIKOWANY
STATUS_DISK=NIEZWERYFIKOWANY
if probe_url http://127.0.0.1:8082/api/health; then STATUS_PANEL=ODPOWIADA; fi
if probe_url http://127.0.0.1:1234/v1/models || probe_url http://127.0.0.1:8080/v1/models; then STATUS_MODEL=ODPOWIADA; fi
if probe_pm2; then STATUS_BOT=PM2_ONLINE_NIEZWERYFIKOWANY_FUNKCJONALNIE; fi
if [[ -d /mnt/e/ai_memory && -r /mnt/e/ai_memory ]]; then STATUS_DISK=DOSTEPNY; fi
if [[ -f "$PROJECT/mfo_rag.py" ]]; then STATUS_RAG=KOD_OBECNY_NIEZWERYFIKOWANY_FUNKCJONALNIE; fi
write_note() {
 local name="$1" status="$2" desc="$3" links="$4"
 cat > "$OUT/Moduly/$name.md" <<EOF
# $name

**Stan:** $status

$desc

## Powiązania
$links

## Uwaga
Stan jest pomiarem punktowym. Nie oznacza potwierdzenia wszystkich funkcji.
EOF
}
write_note 'Windows 11' NIEZWERYFIKOWANY 'System hostujący WSL.' '[[WSL Ubuntu]]'
write_note 'WSL Ubuntu' DZIALA 'Środowisko wykonania skryptu.' '[[Windows 11]] · [[Panel MFO]] · [[Modele AI]] · [[PM2 WhatsApp]] · [[Pamiec AI]]'
write_note 'Panel MFO' "$STATUS_PANEL" 'HTTP GET /api/health na porcie 8082.' '[[WSL Ubuntu]] · [[Modele AI]] · [[Pamiec AI]]'
write_note 'Modele AI' "$STATUS_MODEL" 'Sprawdzenie /v1/models na portach 1234 i 8080.' '[[WSL Ubuntu]] · [[Panel MFO]] · [[JCODE]]'
write_note 'PM2 WhatsApp' "$STATUS_BOT" 'Status PM2 nie dowodzi odpowiedzi na wiadomość.' '[[WSL Ubuntu]] · [[Panel MFO]]'
write_note 'Pamiec AI' "$STATUS_DISK" 'Katalog /mnt/e/ai_memory.' '[[WSL Ubuntu]] · [[RAG]] · [[Panel MFO]]'
write_note 'RAG' "$STATUS_RAG" 'Wykrywanie obecności mfo_rag.py.' '[[Pamiec AI]] · [[Modele AI]]'
write_note 'JCODE' NIEZWERYFIKOWANY 'Agent kodujący. Stan wymaga osobnego testu.' '[[Modele AI]] · [[WSL Ubuntu]]'
cat > "$OUT/START.md" <<'EOF'
# MFO TURBO AI CENTER — mapa systemu

Otwórz ten katalog jako skarbiec Obsidian, następnie wybierz widok grafu.

## Moduły
- [[Windows 11]]
- [[WSL Ubuntu]]
- [[Panel MFO]]
- [[Modele AI]]
- [[PM2 WhatsApp]]
- [[Pamiec AI]]
- [[RAG]]
- [[JCODE]]

## Znaczenie statusów
- ODPOWIADA: punkt HTTP zwrócił sukces.
- DOSTEPNY: katalog istnieje i jest czytelny.
- NIEZWERYFIKOWANY: brak wystarczających dowodów.

## Bezpieczeństwo
Skrypt nie restartuje usług, nie zmienia autostartu i nie usuwa danych.
Powiązania oznaczają relacje opisowe, nie dowód bezpośredniego wywołania API.
EOF
python3 - "$OUT" <<'PY'
import pathlib,re,sys
root=pathlib.Path(sys.argv[1]);files=list(root.rglob('*.md'))
names={p.stem for p in files};broken=[];edges=0
for p in files:
 for target in re.findall(r'\[\[([^\]|#]+)',p.read_text(encoding='utf-8')):
  edges+=1
  if target not in names:broken.append((p.name,target))
print('NOTATKI=',len(files),'POLACZENIA=',edges,'BLEDNE_LINKI=',len(broken))
for a,b in broken:print('BLAD_LINKU',a,b)
if len(files)<9 or edges<8 or broken:sys.exit(2)
PY
printf 'WYNIK_TESTU_GRAFU=OK\nSKARBIEC=%s\n' "$OUT"
if command -v powershell.exe >/dev/null; then echo WINDOWS_POWERSHELL=DOSTEPNY; else echo WINDOWS_POWERSHELL=NIEDOSTEPNY; fi
echo WYNIK_OTWARCIA=NIEZWERYFIKOWANY
echo MFO_VAULT_BUILD=ZAKONCZONY
