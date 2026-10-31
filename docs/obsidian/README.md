# MFO TURBO AI CENTER: skarbiec wizualizacji

30 modułów, źródła dowodów i jawne ograniczenia testów. Bieżąca weryfikacja: [[Raport_weryfikacji_20261031]], 17 modułów działa w opisanym zakresie, 2 nie działają, 11 pozostaje niezweryfikowanych. Potwierdzono brak źródła historii/RAG oraz ryzyko odtworzenia Flask. To dokumentacja, nie instalator usług MFO. Na nowym komputerze statusy są historyczną migawką z 31 października 2026, nie wynikiem testów nowego hosta.

## Otwieranie
1. Otwórz ten folder jako istniejący skarbiec Obsidiana.
2. Otwórz START.md, następnie Architektura.md w trybie odczytu.
3. Otwórz wbudowany Widok grafu, filtr `path:Moduly`. Bez dodatków społeczności.
4. Każda notatka modułu podaje status, zakres sprawdzenia i źródło dowodu. Powiązania opisowe nie oznaczają zawsze bezpośredniego wywołania API.

## Odtworzenie z Git na nowym komputerze
Repozytorium docelowe: `xxxkiniu-cmyk/mfo-turbo-ai-center`. Dokumentacja znajduje się w osobnym katalogu `docs/obsidian/`.

```bash
git clone https://github.com/xxxkiniu-cmyk/mfo-turbo-ai-center.git mfo-mapa
cd mfo-mapa/docs/obsidian
python3 tools/verify_vault.py .
```

Otwórz folder `mfo-mapa/docs/obsidian` w Obsidianie. Nie kopiuj starych workspace.json. Nie potrzebujesz modeli, sekretów, konta Sync ani serwera MFO, aby przeglądać notatki i graf. Na Windows użyj dostępnego Python 3 do testu lub zweryfikuj notatki bezpośrednio w Obsidianie.

Repozytorium jest publiczne. Publikowana paczka nie zawiera lokalnych dowodów, historii rozmów ani poświadczeń. Statusy modułów pozostają historyczną migawką, a nie testem funkcjonalnym integracji GitHub.

## Źródła i narzędzia
- Moduly/*.md: źródłowe notatki i powiązania.
- START.md: nawigacja.
- Architektura.md: dwa źródłowe diagramy Mermaid.
- mfo_all.sh: pierwotny generator uproszczonej mapy. Tworzy nowy katalog z datą i nie odtwarza samodzielnie pełnej rozbudowanej mapy. Nie uruchamiaj go do zwykłego odtworzenia tego skarbca.
- SKILL.md: reguły bezpiecznej aktualizacji.
- tools/verify_vault.py: kontrola łączy, statusów i wzorców sekretów w plikach Git.
- .obsidian/app.json, appearance.json, graph.json i core-plugins.json: bezpieczne ustawienia bez historii okien i dodatków społeczności.

## Prywatność i ograniczenia
Dowody/ jest lokalne i wykluczone z Git: zawiera logi wykonania i zrzuty ekranu. Nie publikujemy instalatora, GGUF, dump.pm2, .env, haseł, tokenów, sesji, historii rozmów ani prywatnych kopii konfiguracji.
Skan wzorców nie jest matematyczną gwarancją braku sekretów. Przed publikacją obowiązuje jawna lista plików i przegląd ich treści.
Nie przetestowano funkcjonalnie wiadomości WhatsApp/Telegram, mikrofonu, inferencji, odtworzenia po restarcie ani integracji Linear. Model Llama jest obecny na dysku, aktywnym modelem jest Qwen. Nie potwierdzono osobnej gotowej mapy HTML MFO, dlatego nie przenoszono z HTML deklaracji o działających funkcjach.
