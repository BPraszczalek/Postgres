# Homelab
## 1. Cel projektu
Nauka relacyjnego języka baz danych PostgresSQL oraz języka Python, poprzez stworzenie relacyjnej bazy danych i automatyzacje zbierania danych z inteligentnego gniazdka za pomocą skryptu!

## 2.Wykorzystane Technologie
* Python - skrypt do pobierania danych z inteligetnego gniazdka do bazy danych
* PostgreSQL - stworzenie bazy danych i zarządzanie nią
* Flask / APScheduler - obsługa serwera i automatyczne harmonogramowanie pobierania danych
* Grafana - połączenie z bazą danych oraz jej wizualizacja 
* AI - wykorzystywany jako asystent i pomoc
* Shelly PLUG - inteligentne gniazdko z którego pobierane są dane
* 
## 3. Główne Funkcjonalności.
Pobieranie danych z inteligentnego gniazdka przy użyciu skryptu w Pythonie, za pomocą harmonogramu, który w regularnych odstępach czasu pobiera dane z gniazdka,
które są zapisywane w bazie PostgreSQL, co pozwala na ich wizualizacje w Grafanie, która łączy się z bazą danych i tworzy czytelne wykresy

## 4. Podsumowanie i Wnioski
Projekt spłenia swój cel - działa stabilnie, dane z gniazdka są zapisywane wedle harmonogramu w bazie PostgreSQL, a wykresy w Grafanie na bieżąco pokazują zużycie energi.
Choć cel projektu został osiągnięty, nie uważam projektu za skończony, ponieważ chciałbym go wykorzystać do dalszej nauki, testowania, eksperymentowania oraz usprawić i rozbudować
