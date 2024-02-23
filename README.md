ENGETO_PYTHON AKADEMIE_PROJEKT 3
================================
Třetí projekt tvořený v rámci kurzu "Python Akademie" od společnosti Engeto

Popis projektu:
---------------
Smyslem projektu bylo vytvořit program k extrahování [dat výsledků parlamentních voleb z roku 2017] (https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) pro libovolný územní celek na úrovni okresů.

INSTALACE KNIHOVEN:
-------------------
Seznam knihoven použitých v kódu: requirements.txt

SPUŠTĚNÍ PROGRAMU:
------------------
Program se spouští pomocí příkazového řádku a vyžaduje dva povinné argumenty. Prvním argumentem je URL vybraného územního celku, jehož volební výsledkz chce uživatel extrahovat. Druhým argumentem je název výsledného souboru, kam se výsledky uloží (musí končit ".csv").

### Příklad pro spuštění (územní celek Prostějov):
1. argument: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
2. argument: vysledky_prostejov.csv

Spuštění programu v příkazovém řádku: python ENGETO_projekt3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_prostejov.csv"


### PRŮBĚH STAHOVÁNÍ:
správně zadané argumenty:
**********ELECTION SCRAPER**********
DOWNLOADING DATA FROM URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
SAVING DATA TO FILE: vysledky_prostejov.csv
DATA SAVED
**********ELECTION SCRAPER**********

chybně zadané argumenty:
**********ELECTION SCRAPER**********
!!! INVALID INPUT !!!
**********ELECTION SCRAPER**********

### ČÁSTEČNÝ VÝSTUP:
code,location,registred,envelopes,valid,Ob�ansk� demokratick� strana, .............
506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
589268,Bediho��,834,527,524,51,0,0,28,1,13,123,2,2,14,1,0,34,0,6,140,0,0,26,0,0,0,0,82,1
589276,B�lovice-Lutot�n,431,279,275,13,0,0,32,0,8,40,1,0,4,0,0,30,0,3,83,0,0,22,0,0,0,1,38,0
589284,Biskupice,238,132,131,14,0,0,9,0,5,24,2,1,1,0,0,10,2,0,34,0,0,10,0,0,0,0,19,0
589292,Bohuslavice,376,236,236,20,0,0,23,0,3,22,3,4,6,0,1,17,0,4,53,1,1,39,0,0,3,0,36,0
589306,Bous�n,107,67,67,5,0,0,4,0,3,14,0,2,0,0,0,7,0,2,10,0,0,9,0,0,0,0,11,0

