---
status: "NIE DZIAŁA"
data_testu: "2026-10-31"
tags: [mfo, modul]
---
# RAG

**Stan: NIE DZIAŁA**, zakres: skonfigurowane źródło historii.

## Weryfikacja
Metoda: stat źródła mfo_memory.HISTORY_DIR, sprawdzenie mfo_rag.get_base_dir i rzeczywisty retrieve z pytaniem syntetycznym przy nieistniejącym źródle.
Wynik: /mnt/e/ai_memory/mem/chat_history nie istnieje (ENOENT), baza mfo_rag również niedostępna, retrieve zwrócił pustą listę. Nie odczytano prywatnych rozmów. Testy jednostkowe memory_rag: 20/20 PASS na danych syntetycznych, co nie naprawia braku produkcyjnego źródła.
Czas pomiarów: 14:45 do 14:46 UTC.

## Powiązania
- [[Pamiec AI]]
- [[Historia JSON]]
- [[Panel MFO]]
