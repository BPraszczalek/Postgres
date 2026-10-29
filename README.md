# Homelab
## 1. Cel projektu
Nauka relacyjnego języka baz danych PostgresSQL oraz języka Python, poprzez stworzenie relacyjnej bazy danych i automatyzacje zbierania danych z inteligentnego gniazdka za pomocą skryptu!

## 2. Architektura i Wykorzystane Technologie
* Python - skrypt do pobierania danych z inteligętnego gniazdka do bazy danych
* PostgreSQL - stworzenie bazy danych
* Flask / APScheduler - 
* Grafanna - połączenie z bazą danych oraz jej wirtualizacja
* AI - wykorzystywany jako asystent, pomoc
## 3. Główne Funkcjonalności.
Automatyczny polling: Skrypt w Pythonie za pomocą harmonogramu (APScheduler) w regularnych odstępach czasu pobiera dane z API inteligentnego gniazdka.
Persistencja danych: Odczytane parametry (napięcie, natężenie, moc, zużycie energii) są automatycznie mapowane i zapisywane w bazie PostgreSQL.
Dashboard analityczny: Grafana łączy się z bazą danych i generuje czytelne wykresy słupkowe oraz liniowe pokazujące obciążenie sieci i historię zużycia energii.

## 4. Podsumowanie i Wnioski
Projekt zakończył się sukcesem – z powodzeniem zintegrowano urządzenia IoT z lokalną infrastrukturalną bazą danych oraz stworzono przejrzysty system monitoringu. Całość została zamknięta w modułowej strukturze, co ułatwia ewentualną rozbudowę o kolejne gniazdka lub czujniki.
