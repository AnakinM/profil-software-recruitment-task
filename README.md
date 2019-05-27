# profil-software-recruitment-task
My solution for recruitment task for a company Profil Software

*EN*
## Desc:
Program downloads a .csv file from [https://api.dane.gov.pl/resources/17363](https://api.dane.gov.pl/resources/17363) which consists of statistics data about number of people who took part/passed the final exams in Poland, distinguished by terytory, year and gender. Program then exports data from .csv file into it's own sqlite database. 
You can then use one of commands listed below to further analyse the data.

## Requirements:
In order to run test_main.py file, pytest is required. You can install it via:
`pip install pytest`

## How to run:
To run program, type
`python main.py`
in your terminal. All required files will be downloaded or created automatically if not found in relative path.

## List of available commands:
**avg** - returns average number of people who participated in exam up to given year.
execution: `avg terytory year gender(optional)`
Where:
*terytory* - any Polish voivodeship or Polska for whole country
*year* - value in range from 2010 up to 2018
*gender* - optional argument. m gets onlu males and f gets only females

**passed** - prints percentage of people who passed exam throughout all years.
execution: `passed terytory gender(optional)`
Where:
*terytory* - any Polish voivodeship or Polska for whole country
*gender* - optional argument. m gets onlu males and f gets only females

**best** - returns voivodeship with highest pass rate in given year.
execution: `best year gender(optional)`
Where:
*year* - value in range from 2010 up to 2018
*gender* - optional argument. m gets onlu males and f gets only females

**regress** - prints voivodeships which noted regression in pass rates compared to previous year.
execution: `regress gender(optional)`
Where:
*gender* - optional argument. m gets onlu males and f gets only females

**compare** - for a given two voivodeships, prints which one had higher pass rate throughout all years.
execution: `compare terytory terytory gender(optional)`
Where:
*terytory* - any Polish voivodeship or Polska for whole country
*gender* - optional argument. m gets onlu males and f gets only females


*PL*
## Opis:
Program pobiera plik .csv ze strony [https://api.dane.gov.pl/resources/17363](https://api.dane.gov.pl/resources/17363) zawierający dane statystyczne o ilości ludzi, którzy przystąpili/zdali maturę, z podziałęm na województwa, lata i płeć. Program eksportuje dane z pliku .csv do swojej własnej bazy danych sqltie. 
Dostępne komendy opisane są ponożej.

## Wymagania:
żeby uruchomić plik test_main.py wymagane jest posiadanie zainstalowanego pytest:
`pip install pytest`

## Jak uruchomić:
W celu uruchomienia programu należy w terminalu wywołać:
`python main.py`
AWszystkie niezbędne pliki zostaną pobrane lub stworzone, jeśli nie zostaną znalezione w folderze z programem.

## Lista dostępnych komend:
**avg** - zwraca średnią liczbę ludzi, którzy przystąpili do egzaminu w danym roku.
Wykonanie: `avg terytory year gender(opcjonalnie)`
Gdzie:
*terytory* - dowolne województwo lub Polska dla wyników dotyczących całego kraju
*year* - wartość z przedziału od 2010 do 2018 włącznie
*gender* - argument opcjonalny. m zwraca mężczyzn, a f zwraca kobiety

**passed** - Wyświetla procent ludzi, którzy zdali maturę na przestrzeni dostępnych lat.
Wykonanie: `passed terytory gender(opcjonalnie)`
Gdzie:
*terytory* - dowolne województwo lub Polska dla wyników dotyczących całego kraju
*gender* - argument opcjonalny. m zwraca mężczyzn, a f zwraca kobiety

**best** - zwraca województwo z najwyższą zdawalnością w danym roku.
Wykonanie: `best year gender(opcjonalnie)`
Gdzie:
*year* - wartość z przedziału od 2010 do 2018 włącznie
*gender* - argument opcjonalny. m zwraca mężczyzn, a f zwraca kobiety

**regress** - wyświetla województwa, które zanotowały regresję w stosunku do poprzednich lat.
Wykonanie: `regress gender(opcjonalnie)`
Gdzie:
*gender* - argument opcjonalny. m zwraca mężczyzn, a f zwraca kobiety

**compare** - dla podanych dwóch województw wyświetla ich porównanie na przestrzeni lat, w stosunku do zdawalności.
Wykonanie: `compare terytory terytory gender(opcjonalnie)`
Gdzie:
*terytory* - dowolne województwo lub Polska dla wyników dotyczących całego kraju
*gender* - argument opcjonalny. m zwraca mężczyzn, a f zwraca kobiety

