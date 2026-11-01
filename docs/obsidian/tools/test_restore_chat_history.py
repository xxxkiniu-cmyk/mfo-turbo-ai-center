"""Testy bezpieczeństwa odtworzenia, tylko syntetyczne pliki tymczasowe."""
import json
from pathlib import Path
import tempfile
import unittest
import restore_chat_history as repair


class RestoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source.json'
        self.pair = {'user': 'Syntetyczne pytanie', 'assistant': 'Syntetyczna odpowiedź'}
        self.source.write_text(json.dumps({'a': self.pair, 'b': self.pair, 'other': {'version': '1'}}))
        self.target = self.root / 'mem/chat_history'
        self.backup = self.root / 'backup'

    def test_restore_backup_dedup_and_unchanged_source(self):
        before = self.source.read_bytes()
        result = repair.restore(self.source, self.target, self.backup)
        self.assertEqual(result['records'], 1)
        self.assertEqual(self.source.read_bytes(), before)
        self.assertEqual((self.backup / 'source-before.json').read_bytes(), before)
        files = list(self.target.glob('*.json'))
        self.assertEqual(len(files), 1)
        self.assertEqual(json.loads(files[0].read_text()), self.pair)
        manifest = json.loads((self.backup / 'manifest.json').read_text())
        self.assertEqual(manifest['state'], 'verified')
        self.assertEqual(manifest['created'][0]['sha256'], repair.digest(files[0].read_bytes()))

    def test_existing_target_is_never_overwritten(self):
        self.target.mkdir(parents=True)
        original = self.target / 'existing.json'
        original.write_text('private sentinel')
        with self.assertRaises(ValueError):
            repair.restore(self.source, self.target, self.backup)
        self.assertEqual(original.read_text(), 'private sentinel')
        self.assertFalse(self.backup.exists())

    def test_symlink_source_and_parent_rejected(self):
        link = self.root / 'source-link.json'
        link.symlink_to(self.source)
        with self.assertRaises(ValueError):
            repair.restore(link, self.target, self.backup)
        real = self.root / 'real'
        real.mkdir()
        self.target.parent.symlink_to(real)
        with self.assertRaises(ValueError):
            repair.restore(self.source, self.target, self.backup)

    def test_invalid_source_does_not_create_target(self):
        self.source.write_text('{')
        with self.assertRaises(ValueError):
            repair.restore(self.source, self.target, self.backup)
        self.assertFalse(self.target.exists())
        self.assertFalse(self.backup.exists())

    def test_existing_backup_is_preserved(self):
        self.backup.mkdir()
        with self.assertRaises(ValueError):
            repair.restore(self.source, self.target, self.backup)
        self.assertFalse(self.target.exists())


if __name__ == '__main__':
    unittest.main()
