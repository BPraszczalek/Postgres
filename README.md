# Homelab

## 1. Cel projektu

Stworzenie autonomicznego systemu monitorowania i zbierania danych o zużyciu energii elektrycznej z inteligentnego gniazdka (np. Shelly), zintegrowanego z relacyjną bazą danych oraz systemem wizualizacji czasu rzeczywistego.
## 2. Architektura i Wykorzystane Technologie

 Warstwa aplikacyjna (Backend): Python (Flask, Requests, APScheduler) – odpowiedzialny za cykliczne odpytywanie urządzenia o parametry sieciowe i energetyczne.

Warstwa składowania danych: PostgreSQL – bezpieczne, relacyjne repozytorium danych historycznych.

Warstwa wizualizacji (Frontend/Dashboard): Grafana – interaktywne wykresy i panele analityczne prezentujące zużycie prądu w czasie.

Środowisko uruchomieniowe: Windows / VS Code / Wirtualne środowisko Python (venv).

## 3. Główne Funkcjonalności

 Automatyczny polling: Skrypt w Pythonie za pomocą harmonogramu (APScheduler) w regularnych odstępach czasu pobiera dane z API inteligentnego gniazdka.

Persistencja danych: Odczytane parametry (napięcie, natężenie, moc, zużycie energii) są automatycznie mapowane i zapisywane w bazie PostgreSQL.

Dashboard analityczny: Grafana łączy się z bazą danych i generuje czytelne wykresy słupkowe oraz liniowe pokazujące obciążenie sieci i historię zużycia energii.

## 4. Podsumowanie i Wnioski

Projekt zakończył się sukcesem – z powodzeniem zintegrowano urządzenia IoT z lokalną infrastrukturalną bazą danych oraz stworzono przejrzysty system monitoringu. Całość została zamknięta w modułowej strukturze, co ułatwia ewentualną rozbudowę o kolejne gniazdka lub czujniki.
