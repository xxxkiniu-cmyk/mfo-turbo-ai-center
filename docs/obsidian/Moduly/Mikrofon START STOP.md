---
status: "NIEZWERYFIKOWANY"
data_testu: "2026-10-31"
tags: [mfo, modul]
---
# Mikrofon START STOP

**Stan: NIEZWERYFIKOWANY**, zakres: sterowanie i nagrywanie.

## Weryfikacja
Metoda: PowerShell Get-Service Audiosrv/AudioEndpointBuilder i Get-PnpDevice -Class AudioEndpoint.
Wynik: obie usługi Running, pięć urządzeń klasy AudioEndpoint ze stanem OK. Nie dowodzi to sprawności mikrofonu wejściowego ani START/STOP. Nie nagrywano i nie przerywano dyktowania.
Czas pomiarów: 14:45 do 14:46 UTC.

## Powiązania
- [[Windows 11]]
- [[Wispr Flow]]
