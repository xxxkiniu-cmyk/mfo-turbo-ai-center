#!/usr/bin/env python3
"""Odtwórz wyłącznie kompletne rekordy user/assistant do nowego katalogu.
Nie nadpisuje plików, nie usuwa źródła, nie drukuje treści rozmów.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import datetime


def digest(data):
    return hashlib.sha256(data).hexdigest()


def plan(source):
    if source.stat().st_size > 16 * 1024 * 1024:
        raise ValueError('Źródło przekracza limit')
    raw = source.read_bytes()
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError('Nieobsługiwany schemat źródła')
    records = {}
    for item in data.values():
        if not isinstance(item, dict):
            continue
        if not all(isinstance(item.get(k), str) and item[k].strip()
                   for k in ('user', 'assistant')):
            continue
        encoded = (json.dumps(item, ensure_ascii=False, sort_keys=True) + '\n').encode()
        records['restored-' + digest(encoded) + '.json'] = encoded
    if not records:
        raise ValueError('Brak kompletnych par rozmów')
    return raw, records


def restore(source, target, backup):
    # Ścieżka docelowa ma być nowa, nie zastępuj istniejącego magazynu.
    if source.is_symlink() or target.exists() or target.is_symlink():
        raise ValueError('Źródło jest dowiązaniem lub cel już istnieje')
    if target.parent.is_symlink() or target.parent.parent.is_symlink():
        raise ValueError('Rodzic celu jest dowiązaniem')
    if backup.exists():
        raise ValueError('Katalog kopii już istnieje')
    raw, records = plan(source)
    backup.mkdir(mode=0o700, parents=True)
    (backup / 'source-before.json').write_bytes(raw)
    manifest = {'date': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'source_sha256': digest(raw), 'target': str(target),
                'created': [], 'state': 'prepared'}
    manifest_path = backup / 'manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2))
    target.mkdir(parents=True, exist_ok=False)
    try:
        for name, encoded in records.items():
            destination = target / name
            with destination.open('xb') as stream:
                stream.write(encoded)
                stream.flush()
                os.fsync(stream.fileno())
            manifest['created'].append({'name': name, 'sha256': digest(encoded)})
            manifest_path.write_text(json.dumps(manifest, indent=2))
            if destination.read_bytes() != encoded:
                raise ValueError('Błąd weryfikacji zapisanej kopii')
        if source.read_bytes() != raw:
            raise ValueError('Źródło zmieniło się w trakcie operacji')
        manifest['state'] = 'verified'
        manifest_path.write_text(json.dumps(manifest, indent=2))
    except Exception:
        manifest['state'] = 'partial_no_data_deleted'
        manifest_path.write_text(json.dumps(manifest, indent=2))
        raise
    return {'records': len(records), 'source_unchanged': True,
            'exclusive_create': True, 'state': 'verified'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path,
                        default=Path('/mnt/e/ai_memory/current/mem/merged_long_term_memory.json'))
    parser.add_argument('--target', type=Path,
                        default=Path('/mnt/e/ai_memory/mem/chat_history'))
    parser.add_argument('--backup', type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    if args.apply:
        if not os.path.ismount('/mnt/e'):
            raise SystemExit('Dysk E nie jest zamontowany')
        if args.backup is None:
            raise SystemExit('Wymagana jawna prywatna ścieżka kopii')
        result = restore(args.source, args.target, args.backup)
    else:
        _, records = plan(args.source)
        result = {'eligible_records': len(records), 'changed': False}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
