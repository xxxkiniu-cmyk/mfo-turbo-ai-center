def zapytaj_turbine(task):
    # Symulujemy błąd sieci lub braki w limicie klucza
    raise Exception("Brak połączenia z chmurą / limit wyczerpany")

def wykonaj_zadanie_z_bezpiecznikiem(task):
    try:
        return zapytaj_turbine(task)
    except Exception as e:
        print(f"⚠️ Ostrzeżenie systemowe: {e}")
        return f"AI_AGENT ogarnal: {task}"

print("--- URUCHAMIAMY TEST BEZPIECZNIKA ---")
wynik = wykonaj_zadanie_z_bezpiecznikiem("Optymalizacja zapłonu i dawki paliwa")
print(wynik)
